"""QA ciclo 2: casos que faltaban según la medición de cobertura y el recorrido manual."""
from datetime import datetime

from conftest import NOW, TUE, at
from fastapi.testclient import TestClient
from tutorias.api import create_app
from tutorias.db import connect
from tutorias.service import TutoringService

DIA_14 = "2030-01-21"  # lunes, 14 días después del NOW de conftest


def test_rn11_disponibilidad_no_ofrece_horarios_a_mas_de_14_dias(world, reloj):
    """Bug del recorrido manual: el día 14 se ofrecían horarios que luego RN11 rechaza."""
    s = world["svc"]
    reloj.ahora = datetime(2030, 1, 7, 10, 0)  # lunes 10:00 → límite: lunes 21 a las 10:00
    libres = s.availability(world["t1"], at(DIA_14, "00:00").date())
    assert libres == ["08:00", "08:30", "09:00", "09:30", "10:00"]
    for hhmm in libres:  # todo lo que se ofrece se puede reservar
        b = s.create_booking(world["t1"], world["s1"], at(DIA_14, hhmm), 30)
        s.cancel_booking(b["id"], world["s1"])


def test_servicio_valida_tutor_sin_pasar_por_la_api(svc):
    """La API valida antes con pydantic; el servicio también debe rechazar (defensa en profundidad)."""
    import pytest
    from tutorias.service import ValidationError
    with pytest.raises(ValidationError):
        svc.create_tutor("   ")
    with pytest.raises(ValidationError):
        svc.create_tutor("Ana", photo=6)
    t = svc.create_tutor("Ana", "Cálculo", 2)["id"]
    with pytest.raises(ValidationError):
        svc.update_tutor(t, photo=-1)
    assert svc.update_tutor(t, subjects="")["subjects"] == ""  # vaciar materias sí se permite


def test_rn12_una_reserva_pasada_no_bloquea_eliminar_al_tutor(world, reloj):
    s = world["svc"]
    s.create_booking(world["t1"], world["s1"], at(TUE, "10:00"), 60)
    reloj.ahora = datetime(2030, 1, 8, 12, 0)  # la reserva ya terminó (sigue «active»)
    assert s.delete_tutor(world["t1"]) == {"deleted": world["t1"]}


def test_migracion_de_base_antigua_sin_columna_photo(tmp_path):
    import sqlite3
    ruta = str(tmp_path / "vieja.db")
    vieja = sqlite3.connect(ruta)
    vieja.execute("CREATE TABLE tutors (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, subjects TEXT NOT NULL DEFAULT '')")
    vieja.execute("INSERT INTO tutors(name, subjects) VALUES ('Ana', 'Cálculo')")
    vieja.commit(); vieja.close()
    svc = TutoringService(connect(ruta), now=lambda: NOW)
    assert svc.list_tutors() == [{"id": 1, "name": "Ana", "subjects": "Cálculo", "photo": 0}]


def test_http_reservas_del_tutor():
    client = TestClient(create_app(TutoringService(connect(":memory:"), now=lambda: NOW)))
    t = client.post("/tutors", json={"name": "Ana"}).json()["id"]
    sid = client.post("/students", json={"name": "Sofía", "email": "s@utp.ac.pa"}).json()["id"]
    client.post("/bookings", json={"tutor_id": t, "student_id": sid, "start": f"{TUE}T10:00:00", "duration_minutes": 60})
    r = client.get(f"/tutors/{t}/bookings")
    assert r.status_code == 200
    assert [(b["student_id"], b["start"]) for b in r.json()] == [(sid, f"{TUE}T10:00:00")]
    assert client.get("/tutors/999/bookings").status_code == 404

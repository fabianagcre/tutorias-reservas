"""CE3 (ensayo) — RN13: máximo 3 h (180 min) de tutoría activa por estudiante por semana (lun–dom).

Datos repartidos en días distintos de la misma semana para no chocar con RN6 (máx. 2/día),
RN3 (lun–vie 08:00–18:00), RN4 (:00/:30) ni RN11 (≤ 14 días). Reloj inyectado: NOW = lunes 2030-01-07 07:00.
"""
import pytest
from conftest import MON, NOW, TUE, at
from tutorias.service import ValidationError

WED = "2030-01-09"
THU = "2030-01-10"
MON_SIGUIENTE = "2030-01-14"


def _dos_horas(s, w):
    s.create_booking(w["t1"], w["s1"], at(MON, "10:00"), 60)
    return s.create_booking(w["t1"], w["s1"], at(TUE, "10:00"), 60)


def test_ce3a_reserva_que_llega_justo_a_3_horas_se_acepta(world):
    s = world["svc"]
    _dos_horas(s, world)
    b = s.create_booking(world["t2"], world["s1"], at(WED, "10:00"), 60)  # total 180 min
    assert b["status"] == "active"


def test_ce3b_reserva_que_pasa_de_3_horas_da_422(world):
    s = world["svc"]
    _dos_horas(s, world)
    s.create_booking(world["t2"], world["s1"], at(WED, "10:00"), 60)
    with pytest.raises(ValidationError) as e:
        s.create_booking(world["t1"], world["s1"], at(THU, "10:00"), 30)  # total 210 min
    assert e.value.status == 422


def test_ce3_canceladas_no_cuentan(world):
    s = world["svc"]
    b = _dos_horas(s, world)
    s.create_booking(world["t2"], world["s1"], at(WED, "10:00"), 60)
    s.cancel_booking(b["id"], world["s1"])  # libera 60 min (RN7)
    assert s.create_booking(world["t1"], world["s1"], at(THU, "10:00"), 60)["status"] == "active"


def test_ce3_otra_semana_no_suma(world):
    s = world["svc"]
    _dos_horas(s, world)
    s.create_booking(world["t2"], world["s1"], at(WED, "10:00"), 60)
    b = s.create_booking(world["t1"], world["s1"], at(MON_SIGUIENTE, "10:00"), 60)
    assert b["status"] == "active"


def test_ce3_http_pasar_de_3_horas_devuelve_422():
    from fastapi.testclient import TestClient
    from tutorias.api import create_app
    from tutorias.db import connect
    from tutorias.service import TutoringService

    client = TestClient(create_app(TutoringService(connect(":memory:"), now=lambda: NOW)))
    t = client.post("/tutors", json={"name": "Ana", "subjects": "Cálculo"}).json()["id"]
    st = client.post("/students", json={"name": "Sofía", "email": "s@utp.ac.pa"}).json()["id"]
    for day in (MON, TUE, WED):
        body = {"tutor_id": t, "student_id": st, "start": f"{day}T10:00:00", "duration_minutes": 60}
        assert client.post("/bookings", json=body).status_code in (200, 201)
    body = {"tutor_id": t, "student_id": st, "start": f"{THU}T10:00:00", "duration_minutes": 30}
    assert client.post("/bookings", json=body).status_code == 422

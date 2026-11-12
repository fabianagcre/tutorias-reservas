import pytest
from conftest import NOW, TUE
from fastapi.testclient import TestClient
from tutorias.api import create_app
from tutorias.db import connect
from tutorias.service import TutoringService


@pytest.fixture
def client():
    svc = TutoringService(connect(":memory:"), now=lambda: NOW)
    return TestClient(create_app(svc))


def _setup(client):
    t = client.post("/tutors", json={"name": "Ana", "subjects": "Cálculo"}).json()["id"]
    s1 = client.post("/students", json={"name": "Sofía", "email": "s@utp.ac.pa"}).json()["id"]
    s2 = client.post("/students", json={"name": "Diego", "email": "d@utp.ac.pa"}).json()["id"]
    return t, s1, s2


def test_flujo_completo_reserva_conflicto_cancelacion(client):
    t, s1, s2 = _setup(client)
    body = {"tutor_id": t, "student_id": s1, "start": f"{TUE}T10:00:00", "duration_minutes": 60}
    assert client.post("/bookings", json=body).status_code == 201
    # CA2: otro estudiante, mismo tutor, horario solapado -> 409
    r = client.post("/bookings", json={**body, "student_id": s2, "start": f"{TUE}T10:30:00"})
    assert r.status_code == 409
    # disponibilidad no muestra 10:00
    av = client.get(f"/tutors/{t}/availability", params={"date": TUE}).json()["free_slots"]
    assert "10:00" not in av
    # cancelar libera
    bid = client.get(f"/students/{s1}/bookings").json()[0]["id"]
    assert client.post(f"/bookings/{bid}/cancel", json={"student_id": s2}).status_code == 403
    assert client.post(f"/bookings/{bid}/cancel", json={"student_id": s1}).status_code == 200
    assert client.post("/bookings", json={**body, "student_id": s2}).status_code == 201


def test_reglas_devuelven_422(client):
    t, s1, _ = _setup(client)
    r = client.post("/bookings", json={"tutor_id": t, "student_id": s1, "start": f"{TUE}T19:00:00", "duration_minutes": 60})
    assert r.status_code == 422 and "detail" in r.json()


def test_recursos_inexistentes_404(client):
    assert client.get("/tutors/99/availability", params={"date": TUE}).status_code == 404

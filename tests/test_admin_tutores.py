"""Administración de tutores (RF12, RF13, RN12): editar y eliminar."""
import pytest
from conftest import NOW
from fastapi.testclient import TestClient
from tutorias.api import create_app
from tutorias.db import connect
from tutorias.service import TutoringService


@pytest.fixture
def client():
    return TestClient(create_app(TutoringService(connect(":memory:"), now=lambda: NOW)))


def _tutor(client, name="Ana", subjects="Cálculo", photo=0):
    return client.post("/tutors", json={"name": name, "subjects": subjects, "photo": photo}).json()["id"]


def _reservar(client, tutor_id):
    sid = client.post("/students", json={"name": "Sofía", "email": "s@utp.ac.pa"}).json()["id"]
    r = client.post("/bookings", json={"tutor_id": tutor_id, "student_id": sid, "start": "2030-01-08T10:00:00", "duration_minutes": 60})
    assert r.status_code == 201
    return sid, r.json()["id"]


def test_ca25_editar_parcialmente_conserva_el_resto(client):
    t = _tutor(client, photo=2)
    r = client.patch(f"/tutors/{t}", json={"name": "Ana María"})
    assert r.status_code == 200
    assert (r.json()["name"], r.json()["subjects"], r.json()["photo"]) == ("Ana María", "Cálculo", 2)
    client.patch(f"/tutors/{t}", json={"photo": 5, "subjects": "Física"})
    assert [(x["name"], x["subjects"], x["photo"]) for x in client.get("/tutors").json()] == [("Ana María", "Física", 5)]


def test_ca25_editar_tutor_inexistente_404(client):
    assert client.patch("/tutors/999", json={"name": "X"}).status_code == 404


@pytest.mark.parametrize("cuerpo", [{"name": "   "}, {"photo": 9}, {"photo": -1}])
def test_ca25_editar_con_datos_invalidos_422(client, cuerpo):
    t = _tutor(client)
    assert client.patch(f"/tutors/{t}", json=cuerpo).status_code == 422
    assert client.get("/tutors").json()[0]["name"] == "Ana"


def test_ca26_eliminar_tutor_sin_reservas(client):
    t = _tutor(client)
    assert client.delete(f"/tutors/{t}").status_code == 200
    assert client.get("/tutors").json() == []


def test_ca26_eliminar_tutor_inexistente_404(client):
    assert client.delete("/tutors/999").status_code == 404


def test_ca27_no_se_elimina_con_reserva_activa_futura(client):
    t = _tutor(client)
    sid, bid = _reservar(client, t)
    r = client.delete(f"/tutors/{t}")
    assert r.status_code == 409
    assert "reserva" in r.json()["detail"]
    assert len(client.get("/tutors").json()) == 1
    # tras cancelar la reserva, ya se puede eliminar
    assert client.post(f"/bookings/{bid}/cancel", json={"student_id": sid}).status_code == 200
    assert client.delete(f"/tutors/{t}").status_code == 200

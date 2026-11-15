"""Interfaz web (RF8-RF10): listar tutores, identificar estudiante por correo y página `/`."""
import pytest
from conftest import NOW
from fastapi.testclient import TestClient
from tutorias.api import create_app
from tutorias.db import connect
from tutorias.service import TutoringService


@pytest.fixture
def client():
    return TestClient(create_app(TutoringService(connect(":memory:"), now=lambda: NOW)))


def test_ca16_listar_tutores(client):
    client.post("/tutors", json={"name": "Ana", "subjects": "Cálculo"})
    client.post("/tutors", json={"name": "Beto", "subjects": "Física"})
    r = client.get("/tutors")
    assert r.status_code == 200
    assert [(t["name"], t["subjects"]) for t in r.json()] == [("Ana", "Cálculo"), ("Beto", "Física")]


def test_ca16_listar_tutores_vacio(client):
    assert client.get("/tutors").json() == []


def test_ca17_estudiante_por_correo(client):
    creado = client.post("/students", json={"name": "Sofía", "email": "Sofia@utp.ac.pa"}).json()
    r = client.get("/students/by-email", params={"email": "SOFIA@utp.ac.pa"})
    assert r.status_code == 200
    assert r.json()["id"] == creado["id"]


def test_ca17_correo_desconocido_404(client):
    r = client.get("/students/by-email", params={"email": "nadie@utp.ac.pa"})
    assert r.status_code == 404
    assert "correo" in r.json()["detail"]


def test_ca18_pagina_principal(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
    assert "Reservas de Tutorías" in r.text

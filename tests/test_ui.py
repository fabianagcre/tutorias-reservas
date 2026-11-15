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


def test_ca20_imagenes_estaticas(client):
    for nombre in ("hero.jpg", "t1.jpg", "t5.jpg"):
        r = client.get(f"/img/{nombre}")
        assert r.status_code == 200
        assert r.headers["content-type"] == "image/jpeg"
    assert client.get("/img/no-existe.jpg").status_code == 404


def test_ca21_foto_del_tutor(client):
    a = client.post("/tutors", json={"name": "Ana", "subjects": "Cálculo", "photo": 3})
    assert a.status_code == 201 and a.json()["photo"] == 3
    b = client.post("/tutors", json={"name": "Beto", "subjects": "Física"}).json()
    assert b["photo"] == 0
    assert [t["photo"] for t in client.get("/tutors").json()] == [3, 0]


@pytest.mark.parametrize("valor", [-1, 6, 99])
def test_ca21_foto_fuera_de_rango_422(client, valor):
    r = client.post("/tutors", json={"name": "Ana", "subjects": "", "photo": valor})
    assert r.status_code == 422


def test_ca22_panel_admin(client):
    r = client.get("/admin")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
    assert "Administración de" in r.text and 'id="tname"' in r.text


def test_ca23_el_estudiante_no_ve_el_alta_de_tutores(client):
    html = client.get("/").text
    assert 'id="tname"' not in html
    assert "Agregar un tutor" not in html


def test_ca24_hoja_de_estilos(client):
    r = client.get("/css/app.css")
    assert r.status_code == 200
    assert "text/css" in r.headers["content-type"]

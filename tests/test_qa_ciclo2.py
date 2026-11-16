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

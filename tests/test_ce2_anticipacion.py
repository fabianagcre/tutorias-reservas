"""CE2 — RN11: solo se reserva si la tutoría inicia como máximo 14 días después de ahora."""
from datetime import datetime

import pytest
from conftest import at
from tutorias.service import ValidationError

# El NOW de conftest (07:00) deja el borde de 14 días fuera de RN3; se fija el reloj inyectado.
AHORA = datetime(2030, 1, 7, 10, 0)  # lunes 10:00
DIA_14 = "2030-01-21"  # lunes, 14 días después


def test_ca14_reserva_a_14_dias_exactos(world):
    s = world["svc"]
    s.now = lambda: AHORA
    b = s.create_booking(world["t1"], world["s1"], at(DIA_14, "10:00"), 60)
    assert b["status"] == "active"


def test_ca15_reserva_a_14_dias_y_30_min(world):
    s = world["svc"]
    s.now = lambda: AHORA
    with pytest.raises(ValidationError):
        s.create_booking(world["t1"], world["s1"], at(DIA_14, "10:30"), 60)


def test_ce2_borde_14_dias_mas_1_segundo(world):
    s = world["svc"]
    s.now = lambda: datetime(2030, 1, 7, 9, 59, 59)  # inicio a 14 días + 1 s
    with pytest.raises(ValidationError):
        s.create_booking(world["t1"], world["s1"], at(DIA_14, "10:00"), 60)

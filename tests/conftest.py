import sys
from datetime import datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from tutorias.db import connect  # noqa: E402
from tutorias.service import TutoringService  # noqa: E402

# "Hoy" fijo: lunes 2030-01-07 07:00. Martes = 2030-01-08.
NOW = datetime(2030, 1, 7, 7, 0)
MON = "2030-01-07"
TUE = "2030-01-08"
SAT = "2030-01-12"


@pytest.fixture
def svc():
    return TutoringService(connect(":memory:"), now=lambda: NOW)


@pytest.fixture
def world(svc):
    return {
        "svc": svc,
        "t1": svc.create_tutor("Ana", "Cálculo")["id"],
        "t2": svc.create_tutor("Luis", "Física")["id"],
        "s1": svc.create_student("Sofía", "sofia@utp.ac.pa")["id"],
        "s2": svc.create_student("Diego", "diego@utp.ac.pa")["id"],
    }


def at(day: str, hhmm: str) -> datetime:
    return datetime.fromisoformat(f"{day}T{hhmm}:00")

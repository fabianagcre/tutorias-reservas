"""Carga tutores de demostración (con su foto) para la presentación.

Uso:  python scripts/seed_demo.py            # usa tutorias.db
      python scripts/seed_demo.py otra.db    # otra base

No hace nada si ya hay tutores, para no pisar datos reales.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from tutorias.db import connect  # noqa: E402
from tutorias.service import TutoringService  # noqa: E402

TUTORES = [  # (nombre, materias, foto 1-5 según el catálogo de web/img)
    ("Ana Torres", "Cálculo, Álgebra", 1),
    ("Lucía Méndez", "Física, Química", 2),
    ("Carlos Rivera", "Programación", 3),
    ("Diego Paz", "Estructuras de Datos", 4),
    ("Mateo Salas", "Bases de Datos", 5),
]

if __name__ == "__main__":
    svc = TutoringService(connect(sys.argv[1] if len(sys.argv) > 1 else "tutorias.db"))
    if svc.list_tutors():
        print("Ya hay tutores registrados: no se agregó nada.")
    else:
        for nombre, materias, foto in TUTORES:
            svc.create_tutor(nombre, materias, foto)
        print(f"Se agregaron {len(TUTORES)} tutores de demostración.")

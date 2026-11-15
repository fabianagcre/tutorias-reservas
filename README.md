# Reservas de Tutorías Universitarias

Proyecto 2 — Tópicos Especiales II (Prof. Regis Rivera). Recorrido: **ODD → SDD → código → pruebas → valor al usuario**.

**Outcome**: eliminar cruces de horario y permitir que el estudiante encuentre y reserve tutorías sin intervención del tutor.

## Ejecutar
```bash
pip install -r requirements.txt
uvicorn --app-dir src tutorias.api:create_app --factory --reload
pytest
python scripts/seed_demo.py   # opcional: tutores de demostración con foto
```
Interfaz web (estudiante): http://localhost:8000/ · Panel del administrador (alta de tutores): http://localhost:8000/admin · Documentación interactiva de la API: http://localhost:8000/docs

## Estructura
- `specs/` outcomes, requisitos, reglas de negocio, arquitectura, modelo de datos, API, criterios de aceptación, plan
- `docs/` bitácora de IA (`ai-log.md`), decisiones (`decisions.md`), pruebas (`testing.md`)
- `src/tutorias/` código · `tests/` pruebas automatizadas

## Equipo
| Rol | Ciclo 1 (specs/base + CE1) | Ciclo 2 (CE2) |
|---|---|---|
| Product / Spec Lead | Fabiana González Crespin (por confirmar) | Uriel Reyna |
| Architecture / Development Lead | Fabiana González Crespin | Fabiana González Crespin |
| QA / DevOps Lead | Uriel Reyna | por confirmar |

Flujo de trabajo: issues → ramas `feature/*` → Pull Request con revisión → merge a `main` (CI con pytest).

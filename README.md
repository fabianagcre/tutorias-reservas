# Reservas de Tutorías Universitarias

[![CI](https://github.com/fabianagcre/tutorias-reservas/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/fabianagcre/tutorias-reservas/actions/workflows/ci.yml)

Proyecto 2 — Tópicos Especiales II (Prof. Regis Rivera). Recorrido: **ODD → SDD → código → pruebas → valor al usuario**.

**Outcome**: eliminar cruces de horario y permitir que el estudiante encuentre y reserve tutorías sin intervención del tutor.

## Ejecutar
```bash
pip install -r requirements.txt
uvicorn --app-dir src tutorias.api:create_app --factory --reload
pytest
```
Documentación interactiva: http://localhost:8000/docs

### Con Docker
```bash
docker build -t tutorias .
docker run -p 8000:8000 tutorias   # http://localhost:8000/docs
```
La base SQLite vive dentro del contenedor y se pierde al borrarlo (es una demostración).

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

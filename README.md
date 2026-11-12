# Reservas de Tutorías Universitarias

Proyecto 2 — Tópicos Especiales II (Prof. Regis Rivera). Recorrido: **ODD → SDD → código → pruebas → valor al usuario**.

**Outcome**: eliminar cruces de horario y permitir que el estudiante encuentre y reserve tutorías sin intervención del tutor.

## Ejecutar
```bash
pip install -r requirements.txt
uvicorn --app-dir src tutorias.api:create_app --factory --reload
pytest
```
Documentación interactiva: http://localhost:8000/docs

## Estructura
- `specs/` outcomes, requisitos, reglas de negocio, arquitectura, modelo de datos, API, criterios de aceptación, plan
- `docs/` bitácora de IA (`ai-log.md`), decisiones (`decisions.md`), pruebas (`testing.md`)
- `src/tutorias/` código · `tests/` pruebas automatizadas

## Equipo
| Rol (ciclo 1) | Integrante |
|---|---|
| Product / Spec Lead | por asignar |
| Architecture / Development Lead | por asignar |
| QA / DevOps Lead | por asignar |

Flujo de trabajo: issues → ramas `feature/*` → Pull Request con revisión → merge a `main` (CI con pytest).

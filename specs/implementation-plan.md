# Plan de implementación

| # | Tarea | Rol líder | Estado |
|---|-------|-----------|--------|
| 1 | Specs ODD/SDD (este directorio) | Product/Spec | ✅ |
| 2 | Esquema SQLite + servicio base (crear tutor/estudiante) | Arquitectura/Dev | ✅ |
| 3 | Reserva con RN1–RN9 + pruebas unitarias | Arquitectura/Dev + QA | ✅ |
| 4 | Disponibilidad y cancelación | Arquitectura/Dev | ✅ |
| 5 | API FastAPI + pruebas de aceptación | Arquitectura/Dev + QA | ✅ |
| 6 | CI en GitHub Actions | QA/DevOps | ✅ |
| 7 | **Cambio de especificación (CE1)**: cancelación solo hasta 2 h antes | Todos | ✅ en `main` (RN10, CA12-13; PR #4; observaciones de QA ciclo 1 en PR #7) |
| 8 | **Cambio de especificación (CE2)**: reservar como máximo 14 días antes del inicio | Todos | ✅ en `main` (RN11, CA14-15; PR #8) |
| 9 | **Interfaz web** (RF8–RF10): `GET /tutors`, `GET /students/by-email` y página `/` | Arquitectura/Dev | ✅ hecho, PR #11 abierto sin fusionar (RF8–RF10, CA16–CA20; CA19 se verifica a mano) |
| 10 | **Panel del administrador** (RF11): el alta de tutores sale de la pantalla del estudiante y pasa a `/admin` (CA22–CA24) | Arquitectura/Dev | ✅ hecho, PR #11 abierto sin fusionar (RF11, CA22–CA24) |
| 11 | **Editar y eliminar tutores** (RF12, RF13, RN12; CA25–CA27) | Arquitectura/Dev | ✅ hecho, PR #11 abierto sin fusionar (RF12, RF13, RN12, CA25–CA27) |
| 12 | **Arquitectura del ciclo 2**: `.gitignore`, `architecture.md` revisado | Arquitectura/Dev | PR #9 abierto sin fusionar (ya integrado en la rama del PR #11) |
| 13 | **Pulido de specs del ciclo 2**: CA16–CA27 en Dado/Cuando/Entonces, O6, trazabilidad RF → O | Product/Spec | En curso, rama `spec/ciclo2-pulido` (apilada sobre el PR #11) |

Estado verificado con git el 2026-11-15: `main` contiene los PR #4, #7 y #8 (34 pruebas); los PR #9 y #11 siguen abiertos (55 pruebas en la rama del #11).

Rotación de roles: ciclo 1 = Fabiana (Product/Spec + Architecture/Dev: specs/base + CE1) y Uriel (QA/DevOps); ciclo 2 = Uriel (Product/Spec), Fabiana (Architecture/Dev) y Michael «Mike» (QA/DevOps).

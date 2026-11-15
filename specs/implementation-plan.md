# Plan de implementación

| # | Tarea | Rol líder | Estado |
|---|-------|-----------|--------|
| 1 | Specs ODD/SDD (este directorio) | Product/Spec | ✅ |
| 2 | Esquema SQLite + servicio base (crear tutor/estudiante) | Arquitectura/Dev | ✅ |
| 3 | Reserva con RN1–RN9 + pruebas unitarias | Arquitectura/Dev + QA | ✅ |
| 4 | Disponibilidad y cancelación | Arquitectura/Dev | ✅ |
| 5 | API FastAPI + pruebas de aceptación | Arquitectura/Dev + QA | ✅ |
| 6 | CI en GitHub Actions | QA/DevOps | ✅ |
| 7 | **Cambio de especificación (CE1)**: cancelación solo hasta 2 h antes | Todos | ✅ (RN10, CA12-13) |
| 8 | **Cambio de especificación (CE2)**: reservar como máximo 14 días antes del inicio | Todos | ✅ (RN11, CA14-15) |
| 9 | **Interfaz web** (RF8–RF10): `GET /tutors`, `GET /students/by-email` y página `/` | Arquitectura/Dev | ✅ (RF8–RF10, CA16–CA19) |

Rotación de roles: ciclo 1 = specs/base + CE1, ciclo 2 = cambio CE2 (los roles rotan).

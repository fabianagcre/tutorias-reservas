# AI Development Log

| Fecha | Actividad | IA utilizada | Solicitud | Resultado | Decisión |
|-------|-----------|--------------|-----------|-----------|----------|
| 2026-11-12 | Lectura del enunciado | Claude (chat/agente) | Leer PDF del Proyecto 2 y extraer restricciones | Lista de entregables y estructura recomendada | Elegir **tutorías universitarias** |
| 2026-11-12 | Fase ODD | Claude | Redactar problema, preguntas de exploración y outcomes | `specs/outcomes.md` | Aceptado; se revisará con el equipo |
| 2026-11-12 | Fase SDD | Claude | Convertir outcomes en requisitos, reglas, API y criterios Given/When/Then | `specs/*.md` | Aceptado |
| 2026-11-12 | Implementación | Claude | Servicio, API FastAPI y SQLite desde las specs | `src/` | Se mantuvo la lógica solo en `service.py` |
| 2026-11-12 | Pruebas | Claude | Una prueba por criterio de aceptación + concurrencia de doble reserva | `tests/` (22 pasan) | Se corrigió un error de hilos: `_require` movido dentro del lock |
| 2026-11-12 | Cambio de spec CE1 | Claude | Ejecutar ciclo completo de cambio (cancelación ≥2 h) | ver `decisions.md` | Aceptado |
| 2026-11-15 | Revisión del PR #4 (CE1) | Claude Code (Opus 5.5, orquestación multiagente) | Revisar el PR con un agente revisor y verificadores adversariales | Aprobado con 5 observaciones | Merge del PR #4; observaciones atendidas en QA ciclo 1 |
| 2026-11-15 | QA ciclo 1 | Claude Code (Opus 5.5, orquestación multiagente) | Atender las observaciones: borde de RN10, CA12/CA13, 422 HTTP, bug de zona horaria (500), docs | Rama `qa/ciclo1-observaciones-pr4`, 30 pruebas pasan | Aceptado; corrección en la API (D4) |
| 2026-11-15 | Cambio de spec CE2 | Claude Code (Opus 5.5, orquestación multiagente) | Ejecutar ciclo de cambio: anticipación máxima de 14 días para reservar | Rama `feature/ce2-anticipacion-maxima` | En revisión por PR |

> Pendiente del equipo: añadir las entradas de las herramientas que cada integrante use realmente.

# AI Development Log

| Fecha | Actividad | IA utilizada | Solicitud | Resultado | Decisión |
|-------|-----------|--------------|-----------|-----------|----------|
| 2026-11-12 | Lectura del enunciado | Claude (chat/agente) | Leer PDF del Proyecto 2 y extraer restricciones | Lista de entregables y estructura recomendada | Elegir **tutorías universitarias** |
| 2026-11-12 | Fase ODD | Claude | Redactar problema, preguntas de exploración y outcomes | `specs/outcomes.md` | Aceptado; se revisará con el equipo |
| 2026-11-12 | Fase SDD | Claude | Convertir outcomes en requisitos, reglas, API y criterios Given/When/Then | `specs/*.md` | Aceptado |
| 2026-11-12 | Implementación | Claude | Servicio, API FastAPI y SQLite desde las specs | `src/` | Se mantuvo la lógica solo en `service.py` |
| 2026-11-12 | Pruebas | Claude | Una prueba por criterio de aceptación + concurrencia de doble reserva | `tests/` (22 pasan) | Se corrigió un error de hilos: `_require` movido dentro del lock |
| 2026-11-12 | Cambio de spec CE1 | Claude | Ejecutar ciclo completo de cambio (cancelación ≥2 h) | ver `decisions.md` | Aceptado |

> Pendiente del equipo: añadir las entradas de las herramientas que cada integrante use realmente.

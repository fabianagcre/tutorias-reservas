# Requisitos (Fase 2 — SDD)

Trazabilidad: cada requisito apunta a un outcome (O#).

## Funcionales
| ID | Requisito | Outcome |
|----|-----------|---------|
| RF1 | Registrar tutores con nombre y materias | O2 |
| RF2 | Registrar estudiantes con nombre y correo | O3 |
| RF3 | Consultar disponibilidad de un tutor en una fecha (franjas libres de 30 min) | O2 |
| RF4 | Crear una reserva (estudiante, tutor, fecha, hora inicio, duración) | O1, O3 |
| RF5 | Rechazar reservas que violen las reglas de negocio con un error claro | O1, O5 |
| RF6 | Cancelar una reserva; el espacio vuelve a estar disponible | O3, O4 |
| RF7 | Listar reservas de un estudiante y de un tutor | O3 |

## No funcionales
| ID | Requisito |
|----|-----------|
| RNF1 | Cualquier lenguaje/stack; el elegido se documenta en `architecture.md` |
| RNF2 | La regla de no doble reserva debe poder verificarse con prueba automatizada |
| RNF3 | Errores de validación devuelven HTTP 4xx con mensaje legible |
| RNF4 | Cobertura de pruebas sobre reglas críticas y criterios de aceptación |

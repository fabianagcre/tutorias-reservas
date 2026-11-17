# Requisitos (Fase 2 — SDD)

Trazabilidad: cada requisito apunta a un outcome (O#).

## Funcionales
| ID | Requisito | Outcome |
|----|-----------|---------|
| RF1 | Registrar tutores con nombre, materias y una foto opcional elegida de un catálogo de 5 (0 = sin foto) | O2, O6 |
| RF2 | Registrar estudiantes con nombre y correo | O3 |
| RF3 | Consultar disponibilidad de un tutor en una fecha (franjas libres de 30 min) | O2 |
| RF4 | Crear una reserva (estudiante, tutor, fecha, hora inicio, duración) | O1, O3 |
| RF5 | Rechazar reservas que violen las reglas de negocio con un error claro | O1, O5 |
| RF6 | Cancelar una reserva; el espacio vuelve a estar disponible | O3, O4 |
| RF7 | Listar reservas de un estudiante y de un tutor | O3 |
| RF8 | Listar los tutores registrados (nombre y materias) para que el estudiante elija | O2 |
| RF9 | Identificar a un estudiante por su correo (sin contraseña, alcance del curso) | O3 |
| RF10 | Interfaz web por pasos: elegir tutor → fecha y horario libre → duración → confirmar → ver y cancelar mis reservas; los errores de reglas se muestran con el mensaje de la API | O2, O3, O5 |
| RF11 | El registro de tutores es una función del administrador: vive en una página aparte (`/admin`) y NO aparece en la pantalla del estudiante, que solo reserva y cancela. En esta versión del curso `/admin` no pide contraseña (mejora futura) | O6 |
| RF12 | El administrador puede editar el nombre, las materias y la foto de un tutor | O2, O6 |
| RF13 | El administrador puede eliminar un tutor, salvo que tenga reservas activas futuras (RN12) | O3, O6 |

## No funcionales
| ID | Requisito |
|----|-----------|
| RNF1 | Cualquier lenguaje/stack; el elegido se documenta en `architecture.md` |
| RNF2 | La regla de no doble reserva debe poder verificarse con prueba automatizada |
| RNF3 | Errores de validación devuelven HTTP 4xx con mensaje legible |
| RNF4 | Cobertura de pruebas sobre reglas críticas y criterios de aceptación |

## Trazabilidad RF → O (pulido del ciclo 2)
- RF2–RF10 conservan su outcome original.
- RF1, RF11, RF12 y RF13 son funciones del administrador y ahora apuntan a **O6** (catálogo de tutores sin intervención técnica). RF1 y RF12 siguen en **O2** porque el nombre, las materias y la foto son lo que ve el estudiante al elegir tutor.
- RF13 pasa de O1, O2 a **O3, O6**: la regla que la acompaña (RN12) no evita cruces de horario (O1); protege que una reserva confirmada del estudiante no se quede sin tutor (O3).
- Cada RF tiene al menos un criterio de aceptación en `acceptance-criteria.md`: RF8 → CA16, RF9 → CA17, RF10 → CA18–CA20 y CA24, RF11 → CA22–CA23, RF12 → CA25, RF13 → CA26, RN12 → CA27, RF1 (foto) → CA21.

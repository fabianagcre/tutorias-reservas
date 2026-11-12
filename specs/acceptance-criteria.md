# Criterios de aceptación (Given / When / Then)

| ID | Criterio | Regla |
|----|----------|-------|
| CA1 | Dado un tutor libre, cuando un estudiante reserva 10:00 por 60 min, entonces la reserva queda activa. | RF4 |
| CA2 | Dada una reserva 10:00–11:00 del tutor, cuando otro estudiante reserva 10:30 con el mismo tutor, entonces se rechaza con 409. | RN1 |
| CA3 | Dada una reserva 10:00–11:00 del estudiante, cuando reserva a las 10:30 con otro tutor, entonces se rechaza con 409. | RN2 |
| CA4 | Dada una reserva 10:00–11:00, cuando se reserva 11:00 con el mismo tutor, entonces se acepta. | RN9 |
| CA5 | Cuando se reserva fuera de 08:00–18:00 o en fin de semana, entonces 422. | RN3 |
| CA6 | Cuando la duración no es 30/60/90/120 o el inicio no es :00/:30, entonces 422. | RN4 |
| CA7 | Cuando la hora de inicio ya pasó, entonces 422. | RN5 |
| CA8 | Dado un estudiante con 2 reservas ese día, cuando intenta una tercera, entonces 422. | RN6 |
| CA9 | Dada una reserva cancelada, cuando otro estudiante reserva el mismo horario, entonces se acepta; y la disponibilidad lo muestra libre. | RN7, RF6 |
| CA10 | Cuando un estudiante distinto al dueño cancela, entonces 403. | RN8 |
| CA11 | La disponibilidad no muestra franjas ocupadas por reservas activas. | RF3 |

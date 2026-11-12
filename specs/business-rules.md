# Reglas de negocio

| ID | Regla |
|----|-------|
| RN1 | **No doble reserva de tutor**: un tutor no puede tener dos reservas activas que se solapen en el tiempo. |
| RN2 | **No doble reserva de estudiante**: un estudiante no puede tener dos reservas activas que se solapen. |
| RN3 | **Horario de atención**: lunes a viernes, 08:00–18:00. La reserva debe terminar a más tardar a las 18:00. |
| RN4 | **Duración**: 30, 60, 90 o 120 minutos. La hora de inicio debe caer en :00 o :30. |
| RN5 | **No reservar en el pasado**: la hora de inicio debe ser posterior al momento actual. |
| RN6 | **Máximo 2 reservas activas por estudiante por día.** |
| RN7 | **Cancelación libera el espacio**: una reserva cancelada no cuenta para RN1, RN2 ni RN6. |
| RN8 | Solo un estudiante dueño de la reserva puede cancelarla. |
| RN9 | Las reservas contiguas (una termina a la hora en que otra empieza) NO se consideran solapadas. |
| RN10 | **Cancelación con anticipación (CE1)**: solo se puede cancelar si faltan al menos 2 horas para el inicio. |

> Cambios posteriores a estas reglas se registran en `docs/decisions.md` y en el historial de git.

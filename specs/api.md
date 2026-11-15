# API

| Método | Ruta | Descripción | Errores |
|--------|------|-------------|---------|
| POST | /tutors | Crea tutor `{name, subjects}` | 422 |
| POST | /students | Crea estudiante `{name, email}` | 422, 409 correo duplicado |
| GET | /tutors/{id}/availability?date=YYYY-MM-DD | Franjas libres de 30 min | 404 |
| POST | /bookings | Crea reserva `{tutor_id, student_id, start, duration_minutes}` | 404, 409 (conflicto), 422 (regla) |
| POST | /bookings/{id}/cancel | Cancela `{student_id}` | 403, 404, 409 ya cancelada, 422 (<2 h, RN10) |
| GET | /students/{id}/bookings | Reservas del estudiante | 404 |
| GET | /tutors/{id}/bookings | Reservas del tutor | 404 |

409 = conflicto de horario; 422 = violación de regla de validación (RN3–RN6).

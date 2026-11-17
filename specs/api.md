# API

| Método | Ruta | Descripción | Errores |
|--------|------|-------------|---------|
| POST | /tutors | Crea tutor `{name, subjects, photo?}` (`photo` 0–5, por defecto 0) | 422 |
| PATCH | /tutors/{id} | Edita tutor; cuerpo parcial `{name?, subjects?, photo?}` (RF12) | 404, 422 |
| DELETE | /tutors/{id} | Elimina tutor sin reservas activas futuras (RF13, RN12) | 404, 409 |
| GET | /tutors | Lista tutores `[{id, name, subjects, photo}]` | — |
| POST | /students | Crea estudiante `{name, email}` | 422, 409 correo duplicado |
| GET | /students/by-email?email= | Devuelve el estudiante con ese correo (RF9) | 404 |
| GET | /tutors/{id}/availability?date=YYYY-MM-DD | Franjas libres de 30 min | 404 |
| POST | /bookings | Crea reserva `{tutor_id, student_id, start, duration_minutes}` | 404, 409 (conflicto), 422 (regla; >14 días, RN11) |
| POST | /bookings/{id}/cancel | Cancela `{student_id}` | 403, 404, 409 ya cancelada, 422 (<2 h, RN10) |
| GET | /students/{id}/bookings | Reservas del estudiante | 404 |
| GET | /tutors/{id}/bookings | Reservas del tutor | 404 |
| GET | / | Interfaz web del estudiante (HTML estático, RF10) | — |
| GET | /admin | Panel del administrador para registrar tutores (RF11) | — |
| GET | /css/{archivo} | Hoja de estilos compartida | 404 |
| GET | /img/{archivo} | Imágenes de la interfaz (fotos de Unsplash, ver `web/img/CREDITOS.md`) | 404 |

409 = conflicto de horario; 422 = violación de regla de validación (RN3–RN6, RN10, RN11).

Validación de entrada: `start` debe enviarse en hora local sin zona horaria (`2030-01-08T10:00:00`); con zona (`Z`, `-05:00`) → 422 (ver `docs/decisions.md`, D4).

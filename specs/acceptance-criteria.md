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
| CA12 | Dada una reserva que inicia en 3 h, cuando el dueño cancela, entonces se acepta. | RN10 |
| CA13 | Dada una reserva que inicia en 1 h, cuando el dueño cancela, entonces 422 y la reserva sigue activa. | RN10 |
| CA14 | Dado ahora = lunes 10:00, cuando un estudiante reserva una tutoría que inicia exactamente 14 días después (lunes 10:00), entonces se acepta. | RN11 |
| CA15 | Dado ahora = lunes 10:00, cuando un estudiante reserva una tutoría que inicia 14 días y 30 min después (lunes 10:30), entonces 422. | RN11 |
| CA16 | Dados dos tutores registrados, cuando se consulta `GET /tutors`, entonces devuelve ambos con nombre y materias. | RF8 |
| CA17 | Dado un estudiante registrado, cuando se consulta `GET /students/by-email` con su correo (sin importar mayúsculas), entonces 200 con sus datos; con un correo desconocido, 404. | RF9 |
| CA18 | Cuando se abre `GET /`, entonces 200 con la página HTML de reservas. | RF10 |
| CA19 | Desde la interfaz, el flujo reservar → ver en "Mis reservas" → cancelar funciona, y un conflicto (409) o violación de regla (422) se muestra con el mensaje de la API. | RF10, RN1–RN11 |
| CA20 | Cuando se pide `GET /img/hero.jpg` (y las fotos de tutores `/img/t1.jpg`…`t5.jpg`), entonces 200 con `image/jpeg`; una imagen inexistente da 404. | RF10 |
| CA21 | Cuando se crea un tutor con `photo` 3, entonces `GET /tutors` lo devuelve con `photo` 3; sin `photo` queda en 0; con `photo` fuera de 0–5, 422. | RF1 |
| CA22 | Cuando se abre `GET /admin`, entonces 200 con la página "Administración de tutores" (formulario de alta de tutores). | RF11 |
| CA23 | Cuando se abre `GET /` (pantalla del estudiante), entonces NO contiene el formulario de alta de tutores. | RF11 |
| CA24 | Cuando se pide `GET /css/app.css`, entonces 200 con `text/css`. | RF10 |
| CA25 | Dado un tutor, cuando el administrador edita solo su nombre o su foto, entonces `GET /tutors` refleja el cambio y conserva los demás campos; con un tutor inexistente, 404; con nombre vacío o foto fuera de 0–5, 422. | RF12 |
| CA26 | Dado un tutor sin reservas activas futuras, cuando se elimina, entonces 200 y deja de aparecer en `GET /tutors`; un id inexistente da 404. | RF13 |
| CA27 | Dado un tutor con una reserva activa futura, cuando se intenta eliminar, entonces 409 y el tutor sigue en la lista; tras cancelar la reserva, la eliminación se acepta. | RN12 |

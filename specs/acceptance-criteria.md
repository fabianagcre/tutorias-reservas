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
| CA16 | **(a)** Dados dos tutores registrados (Ana/Cálculo y Beto/Física), cuando se consulta `GET /tutors`, entonces 200 con ambos, con su nombre y materias, en el orden en que se registraron. **(b)** Dado que no hay tutores registrados, cuando se consulta `GET /tutors`, entonces devuelve una lista vacía. | RF8 |
| CA17 | **(a)** Dado un estudiante registrado con el correo `Sofia@utp.ac.pa`, cuando se consulta `GET /students/by-email` con `SOFIA@utp.ac.pa`, entonces 200 con ese mismo estudiante (no distingue mayúsculas). **(b)** Dado un correo que no está registrado, cuando se consulta `GET /students/by-email`, entonces 404 con un mensaje que menciona el correo. | RF9 |
| CA18 | Dado el servidor en marcha, cuando se abre `GET /`, entonces 200 con una página HTML que contiene «Reservas de Tutorías». | RF10 |
| CA19a | Dado un estudiante identificado y un tutor con horario libre, cuando reserva desde la interfaz (tutor → fecha y horario → duración → confirmar), entonces la reserva aparece en «Mis reservas». **Verificación manual (E2E con Playwright, `docs/testing.md`); sin prueba automatizada en `tests/`.** | RF10 |
| CA19b | Dada una reserva activa en «Mis reservas», cuando el estudiante la cancela desde la interfaz (con confirmación), entonces figura como «Cancelada» y la pantalla avisa que el horario quedó libre. **Verificación manual (E2E, `docs/testing.md`).** | RF10, RN7 |
| CA19c | Dado un horario que viola una regla, cuando el estudiante intenta reservarlo desde la interfaz, entonces la pantalla muestra en rojo el mensaje (`detail`) que devuelve la API para el 409 (conflicto) o el 422 (regla). **Verificación manual (E2E, `docs/testing.md`; la corrida registrada cubrió el 422 de RN6); el código 409/422 de cada regla ya lo verifican CA1–CA15.** | RF10, RN1–RN11 |
| CA20 | **(a)** Dadas las imágenes de la interfaz, cuando se piden `GET /img/hero.jpg`, `GET /img/t1.jpg` y `GET /img/t5.jpg`, entonces cada una responde 200 con `image/jpeg`. **(b)** Dado un nombre de imagen que no existe, cuando se pide `GET /img/no-existe.jpg`, entonces 404. | RF10 |
| CA21 | **(a)** Dado el catálogo de 5 fotos, cuando se crea un tutor con `photo` 3, entonces 201 y `GET /tutors` lo devuelve con `photo` 3. **(b)** Dado un alta sin `photo`, cuando se crea el tutor, entonces queda con `photo` 0 (sin foto). **(c)** Dado un `photo` fuera de 0–5 (-1, 6 o 99), cuando se crea el tutor, entonces 422. | RF1 |
| CA22 | Dado el servidor en marcha, cuando se abre `GET /admin`, entonces 200 con una página HTML «Administración de tutores» que contiene el formulario de alta (campo de nombre `id="tname"`). | RF11 |
| CA23 | Dado el servidor en marcha, cuando se abre `GET /` (pantalla del estudiante), entonces la página NO contiene el formulario de alta de tutores (ni el campo `id="tname"` ni el texto «Agregar un tutor»). | RF11 |
| CA24 | Dado el servidor en marcha, cuando se pide `GET /css/app.css`, entonces 200 con `text/css`. | RF10 |
| CA25 | **(a)** Dado un tutor (Ana, Cálculo, foto 2), cuando el administrador edita solo su nombre, entonces 200 y se conservan las materias y la foto; y cuando luego edita solo la foto y las materias, `GET /tutors` refleja ambos cambios y conserva el nombre. **(b)** Dado un id de tutor inexistente, cuando se edita, entonces 404. **(c)** Dado un tutor, cuando se edita con nombre en blanco o con foto fuera de 0–5, entonces 422 y el tutor no cambia. | RF12 |
| CA26 | **(a)** Dado un tutor sin reservas activas futuras, cuando el administrador lo elimina, entonces 200 y deja de aparecer en `GET /tutors`. **(b)** Dado un id de tutor inexistente, cuando se elimina, entonces 404. | RF13 |
| CA27 | **(a)** Dado un tutor con una reserva activa futura, cuando el administrador intenta eliminarlo, entonces 409 con un mensaje que menciona la reserva, y el tutor sigue en `GET /tutors`. **(b)** Dado ese mismo tutor después de cancelar la reserva, cuando se elimina, entonces 200. | RN12 |

## Notas del pulido (ciclo 2, CA16–CA27)
Reescritura en Dado / Cuando / Entonces sin cambiar los IDs que citan las pruebas (`tests/test_ui.py`, `tests/test_admin_tutores.py`). Cuando el texto anterior y la prueba no coincidían, el texto se alineó con lo que la prueba verifica:
- **CA16**: se añade el escenario de lista vacía (`test_ca16_listar_tutores_vacio`) y que el orden es el de registro.
- **CA17**: el 404 incluye un mensaje que menciona el correo (lo comprueba la prueba).
- **CA18**: la prueba exige que la página contenga «Reservas de Tutorías».
- **CA19**: se divide en CA19a/b/c. Es el único criterio sin prueba automatizada; se verificó a mano con Playwright (`docs/testing.md`). Queda propuesta una prueba E2E en el repo (rol QA).
- **CA20**: la prueba solo pide `hero.jpg`, `t1.jpg` y `t5.jpg`; el texto anterior decía `t1`…`t5`. Si QA amplía la prueba a `t1`–`t5`, se vuelve a ampliar el criterio.
- **CA22 / CA23**: se nombran las marcas concretas que revisa la prueba (`id="tname"`, «Agregar un tutor»).
- **CA25**: el texto decía «solo su nombre o su foto», pero la prueba también edita las materias; ahora lo dice.
- **CA27**: el 409 trae un mensaje que menciona la reserva (lo comprueba la prueba).
- Fuera de este pulido: CA5, CA6, CA7 y CA11 aún no empiezan con «Dado»; queda el borde de RN12 sin criterio (una reserva activa que ya empezó no bloquea la eliminación).

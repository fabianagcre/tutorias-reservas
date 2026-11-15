# Decisiones

## D1 — Stack: Python + FastAPI + SQLite
Sin infraestructura, suficiente para el alcance. Ver `specs/architecture.md`.

## D2 — Reglas solo en la capa de servicio
La API traduce errores a HTTP; no duplica reglas.

## D3 — Reloj inyectable
Permite probar RN5 (pasado) y la regla de cancelación sin depender de la hora real.

## D4 — Fechas en hora local sin zona horaria
El servicio compara `start` con el reloj local (naive). Un `start` con zona (`...Z`) provocaba un 500 (`TypeError` aware vs naive). La API lo rechaza en el validador de `BookingIn` con 422 pidiendo hora local sin zona; es validación de entrada, así que no se toca `service.py` (D2).

## CE1 — Cambio de especificación: cancelación con 2 horas de anticipación
**Solicitud (a mitad del desarrollo):** "Un estudiante solo puede cancelar si faltan al menos 2 horas para la tutoría."
Ciclo seguido: cambio solicitado → `business-rules.md` (RN10) → `acceptance-criteria.md` (CA12/CA13) → `implementation-plan.md` → `service.py` → pruebas → resultados (`docs/testing.md`).
Rama: `feature/ce1-cancelacion-2h`.

## CE2 — Cambio de especificación: reserva con máximo 14 días de anticipación
**Solicitud (a mitad del desarrollo):** "Para evitar que pocos estudiantes acaparen la agenda del tutor, una reserva solo puede hacerse si la tutoría inicia como máximo 14 días después del momento actual."
Ciclo seguido: cambio solicitado → `business-rules.md` (RN11) → `acceptance-criteria.md` (CA14/CA15) → `implementation-plan.md` y `api.md` → pruebas (rojas) → `service.py` → pruebas verdes.
Borde: exactamente 14 días se acepta; cualquier exceso (incluso 1 s) da 422. Como el "ahora" de `tests/conftest.py` es 07:00 (fuera de RN3), las pruebas fijan el reloj inyectado a las 10:00.
Rama: `feature/ce2-anticipacion-maxima`.
Resultado: 28 passed

## D5 — Interfaz web estática servida por FastAPI
**Contexto:** solo había API + Swagger; el estudiante no tenía una forma real de reservar (outcomes O2/O3).
**Decisión:** una página única (`src/tutorias/web/index.html`, HTML/CSS/JS puro) servida en `/`, con flujo por pasos inspirado en SimplyBook.me: elegir tutor → fecha y horario → confirmar → mis reservas. Sin framework ni paso de build, para no tocar el stack ni el CI. Estilo visual tomado de la referencia de SimplyBook.me (fondo blanco/celeste, títulos azul marino con palabra resaltada, botones en píldora coral y celeste, hero con curva y widget de reserva con pestañas); ilustración y logotipo propios (SVG), ilustraciones y logotipo propios (SVG). Fotos de Unsplash (licencia gratuita, créditos en `web/img/CREDITOS.md`) descargadas al repo para no depender de internet en la demo. El `<select>` y el `<input type="date">` nativos se reemplazaron por un desplegable y un calendario propios (accesibles con teclado: flechas, Enter, Esc) con las mismas restricciones de las reglas: sin fines de semana, sin pasado y hasta 14 días. La foto del tutor la elige quien lo registra (catálogo de 5, 0 = sin foto) y se guarda en `tutors.photo` (RF1, CA21), para que el nombre y la foto coincidan; los tutores existentes quedan sin foto (muestran su inicial). `db.connect` migra bases viejas con `ALTER TABLE`. Paleta y logo: se usa el escudo oficial de la UTP y los colores del logo (morado `#482868`, verde `#284838`, negro y dorado `#b88828`).
**Consecuencias:** la interfaz no duplica reglas (D2): muestra el mensaje que devuelve la API (409/422). Se añadieron `GET /tutors` y `GET /students/by-email` (identificación por correo, sin contraseña: alcance del curso; la sesión se guarda en `localStorage`). Todo texto dinámico se inserta con `textContent`, nunca como HTML.
**Rama / issue:** `feature/interfaz-web`, issue #10.

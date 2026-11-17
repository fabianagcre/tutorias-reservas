# Ensayo del cambio de requerimiento en vivo (CE3)

En la presentación el profesor puede pedir un cambio inesperado. Este documento prepara tres pedidos posibles y registra un ensayo cronometrado.

Ciclo que seguimos en todos los casos (igual que CE1 y CE2, ver `docs/decisions.md`):

1. Cambio solicitado (frase exacta del profesor).
2. Especificación: `specs/business-rules.md` (y `requirements.md` / `api.md` si hay endpoint nuevo).
3. Criterios de aceptación: `specs/acceptance-criteria.md` en Dado/Cuando/Entonces.
4. Plan: fila nueva en `specs/implementation-plan.md`.
5. Pruebas primero (rojas) en `tests/`.
6. Código mínimo en `src/tutorias/service.py` (y `api.py` si hay endpoint).
7. Resultados: `pytest -q`, fila del plan cerrada y entrada en `docs/decisions.md`.

Reparto en vivo: Uriel escribe la regla y los criterios (pasos 1–4), Mike escribe las pruebas (paso 5), Fabiana escribe el código (paso 6) y Mike corre la suite (paso 7).

---

## Pedido 1 — Límite semanal de horas

> «Un estudiante no puede acumular más de 3 horas de tutoría por semana.»

**Regla nueva:** RN13. Semana de lunes a domingo, la de la fecha de inicio de la reserva; cuentan solo las reservas activas (RN7); llegar justo a 180 min se acepta, pasarse da 422.

**Archivos de `specs/`:** `business-rules.md` (RN13), `acceptance-criteria.md` (CE3-a, CE3-b), `implementation-plan.md` (fila CE3), `api.md` (`POST /bookings` añade «422 por RN13» y la leyenda del 422).

**Criterios nuevos:**

| ID | Criterio | Regla |
|----|----------|-------|
| CE3-a | Dado un estudiante con reservas activas de 60 min el lunes y el martes de la misma semana (120 min), cuando reserva 60 min el miércoles de esa semana (total justo 180 min), entonces se acepta. | RN13 |
| CE3-b | Dado un estudiante con 180 min de reservas activas en la semana (lunes, martes y miércoles), cuando reserva 30 min el jueves de esa semana (total 210 min), entonces se rechaza con 422. | RN13 |
| CE3-c | Dado un estudiante con 180 min en la semana de los que se cancela una reserva de 60 min, cuando reserva 60 min en esa semana, entonces se acepta (las canceladas no suman). | RN13, RN7 |

**Orden del ciclo:** RN13 → CE3-a/b/c → plan y `api.md` → pruebas rojas → validación en `create_booking` → pytest completo.

**Riesgos:**
- Ambigüedad de «semana»: ¿calendario (lunes–domingo) o los últimos 7 días? Hay que preguntarle al profesor y escribir la respuesta en la regla.
- ¿Cuentan las reservas activas que ya pasaron en esa misma semana? En el ensayo se decidió que sí.
- Las pruebas deben repartir las reservas en días distintos para no chocar con RN6 (máx. 2 por día).

## Pedido 2 — Fechas bloqueadas por el tutor (feriados)

> «Los tutores pueden bloquear fechas (feriados) y en ellas no se puede reservar.»

**Regla nueva:** RN14. Un tutor puede marcar una fecha como bloqueada; ese día no se puede reservar con ese tutor (422) y la disponibilidad de ese día sale vacía.

**Archivos de `specs/`:** `requirements.md` (RF14: bloquear y desbloquear fechas), `business-rules.md` (RN14), `data-model.md` (tabla `blocked_dates(tutor_id, date)`, única por tutor y fecha), `api.md` (`POST /tutors/{id}/blocked-dates {date}`, `DELETE /tutors/{id}/blocked-dates/{date}`, `GET /tutors/{id}/blocked-dates`, y el 422 nuevo en `POST /bookings`), `acceptance-criteria.md`, `implementation-plan.md`.

**Criterios nuevos:**

| ID | Criterio | Regla |
|----|----------|-------|
| CE3-d | Dado un tutor con el martes bloqueado, cuando un estudiante reserva con ese tutor el martes a las 10:00, entonces 422 y la reserva no se crea. | RN14 |
| CE3-e | Dado un tutor con el martes bloqueado, cuando se consulta su disponibilidad del martes, entonces la lista de franjas está vacía. | RN14, RF3 |
| CE3-f | Dado un tutor con el martes bloqueado, cuando otro tutor sin bloqueo recibe una reserva el martes, entonces se acepta (el bloqueo es por tutor). | RN14 |
| CE3-g | Dado un tutor con el martes bloqueado, cuando se desbloquea y se reserva el martes, entonces se acepta. | RF14 |

**Orden del ciclo:** RF14/RN14 → modelo de datos y API → criterios → plan → pruebas rojas (servicio y HTTP) → tabla nueva en `db.py`, servicio y endpoints → pytest completo.

**Riesgos:**
- Es el pedido más grande: tabla nueva, tres endpoints y cambios en la disponibilidad. Difícilmente cabe en 15 minutos; en vivo conviene hacer solo el servicio, la regla y `POST`, y dejar `DELETE` y `GET` como siguiente paso.
- ¿Qué pasa con las reservas que ya existen en una fecha que se bloquea después? Hay que decidir si se rechaza el bloqueo (409, como RN12) o se permite y se avisa.
- Una base vieja necesita migración (como `photo` en `db.connect`).
- ¿Quién bloquea? Si es el tutor, no hay pantalla de tutor; si es el administrador, va en `/admin` (sin autenticación, D6).

## Pedido 3 — Duración mínima de 60 minutos

> «La duración mínima de una tutoría pasa a 60 minutos.»

**Regla modificada:** RN4 pasa a «60, 90 o 120 minutos; inicio en :00 o :30».

**Archivos de `specs/`:** `business-rules.md` (RN4), `acceptance-criteria.md` (CA6 y criterios nuevos), `implementation-plan.md`. `api.md` no cambia de códigos (sigue siendo 422). Revisar `requirements.md` RF3: la disponibilidad sigue en franjas de 30 min porque el inicio puede ser :30.

**Criterios nuevos o modificados:**

| ID | Criterio | Regla |
|----|----------|-------|
| CE3-h | Dado un tutor libre el martes, cuando un estudiante reserva 30 min a las 10:00, entonces 422 con un mensaje que indica las duraciones permitidas. | RN4 |
| CE3-i | Dado un tutor libre el martes, cuando un estudiante reserva 60 min a las 10:00, entonces se acepta. | RN4 |
| CA6 (modificado) | Dado un tutor libre, cuando la duración no es 60/90/120 o el inicio no es :00/:30, entonces 422. | RN4 |

**Pruebas existentes que usan 30 min** (búsqueda en `tests/` de esta rama, 55 pruebas):

| Prueba | Línea | Qué hace con 30 min | Efecto del cambio |
|---|---|---|---|
| `test_booking_rules.py::test_ca2_no_doble_reserva_tutor` | 18 | Espera 409 al reservar 10:30 por 30 min sobre una reserva 10:00–11:00 | **Se rompe:** `_validate_slot` (RN4) corre antes del cruce, así que daría 422 en vez de 409. Cambiar a 60 min. |
| `test_booking_rules.py::test_ca5_horario_de_atencion` | 37 | Caso `(TUE, "07:30", 30)` espera 422 | Sigue pasando, pero por RN4 y no por RN3: deja de probar el horario. Cambiar a 60 min. |
| `test_booking_rules.py::test_ca8_maximo_dos_por_dia` | 56, 57, 59 | Tres reservas de 30 min (08:00, 09:00, 10:00); espera la 3.ª en 422 | **Se rompe:** la primera ya da 422. Cambiar las tres a 60 min (08:00, 09:00 y 10:00 siguen sin cruzarse). |
| `test_booking_rules.py::test_ca6_duracion_e_inicio` | 43 | Casos 45 y 150 | No se rompe; hay que **añadir** el caso 30 → 422. |

Fuera de `tests/` también usan 30 min: la lista `DUR` de `src/tutorias/web/index.html` (línea 228, opción «30 minutos») y el mensaje de error de `service.py` («30, 60, 90 o 120»). En la rama del ensayo, CE3-b (`tests/test_ce3_ensayo.py`) reserva 30 min el jueves; si se aplicaran ambos cambios habría que pasarlo a 60 min.

**Orden del ciclo:** RN4 → CA6 modificado y CE3-h/i → plan → ajustar las pruebas de la tabla y añadir las nuevas (rojas) → `ALLOWED_DURATIONS = (60, 90, 120)` y su mensaje → quitar la opción de 30 min de la interfaz → pytest completo.

**Riesgos:**
- Es el único pedido que **rompe pruebas que ya pasaban**: hay que explicar en vivo que cambiar las pruebas es parte del cambio de especificación, no un truco para ponerlas en verde.
- Las reservas de 30 min que ya existen en la base siguen siendo válidas (la regla se aplica al crear); hay que decirlo en la regla.
- Si se olvida la interfaz, el estudiante ve una opción que siempre da 422.

---

## Ensayo realizado (CE3-1)

Se ensayó el **pedido 1** (RN13, límite de 3 h por semana) el 2026-11-15, en la rama local `feature/ce3-ensayo`, creada desde `main` (34 pruebas). La rama **no se fusionó** a `main` ni se subió: es solo práctica.

**Quién:** Uriel con Claude Code, sin Fabiana ni Mike. Por eso el tiempo no incluye la coordinación entre tres personas.

**Tiempos por paso** (hora tomada con `date +%T` al empezar y al terminar cada paso; la hora de cada commit coincide con el fin del paso, ±1 s):

| Paso | Inicio | Fin | Duración | Commit |
|---|---|---|---|---|
| 1. Spec RN13 (`business-rules.md`) | 19:18:51 | 19:19:23 | 32 s | `177c958` |
| 2. Criterios CE3-a / CE3-b | 19:19:45 | 19:19:46 | 1 s | `783796d` |
| 3. Plan (`implementation-plan.md`) y `api.md` | 19:20:13 | 19:20:15 | 2 s | `87c1309` |
| 4. Pruebas primero (rojas) | 19:20:41 | 19:21:03 | 22 s | `19dc46d` |
| 5. Código mínimo (`service.py`) | 19:21:29 | 19:22:55 | 1 min 26 s | `2e681ec` |
| 6. Resultados (pytest completo y fila del plan) | 19:23:11 | 19:23:40 | 29 s | `e3839e5` |
| **Total, de punta a punta** | 19:18:51 | 19:23:40 | **4 min 49 s** | |

**Total frente a la meta:** 4 min 49 s, frente a una meta de menos de 15 min. Las duraciones por paso se ven más cortas de lo real: el texto de cada paso se redactó antes de llamar a `date`, así que ese tiempo cae en los huecos entre pasos (de 16 a 34 s). El total sí lo incluye.

**Resultados:**
- Pruebas rojas (paso 4, solo `tests/test_ce3_ensayo.py`): `2 failed, 3 passed`. Fallaron CE3-b y la prueba HTTP del 422. Las 3 que pasan (CE3-a, canceladas y otra semana) son casos que deben aceptarse y sirven de guarda contra una regla que rechace de más.
- Suite completa (paso 6): `39 passed, 1 warning in 1.23s` (34 de `main` + 5 nuevas). El aviso es la deprecación de `httpx` en Starlette, que ya existía.

**Dificultades:**
- El primer intento de código falló al importar (`SyntaxError`) porque se perdieron las comillas del SQL al editar con un script dentro de un heredoc. Costó unos 40 s. En vivo conviene editar directamente en el editor.
- La regla toma la semana de la fecha de inicio de la reserva, no la de «ahora»; las reservas activas que ya pasaron en esa semana también cuentan.
- No se actualizaron `docs/decisions.md` ni `docs/testing.md` en la rama del ensayo. En la presentación sí hay que hacerlo, como en CE1 y CE2.

## Pendiente

- **Repetir el ensayo con Fabiana (código) y Mike (pruebas)**, con Uriel en la spec y los criterios, para medir el tiempo real con coordinación y traspasos.
- Decidir con el equipo si en vivo se usa el pedido 1 (ya ensayado) o el 3 (rompe pruebas existentes y es más vistoso).
- Descartar o archivar la rama `feature/ce3-ensayo` después del ensayo con el equipo.

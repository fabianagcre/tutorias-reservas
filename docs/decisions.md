# Decisiones

## D1 — Stack: Python + FastAPI + SQLite
Sin infraestructura, suficiente para el alcance. Ver `specs/architecture.md`.

## D2 — Reglas solo en la capa de servicio
La API traduce errores a HTTP; no duplica reglas.

## D3 — Reloj inyectable
Permite probar RN5 (pasado) y la regla de cancelación sin depender de la hora real.

## CE1 — Cambio de especificación: cancelación con 2 horas de anticipación
**Solicitud (a mitad del desarrollo):** "Un estudiante solo puede cancelar si faltan al menos 2 horas para la tutoría."
Ciclo seguido: cambio solicitado → `business-rules.md` (RN10) → `acceptance-criteria.md` (CA12/CA13) → `implementation-plan.md` → `service.py` → pruebas → resultados (`docs/testing.md`).
Rama: `feature/ce1-cancelacion-2h`.

## CE2 — Cambio de especificación: reserva con máximo 14 días de anticipación
**Solicitud (a mitad del desarrollo):** "Para evitar que pocos estudiantes acaparen la agenda del tutor, una reserva solo puede hacerse si la tutoría inicia como máximo 14 días después del momento actual."
Ciclo seguido: cambio solicitado → `business-rules.md` (RN11) → `acceptance-criteria.md` (CA14/CA15) → `implementation-plan.md` y `api.md` → pruebas (rojas) → `service.py` → pruebas verdes.
Borde: exactamente 14 días se acepta; cualquier exceso (incluso 1 s) da 422. Como el "ahora" de `tests/conftest.py` es 07:00 (fuera de RN3), las pruebas fijan el reloj inyectado a las 10:00.
Rama: `feature/ce2-anticipacion-maxima`.
Resultado: 27 passed

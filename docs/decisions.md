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

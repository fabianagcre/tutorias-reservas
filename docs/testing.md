# Estrategia de pruebas

- `tests/test_booking_rules.py`: unitarias de reglas de negocio y una prueba por criterio de aceptación (CA1–CA11).
- `tests/test_concurrency.py`: **no doble reserva (RN1)** con 10 hilos compitiendo por el mismo horario.
- `tests/test_api_acceptance.py`: flujo HTTP completo (reserva → conflicto 409 → cancelación → re-reserva).
- Ejecutar: `pytest`. CI: `.github/workflows/ci.yml`.

## Resultados
Ver el último run en GitHub Actions.

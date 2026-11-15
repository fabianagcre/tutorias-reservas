# Estrategia de pruebas

- `tests/test_booking_rules.py`: unitarias de reglas de negocio y una prueba por criterio de aceptación (CA1–CA13).
- `tests/test_concurrency.py`: **no doble reserva (RN1)** con 10 hilos compitiendo por el mismo horario.
- `tests/test_api_acceptance.py`: flujo HTTP completo (reserva → conflicto 409 → cancelación → re-reserva).
- Pruebas nuevas (QA ciclo 1, rama `qa/ciclo1-observaciones-pr4`):
  - `test_rn10_borde_exacto_de_2h` (reloj mutable `reloj` en `conftest.py`): reserva 10:00; reloj 08:00 → se cancela, 08:00:01 → 422, 07:59:59 → se cancela.
  - `test_ca12_cancelar_con_anticipacion` / `test_ca13_no_cancelar_con_menos_de_2h`: alineadas con los datos de CA12 (inicia en 3 h) y CA13 (inicia en 1 h).
  - `test_cancelar_con_menos_de_2h_devuelve_422`: cancelación HTTP con <2 h → 422 y la reserva sigue activa.
  - `test_start_con_zona_horaria_devuelve_422`: `start` con zona (`Z`, `-05:00`) → 422 en lugar de 500 (D4).
- Ejecutar: `pytest`. CI: `.github/workflows/ci.yml`.

## Resultados
Run local en la rama `qa/ciclo1-observaciones-pr4` (Python 3.13, `python -m pytest -q`):

```
..............................                                           [100%]
30 passed, 1 warning in 0.92s
```

El aviso es una deprecación de `httpx` en `starlette.testclient`, ajena al proyecto. CI: ver el último run en GitHub Actions.

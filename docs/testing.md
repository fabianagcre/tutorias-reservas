# Estrategia de pruebas

- `tests/test_booking_rules.py`: unitarias de reglas de negocio y una prueba por criterio de aceptación (CA1–CA13).
- `tests/test_concurrency.py`: **no doble reserva (RN1)** con 10 hilos compitiendo por el mismo horario.
- `tests/test_api_acceptance.py`: flujo HTTP completo (reserva → conflicto 409 → cancelación → re-reserva).
- Pruebas nuevas (QA ciclo 1, rama `qa/ciclo1-observaciones-pr4`):
  - `test_rn10_borde_exacto_de_2h` (reloj mutable `reloj` en `conftest.py`): reserva 10:00; reloj 08:00 → se cancela, 08:00:01 → 422, 07:59:59 → se cancela.
  - `test_ca12_cancelar_con_anticipacion` / `test_ca13_no_cancelar_con_menos_de_2h`: alineadas con los datos de CA12 (inicia en 3 h) y CA13 (inicia en 1 h).
  - `test_cancelar_con_menos_de_2h_devuelve_422`: cancelación HTTP con <2 h → 422 y la reserva sigue activa.
  - `test_start_con_zona_horaria_devuelve_422`: `start` con zona (`Z`, `-05:00`) → 422 en lugar de 500 (D4).
- Interfaz web (RF8–RF10, `tests/test_ui.py`): `GET /tutors` (CA16), `GET /students/by-email` con 200/404 y sin distinguir mayúsculas (CA17) y `GET /` devuelve la página (CA18).
- `test_ca20_imagenes_estaticas`: las fotos se sirven en `/img/*` (200 `image/jpeg`) y una inexistente da 404 (CA20).
- CA19 (flujo en la pantalla) se verificó a mano con un navegador automatizado (Chrome + Playwright, local, no forma parte del repo): registro → crear tutor → calendario propio (días deshabilitados, límite de 14 días, clic afuera y Esc cierran) y desplegable de duración (ratón y teclado) → reservar 10:00 → intento de 3.ª reserva del día (RN6) con el mensaje de la API → cancelar con confirmación → la sesión persiste al recargar → vista móvil.
- Ejecutar: `pytest`. CI: `.github/workflows/ci.yml`.

## Resultados
Run local en la rama `feature/interfaz-web` (Python 3.14, `python -m pytest -q`; incluye QA ciclo 1, CE2 y la interfaz):

```
40 passed, 2 warnings in 2.37s
```

El aviso es una deprecación de `httpx` en `starlette.testclient`, ajena al proyecto. CI: ver el último run en GitHub Actions.

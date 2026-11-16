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
- `test_ca21_foto_del_tutor` y `test_ca21_foto_fuera_de_rango_422` (3 casos): la foto se guarda y se lista; por defecto 0; fuera de 0–5 → 422 (CA21).
- `test_ca22_panel_admin`, `test_ca23_el_estudiante_no_ve_el_alta_de_tutores`, `test_ca24_hoja_de_estilos`: el panel `/admin` existe, la pantalla del estudiante no tiene el alta de tutores y los estilos se sirven en `/css/app.css` (CA22–CA24).
- Colores de los mensajes verificados en el navegador: error `rgb(176,16,47)` sobre rosado, éxito verde, aviso neutro morado.
- `tests/test_admin_tutores.py` (8 casos): editar parcialmente y con datos inválidos, eliminar sin reservas, 404 y el bloqueo con reserva activa futura que se levanta al cancelar (CA25–CA27, RN12).
- CA19 (flujo en la pantalla) se verificó a mano con un navegador automatizado (Chrome + Playwright, local, no forma parte del repo): registro → crear tutor → calendario propio (días deshabilitados, límite de 14 días, clic afuera y Esc cierran) y desplegable de duración (ratón y teclado) → elegir la foto del tutor al registrarlo (queda guardada y aparece en la tarjeta correcta) → reservar 10:00 → intento de 3.ª reserva del día (RN6) con el mensaje de la API → cancelar con confirmación → la sesión persiste al recargar → vista móvil.
- Ejecutar: `pytest`. CI: `.github/workflows/ci.yml`.

- QA ciclo 2 (`tests/test_qa_ciclo2.py`, rama `qa/ciclo2-cobertura`): bug de RN11 en la disponibilidad hallado en el recorrido manual (prueba roja `b08e69e` → corrección `fd5e4c4`), validaciones del servicio sin pasar por la API, RN12 con una reserva ya pasada, migración de una base sin la columna `photo` y `GET /tutors/{id}/bookings`.

## Matriz de trazabilidad CA → prueba

| CA | Regla / RF | Prueba(s) |
|---|---|---|
| CA1 | RF4 | `test_booking_rules.py::test_ca1_reserva_valida` |
| CA2 | RN1 | `test_booking_rules.py::test_ca2_no_doble_reserva_tutor`, `test_concurrency.py::test_no_doble_reserva_concurrente`, `test_api_acceptance.py::test_flujo_completo_reserva_conflicto_cancelacion` |
| CA3 | RN2 | `test_booking_rules.py::test_ca3_no_doble_reserva_estudiante` |
| CA4 | RN9 | `test_booking_rules.py::test_ca4_reservas_contiguas_permitidas` |
| CA5 | RN3 | `test_booking_rules.py::test_ca5_horario_de_atencion` (3 casos), `test_api_acceptance.py::test_reglas_devuelven_422` |
| CA6 | RN4 | `test_booking_rules.py::test_ca6_duracion_e_inicio` (3 casos) |
| CA7 | RN5 | `test_booking_rules.py::test_ca7_no_reservar_en_el_pasado` |
| CA8 | RN6 | `test_booking_rules.py::test_ca8_maximo_dos_por_dia` |
| CA9 | RN7, RF6 | `test_booking_rules.py::test_ca9_cancelar_libera_el_espacio`, `test_api_acceptance.py::test_flujo_completo_reserva_conflicto_cancelacion` (vía HTTP) |
| CA10 | RN8 | `test_booking_rules.py::test_ca10_solo_el_dueno_cancela` |
| CA11 | RF3 | `test_booking_rules.py::test_ca11_disponibilidad_excluye_ocupadas` |
| CA12 | RN10 | `test_booking_rules.py::test_ca12_cancelar_con_anticipacion`, `test_rn10_borde_exacto_de_2h` |
| CA13 | RN10 | `test_booking_rules.py::test_ca13_no_cancelar_con_menos_de_2h`, `test_api_acceptance.py::test_cancelar_con_menos_de_2h_devuelve_422` |
| CA14 | RN11 | `test_ce2_anticipacion.py::test_ca14_reserva_a_14_dias_exactos` |
| CA15 | RN11 | `test_ce2_anticipacion.py::test_ca15_reserva_a_14_dias_y_30_min`, `test_ce2_borde_14_dias_mas_1_segundo`, `test_ce2_http_reserva_a_mas_de_14_dias_devuelve_422`, `test_qa_ciclo2.py::test_rn11_disponibilidad_no_ofrece_horarios_a_mas_de_14_dias` |
| CA16 | RF8 | `test_ui.py::test_ca16_listar_tutores`, `test_ca16_listar_tutores_vacio` |
| CA17 | RF9 | `test_ui.py::test_ca17_estudiante_por_correo` (mayúsculas), `test_ca17_correo_desconocido_404` |
| CA18 | RF10 | `test_ui.py::test_ca18_pagina_principal` |
| CA19 | RF10, RN1–RN11 | **Sin prueba automatizada en el repo.** Recorrido manual con navegador (Playwright, local) — ver «Recorrido manual QA ciclo 2» |
| CA20 | RF10 | `test_ui.py::test_ca20_imagenes_estaticas` |
| CA21 | RF1 | `test_ui.py::test_ca21_foto_del_tutor`, `test_ca21_foto_fuera_de_rango_422` (3 casos) |
| CA22 | RF11 | `test_ui.py::test_ca22_panel_admin` |
| CA23 | RF11 | `test_ui.py::test_ca23_el_estudiante_no_ve_el_alta_de_tutores` |
| CA24 | RF10 | `test_ui.py::test_ca24_hoja_de_estilos` |
| CA25 | RF12 | `test_admin_tutores.py::test_ca25_editar_parcialmente_conserva_el_resto`, `test_ca25_editar_tutor_inexistente_404`, `test_ca25_editar_con_datos_invalidos_422` (3 casos) |
| CA26 | RF13 | `test_admin_tutores.py::test_ca26_eliminar_tutor_sin_reservas`, `test_ca26_eliminar_tutor_inexistente_404` |
| CA27 | RN12 | `test_admin_tutores.py::test_ca27_no_se_elimina_con_reserva_activa_futura`, `test_qa_ciclo2.py::test_rn12_una_reserva_pasada_no_bloquea_eliminar_al_tutor` |

## Recorrido manual QA ciclo 2 (PR #11, 2026-11-16)

Navegador automatizado (Chromium + Playwright, local, fuera del repo), reloj del servidor fijo en martes 17-nov-2026 07:00, zona `America/Panama`. 18 de 21 comprobaciones ✅.

| # | Comprobación | Resultado |
|---|---|---|
| A1 | Registrar tutor con nombre, materias y foto | ✅ aparece con `/img/t3.jpg` |
| A2 | Guardar con nombre vacío → mensaje rojo | ⚠️ rojo, pero el texto es «El nombre es obligatorio.» (validación del navegador), no «El nombre del tutor es obligatorio» |
| A3 | Editar nombre/materias/foto; «Cancelar» no cambia nada | ✅ |
| A4 | Eliminar sin reservas (pide «Sí, eliminar») | ✅ |
| A5 | Eliminar con reserva futura → rojo (RN12); tras cancelar, se elimina | ✅ |
| S1 | Correo nuevo pide nombre; existente (en mayúsculas) entra directo | ✅ |
| S2 | Tutor → calendario → horario → duración → confirmar | ✅ el calendario bloquea pasado, fines de semana y > 14 días |
| S2c | Día 14 (1-dic) a las 10:00 | ❌ el calendario ofrecía la hora y la API la rechazaba con 422 (RN11). **Corregido** en `fd5e4c4` |
| S3 | Tercera reserva del día → rojo (RN6) | ✅ |
| S4 | Otro estudiante, mismo horario del tutor → rojo (RN1) | ✅ y el horario deja de ofrecerse |
| S5 | Cancelar con confirmación; con < 2 h → rojo (RN10) | ✅ |
| S6 | El estudiante no ve formulario de tutores | ✅ |
| S7 | Móvil 390 px sin desbordes; la sesión sigue tras recargar | ✅ |
| extra | Tras eliminar un tutor, «Mis reservas» de una sesión abierta | ⚠️ sigue mostrando el nombre antiguo hasta recargar (la lista de tutores queda en caché en el navegador) |

## Resultados
Run local en la rama `qa/ciclo2-cobertura` (Python 3.12.13, macOS), `pytest -q --cov=src/tutorias --cov-branch --cov-report=term-missing`:

```
================================ tests coverage ================================
______________ coverage: platform darwin, python 3.12.13-final-0 _______________

Name                       Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------------
src/tutorias/__init__.py       0      0      0      0   100%
src/tutorias/api.py           83      0      2      0   100%
src/tutorias/db.py            10      0      2      0   100%
src/tutorias/service.py      141      0     46      0   100%
----------------------------------------------------------------------
TOTAL                        234      0     50      0   100%
60 passed, 1 warning in 0.73s
```

El aviso es una deprecación de `httpx` en `starlette.testclient`, ajena al proyecto. CI: ver el run del PR en GitHub Actions.

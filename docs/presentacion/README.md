# Presentación del Proyecto 2

- **`index.html`** — la presentación (un solo archivo; abre en cualquier navegador). Las imágenes están en `assets/`.
- **`Reservas-Tutorias.pdf`** — copia en PDF por si falla el proyector (19 páginas).

## Cómo presentarla
Abre `index.html` en el navegador y pon pantalla completa (F11).

| Tecla | Acción |
|---|---|
| ← → · espacio | cambiar de diapositiva |
| **N** | ver las **notas del presentador** (quién presenta y qué decir) |
| **E** | modo edición: cambia cualquier texto; **Ctrl+S** descarga el HTML editado |
| Inicio / Fin | primera / última |

Se puede abrir una diapositiva concreta con `index.html#7`.

## Quién presenta qué (sugerido)
1–6 Uriel (problema, outcomes, SDD, reglas) · 6–10 Fabiana (arquitectura y demo) · 11–13 Uriel y Fabiana (cambios de especificación) · 14–15 Mike (pruebas y CI) · 16–19 todos.

## Antes de presentar
1. `python scripts/seed_demo.py` y levantar el servidor (`uvicorn --app-dir src tutorias.api:create_app --factory`).
2. Probar `http://localhost:8000/` y `http://localhost:8000/admin`.
3. Las fuentes se cargan de Google Fonts: sin internet se ven con una letra del sistema (el contenido no cambia).

Las capturas de `assets/` son de la aplicación real con datos de demostración.

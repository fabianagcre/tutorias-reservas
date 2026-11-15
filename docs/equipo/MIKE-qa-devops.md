# Pasos para Mike — QA / DevOps Lead (ciclo 2)

> **Cómo usar este archivo:** ábrelo en tu IA (Claude, Copilot, ChatGPT, la que uses) y pégale todo el contenido, o dile:
> *«Lee `docs/equipo/MIKE-qa-devops.md` y ayúdame a hacer los pasos en orden. Trabaja en ramas, haz commits pequeños y no hagas push a `main`.»*
> Todo lo que hagas con IA se anota en `docs/ai-log.md` (ver sección 5).

## 1. Contexto del proyecto (léelo primero)

- **Materia:** Tópicos Especiales II, Prof. Regis Rivera. **Proyecto 2:** sistema de reservas de **tutorías universitarias** con el recorrido **ODD → SDD → código → pruebas → valor al usuario**. Se evalúa el *proceso*, no la herramienta.
- **Repo:** https://github.com/fabianagcre/tutorias-reservas (acepta la invitación si aún no lo hiciste).
- **Stack:** Python 3.11+, FastAPI, SQLite, pytest, GitHub Actions. Interfaz web estática (HTML/CSS/JS sin build).
- **Equipo y roles del ciclo 2:** Uriel = **Product/Spec Lead** · Fabiana = **Architecture/Dev Lead** · Michael (Mike) = **QA/DevOps Lead** (tú; a confirmar en el README).
- **Estado actual (15-nov-2026):**
  - `main`: reglas RN1–RN11, cambios de especificación CE1 (cancelar con ≥2 h) y CE2 (reservar máx. 14 días), QA ciclo 1 (hecho por Uriel). **34 pruebas**, CI verde.
  - **PR #9** `chore/ciclo2-arquitectura-dev`: `.gitignore`, `architecture.md`, `ai-log`. Abierto, sin revisión.
  - **PR #11** `feature/interfaz-web`: interfaz del estudiante (`/`), panel del administrador (`/admin`), editar/eliminar tutores, foto del tutor, diseño con logo y colores de la UTP. Añade RF8–RF13, RN12, CA16–CA27. **55 pruebas**, CI verde. Abierto, sin revisión.
  - Orden de merge acordado: **#9 primero, luego #11** (chocan solo en `docs/ai-log.md` y `docs/decisions.md`; lo resuelve Fabiana conservando ambas versiones).
- **Reglas de negocio:** RN1 no doble reserva del tutor · RN2 no doble reserva del estudiante · RN3 lun–vie 08:00–18:00 · RN4 duración 30/60/90/120 e inicio :00/:30 · RN5 no reservar en el pasado · RN6 máx. 2 reservas activas/día por estudiante · RN7 cancelar libera el espacio · RN8 solo el dueño cancela · RN9 reservas contiguas permitidas · RN10 cancelar con ≥2 h (CE1) · RN11 reservar máx. 14 días antes (CE2) · RN12 no eliminar un tutor con reservas activas futuras.
- **Pruebas actuales:** `tests/test_booking_rules.py` (reglas y CA1–CA13), `tests/test_concurrency.py` (**no doble reserva con 10 hilos**, obligatoria en la rúbrica), `tests/test_api_acceptance.py`, `tests/test_ce2_anticipacion.py`, `tests/test_ui.py`, `tests/test_admin_tutores.py`. El reloj es inyectable (`reloj` en `tests/conftest.py`).

### Cómo levantar el proyecto (PowerShell)
```powershell
git clone https://github.com/fabianagcre/tutorias-reservas.git
cd tutorias-reservas
git fetch --all
git checkout feature/interfaz-web
pip install -r requirements.txt
pytest -q                                 # debe dar 55 passed
python scripts/seed_demo.py               # tutores de demostración con foto
uvicorn --app-dir src tutorias.api:create_app --factory --reload
# Estudiante: http://localhost:8000/   ·   Admin: http://localhost:8000/admin   ·   API: http://localhost:8000/docs
```

### Flujo de trabajo obligatorio
issue → rama (`qa/…`, `ci/…`, `test/…`) **desde `main`** → commits pequeños con prefijo (`test:`, `ci:`, `docs:`, `fix:`, `chore:`) → Pull Request a `main` → **revisión de otra persona** + CI verde → merge. **Nunca push directo a `main`.** Para pruebas nuevas: primero **roja**, luego el código, luego **verde** (queda en el historial como evidencia).

## 2. Tu parte (qué te toca como QA/DevOps)

Responsable de **pruebas, integración y despliegue**. Los pasos, en orden de prioridad:

### Paso 1 — Revisar y validar los PR #9 y #11 (lo más urgente)
1. Corre `pytest -q` en `feature/interfaz-web` (esperado: **55 passed**) y en `chore/ciclo2-arquitectura-dev` (esperado: **34 passed**).
2. Recorrido manual (anota ✅/❌ y captura de pantalla de cada fallo):

   **Administrador — `/admin`**
   - [ ] Registrar un tutor con nombre, materias y foto → aparece con la foto elegida.
   - [ ] Guardar con el nombre vacío → mensaje **rojo** «El nombre del tutor es obligatorio».
   - [ ] Editar un tutor (nombre/materias/foto) → se guarda; «Cancelar» no cambia nada.
   - [ ] Eliminar un tutor sin reservas (pide confirmar «Sí, eliminar») → desaparece.
   - [ ] Eliminar un tutor **con** una reserva futura activa → mensaje rojo (RN12); al cancelar la reserva, ya se puede eliminar.

   **Estudiante — `/`**
   - [ ] Correo nuevo → pide el nombre y lo registra; correo existente → entra directo.
   - [ ] Elegir tutor → calendario (no deja fines de semana, pasado ni más de 14 días) → horarios libres → duración → confirmar.
   - [ ] Probar una tercera reserva el mismo día → error rojo (RN6).
   - [ ] Otro estudiante intenta el mismo horario del tutor → error rojo (RN1).
   - [ ] «Mis reservas»: cancelar (pide confirmar); cancelar con menos de 2 h → error rojo (RN10).
   - [ ] El estudiante **no** ve ningún formulario para agregar tutores.
   - [ ] Vista móvil (ancho ≈ 390 px) y recarga (la sesión se mantiene).
3. Deja tu revisión en GitHub: *Review changes → Approve* o *Request changes*, con tu lista de resultados. Verifica también que **CI** y **GitGuardian** están en verde en la pestaña *Checks*.

### Paso 2 — Matriz de trazabilidad y cobertura (rama `qa/ciclo2-cobertura`)
- Instala `pytest-cov` y mide: `pytest --cov=src/tutorias --cov-report=term-missing`. Meta: **≥ 90 %** en `service.py` y `api.py`.
- Añade pruebas **solo para lo que falte** (ramas sin cubrir). Ideas: `delete_tutor` con una reserva **ya pasada** (no debe bloquear), `update_tutor` con `subjects` vacío, la migración de una base antigua en `db.connect`, `GET /students/by-email` sin distinguir mayúsculas, una reserva cancelada que libera el hueco para otro estudiante vía HTTP.
- En `docs/testing.md` crea una **tabla de trazabilidad** `CA → nombre de la prueba` para CA1–CA27 (si un CA no tiene prueba, ahí se ve).
- Registra los resultados **reales**: salida de `pytest` y enlace al run de Actions (copia lo que veas, no inventes).

### Paso 3 — DevOps: CI y empaquetado (rama `ci/mejoras`)
- `.github/workflows/ci.yml`: correr en `push` **y** `pull_request`; matriz de Python **3.11 y 3.12** (el stack dice 3.11+); caché de pip; paso con cobertura (`--cov` mostrado en el resumen del run).
- Añade la **insignia (badge) de CI** al README.
- Opcional, suma puntos: `Dockerfile` + instrucciones `docker build / docker run -p 8000:8000` en el README (o un script `run.ps1`), para demostrar el «despliegue».
- Pídele a Fabiana (dueña del repo) activar **protección de `main`** en *Settings → Branches*: exigir PR, 1 aprobación y CI verde.

### Paso 4 — Ensayo del cambio de requerimiento en vivo (CE3), lado QA
Uriel prepara 3 cambios posibles en `docs/ensayo-ce3.md`. Tu rol en el ensayo: **escribir primero las pruebas rojas** a partir de los criterios de aceptación que Uriel redacte, esperar a que Fabiana implemente, y mostrar las pruebas **en verde** y el resultado del CI. Cronometra el ciclo completo (meta < 15 min). La rama de ensayo no se fusiona a `main`.

### Paso 5 — Material de presentación (tu sección)
Cada quien arma su parte y Fabiana las une. **Tu parte: pruebas y calidad.**
1. **Estrategia de pruebas:** pirámide (unitarias de reglas → conflictos → HTTP → criterios de aceptación), con una captura de `pytest`.
2. **La regla crítica:** *no doble reserva* — explica `test_concurrency.py` (10 hilos compitiendo por el mismo horario; solo uno gana).
3. **Evidencia rojo → verde de los cambios de especificación:** CE1 (`b2ba843`, PR #4) y CE2 (`9d70df4` rojas → `cb36367` verdes, PR #8). Muestra la captura del run de Actions fallido/verde si existe.
4. **Calidad:** el bug que encontraste en QA ciclo 1 (un `start` con zona horaria daba 500 y ahora da 422), cobertura final y el recorrido manual del paso 1.

### Paso 6 — Cierre
- Etiqueta de entrega: `git tag v1.0` en `main` cuando #9 y #11 estén fusionados y el CI en verde (confírmalo con Fabiana antes de empujar la etiqueta).
- README, tabla **Equipo**: tu nombre como QA/DevOps del ciclo 2 (sin «por confirmar»).

## 3. Entregables y criterio de «listo»
- [ ] PR #9 y #11 revisados con tu lista de resultados (aprobados o con cambios solicitados).
- [ ] Cobertura medida (meta ≥ 90 %), pruebas añadidas y matriz CA → prueba en `docs/testing.md` con resultados reales.
- [ ] CI con push + PR, matriz 3.11/3.12 y badge en el README (Docker opcional).
- [ ] Ensayo CE3 cronometrado (lado QA).
- [ ] Diapositivas de la sección 5 entregadas a Fabiana.
- [ ] Tu entrada en `docs/ai-log.md`.

## 4. Reglas para tu IA
- Trabaja siempre en una rama; commits pequeños y con prefijo; **no** `git push` a `main`, **no** `--force`, **no** `--no-verify`.
- No inventes resultados: si dices «pasan N pruebas» o «cobertura X %», ejecútalo y copia la salida.
- Una prueba nueva debe fallar primero por la razón correcta antes de que el código la haga pasar.
- No cambies `src/` (es de Fabiana) salvo para corregir un bug que tus pruebas demuestren; en ese caso, commit aparte `fix:` y avísale en el PR.
- Las pruebas de navegador (Playwright) son opcionales y **locales**; no se suben al repo ni al CI.

## 5. Registrar el uso de IA (obligatorio)
Añade **una fila por actividad** al final de la tabla de `docs/ai-log.md`:

| Fecha | Actividad | IA utilizada | Solicitud | Resultado | Decisión |
|---|---|---|---|---|---|
| 2026-11-1X | Cobertura y pruebas faltantes | *(la IA que uses y su versión)* | *(lo que le pediste)* | *(qué produjo)* | *(qué aceptaste, cambiaste o descartaste y por qué)* |

La columna **Decisión** es la más importante: muestra que tú juzgaste el resultado de la IA, no que lo copiaste.

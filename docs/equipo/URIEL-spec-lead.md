# Pasos para Uriel — Product / Spec Lead (ciclo 2)

> **Cómo usar este archivo:** ábrelo en tu IA (Claude, Copilot, ChatGPT, la que uses) y pégale todo el contenido, o dile:
> *«Lee `docs/equipo/URIEL-spec-lead.md` y ayúdame a hacer los pasos en orden. Trabaja en ramas, haz commits pequeños y no hagas push a `main`.»*
> Todo lo que hagas con IA se anota en `docs/ai-log.md` (ver sección 5).

## 1. Contexto del proyecto (léelo primero)

- **Materia:** Tópicos Especiales II, Prof. Regis Rivera. **Proyecto 2:** sistema de reservas de **tutorías universitarias** con el recorrido **ODD → SDD → código → pruebas → valor al usuario**. Se evalúa el *proceso*, no la herramienta.
- **Repo:** https://github.com/fabianagcre/tutorias-reservas (acepta la invitación si aún no lo hiciste).
- **Stack:** Python 3.11+, FastAPI, SQLite, pytest, GitHub Actions. Interfaz web estática (HTML/CSS/JS sin build).
- **Equipo y roles del ciclo 2:** Uriel = **Product/Spec Lead** (tú) · Fabiana = **Architecture/Dev Lead** · Michael (Mike) = **QA/DevOps Lead** (a confirmar en el README).
- **Estado actual (15-nov-2026):**
  - `main`: reglas RN1–RN11, cambios de especificación CE1 (cancelar con ≥2 h) y CE2 (reservar máx. 14 días), QA ciclo 1. **34 pruebas**, CI verde.
  - **PR #9** `chore/ciclo2-arquitectura-dev`: `.gitignore`, `architecture.md`, `ai-log`. Abierto, sin revisión.
  - **PR #11** `feature/interfaz-web`: interfaz web del estudiante (`/`), panel del administrador (`/admin`), editar/eliminar tutores, foto del tutor, diseño con logo y colores de la UTP. Añade RF8–RF13, RN12, CA16–CA27. **55 pruebas**, CI verde. Abierto, sin revisión.
  - Orden de merge acordado: **#9 primero, luego #11** (chocan solo en `docs/ai-log.md` y `docs/decisions.md`: se resuelve conservando ambas versiones; lo hace Fabiana).
- **Reglas de negocio:** RN1 no doble reserva del tutor · RN2 no doble reserva del estudiante · RN3 lun–vie 08:00–18:00 · RN4 duración 30/60/90/120 e inicio :00/:30 · RN5 no reservar en el pasado · RN6 máx. 2 reservas activas/día por estudiante · RN7 cancelar libera el espacio · RN8 solo el dueño cancela · RN9 reservas contiguas permitidas · RN10 cancelar con ≥2 h (CE1) · RN11 reservar máx. 14 días antes (CE2) · RN12 no eliminar un tutor con reservas activas futuras.

### Cómo levantar el proyecto (PowerShell)
```powershell
git clone https://github.com/fabianagcre/tutorias-reservas.git
cd tutorias-reservas
git fetch --all
git checkout feature/interfaz-web        # para ver la interfaz y las specs nuevas
pip install -r requirements.txt
pytest -q                                 # debe dar 55 passed
python scripts/seed_demo.py               # tutores de demostración con foto
uvicorn --app-dir src tutorias.api:create_app --factory --reload
# Estudiante: http://localhost:8000/   ·   Admin: http://localhost:8000/admin   ·   API: http://localhost:8000/docs
```

### Flujo de trabajo obligatorio
issue → rama (`feature/…`, `docs/…`, `spec/…`) **desde `main`** → commits pequeños con prefijo (`spec:`, `test:`, `feat:`, `docs:`, `fix:`, `chore:`) → Pull Request a `main` → **revisión de otra persona** + CI verde → merge. **Nunca push directo a `main`.**

## 2. Tu parte (qué te toca como Spec Lead)

Responsable de **requisitos, outcomes, especificaciones y backlog**. Los pasos, en orden de prioridad:

### Paso 1 — Revisar los PR #9 y #11 desde la mirada de especificación
- Abre https://github.com/fabianagcre/tutorias-reservas/pull/11 → *Files changed* → lee solo `specs/` y `docs/`.
- Comprueba que **cada** RF8–RF13 y RN12 tiene al menos un criterio de aceptación (CA16–CA27) y que cada CA tiene su prueba en `tests/` (busca `test_ca16`…`test_ca27`).
- Deja la revisión en GitHub: *Review changes → Approve* o *Request changes* con comentarios concretos. En el #9 revisa que `architecture.md` coincida con lo que hay en `src/`.

### Paso 2 — Pulir las especificaciones nuevas (rama `spec/ciclo2-pulido`)
- Reescribe **CA16–CA27** en formato **Dado / Cuando / Entonces**, igual que CA1–CA15 (hoy están más cortos).
- `specs/outcomes.md`: añade un outcome para el administrador, por ejemplo *«O6 — El administrador mantiene el catálogo de tutores sin intervención técnica»*, con su indicador (*«alta, edición y baja de un tutor en ≤ 3 clics»*). Sube la trazabilidad en `requirements.md` (RF8–RF13 → O#).
- `specs/implementation-plan.md`: actualiza estados y la línea final de rotación de roles con los **nombres reales** (ciclo 1: Fabiana specs/base + CE1; Uriel QA; ciclo 2: Uriel Spec, Fabiana Dev, Mike QA).
- Entrega: PR a `main` con commits `spec: …`.

### Paso 3 — Backlog e issues
- Crea **un issue por funcionalidad ya hecha** (interfaz estudiante, panel admin, editar/eliminar tutores, foto del tutor, diseño UTP) enlazándolos a su RF/CA y al PR, y ciérralos cuando se fusionen. *(Para la rúbrica: «Issues» + «Commits identificables».)*
- Crea y **asigna** issues de backlog futuro (un responsable cada uno):
  - Autenticación del administrador (`/admin` hoy no pide contraseña — limitación D6).
  - Recordatorios por correo antes de la tutoría.
  - Horario de disponibilidad propio por tutor.
  - Vista de agenda del tutor.
- Usa etiquetas (`spec`, `dev`, `qa`, `docs`, `backlog`).

### Paso 4 — Preparar y ensayar el cambio de requerimiento en vivo (CE3)
El profesor puede pedir **un cambio inesperado durante la presentación**. Ensayamos el ciclo completo: *cambio solicitado → actualizar especificación → actualizar criterios de aceptación → actualizar plan → modificar código → modificar pruebas → ver resultados*.
- Escribe **3 pedidos de cambio realistas** en `docs/ensayo-ce3.md` (con la frase exacta que diría el profesor). Propuestas:
  1. *«Un estudiante no puede acumular más de 3 horas de tutoría por semana.»* (nueva RN13)
  2. *«Los tutores pueden bloquear fechas (feriados) y en ellas no se puede reservar.»* (endpoint + regla)
  3. *«La duración mínima de una tutoría pasa a 60 minutos.»* (modifica RN4)
- Para cada uno indica **qué archivos de `specs/` se tocan**, los CA nuevos en Dado/Cuando/Entonces y el orden del ciclo.
- Ensaya **uno completo** en una rama `feature/ce3-ensayo` junto con Fabiana (código) y Mike (pruebas). Tú escribes primero la spec y los criterios. **Mide el tiempo**: la meta es < 15 minutos.
- Al terminar el ensayo **no fusiones** esa rama a `main` (es solo práctica), o descártala.

### Paso 5 — Material de presentación (tu sección)
Hacen falta diapositivas; cada quien arma su parte y Fabiana las une (o se genera una base con IA). **Tu parte: problema y proceso.**
1. **Problema y outcome (ODD):** pregunta guía, problema, outcomes O1–O6 con sus indicadores (`specs/outcomes.md`).
2. **De outcomes a especificaciones (SDD):** requisitos, reglas, criterios Dado/Cuando/Entonces, trazabilidad (`specs/`).
3. **Evidencia del cambio de especificación (obligatoria en la rúbrica).** Muestra el ciclo con commits reales:
   - **CE1** (cancelar con ≥2 h): `31080d1` spec → `b8292cf` código → `b2ba843` pruebas → PR #4.
   - **CE2** (máx. 14 días): `6cd6367` spec → `9d70df4` pruebas rojas → `cb36367` código → `0f6ccbe` resultados → PR #8.
   - Una diapositiva por cambio, con la frase del cambio, la fila que se tocó en cada archivo y el resultado de las pruebas.

### Paso 6 — README y cierre
- Tabla **Equipo** del README: roles reales por ciclo (sin «por confirmar»).
- Verifica que la estructura de la rúbrica está completa: `specs/` (los 8 archivos), `docs/` (`ai-log`, `decisions`, `testing`), `src/`, `tests/`.

## 3. Entregables y criterio de «listo»
- [ ] PR #9 y #11 revisados (aprobados o con comentarios resueltos).
- [ ] CA16–CA27 en formato Dado/Cuando/Entonces; outcome del administrador; plan con roles reales.
- [ ] Issues creados/asignados y cerrados donde corresponda.
- [ ] `docs/ensayo-ce3.md` con 3 cambios + un ensayo completo cronometrado.
- [ ] Diapositivas de las secciones 1–3 entregadas a Fabiana.
- [ ] Tu entrada en `docs/ai-log.md`.

## 4. Reglas para tu IA
- Trabaja siempre en una rama; commits pequeños y con prefijo; **no** `git push` a `main`, **no** `--force`.
- No inventes resultados: si dices «pasan N pruebas», corre `pytest -q` y copia la salida.
- No cambies código de `src/` ni `tests/` (es de Fabiana y Mike) salvo en el ensayo CE3; propón y comenta en el PR.
- Una afirmación en una especificación debe poder verificarse con una prueba; si no, es una mala especificación.

## 5. Registrar el uso de IA (obligatorio)
Añade **una fila por actividad** al final de la tabla de `docs/ai-log.md`:

| Fecha | Actividad | IA utilizada | Solicitud | Resultado | Decisión |
|---|---|---|---|---|---|
| 2026-11-1X | Revisión de specs del PR #11 | *(la IA que uses y su versión)* | *(lo que le pediste)* | *(qué produjo)* | *(qué aceptaste, cambiaste o descartaste y por qué)* |

La columna **Decisión** es la más importante: muestra que tú juzgaste el resultado de la IA, no que lo copiaste.

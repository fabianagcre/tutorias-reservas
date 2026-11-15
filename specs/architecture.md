# Arquitectura

## Stack (libertad tecnológica, RNF1)
- Lenguaje: **Python 3.11+**
- API: **FastAPI**
- Persistencia: **SQLite** (módulo estándar `sqlite3`)
- Pruebas: **pytest** + `httpx`/TestClient
- CI: GitHub Actions

## Capas
```
api.py        -> HTTP, validación de entrada, traducción de errores
service.py    -> reglas de negocio (RN1..RN9), única capa con lógica
db.py         -> esquema y conexión SQLite
web/index.html-> pantalla del estudiante (HTML/JS sin build), servida en `/`
web/admin.html-> panel del administrador (alta, edición y baja de tutores), servido en `/admin`
web/css, web/img -> estilos compartidos y fotos (Unsplash + escudo UTP), servidos en `/css` y `/img`
```
- El reloj (`now`) se inyecta en el servicio para poder probar RN5 y cancelaciones.
- Las reglas viven solo en `service.py`; la API no duplica validaciones de negocio.

## Decisiones clave
- SQLite: cero infraestructura para el curso, suficiente para el alcance.
- Detección de solapamiento en una sola transacción (`BEGIN IMMEDIATE`) para evitar condiciones de carrera.

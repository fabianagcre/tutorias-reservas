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
```
- El reloj (`now`) se inyecta en el servicio para poder probar RN5 y cancelaciones.
- Las reglas viven solo en `service.py`; la API no duplica validaciones de negocio.

## Decisiones clave
- SQLite: cero infraestructura para el curso, suficiente para el alcance.
- Detección de solapamiento en una sola transacción (`BEGIN IMMEDIATE`) para evitar condiciones de carrera.

# Distrito Chilaquil

Proyecto ejecutable local en Python 3.12.6 con arquitectura hexagonal, separacion estricta entre core transaccional y ETL analitico.

## 1. Objetivo del proyecto

- Core transaccional de ordenes (DDD puro)
- API HTTP con FastAPI
- Persistencia PostgreSQL async (SQLAlchemy 2.x + asyncpg)
- Publicacion de eventos con Kafka (aiokafka)
- ETL separado del core para capas analiticas
- UI demo local (HTML/CSS/JS)
- CI/CD base, Docker y evidencia de seguridad

## 2. Reglas de arquitectura

- `src/domain`: negocio puro, sin FastAPI/Pydantic/SQLAlchemy.
- `src/application`: puertos + casos de uso.
- `src/infrastructure`: adaptadores (API, DB, eventos, settings).
- `src/etl`: extraccion/transformacion/carga separada del dominio.

## 3. Diagramas (Mermaid)

### 3.1 Arquitectura hexagonal

```mermaid
flowchart LR
    UI[Interfaz demo] --> API[Adaptador FastAPI]
    API --> APP[Capa aplicacion\nCasos de uso + puertos]
    APP --> DOM[Capa dominio\nEntidades + reglas]
    APP --> OUT[Puertos de salida]

    OUT --> DB[(PostgreSQL asincrono)]
    OUT --> KAFKA[(Publicador Kafka)]

    DB --> ETL[Capa ETL\nextraer/transformar/cargar]
    ETL --> DW[(Modelo analitico)]
```

### 3.2 Secuencia Crear Orden

```mermaid
sequenceDiagram
    participant Cliente as Cliente/API
    participant Router as Router FastAPI
    participant CasoUso as CasoDeUsoCrearOrden
    participant Repo as PuertoRepositorioOrdenes
    participant Evento as PuertoPublicadorEventos

    Cliente->>Router: POST /orders
    Router->>CasoUso: ejecutar(comando)
    CasoUso->>Repo: guardar(orden)
    Repo-->>CasoUso: orden persistida
    CasoUso->>Evento: publicar(orden_creada.v1)
    CasoUso-->>Router: OrdenDTO
    Router-->>Cliente: 201 Creada
```

### 3.3 Despliegue local con Docker Compose

```mermaid
flowchart LR
    Usuario[Usuario] --> UI[UI estatica :5500]
    UI --> API[API FastAPI :8000]
    API --> PG[(PostgreSQL :5432)]
    API --> KF[(Kafka :9092)]
    MIG[Servicio de migraciones] --> PG
```

### 3.4 DER ETL (staging + analitico)

```mermaid
erDiagram
    STG_CLIENTES ||--o{ STG_ORDENES : origen_cliente
    STG_PRODUCTOS ||--o{ STG_ITEMS_ORDEN : origen_producto
    STG_ORDENES ||--|{ STG_ITEMS_ORDEN : origen_detalle
    STG_ORDENES ||--|| STG_FACTURAS : origen_factura

    STG_CLIENTES ||--o{ DIM_CLIENTE : carga_scd
    STG_PRODUCTOS ||--o{ DIM_PRODUCTO : carga_scd
    STG_ORDENES ||--o{ DIM_SUCURSAL : catalogo_sucursal

    DIM_CLIENTE ||--o{ FACT_ORDENES : dimensiona
    DIM_SUCURSAL ||--o{ FACT_ORDENES : dimensiona
    DIM_TIEMPO ||--o{ FACT_ORDENES : dimensiona

    DIM_CLIENTE ||--o{ FACT_ITEMS_ORDEN : dimensiona
    DIM_PRODUCTO ||--o{ FACT_ITEMS_ORDEN : dimensiona
    DIM_SUCURSAL ||--o{ FACT_ITEMS_ORDEN : dimensiona
    DIM_TIEMPO ||--o{ FACT_ITEMS_ORDEN : dimensiona

    DIM_CLIENTE ||--o{ FACT_FACTURAS : dimensiona
    DIM_TIEMPO ||--o{ FACT_FACTURAS : dimensiona
```

Diagrama completo:

- `docs/der_etl.mmd`

## 4. Requisitos

- Python 3.12.6
- Poetry 2.x
- Docker Desktop (para compose)

## 5. Variables de entorno

Copiar `.env.example` a `.env` y ajustar si aplica.

Variables clave:

- `DATABASE_URL`
- `INTEGRATION_DATABASE_URL`
- `KAFKA_BOOTSTRAP_SERVERS`
- `KAFKA_ENABLED`
- `RUN_KAFKA_SMOKE`
- `LOG_LEVEL`
- `REQUEST_ID_HEADER`

## 6. Ejecucion local sin Docker

```powershell
cd C:\Users\Jorge\Desktop\Proyecto_Python
poetry env use 3.12
poetry install
poetry run alembic upgrade head
poetry run uvicorn src.infrastructure.api.main:app --reload --host 127.0.0.1 --port 8000
```

## 7. UI demo local (Windows)

Manual tecnico en:

- `docs/ui_windows.md`

Manual no tecnico paso a paso:

- `docs/manual_operacion_ui.txt`

Resumen sencillo de procesos del proyecto:

- `docs/resumen_procesos_sencillo.md`

## 8. Ejecucion con Docker Compose

### 8.1 Levantar stack completo

```powershell
docker compose up --build -d
```

Servicios:

- API: `http://127.0.0.1:8000`
- Health liveness: `http://127.0.0.1:8000/health`
- Health readiness: `http://127.0.0.1:8000/health/ready`

Nota de datos semilla:

- Al levantar `app`, se ejecuta el servicio `seed` y carga `data/seed/*.csv` a PostgreSQL.
- Si quieres forzar una recarga manual de semillas:

```powershell
docker compose run --rm seed
```

### 8.2 Logs

```powershell
docker compose logs -f app
```

### 8.3 Apagar stack

```powershell
docker compose down -v
```

## 9. Testing y calidad

```powershell
py -3.12 --version
poetry --version
poetry env use 3.12
poetry install
poetry run ruff check .
poetry run mypy src
poetry run pytest -q
poetry run bandit -q -r src
poetry run safety check
poetry run pip-audit
```

### 9.1 Pruebas de integracion con DB real

```powershell
$env:INTEGRATION_DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/distrito_chilaquil"
poetry run pytest -q tests/integration/test_db_repositories.py
poetry run pytest -q tests/integration/test_api_with_db.py
```

### 9.2 Smoke Kafka (opcional)

```powershell
$env:RUN_KAFKA_SMOKE="true"
$env:KAFKA_BOOTSTRAP_SERVERS="localhost:9092"
poetry run pytest -q tests/integration/test_events_kafka_publisher.py
```

## 10. Observabilidad minima

- Middleware de request logging con:
  - metodo
  - path
  - status
  - duracion en ms
  - request id
- Header de trazabilidad en respuesta: `X-Request-ID` (configurable).
- Endpoints de salud:
  - `/health` (liveness)
  - `/health/ready` (DB + Kafka)

## 11. CI/CD

Workflow:

- `.github/workflows/ci.yml`

Pipeline ejecuta:

- `ruff`
- `mypy`
- `pytest` (unit + integration + contract)
- `bandit`
- `pip-audit`
- `safety` (best effort)

La CI levanta `postgres` y `kafka` con `docker compose` para pruebas de integracion y smoke Kafka.

## 12. Evidencia de seguridad (espanol)

Ver documento:

- `docs/security_evidence.md`

Incluye:

- fecha de ejecucion
- comandos usados
- resultado de `bandit`, `safety`, `pip-audit`
- remediacion aplicada para CVE de Starlette

## 13. Comandos de verificacion de dependencias externas

### PostgreSQL

```powershell
docker compose up -d postgres
poetry run python -c "import asyncio,asyncpg;async def m():\n c=await asyncpg.connect('postgresql://postgres:postgres@localhost:5432/distrito_chilaquil');\n print(await c.fetchval('SELECT 1'));\n await c.close();\nasyncio.run(m())"
```

### Kafka

```powershell
docker compose up -d kafka
poetry run python -c "import socket; s=socket.create_connection(('localhost',9092),2); print('kafka_ok'); s.close()"
```

## 14. Estructura de alto nivel

```text
src/
  domain/
  application/
  infrastructure/
  etl/
ui/
tests/
  unit/
  integration/
```

## 15. Limites conocidos

- La UI no incluye edicion de clientes/productos (solo alta + listado).
- El servicio `seed` inserta por `ON CONFLICT DO NOTHING`; no sobreescribe registros existentes.

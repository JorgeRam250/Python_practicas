# Resumen sencillo de procesos del proyecto

Este documento explica en palabras simples que procesos existen en Distrito Chilaquil y para que sirve cada uno.

## 1) Proceso de negocio principal (ordenes)

1. Se registra un cliente.
2. Se crea un producto.
3. Se crea una orden con sus items.
4. La orden cambia de estado (`PENDING`, `IN_PROGRESS`, `SHIPPED`, `COMPLETED`, `CANCELLED`).
5. La factura externa se guarda como registro aparte.

Idea clave: las reglas de negocio viven en `src/domain`, no en la API ni en la UI.

## 2) Proceso de aplicacion (casos de uso)

La capa `src/application` coordina acciones sin depender de tecnologia concreta:

- `RegisterCustomer`
- `CreateProduct`
- `CreateOrder`
- `Get/List Orders`
- `UpdateOrderStatus`

Usa puertos para hablar con repositorios, eventos y unidad de trabajo.

## 3) Proceso API (FastAPI)

La API expone endpoints para clientes, productos, ordenes y salud:

- `/customers`
- `/products`
- `/orders`
- `/health`
- `/health/ready`

La API valida entrada/salida y mapea errores HTTP, pero no implementa reglas de negocio.

## 4) Proceso de persistencia (PostgreSQL + Alembic)

1. Modelos ORM en `src/infrastructure/db/models.py`.
2. Repositorios concretos implementan puertos.
3. Alembic aplica migraciones.
4. UnitOfWork confirma o revierte transacciones.

En Docker, el servicio `migrate` corre `alembic upgrade head` antes de levantar `app`.

## 5) Proceso de eventos (Kafka)

Cuando hay cambios importantes (por ejemplo orden creada o cambio de estado), se puede publicar evento en Kafka por medio de `AIOKafkaEventPublisher`.

Si `KAFKA_ENABLED=false`, el publicador queda en no-op controlado.

## 6) Proceso ETL (separado del core)

Pipeline en `src/etl`:

1. `extract.py`: lee CSV seed.
2. `transform.py`: tipa datos y normaliza campos.
3. `transform.py`: valida FKs, cantidades y totales.
4. `load.py`: escribe CSV de staging.
5. `pipeline.py`: orquesta extract -> transform -> validate -> load.

Separacion importante: ETL no contamina `src/domain`.

## 7) Proceso UI demo

La UI (HTML/CSS/JS) en `ui/` consume la API:

- lista y detalle de ordenes
- alta de productos
- alta de ordenes
- vista de clientes/productos segun contrato API disponible

No contiene logica de negocio.

## 8) Proceso de observabilidad

Se registra:

- metodo HTTP
- ruta
- status
- tiempo de respuesta
- `X-Request-ID`

Salud operativa:

- `/health`: liveness rapido
- `/health/ready`: verifica DB y Kafka

## 9) Proceso Docker

`docker-compose.yml` define:

- `postgres`
- `kafka`
- `migrate`
- `app`

Flujo esperado:

1. Arrancan `postgres` y `kafka`.
2. Corre `migrate`.
3. Arranca `app`.

## 10) Proceso de calidad y seguridad

Checklist de herramientas:

- `ruff`
- `mypy`
- `pytest`
- `bandit`
- `safety`
- `pip-audit`

El workflow de CI ejecuta estas validaciones automaticamente.

## 11) Proceso de operacion para usuarios

- Manual tecnico: `docs/ui_windows.md`
- Manual no tecnico: `docs/manual_operacion_ui.txt`

## 12) Resultado final

El proyecto quedo con:

- arquitectura por capas (hexagonal)
- dominio desacoplado
- ETL separado
- API ejecutable
- persistencia real
- eventos
- UI demo
- Docker + CI + pruebas + evidencia de seguridad

# UI demo en Windows (Fase 7)

## 1) Levantar API local

```powershell
cd C:\Users\Jorge\Desktop\Proyecto_Python
poetry run uvicorn src.infrastructure.api.main:app --reload --host 127.0.0.1 --port 8000
```

## 2) Levantar UI estatica

En una segunda terminal:

```powershell
cd C:\Users\Jorge\Desktop\Proyecto_Python\ui
py -3.12 -m http.server 5500
```

Abrir en navegador:

- `http://127.0.0.1:5500`

## 3) Configurar Base URL en UI

En el panel superior de la UI:

- `Base URL API` = `http://127.0.0.1:8000`

La UI guarda esta URL en `localStorage`.

## 4) Vistas disponibles

- Orders: listado, detalle, cambio de status.
- Customers: listado (si API expone `GET /customers`).
- Products: listado (si API expone `GET /products`) y alta via `POST /products`.
- Create Order: alta via `POST /orders`.

## 5) Nota de compatibilidad del contrato actual

La API actual implementa:

- `POST /customers`
- `POST /products`
- `GET/POST/PATCH /orders...`

Si `GET /customers` o `GET /products` no existen, la UI muestra `N/A` sin romper la navegacion.
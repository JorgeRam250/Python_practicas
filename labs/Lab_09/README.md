# Laboratorio de FastAPI: CRUD de Orders con Autenticación JWT

## Descripción del Proyecto

Este proyecto implementa una API REST completa utilizando FastAPI para gestionar órdenes (orders) con autenticación JWT, validación de datos y pruebas automatizadas.

## Estructura del Proyecto

```
Windsurf/
├── main.py              # Aplicación principal de FastAPI
├── test_orders.py       # Pruebas automatizadas con pytest
├── requirements.txt     # Dependencias del proyecto
├── README.md           # Documentación del proyecto
├── orders.db           # Base de datos SQLite (se crea automáticamente)
└── examples/           # Ejemplos de uso
    ├── ejemplo_basico.py
    ├── ejemplo_avanzado.py
    └── ejemplo_testing.py
```

## Instalación

1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

2. Iniciar el servidor:
```bash
python main.py
```
=============================================================================
## Inicia el servidor directamente:

python main.py

## En otra terminal ejecuta el ejemplo:

python setup.py

=============================================================================

La API estará disponible en `http://localhost:8000`

## Documentación de la API

Una vez iniciado el servidor, puedes acceder a:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Endpoints Disponibles

### Autenticación
- `POST /login` - Iniciar sesión y obtener token JWT
- `GET /users/me` - Obtener información del usuario actual

### CRUD de Orders
- `POST /orders/` - Crear una nueva orden
- `GET /orders/` - Obtener todas las órdenes
- `GET /orders/{order_id}` - Obtener una orden por ID
- `PUT /orders/{order_id}` - Actualizar una orden
- `DELETE /orders/{order_id}` - Eliminar una orden

## Usuario por Defecto

- **Username**: `admin`
- **Password**: `admin123`

## Ejecutar Pruebas

```bash
pytest test_orders.py -v
```

## Conceptos Clave Explicados

### 1. Estructura de Proyecto
- **main.py**: Contiene toda la lógica de la API
- **test_orders.py**: Pruebas automatizadas para verificar el funcionamiento
- **requirements.txt**: Lista de dependencias necesarias

### 2. Modelos Pydantic
Los modelos Pydantic definen la estructura y validación de datos:
- `User`: Para autenticación
- `Order`: Para las órdenes
- `Token`: Para respuestas de autenticación

### 3. Autenticación JWT
- JSON Web Tokens para seguridad
- Los tokens expiran en 30 minutos
- Se requiere token para acceder a los endpoints de orders

### 4. Base de Datos SQLite
- Base de datos ligera y temporal
- Se crea automáticamente al iniciar la aplicación
- Tablas: `users` y `orders`

### 5. Middleware CORS
- Permite solicitudes desde diferentes dominios
- Configurado para aceptar todos los orígenes (solo para desarrollo)

## Ejemplos de Uso

Ver la carpeta `examples/` para ejemplos prácticos de cómo usar la API.

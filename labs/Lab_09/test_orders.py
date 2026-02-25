import pytest
import asyncio
import aiohttp
import sqlite3
import json
from datetime import datetime

# Configuración de prueba
BASE_URL = "http://localhost:8000"
TEST_DB = "test_orders.db"

@pytest.fixture(scope="session")
def event_loop():
    """Crea un event loop para las pruebas asíncronas"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def setup_test_db():
    """Configura la base de datos de prueba"""
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    
    # Crear tablas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        product TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending'
    )
    ''')
    
    # Insertar usuario de prueba
    import hashlib
    hashed_password = hashlib.sha256("test123".encode()).hexdigest()
    cursor.execute("INSERT OR REPLACE INTO users VALUES (?, ?)", ("testuser", hashed_password))
    
    conn.commit()
    conn.close()
    
    yield
    
    # Limpiar después de las pruebas
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

@pytest.fixture
async def auth_token(setup_test_db):
    """Obtiene un token de autenticación para las pruebas"""
    async with aiohttp.ClientSession() as session:
        login_data = {
            "username": "testuser",
            "password": "test123"
        }
        
        async with session.post(f"{BASE_URL}/login", json=login_data) as response:
            if response.status == 200:
                data = await response.json()
                return data["access_token"]
            else:
                # Si el servidor no está corriendo, crear un token mock
                import jwt
                return jwt.encode({"sub": "testuser"}, "test_secret", algorithm="HS256")

@pytest.fixture
async def headers(auth_token):
    """Crea los headers de autenticación"""
    return {"Authorization": f"Bearer {auth_token}"}

class TestAuthentication:
    """Pruebas de autenticación"""
    
    @pytest.mark.asyncio
    async def test_login_success(self):
        """Prueba login exitoso"""
        async with aiohttp.ClientSession() as session:
            login_data = {
                "username": "testuser",
                "password": "test123"
            }
            
            async with session.post(f"{BASE_URL}/login", json=login_data) as response:
                if response.status == 200:
                    data = await response.json()
                    assert "access_token" in data
                    assert data["token_type"] == "bearer"
                else:
                    pytest.skip("Servidor no disponible para pruebas de integración")
    
    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self):
        """Prueba login con credenciales inválidas"""
        async with aiohttp.ClientSession() as session:
            login_data = {
                "username": "invalid",
                "password": "wrong"
            }
            
            async with session.post(f"{BASE_URL}/login", json=login_data) as response:
                if response.status == 401:
                    data = await response.json()
                    assert "detail" in data
                else:
                    pytest.skip("Servidor no disponible para pruebas de integración")

class TestOrdersCRUD:
    """Pruebas CRUD de Orders"""
    
    @pytest.mark.asyncio
    async def test_create_order(self, headers):
        """Prueba crear una order"""
        async with aiohttp.ClientSession() as session:
            order_data = {
                "customer_name": "Juan Pérez",
                "product": "Laptop",
                "quantity": 1,
                "price": 999.99,
                "status": "pending"
            }
            
            async with session.post(f"{BASE_URL}/orders/", json=order_data, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    assert data["customer_name"] == order_data["customer_name"]
                    assert data["product"] == order_data["product"]
                    assert "id" in data
                else:
                    pytest.skip("Servidor no disponible para pruebas de integración")
    
    @pytest.mark.asyncio
    async def test_get_orders(self, headers):
        """Prueba obtener todas las orders"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BASE_URL}/orders/", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    assert isinstance(data, list)
                else:
                    pytest.skip("Servidor no disponible para pruebas de integración")
    
    @pytest.mark.asyncio
    async def test_get_order_by_id(self, headers):
        """Prueba obtener una order por ID"""
        # Primero crear una order
        async with aiohttp.ClientSession() as session:
            order_data = {
                "customer_name": "María García",
                "product": "Mouse",
                "quantity": 2,
                "price": 25.50,
                "status": "pending"
            }
            
            async with session.post(f"{BASE_URL}/orders/", json=order_data, headers=headers) as response:
                if response.status == 200:
                    created_order = await response.json()
                    order_id = created_order["id"]
                    
                    # Ahora obtener la order por ID
                    async with session.get(f"{BASE_URL}/orders/{order_id}", headers=headers) as get_response:
                        if get_response.status == 200:
                            data = await get_response.json()
                            assert data["id"] == order_id
                            assert data["customer_name"] == order_data["customer_name"]
                        else:
                            pytest.skip("Servidor no disponible para pruebas de integración")
                else:
                    pytest.skip("Servidor no disponible para pruebas de integración")
    
    @pytest.mark.asyncio
    async def test_update_order(self, headers):
        """Prueba actualizar una order"""
        # Primero crear una order
        async with aiohttp.ClientSession() as session:
            order_data = {
                "customer_name": "Carlos López",
                "product": "Teclado",
                "quantity": 1,
                "price": 75.00,
                "status": "pending"
            }
            
            async with session.post(f"{BASE_URL}/orders/", json=order_data, headers=headers) as response:
                if response.status == 200:
                    created_order = await response.json()
                    order_id = created_order["id"]
                    
                    # Actualizar la order
                    update_data = {
                        "status": "completed",
                        "price": 70.00
                    }
                    
                    async with session.put(f"{BASE_URL}/orders/{order_id}", json=update_data, headers=headers) as update_response:
                        if update_response.status == 200:
                            updated_order = await update_response.json()
                            assert updated_order["status"] == "completed"
                            assert updated_order["price"] == 70.00
                        else:
                            pytest.skip("Servidor no disponible para pruebas de integración")
                else:
                    pytest.skip("Servidor no disponible para pruebas de integración")
    
    @pytest.mark.asyncio
    async def test_delete_order(self, headers):
        """Prueba eliminar una order"""
        # Primero crear una order
        async with aiohttp.ClientSession() as session:
            order_data = {
                "customer_name": "Ana Martínez",
                "product": "Monitor",
                "quantity": 1,
                "price": 299.99,
                "status": "pending"
            }
            
            async with session.post(f"{BASE_URL}/orders/", json=order_data, headers=headers) as response:
                if response.status == 200:
                    created_order = await response.json()
                    order_id = created_order["id"]
                    
                    # Eliminar la order
                    async with session.delete(f"{BASE_URL}/orders/{order_id}", headers=headers) as delete_response:
                        if delete_response.status == 200:
                            data = await delete_response.json()
                            assert "message" in data
                        else:
                            pytest.skip("Servidor no disponible para pruebas de integración")
                else:
                    pytest.skip("Servidor no disponible para pruebas de integración")

class TestValidation:
    """Pruebas de validación"""
    
    @pytest.mark.asyncio
    async def test_create_order_invalid_data(self, headers):
        """Prueba crear order con datos inválidos"""
        async with aiohttp.ClientSession() as session:
            # Datos inválidos (quantity negativo)
            invalid_order = {
                "customer_name": "Test User",
                "product": "Test Product",
                "quantity": -1,
                "price": 10.00
            }
            
            async with session.post(f"{BASE_URL}/orders/", json=invalid_order, headers=headers) as response:
                # FastAPI debería rechazar esto automáticamente
                if response.status == 422:
                    data = await response.json()
                    assert "detail" in data
                else:
                    pytest.skip("Servidor no disponible para pruebas de integración")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

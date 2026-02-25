"""
Ejemplo 3: Testing Automatizado de la API
Este ejemplo muestra cómo realizar pruebas automatizadas
"""

import pytest
import requests
import json
import time
import sqlite3
import hashlib
import os

# Configuración de pruebas
BASE_URL = "http://localhost:8000"
TEST_DB = "test_orders.db"

class TestOrdersAPI:
    """Clase de testing para la API de Orders"""
    
    @classmethod
    def setup_class(cls):
        """Configuración inicial para todas las pruebas"""
        print("\n=== INICIANDO PRUEBAS AUTOMATIZADAS ===")
        
        # Verificar que el servidor esté corriendo
        try:
            response = requests.get(f"{BASE_URL}/docs", timeout=5)
            if response.status_code != 200:
                pytest.skip("El servidor no está corriendo o no es accesible")
        except requests.exceptions.RequestException:
            pytest.skip("No se puede conectar al servidor. Inicia el servidor con: python main.py")
        
        # Configurar base de datos de prueba
        cls.setup_test_database()
        
        # Obtener token de autenticación
        cls.token = cls.get_auth_token()
        cls.headers = {"Authorization": f"Bearer {cls.token}"}
    
    @classmethod
    def setup_test_database(cls):
        """Configurar base de datos para pruebas"""
        # Crear base de datos de prueba
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
        hashed_password = hashlib.sha256("test123".encode()).hexdigest()
        cursor.execute("INSERT OR REPLACE INTO users VALUES (?, ?)", ("testuser", hashed_password))
        
        conn.commit()
        conn.close()
    
    @classmethod
    def get_auth_token(cls):
        """Obtener token de autenticación para pruebas"""
        login_data = {
            "username": "admin",  # Usar el usuario por defecto
            "password": "admin123"
        }
        
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            pytest.skip("No se pudo obtener token de autenticación")
    
    def test_01_authentication(self):
        """Prueba 1: Autenticación"""
        print("\n1. Probando autenticación...")
        
        # Login exitoso
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        print("   ✅ Login exitoso")
        
        # Login fallido
        invalid_login = {
            "username": "invalid",
            "password": "wrong"
        }
        
        response = requests.post(f"{BASE_URL}/login", json=invalid_login)
        assert response.status_code == 401
        print("   ✅ Login inválido rechazado correctamente")
    
    def test_02_create_order(self):
        """Prueba 2: Crear orden"""
        print("\n2. Probando creación de órdenes...")
        
        order_data = {
            "customer_name": "Cliente de Prueba",
            "product": "Producto de Prueba",
            "quantity": 2,
            "price": 99.99,
            "status": "pending"
        }
        
        response = requests.post(f"{BASE_URL}/orders/", json=order_data, headers=self.headers)
        assert response.status_code == 200
        
        created_order = response.json()
        assert created_order["customer_name"] == order_data["customer_name"]
        assert created_order["product"] == order_data["product"]
        assert created_order["quantity"] == order_data["quantity"]
        assert created_order["price"] == order_data["price"]
        assert created_order["status"] == order_data["status"]
        assert "id" in created_order
        
        # Guardar ID para pruebas posteriores
        self.test_order_id = created_order["id"]
        print(f"   ✅ Orden creada con ID: {self.test_order_id}")
    
    def test_03_get_orders(self):
        """Prueba 3: Obtener todas las órdenes"""
        print("\n3. Probando obtención de todas las órdenes...")
        
        response = requests.get(f"{BASE_URL}/orders/", headers=self.headers)
        assert response.status_code == 200
        
        orders = response.json()
        assert isinstance(orders, list)
        assert len(orders) >= 1  # Al menos la orden creada en la prueba anterior
        
        print(f"   ✅ Se encontraron {len(orders)} órdenes")
    
    def test_04_get_order_by_id(self):
        """Prueba 4: Obtener orden por ID"""
        print("\n4. Probando obtención de orden por ID...")
        
        # Usar el ID de la orden creada en la prueba 2
        if not hasattr(self, 'test_order_id'):
            pytest.skip("No hay ID de orden para probar")
        
        response = requests.get(f"{BASE_URL}/orders/{self.test_order_id}", headers=self.headers)
        assert response.status_code == 200
        
        order = response.json()
        assert order["id"] == self.test_order_id
        assert "customer_name" in order
        assert "product" in order
        
        print(f"   ✅ Orden {self.test_order_id} encontrada correctamente")
        
        # Probar con ID inexistente
        response = requests.get(f"{BASE_URL}/orders/99999", headers=self.headers)
        assert response.status_code == 404
        print("   ✅ ID inexistente manejado correctamente")
    
    def test_05_update_order(self):
        """Prueba 5: Actualizar orden"""
        print("\n5. Probando actualización de órdenes...")
        
        if not hasattr(self, 'test_order_id'):
            pytest.skip("No hay ID de orden para probar")
        
        update_data = {
            "status": "completed",
            "price": 89.99
        }
        
        response = requests.put(f"{BASE_URL}/orders/{self.test_order_id}", 
                              json=update_data, headers=self.headers)
        assert response.status_code == 200
        
        updated_order = response.json()
        assert updated_order["id"] == self.test_order_id
        assert updated_order["status"] == "completed"
        assert updated_order["price"] == 89.99
        
        print(f"   ✅ Orden {self.test_order_id} actualizada correctamente")
    
    def test_06_delete_order(self):
        """Prueba 6: Eliminar orden"""
        print("\n6. Probando eliminación de órdenes...")
        
        if not hasattr(self, 'test_order_id'):
            pytest.skip("No hay ID de orden para probar")
        
        response = requests.delete(f"{BASE_URL}/orders/{self.test_order_id}", headers=self.headers)
        assert response.status_code == 200
        
        result = response.json()
        assert "message" in result
        
        # Verificar que la orden fue eliminada
        response = requests.get(f"{BASE_URL}/orders/{self.test_order_id}", headers=self.headers)
        assert response.status_code == 404
        
        print(f"   ✅ Orden {self.test_order_id} eliminada correctamente")
    
    def test_07_validation_errors(self):
        """Prueba 7: Validación de errores"""
        print("\n7. Probando validación de datos...")
        
        # Datos inválidos
        invalid_orders = [
            {
                "customer_name": "Test",
                "product": "Test",
                "quantity": -1,  # Inválido
                "price": 10.00
            },
            {
                "customer_name": "",  # Inválido
                "product": "Test",
                "quantity": 1,
                "price": 10.00
            },
            {
                "customer_name": "Test",
                "product": "Test",
                "quantity": 1,
                "price": -10.00  # Inválido
            }
        ]
        
        for i, invalid_order in enumerate(invalid_orders, 1):
            response = requests.post(f"{BASE_URL}/orders/", json=invalid_order, headers=self.headers)
            assert response.status_code == 422  # Unprocessable Entity
            print(f"   ✅ Orden inválida {i} rechazada correctamente")
    
    def test_08_unauthorized_access(self):
        """Prueba 8: Acceso no autorizado"""
        print("\n8. Probando acceso no autorizado...")
        
        # Intentar acceder sin token
        response = requests.get(f"{BASE_URL}/orders/")
        assert response.status_code == 403  # Forbidden
        
        # Intentar acceder con token inválido
        invalid_headers = {"Authorization": "Bearer invalid_token"}
        response = requests.get(f"{BASE_URL}/orders/", headers=invalid_headers)
        assert response.status_code == 401  # Unauthorized
        
        print("   ✅ Acceso no autorizado manejado correctamente")
    
    @classmethod
    def teardown_class(cls):
        """Limpieza después de todas las pruebas"""
        print("\n=== LIMPIEZA DE PRUEBAS ===")
        
        # Eliminar base de datos de prueba
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
            print("✅ Base de datos de prueba eliminada")
        
        print("=== PRUEBAS COMPLETADAS ===\n")

def run_manual_tests():
    """Ejecutar pruebas manuales sin pytest"""
    print("=== EJECUTANDO PRUEBAS MANUALES ===")
    
    # Crear instancia de pruebas
    test_instance = TestOrdersAPI()
    
    try:
        # Configurar
        test_instance.setup_class()
        
        # Ejecutar pruebas una por una
        test_methods = [
            test_instance.test_01_authentication,
            test_instance.test_02_create_order,
            test_instance.test_03_get_orders,
            test_instance.test_04_get_order_by_id,
            test_instance.test_05_update_order,
            test_instance.test_06_delete_order,
            test_instance.test_07_validation_errors,
            test_instance.test_08_unauthorized_access
        ]
        
        passed = 0
        failed = 0
        
        for test_method in test_methods:
            try:
                test_method()
                passed += 1
                print(f"✅ {test_method.__name__} - PASÓ")
            except Exception as e:
                failed += 1
                print(f"❌ {test_method.__name__} - FALLÓ: {e}")
        
        # Limpiar
        test_instance.teardown_class()
        
        print(f"\n=== RESUMEN DE PRUEBAS ===")
        print(f"✅ Pasadas: {passed}")
        print(f"❌ Fallidas: {failed}")
        print(f"Total: {passed + failed}")
        
    except Exception as e:
        print(f"❌ Error en la configuración de pruebas: {e}")

if __name__ == "__main__":
    # Opción 1: Ejecutar con pytest (recomendado)
    # pytest.run([__file__, "-v"])
    
    # Opción 2: Ejecutar pruebas manuales
    run_manual_tests()

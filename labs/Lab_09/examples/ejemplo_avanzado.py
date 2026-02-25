"""
Ejemplo 2: Uso Avanzado de la API de Orders
Este ejemplo muestra operaciones más complejas y manejo de errores
"""

import requests
import json
import time
from datetime import datetime

class OrdersAPI:
    """Clase para interactuar con la API de Orders"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.token = None
        self.headers = {}
    
    def login(self, username="admin", password="admin123"):
        """Iniciar sesión y obtener token"""
        try:
            response = requests.post(f"{self.base_url}/login", json={
                "username": username,
                "password": password
            })
            
            if response.status_code == 200:
                self.token = response.json()["access_token"]
                self.headers = {"Authorization": f"Bearer {self.token}"}
                return True
            else:
                print(f"Error en login: {response.status_code} - {response.text}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ No se puede conectar al servidor")
            return False
    
    def create_order(self, order_data):
        """Crear una nueva orden con manejo de errores"""
        try:
            response = requests.post(f"{self.base_url}/orders/", 
                                   json=order_data, 
                                   headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 422:
                print("❌ Error de validación:", response.json())
                return None
            elif response.status_code == 401:
                print("❌ No autorizado. Token inválido o expirado")
                return None
            else:
                print(f"❌ Error al crear orden: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return None
    
    def get_orders(self):
        """Obtener todas las órdenes"""
        try:
            response = requests.get(f"{self.base_url}/orders/", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Error al obtener órdenes: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return None
    
    def get_order(self, order_id):
        """Obtener una orden por ID"""
        try:
            response = requests.get(f"{self.base_url}/orders/{order_id}", 
                                  headers=self.headers)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                print(f"❌ Orden con ID {order_id} no encontrada")
                return None
            else:
                print(f"❌ Error al obtener orden: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return None
    
    def update_order(self, order_id, update_data):
        """Actualizar una orden"""
        try:
            response = requests.put(f"{self.base_url}/orders/{order_id}", 
                                  json=update_data, 
                                  headers=self.headers)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                print(f"❌ Orden con ID {order_id} no encontrada")
                return None
            else:
                print(f"❌ Error al actualizar orden: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return None
    
    def delete_order(self, order_id):
        """Eliminar una orden"""
        try:
            response = requests.delete(f"{self.base_url}/orders/{order_id}", 
                                     headers=self.headers)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                print(f"❌ Orden con ID {order_id} no encontrada")
                return None
            else:
                print(f"❌ Error al eliminar orden: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return None

def ejemplo_avanzado():
    """Ejemplo avanzado usando la clase OrdersAPI"""
    
    print("=== EJEMPLO AVANZADO DE API FASTAPI ===\n")
    
    # Crear instancia de la API
    api = OrdersAPI()
    
    # 1. Login
    print("1. Conectando a la API...")
    if not api.login():
        return
    print("✅ Conexión exitosa\n")
    
    # 2. Crear múltiples órdenes
    print("2. Creando múltiples órdenes...")
    orders_data = [
        {
            "customer_name": "María González",
            "product": "Smartphone iPhone 15",
            "quantity": 2,
            "price": 999.99,
            "status": "pending"
        },
        {
            "customer_name": "Carlos Rodríguez",
            "product": "Tablet Samsung Galaxy",
            "quantity": 1,
            "price": 449.99,
            "status": "pending"
        },
        {
            "customer_name": "Ana López",
            "product": "Auriculares Bluetooth",
            "quantity": 3,
            "price": 79.99,
            "status": "pending"
        }
    ]
    
    created_orders = []
    for i, order_data in enumerate(orders_data, 1):
        print(f"   Creando orden {i}...")
        order = api.create_order(order_data)
        if order:
            created_orders.append(order)
            print(f"   ✅ Orden {order['id']} creada: {order['customer_name']}")
        else:
            print(f"   ❌ Error al crear orden {i}")
    
    print(f"\n✅ Se crearon {len(created_orders)} órdenes\n")
    
    # 3. Listar todas las órdenes
    print("3. Listando todas las órdenes...")
    all_orders = api.get_orders()
    if all_orders:
        print(f"   Total de órdenes: {len(all_orders)}")
        for order in all_orders:
            print(f"   - ID {order['id']}: {order['customer_name']} - {order['product']} (${order['price']}) - {order['status']}")
    print()
    
    # 4. Actualizar órdenes masivamente
    print("4. Actualizando estados de órdenes...")
    for order in created_orders[:2]:  # Actualizar las primeras 2
        update_data = {
            "status": "shipped"
        }
        updated_order = api.update_order(order['id'], update_data)
        if updated_order:
            print(f"   ✅ Orden {updated_order['id']} actualizada a: {updated_order['status']}")
    
    # 5. Aplicar descuentos
    print("\n5. Aplicando descuentos especiales...")
    for order in created_orders:
        if order['product'] == 'Smartphone iPhone 15':
            # 10% de descuento en iPhones
            new_price = order['price'] * 0.9
            update_data = {"price": round(new_price, 2)}
            updated_order = api.update_order(order['id'], update_data)
            if updated_order:
                print(f"   ✅ Descuento aplicado a orden {updated_order['id']}: ${updated_order['price']}")
    
    # 6. Buscar órdenes por estado
    print("\n6. Buscando órdenes por estado...")
    all_orders = api.get_orders()
    if all_orders:
        pending_orders = [o for o in all_orders if o['status'] == 'pending']
        shipped_orders = [o for o in all_orders if o['status'] == 'shipped']
        
        print(f"   Órdenes pendientes: {len(pending_orders)}")
        print(f"   Órdenes enviadas: {len(shipped_orders)}")
    
    # 7. Calcular estadísticas
    print("\n7. Calculando estadísticas...")
    if all_orders:
        total_revenue = sum(order['price'] * order['quantity'] for order in all_orders)
        avg_order_value = total_revenue / len(all_orders) if all_orders else 0
        
        print(f"   Ingreso total: ${total_revenue:.2f}")
        print(f"   Valor promedio por orden: ${avg_order_value:.2f}")
        print(f"   Producto más caro: ${max(order['price'] for order in all_orders):.2f}")
        print(f"   Producto más barato: ${min(order['price'] for order in all_orders):.2f}")
    
    # 8. Intentar crear orden inválida (para demostrar validación)
    print("\n8. Probando validación de datos...")
    invalid_order = {
        "customer_name": "Test User",
        "product": "Test Product",
        "quantity": -5,  # Inválido: cantidad negativa
        "price": 10.00
    }
    
    result = api.create_order(invalid_order)
    if result is None:
        print("   ✅ Validación funcionó correctamente (orden rechazada)")
    
    print("\n=== ¡EJEMPLO AVANZADO COMPLETADO! ===")

if __name__ == "__main__":
    ejemplo_avanzado()

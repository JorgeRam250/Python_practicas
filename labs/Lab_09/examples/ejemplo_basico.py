"""
Ejemplo 1: Uso Básico de la API de Orders
Este ejemplo muestra cómo interactuar con la API de forma sencilla
"""

import requests
import json

# Configuración
BASE_URL = "http://localhost:8000"

def ejemplo_basico():
    """Ejemplo básico de uso de la API"""
    
    print("=== EJEMPLO BÁSICO DE API FASTAPI ===\n")
    
    # 1. Iniciar sesión para obtener token
    print("1. Iniciando sesión...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            print("✅ Login exitoso")
            print(f"Token: {token[:20]}...\n")
        else:
            print("❌ Error en login")
            return
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. Asegúrate de que está corriendo en http://localhost:8000")
        return
    
    # 2. Crear una nueva orden
    print("2. Creando una nueva orden...")
    order_data = {
        "customer_name": "Juan Pérez",
        "product": "Laptop Gaming",
        "quantity": 1,
        "price": 1299.99,
        "status": "pending"
    }
    
    response = requests.post(f"{BASE_URL}/orders/", json=order_data, headers=headers)
    if response.status_code == 200:
        created_order = response.json()
        order_id = created_order["id"]
        print(f"✅ Orden creada con ID: {order_id}")
        print(f"   Cliente: {created_order['customer_name']}")
        print(f"   Producto: {created_order['product']}")
        print(f"   Precio: ${created_order['price']}\n")
    else:
        print("❌ Error al crear orden")
        return
    
    # 3. Obtener todas las órdenes
    print("3. Obteniendo todas las órdenes...")
    response = requests.get(f"{BASE_URL}/orders/", headers=headers)
    if response.status_code == 200:
        orders = response.json()
        print(f"✅ Se encontraron {len(orders)} órdenes:")
        for order in orders:
            print(f"   - ID {order['id']}: {order['customer_name']} - {order['product']} (${order['price']})")
        print()
    
    # 4. Obtener una orden específica
    print(f"4. Obteniendo orden con ID {order_id}...")
    response = requests.get(f"{BASE_URL}/orders/{order_id}", headers=headers)
    if response.status_code == 200:
        order = response.json()
        print(f"✅ Orden encontrada:")
        print(f"   ID: {order['id']}")
        print(f"   Cliente: {order['customer_name']}")
        print(f"   Producto: {order['product']}")
        print(f"   Cantidad: {order['quantity']}")
        print(f"   Precio: ${order['price']}")
        print(f"   Estado: {order['status']}\n")
    
    # 5. Actualizar la orden
    print(f"5. Actualizando orden {order_id}...")
    update_data = {
        "status": "completed",
        "price": 1199.99  # Descuento especial
    }
    
    response = requests.put(f"{BASE_URL}/orders/{order_id}", json=update_data, headers=headers)
    if response.status_code == 200:
        updated_order = response.json()
        print(f"✅ Orden actualizada:")
        print(f"   Nuevo estado: {updated_order['status']}")
        print(f"   Nuevo precio: ${updated_order['price']}\n")
    
    # 6. Eliminar la orden
    print(f"6. Eliminando orden {order_id}...")
    response = requests.delete(f"{BASE_URL}/orders/{order_id}", headers=headers)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result['message']}\n")
    
    print("=== ¡EJEMPLO BÁSICO COMPLETADO! ===")

if __name__ == "__main__":
    ejemplo_basico()

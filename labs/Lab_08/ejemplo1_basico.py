#!/usr/bin/env python3
"""
Ejemplo 1: Uso básico de SQLAlchemy ORM
Este ejemplo muestra cómo crear usuarios, pedidos y items de pedido
usando las operaciones CRUD básicas.
"""

from database import create_tables, get_db
from crud import create_user, create_order, create_order_item, get_user, get_user_orders
from models import User, Order, OrderItem

def main():
    print("=== Ejemplo 1: Uso básico de SQLAlchemy ORM ===\n")
    
    # Crear las tablas en la base de datos
    create_tables()
    
    # Obtener una sesión de base de datos
    db = next(get_db())
    
    try:
        # 1. Crear un usuario
        print("1. Creando usuario...")
        user = create_user(db, "juanperez", "juan@example.com")
        print(f"   Usuario creado: {user}")
        
        # 2. Crear un pedido para el usuario
        print("\n2. Creando pedido...")
        order = create_order(db, user.id)
        print(f"   Pedido creado: {order}")
        
        # 3. Agregar items al pedido
        print("\n3. Agregando items al pedido...")
        item1 = create_order_item(db, order.id, "Laptop HP", 1, 899.99)
        item2 = create_order_item(db, order.id, "Mouse Logitech", 2, 25.50)
        print(f"   Item 1: {item1}")
        print(f"   Item 2: {item2}")
        
        # 4. Consultar información
        print("\n4. Consultando información...")
        retrieved_user = get_user(db, user.id)
        user_orders = get_user_orders(db, user.id)
        
        print(f"   Usuario recuperado: {retrieved_user}")
        print(f"   Pedidos del usuario: {len(user_orders)}")
        print(f"   Total del pedido: ${user_orders[0].total_amount:.2f}")
        
        # 5. Mostrar items del pedido
        print("\n5. Items del pedido:")
        for order in user_orders:
            items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
            for item in items:
                print(f"   - {item.product_name}: {item.quantity} x ${item.unit_price:.2f} = ${item.quantity * item.unit_price:.2f}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()

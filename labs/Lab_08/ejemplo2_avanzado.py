#!/usr/bin/env python3
"""
Ejemplo 2: Operaciones avanzadas con SQLAlchemy
Este ejemplo muestra consultas complejas, relaciones y transacciones
"""

from database import create_tables, get_db
from crud import create_user, create_order, create_order_item, get_user_by_email, update_user
from models import User, Order, OrderItem
from sqlalchemy.orm import joinedload
from sqlalchemy import func, and_, or_

def main():
    print("=== Ejemplo 2: Operaciones avanzadas con SQLAlchemy ===\n")
    
    # Crear las tablas
    create_tables()
    db = next(get_db())
    
    try:
        # 1. Crear múltiples usuarios
        print("1. Creando múltiples usuarios...")
        users_data = [
            ("maria_garcia", "maria@example.com"),
            ("carlos_rodriguez", "carlos@example.com"),
            ("ana_martinez", "ana@example.com")
        ]
        
        created_users = []
        for username, email in users_data:
            user = create_user(db, username, email)
            created_users.append(user)
            print(f"   Usuario creado: {user}")
        
        # 2. Crear pedidos con múltiples items
        print("\n2. Creando pedidos con múltiples items...")
        
        # Pedidos para María
        order1 = create_order(db, created_users[0].id)
        create_order_item(db, order1.id, "iPhone 15", 1, 999.99)
        create_order_item(db, order1.id, "AirPods", 1, 249.99)
        
        # Pedidos para Carlos
        order2 = create_order(db, created_users[1].id)
        create_order_item(db, order2.id, "MacBook Pro", 1, 1999.99)
        create_order_item(db, order2.id, "Magic Mouse", 1, 79.99)
        create_order_item(db, order2.id, "USB-C Cable", 2, 19.99)
        
        # Pedidos para Ana
        order3 = create_order(db, created_users[2].id)
        create_order_item(db, order3.id, "iPad Air", 1, 599.99)
        
        print(f"   Creados 3 pedidos con items")
        
        # 3. Consulta con relaciones (eager loading)
        print("\n3. Consulta con relaciones (eager loading)...")
        users_with_orders = db.query(User).options(joinedload(User.orders)).all()
        
        for user in users_with_orders:
            print(f"   Usuario: {user.username} - Pedidos: {len(user.orders)}")
            for order in user.orders:
                print(f"     Pedido #{order.id}: Total ${order.total_amount:.2f}")
        
        # 4. Consultas complejas con agregaciones
        print("\n4. Consultas con agregaciones...")
        
        # Total de ventas por usuario
        sales_by_user = db.query(
            User.username,
            func.sum(Order.total_amount).label('total_sales')
        ).join(Order).group_by(User.id).all()
        
        print("   Ventas totales por usuario:")
        for username, total in sales_by_user:
            print(f"     {username}: ${total:.2f}")
        
        # 5. Consultas con filtros complejos
        print("\n5. Consultas con filtros complejos...")
        
        # Pedidos con total mayor a $500
        expensive_orders = db.query(Order).filter(Order.total_amount > 500).all()
        print(f"   Pedidos con total > $500: {len(expensive_orders)}")
        
        # Items con precio unitario entre $50 y $200
        mid_range_items = db.query(OrderItem).filter(
            and_(OrderItem.unit_price >= 50, OrderItem.unit_price <= 200)
        ).all()
        print(f"   Items con precio entre $50 y $200: {len(mid_range_items)}")
        
        # 6. Transacciones
        print("\n6. Demostración de transacciones...")
        
        try:
            # Actualizar información de usuario
            updated_user = update_user(db, created_users[0].id, username="maria_garcia_updated")
            print(f"   Usuario actualizado: {updated_user}")
            
            # Simular un error y rollback
            db.begin_nested()
            create_user(db, "test_user", "test@example.com")
            raise Exception("Error simulado para demostrar rollback")
            
        except Exception as e:
            db.rollback()
            print(f"   Rollback ejecutado: {e}")
        
        # 7. Estadísticas finales
        print("\n7. Estadísticas finales...")
        
        total_users = db.query(func.count(User.id)).scalar()
        total_orders = db.query(func.count(Order.id)).scalar()
        total_items = db.query(func.count(OrderItem.id)).scalar()
        total_revenue = db.query(func.sum(Order.total_amount)).scalar()
        
        print(f"   Total usuarios: {total_users}")
        print(f"   Total pedidos: {total_orders}")
        print(f"   Total items: {total_items}")
        print(f"   Ingresos totales: ${total_revenue:.2f}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Ejemplo 3: Migraciones con Alembic y gestión de esquema
Este ejemplo muestra cómo trabajar con migraciones de base de datos
"""

import os
import sqlite3
from database import create_tables, get_db
from crud import create_user, create_order, create_order_item
from models import User, Order, OrderItem

def setup_database_file():
    """Configurar base de datos SQLite en archivo para demostrar migraciones"""
    db_file = "lab_migrations.db"
    
    # Eliminar archivo si existe
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"   Archivo de base de datos existente eliminado: {db_file}")
    
    # Crear conexión a la base de datos
    conn = sqlite3.connect(db_file)
    conn.close()
    
    return db_file

def create_initial_schema():
    """Crear esquema inicial usando SQLAlchemy"""
    print("2. Creando esquema inicial con SQLAlchemy...")
    
    # Modificar la URL de la base de datos para usar archivo
    from database import engine, DATABASE_URL
    original_url = DATABASE_URL
    
    # Actualizar el motor para usar archivo
    from sqlalchemy import create_engine
    engine = create_engine("sqlite:///lab_migrations.db", echo=False)
    
    from models import Base
    Base.metadata.create_all(bind=engine)
    
    print("   Esquema inicial creado exitosamente")

def verify_schema():
    """Verificar el esquema de la base de datos"""
    print("\n3. Verificando esquema de la base de datos...")
    
    conn = sqlite3.connect("lab_migrations.db")
    cursor = conn.cursor()
    
    # Obtener lista de tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("   Tablas creadas:")
    for table in tables:
        table_name = table[0]
        print(f"     - {table_name}")
        
        # Obtener información de columnas
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        for col in columns:
            print(f"       * {col[1]} ({col[2]})")
    
    conn.close()

def populate_sample_data():
    """Poblar la base de datos con datos de ejemplo"""
    print("\n4. Poblando base de datos con datos de ejemplo...")
    
    # Configurar base de datos para usar archivo
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    engine = create_engine("sqlite:///lab_migrations.db", echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Crear usuarios
        user1 = create_user(db, "pedro_lopez", "pedro@example.com")
        user2 = create_user(db, "lucia_morales", "lucia@example.com")
        
        print(f"   Usuarios creados: {user1.username}, {user2.username}")
        
        # Crear pedidos
        order1 = create_order(db, user1.id)
        create_order_item(db, order1.id, "Samsung Galaxy", 1, 799.99)
        create_order_item(db, order1.id, "Samsung Watch", 1, 299.99)
        
        order2 = create_order(db, user2.id)
        create_order_item(db, order2.id, "Sony Headphones", 1, 199.99)
        
        print(f"   Pedidos creados con items")
        
        # Verificar datos
        users_count = db.query(User).count()
        orders_count = db.query(Order).count()
        items_count = db.query(OrderItem).count()
        
        print(f"   Registros insertados: {users_count} usuarios, {orders_count} pedidos, {items_count} items")
        
    except Exception as e:
        print(f"   Error al poblar datos: {e}")
        db.rollback()
    finally:
        db.close()

def demonstrate_migration_simulation():
    """Simular una migración (agregar nueva columna)"""
    print("\n5. Simulando migración (agregando nueva columna)...")
    
    conn = sqlite3.connect("lab_migrations.db")
    cursor = conn.cursor()
    
    try:
        # Agregar nueva columna a la tabla users
        cursor.execute("ALTER TABLE users ADD COLUMN phone VARCHAR(20);")
        print("   Columna 'phone' agregada a la tabla 'users'")
        
        # Agregar datos a la nueva columna
        cursor.execute("UPDATE users SET phone = '555-0101' WHERE id = 1;")
        cursor.execute("UPDATE users SET phone = '555-0102' WHERE id = 2;")
        print("   Datos de teléfono agregados")
        
        conn.commit()
        
        # Verificar la nueva estructura
        cursor.execute("PRAGMA table_info(users);")
        columns = cursor.fetchall()
        print("   Nueva estructura de la tabla users:")
        for col in columns:
            print(f"     * {col[1]} ({col[2]})")
        
    except Exception as e:
        print(f"   Error en migración: {e}")
        conn.rollback()
    finally:
        conn.close()

def backup_and_restore():
    """Demostrar backup y restauración"""
    print("\n6. Demostración de backup y restauración...")
    
    # Crear backup
    backup_file = "lab_migrations_backup.db"
    
    conn = sqlite3.connect("lab_migrations.db")
    backup_conn = sqlite3.connect(backup_file)
    
    try:
        conn.backup(backup_conn)
        print(f"   Backup creado: {backup_file}")
        
        # Verificar backup
        cursor = backup_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users;")
        user_count = cursor.fetchone()[0]
        print(f"   Usuarios en backup: {user_count}")
        
    except Exception as e:
        print(f"   Error en backup: {e}")
    finally:
        conn.close()
        backup_conn.close()

def main():
    print("=== Ejemplo 3: Migraciones con Alembic y gestión de esquema ===\n")
    
    try:
        # 1. Configurar base de datos
        print("1. Configurando base de datos...")
        db_file = setup_database_file()
        print(f"   Base de datos configurada: {db_file}")
        
        # 2. Crear esquema inicial
        create_initial_schema()
        
        # 3. Verificar esquema
        verify_schema()
        
        # 4. Poblar con datos
        populate_sample_data()
        
        # 5. Simular migración
        demonstrate_migration_simulation()
        
        # 6. Backup y restauración
        backup_and_restore()
        
        print("\n=== Proceso completado exitosamente ===")
        print("Archivos generados:")
        print("  - lab_migrations.db (base de datos principal)")
        print("  - lab_migrations_backup.db (backup)")
        
    except Exception as e:
        print(f"Error en el proceso: {e}")

if __name__ == "__main__":
    main()

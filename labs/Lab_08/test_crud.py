import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Order, OrderItem
from crud import create_user, get_user, create_order, create_order_item, get_user_orders, get_order_items

# Configuración de la base de datos para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Fixture para crear una sesión de base de datos para cada prueba"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

def test_create_user(db_session):
    """Prueba crear un usuario"""
    user = create_user(db_session, "johndoe", "john@example.com")
    assert user.id is not None
    assert user.username == "johndoe"
    assert user.email == "john@example.com"

def test_get_user(db_session):
    """Prueba obtener un usuario"""
    # Crear usuario
    user = create_user(db_session, "janedoe", "jane@example.com")
    
    # Obtener usuario
    retrieved_user = get_user(db_session, user.id)
    assert retrieved_user is not None
    assert retrieved_user.username == "janedoe"
    assert retrieved_user.email == "jane@example.com"

def test_create_order(db_session):
    """Prueba crear un pedido"""
    # Crear usuario primero
    user = create_user(db_session, "testuser", "test@example.com")
    
    # Crear pedido
    order = create_order(db_session, user.id, 100.0)
    assert order.id is not None
    assert order.user_id == user.id
    assert order.total_amount == 100.0

def test_create_order_item(db_session):
    """Prueba crear un item de pedido"""
    # Crear usuario y pedido
    user = create_user(db_session, "itemuser", "item@example.com")
    order = create_order(db_session, user.id)
    
    # Crear item
    item = create_order_item(db_session, order.id, "Laptop", 1, 999.99)
    assert item.id is not None
    assert item.product_name == "Laptop"
    assert item.quantity == 1
    assert item.unit_price == 999.99
    
    # Verificar que el total del pedido se actualizó
    updated_order = get_user_orders(db_session, user.id)[0]
    assert updated_order.total_amount == 999.99

def test_get_user_orders(db_session):
    """Prueba obtener pedidos de un usuario"""
    # Crear usuario
    user = create_user(db_session, "orderuser", "order@example.com")
    
    # Crear múltiples pedidos
    order1 = create_order(db_session, user.id, 50.0)
    order2 = create_order(db_session, user.id, 75.0)
    
    # Obtener pedidos del usuario
    orders = get_user_orders(db_session, user.id)
    assert len(orders) == 2
    assert orders[0].user_id == user.id
    assert orders[1].user_id == user.id

def test_get_order_items(db_session):
    """Prueba obtener items de un pedido"""
    # Crear usuario y pedido
    user = create_user(db_session, "itemsuser", "items@example.com")
    order = create_order(db_session, user.id)
    
    # Crear múltiples items
    item1 = create_order_item(db_session, order.id, "Mouse", 2, 25.0)
    item2 = create_order_item(db_session, order.id, "Keyboard", 1, 50.0)
    
    # Obtener items del pedido
    items = get_order_items(db_session, order.id)
    assert len(items) == 2
    assert items[0].order_id == order.id
    assert items[1].order_id == order.id

def test_complete_workflow(db_session):
    """Prueba del flujo completo: usuario -> pedido -> items"""
    # 1. Crear usuario
    user = create_user(db_session, "workflowuser", "workflow@example.com")
    
    # 2. Crear pedido
    order = create_order(db_session, user.id)
    
    # 3. Agregar items al pedido
    create_order_item(db_session, order.id, "Monitor", 1, 299.99)
    create_order_item(db_session, order.id, "Webcam", 1, 89.99)
    
    # 4. Verificar resultados
    orders = get_user_orders(db_session, user.id)
    assert len(orders) == 1
    
    items = get_order_items(db_session, orders[0].id)
    assert len(items) == 2
    assert orders[0].total_amount == 389.98  # 299.99 + 89.99

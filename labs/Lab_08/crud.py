from sqlalchemy.orm import Session
from models import User, Order, OrderItem
from database import get_db
from typing import List, Optional

# CRUD para User
def create_user(db: Session, username: str, email: str) -> User:
    """Crear un nuevo usuario"""
    db_user = User(username=username, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> Optional[User]:
    """Obtener un usuario por ID"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Obtener un usuario por email"""
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Obtener lista de usuarios"""
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, username: str = None, email: str = None) -> Optional[User]:
    """Actualizar un usuario"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        if username:
            db_user.username = username
        if email:
            db_user.email = email
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    """Eliminar un usuario"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

# CRUD para Order
def create_order(db: Session, user_id: int, total_amount: float = 0.0) -> Order:
    """Crear un nuevo pedido"""
    db_order = Order(user_id=user_id, total_amount=total_amount)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int) -> Optional[Order]:
    """Obtener un pedido por ID"""
    return db.query(Order).filter(Order.id == order_id).first()

def get_user_orders(db: Session, user_id: int) -> List[Order]:
    """Obtener todos los pedidos de un usuario"""
    return db.query(Order).filter(Order.user_id == user_id).all()

# CRUD para OrderItem
def create_order_item(db: Session, order_id: int, product_name: str, 
                     quantity: int, unit_price: float) -> OrderItem:
    """Crear un nuevo item de pedido"""
    db_item = OrderItem(
        order_id=order_id,
        product_name=product_name,
        quantity=quantity,
        unit_price=unit_price
    )
    db.add(db_item)
    
    # Actualizar el total del pedido
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        order.total_amount += quantity * unit_price
        db.commit()
    
    db.refresh(db_item)
    return db_item

def get_order_items(db: Session, order_id: int) -> List[OrderItem]:
    """Obtener todos los items de un pedido"""
    return db.query(OrderItem).filter(OrderItem.order_id == order_id).all()

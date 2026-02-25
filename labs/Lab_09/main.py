from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import hashlib
import jwt
from datetime import datetime, timedelta
import os

# Configuración
SECRET_KEY = "tu_clave_secreta_aqui"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Inicialización de FastAPI
app = FastAPI(title="API de Orders", version="1.0.0")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seguridad
security = HTTPBearer()

# Modelos Pydantic
class User(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Order(BaseModel):
    id: Optional[int] = None
    customer_name: str
    product: str
    quantity: int
    price: float
    status: str = "pending"

class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    product: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    status: Optional[str] = None

# Base de datos
def init_db():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    
    # Tabla de usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
    ''')
    
    # Tabla de orders
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
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        hashed_password = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute("INSERT INTO users VALUES (?, ?)", ("admin", hashed_password))
    
    conn.commit()
    conn.close()

# Funciones de autenticación
def verify_password(plain_password, hashed_password):
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

def get_password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Endpoints de autenticación
@app.post("/login", response_model=Token)
async def login(user: User):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (user.username,))
    result = cursor.fetchone()
    conn.close()
    
    if not result or not verify_password(user.password, result[0]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: str = Depends(verify_token)):
    return {"username": current_user}

# Endpoints CRUD de Orders
@app.post("/orders/", response_model=Order)
async def create_order(order: Order, current_user: str = Depends(verify_token)):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO orders (customer_name, product, quantity, price, status)
    VALUES (?, ?, ?, ?, ?)
    ''', (order.customer_name, order.product, order.quantity, order.price, order.status))
    order.id = cursor.lastrowid
    conn.commit()
    conn.close()
    return order

@app.get("/orders/", response_model=List[Order])
async def get_orders(current_user: str = Depends(verify_token)):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    conn.close()
    
    orders = []
    for row in rows:
        orders.append(Order(
            id=row[0],
            customer_name=row[1],
            product=row[2],
            quantity=row[3],
            price=row[4],
            status=row[5]
        ))
    return orders

@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: int, current_user: str = Depends(verify_token)):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE id=?", (order_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Order no encontrada")
    
    return Order(
        id=row[0],
        customer_name=row[1],
        product=row[2],
        quantity=row[3],
        price=row[4],
        status=row[5]
    )

@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, order_update: OrderUpdate, current_user: str = Depends(verify_token)):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    
    # Obtener order actual
    cursor.execute("SELECT * FROM orders WHERE id=?", (order_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Order no encontrada")
    
    # Actualizar campos
    update_data = order_update.dict(exclude_unset=True)
    if not update_data:
        conn.close()
        return Order(
            id=row[0],
            customer_name=row[1],
            product=row[2],
            quantity=row[3],
            price=row[4],
            status=row[5]
        )
    
    set_clause = ", ".join([f"{k} = ?" for k in update_data.keys()])
    values = list(update_data.values()) + [order_id]
    
    cursor.execute(f"UPDATE orders SET {set_clause} WHERE id=?", values)
    conn.commit()
    
    # Obtener order actualizada
    cursor.execute("SELECT * FROM orders WHERE id=?", (order_id,))
    row = cursor.fetchone()
    conn.close()
    
    return Order(
        id=row[0],
        customer_name=row[1],
        product=row[2],
        quantity=row[3],
        price=row[4],
        status=row[5]
    )

@app.delete("/orders/{order_id}")
async def delete_order(order_id: int, current_user: str = Depends(verify_token)):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE id=?", (order_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Order no encontrada")
    
    cursor.execute("DELETE FROM orders WHERE id=?", (order_id,))
    conn.commit()
    conn.close()
    
    return {"message": "Order eliminada exitosamente"}

# Inicializar base de datos al iniciar
@app.on_event("startup")
async def startup_event():
    init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Guía Completa del Laboratorio: Acceso a datos y ORM

## 📋 Descripción General

Este laboratorio te enseñará a trabajar con bases de datos en Python usando SQLAlchemy ORM, uno de los frameworks más potentes para el manejo de bases de datos relacionales.

## 🎯 Objetivos del Laboratorio

1. **Modelar entidades y relaciones** usando SQLAlchemy ORM
2. **Implementar operaciones CRUD** (Crear, Leer, Actualizar, Eliminar)
3. **Gestionar migraciones** con Alembic
4. **Realizar pruebas** con SQLite en memoria

## 📁 Estructura del Proyecto

```
Windsurf/
├── requirements.txt          # Dependencias del proyecto
├── README.md                 # Documentación básica
├── models.py                 # Modelos de datos (User, Order, OrderItem)
├── database.py               # Configuración de la base de datos
├── crud.py                   # Operaciones CRUD
├── test_crud.py              # Pruebas unitarias
├── ejemplo1_basico.py        # Ejemplo básico de uso
├── ejemplo2_avanzado.py      # Ejemplo con operaciones avanzadas
├── ejemplo3_migraciones.py    # Ejemplo de migraciones
├── alembic.ini              # Configuración de Alembic
├── alembic/                 # Directorio de migraciones
│   ├── env.py               # Entorno de Alembic
│   ├── script.py.mako       # Plantilla de migraciones
│   └── versions/            # Versiones de migraciones
│       └── 001_initial_migration.py
└── guia_completa.md         # Esta guía
```

## 🔧 Instalación y Configuración

### Paso 1: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 2: Entender los componentes principales

#### 1. **Models (models.py)**
Define la estructura de tus tablas de base de datos como clases Python:

```python
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
```

#### 2. **Database (database.py)**
Configura la conexión a la base de datos:

```python
engine = create_engine("sqlite:///:memory:")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

#### 3. **CRUD Operations (crud.py)**
Implementa las operaciones básicas de base de datos:

```python
def create_user(db: Session, username: str, email: str) -> User:
    db_user = User(username=username, email=email)
    db.add(db_user)
    db.commit()
    return db_user
```

## 📚 Conceptos Clave Explicados

### 1. **ORM (Object-Relational Mapping)**
El ORM te permite trabajar con bases de datos usando objetos Python en lugar de SQL directo.

**Ventajas:**
- Código más legible y mantenible
- Protección contra inyección SQL
- Independencia del motor de base de datos

### 2. **Modelos y Relaciones**
- **User**: Entidad principal que representa a los usuarios
- **Order**: Pedidos realizados por los usuarios (relación muchos-a-uno con User)
- **OrderItem**: Items dentro de cada pedido (relación muchos-a-uno con Order)

### 3. **Sesiones de Base de Datos**
Las sesiones gestionan las transacciones y el estado de los objetos:

```python
db = SessionLocal()
try:
    # Operaciones de base de datos
    db.commit()
except Exception:
    db.rollback()
finally:
    db.close()
```

### 4. **Migraciones con Alembic**
Alembic gestiona los cambios en el esquema de la base de datos:

```bash
# Crear nueva migración
alembic revision --autogenerate -m "descripcion del cambio"

# Aplicar migraciones
alembic upgrade head
```

## 🚀 Ejecutando los Ejemplos

### Ejemplo 1: Uso Básico
```bash
python ejemplo1_basico.py
```
**Qué aprenderás:**
- Crear usuarios, pedidos y items
- Realizar consultas básicas
- Entender las relaciones entre modelos

### Ejemplo 2: Operaciones Avanzadas
```bash
python ejemplo2_avanzado.py
```
**Qué aprenderás:**
- Consultas complejas con joins
- Agregaciones y funciones SQL
- Manejo de transacciones
- Filtros avanzados

### Ejemplo 3: Migraciones
```bash
python ejemplo3_migraciones.py
```
**Qué aprenderás:**
- Creación y modificación de esquemas
- Backup y restauración
- Simulación de migraciones

## 🧪 Ejecutando Pruebas

```bash
pytest test_crud.py -v
```

Las pruebas verifican:
- ✅ Creación de usuarios
- ✅ Creación de pedidos y items
- ✅ Consultas y relaciones
- ✅ Flujo completo del sistema

## 📊 Flujo de Trabajo Típico

### 1. **Definir Modelos**
```python
# models.py
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
```

### 2. **Crear Migración**
```bash
alembic revision --autogenerate -m "Add products table"
```

### 3. **Aplicar Migración**
```bash
alembic upgrade head
```

### 4. **Implementar CRUD**
```python
# crud.py
def create_product(db: Session, name: str, price: float) -> Product:
    db_product = Product(name=name, price=price)
    db.add(db_product)
    db.commit()
    return db_product
```

### 5. **Escribir Pruebas**
```python
# test_crud.py
def test_create_product(db_session):
    product = create_product(db_session, "Laptop", 999.99)
    assert product.name == "Laptop"
    assert product.price == 999.99
```

## 🔍 Buenas Prácticas

### 1. **Manejo de Sesiones**
```python
# ✅ Bueno: Usar context managers
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 2. **Validaciones**
```python
# ✅ Bueno: Validar datos antes de guardar
def create_user(db: Session, username: str, email: str) -> User:
    if len(username) < 3:
        raise ValueError("Username too short")
    
    db_user = User(username=username, email=email)
    db.add(db_user)
    db.commit()
    return db_user
```

### 3. **Consultas Eficientes**
```python
# ✅ Bueno: Usar eager loading para relaciones
users_with_orders = db.query(User).options(joinedload(User.orders)).all()

# ❌ Malo: N+1 query problem
users = db.query(User).all()
for user in users:
    orders = user.orders  # Esto genera una consulta por cada usuario
```

## 🐛 Problemas Comunes y Soluciones

### 1. **Error: "SQLite objects created in a thread can only be used in that same thread"**
**Solución:** Agregar `connect_args={"check_same_thread": False}` al crear el engine.

### 2. **Error: "Foreign key constraint failed"**
**Solución:** Verificar que los registros relacionados existen antes de crear las relaciones.

### 3. **Error: "Session is closed"**
**Solución:** Asegurarse de no usar la sesión después de cerrarla.

## 📈 Extensiones y Mejoras

### 1. **Agregar Pydantic para validación**
```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    
    class Config:
        from_attributes = True
```

### 2. **Implementar paginación**
```python
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()
```

### 3. **Agregar logging**
```python
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

## 🎓 Evaluación del Laboratorio

Para completar exitosamente este laboratorio, deberás:

1. **✅ Entender los modelos** y sus relaciones
2. **✅ Implementar operaciones CRUD** básicas
3. **✅ Crear y aplicar migraciones** con Alembic
4. **✅ Escribir pruebas** que verifiquen el funcionamiento
5. **✅ Ejecutar los ejemplos** y entender su salida

## 📖 Recursos Adicionales

- [Documentación oficial de SQLAlchemy](https://docs.sqlalchemy.org/)
- [Documentación de Alembic](https://alembic.sqlalchemy.org/)
- [Tutorial de SQLAlchemy ORM](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)
- [Best Practices for SQLAlchemy](https://docs.sqlalchemy.org/en/14/orm/persistence_techniques.html)

---

**¡Felicidades!** Ahora tienes una base sólida para trabajar con bases de datos en Python usando SQLAlchemy ORM.

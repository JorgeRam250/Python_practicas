from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Configuración de la base de datos SQLite en memoria
DATABASE_URL = "sqlite:///:memory:"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear todas las tablas
def create_tables():
    Base.metadata.create_all(bind=engine)

# Obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

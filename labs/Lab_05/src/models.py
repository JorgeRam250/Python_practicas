"""
Modelos de datos con TypedDict y tipos avanzados
"""

from typing import Literal, TypedDict, Union, Dict, List, Optional
from datetime import datetime


class Usuario(TypedDict):
    """TypedDict para representar un usuario."""
    id: int
    nombre: str
    email: str
    edad: Optional[int]
    activo: bool
    fecha_registro: datetime


class Producto(TypedDict):
    """TypedDict para representar un producto."""
    id: int
    nombre: str
    precio: float
    categoria: Literal["electrónica", "ropa", "alimentos", "libros"]
    stock: int
    disponible: bool


class Pedido(TypedDict):
    """TypedDict para representar un pedido."""
    id: int
    usuario_id: int
    productos: List[Dict[str, Union[int, float]]]
    total: float
    estado: Literal["pendiente", "procesando", "enviado", "entregado", "cancelado"]
    fecha_pedido: datetime


# Alias de tipo para mayor claridad
ID = Union[int, str]
Precio = Union[int, float]
EstadoPedido = Literal["pendiente", "procesando", "enviado", "entregado", "cancelado"]
CategoriaProducto = Literal["electrónica", "ropa", "alimentos", "libros"]


def crear_usuario(
    id: ID, 
    nombre: str, 
    email: str, 
    edad: Optional[int] = None
) -> Usuario:
    """
    Crea un nuevo usuario con validación de tipos.
    
    Args:
        id: Identificador único del usuario
        nombre: Nombre completo del usuario
        email: Correo electrónico del usuario
        edad: Edad opcional del usuario
        
    Returns:
        Usuario: Diccionario tipado con los datos del usuario
    """
    return {
        "id": int(id),
        "nombre": nombre,
        "email": email,
        "edad": edad,
        "activo": True,
        "fecha_registro": datetime.now()
    }


def crear_producto(
    id: ID,
    nombre: str,
    precio: Precio,
    categoria: CategoriaProducto,
    stock: int = 0
) -> Producto:
    """
    Crea un nuevo producto con validación de categorías.
    
    Args:
        id: Identificador único del producto
        nombre: Nombre del producto
        precio: Precio del producto
        categoria: Categoría del producto (valores predefinidos)
        stock: Cantidad en stock
        
    Returns:
        Producto: Diccionario tipado con los datos del producto
    """
    return {
        "id": int(id),
        "nombre": nombre,
        "precio": float(precio),
        "categoria": categoria,
        "stock": stock,
        "disponible": stock > 0
    }


def validar_email(email: str) -> bool:
    """
    Valida si un email tiene formato correcto.
    
    Args:
        email: Correo electrónico a validar
        
    Returns:
        bool: True si el email es válido, False otherwise
    """
    # Validación simple de email
    return "@" in email and "." in email.split("@")[-1]

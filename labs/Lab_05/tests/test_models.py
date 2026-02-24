"""
Tests para los modelos con type hints
"""

import pytest
from datetime import datetime
from src.models import (
    Usuario, Producto, Pedido, 
    crear_usuario, crear_producto, validar_email,
    ID, Precio, CategoriaProducto
)


class TestUsuario:
    """Tests para la clase Usuario y funciones relacionadas."""
    
    def test_crear_usuario_basico(self) -> None:
        """Test para crear usuario con datos básicos."""
        usuario = crear_usuario(1, "Juan Pérez", "juan@example.com")
        
        assert usuario["id"] == 1
        assert usuario["nombre"] == "Juan Pérez"
        assert usuario["email"] == "juan@example.com"
        assert usuario["edad"] is None
        assert usuario["activo"] is True
        assert isinstance(usuario["fecha_registro"], datetime)
    
    def test_crear_usuario_con_edad(self) -> None:
        """Test para crear usuario con edad."""
        usuario = crear_usuario("2", "María García", "maria@example.com", 25)
        
        assert usuario["id"] == 2
        assert usuario["edad"] == 25
    
    def test_crear_usuario_id_string(self) -> None:
        """Test para crear usuario con ID como string."""
        usuario = crear_usuario("123", "Test User", "test@example.com")
        
        assert usuario["id"] == 123  # Debe convertir a int
    
    def test_validar_email_valido(self) -> None:
        """Test para validar emails válidos."""
        assert validar_email("usuario@dominio.com") is True
        assert validar_email("test.email@sub.dominio.org") is True
    
    def test_validar_email_invalido(self) -> None:
        """Test para validar emails inválidos."""
        assert validar_email("usuario@") is False
        assert validar_email("@dominio.com") is False
        assert validar_email("usuario.dominio.com") is False
        assert validar_email("") is False


class TestProducto:
    """Tests para la clase Producto y funciones relacionadas."""
    
    def test_crear_producto_basico(self) -> None:
        """Test para crear producto básico."""
        producto = crear_producto(
            1, 
            "Laptop", 
            999.99, 
            "electrónica"
        )
        
        assert producto["id"] == 1
        assert producto["nombre"] == "Laptop"
        assert producto["precio"] == 999.99
        assert producto["categoria"] == "electrónica"
        assert producto["stock"] == 0
        assert producto["disponible"] is False
    
    def test_crear_producto_con_stock(self) -> None:
        """Test para crear producto con stock."""
        producto = crear_producto(
            "2", 
            "Camiseta", 
            29.99, 
            "ropa",
            50
        )
        
        assert producto["id"] == 2
        assert producto["stock"] == 50
        assert producto["disponible"] is True
    
    def test_crear_producto_precio_int(self) -> None:
        """Test para crear producto con precio entero."""
        producto = crear_producto(3, "Libro", 150, "libros")
        
        assert producto["precio"] == 150.0  # Debe convertir a float
    
    def test_tipos_categoria_validos(self) -> None:
        """Test para verificar categorías válidas."""
        categorias_validas: list[CategoriaProducto] = [
            "electrónica", "ropa", "alimentos", "libros"
        ]
        
        for categoria in categorias_validas:
            producto = crear_producto(1, "Test", 10.0, categoria)
            assert producto["categoria"] == categoria


class TestTipos:
    """Tests para verificar los tipos definidos."""
    
    def test_tipo_id(self) -> None:
        """Test para el tipo ID (Union[int, str])."""
        ids_validos: list[ID] = [1, "123", 456, "789"]
        
        for id_val in ids_validos:
            usuario = crear_usuario(id_val, "Test", "test@example.com")
            assert isinstance(usuario["id"], int)
    
    def test_tipo_precio(self) -> None:
        """Test para el tipo Precio (Union[int, float])."""
        precios_validos: list[Precio] = [100, 99.99, 0, 50.5]
        
        for precio in precios_validos:
            producto = crear_producto(1, "Test", precio, "alimentos")
            assert isinstance(producto["precio"], float)
    
    def test_usuario_typed_dict(self) -> None:
        """Test para verificar TypedDict de Usuario."""
        usuario: Usuario = {
            "id": 1,
            "nombre": "Test",
            "email": "test@example.com",
            "edad": None,
            "activo": True,
            "fecha_registro": datetime.now()
        }
        
        # Verificar que todos los campos requeridos están presentes
        assert "id" in usuario
        assert "nombre" in usuario
        assert "email" in usuario
        assert "edad" in usuario
        assert "activo" in usuario
        assert "fecha_registro" in usuario
    
    def test_producto_typed_dict(self) -> None:
        """Test para verificar TypedDict de Producto."""
        producto: Producto = {
            "id": 1,
            "nombre": "Test",
            "precio": 10.0,
            "categoria": "electrónica",
            "stock": 5,
            "disponible": True
        }
        
        # Verificar que todos los campos requeridos están presentes
        assert "id" in producto
        assert "nombre" in producto
        assert "precio" in producto
        assert "categoria" in producto
        assert "stock" in producto
        assert "disponible" in producto

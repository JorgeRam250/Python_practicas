"""
Tests para los servicios con Protocol y tipos avanzados
"""

import pytest
from unittest.mock import Mock
from src.services import (
    Procesable, Guardable, RepositorioBase, UsuarioRepositorio,
    PedidoServicio, ProcesadorPedidos
)
from src.models import EstadoPedido


class MockProcesable:
    """Clase mock que implementa el protocol Procesable."""
    
    def __init__(self, resultado: str = "procesado") -> None:
        self.resultado = resultado
    
    def procesar(self) -> str:
        return self.resultado


class MockGuardable:
    """Clase mock que implementa el protocol Guardable."""
    
    def __init__(self, exito: bool = True) -> None:
        self.exito = exito
        self.guardado = False
    
    def guardar(self) -> bool:
        self.guardado = True
        return self.exito


class TestProtocolos:
    """Tests para verificar el funcionamiento de Protocol."""
    
    def test_procesable_protocol(self) -> None:
        """Test para protocol Procesable."""
        procesable: Procesable = MockProcesable("test_resultado")
        
        resultado = procesable.procesar()
        assert resultado == "test_resultado"
    
    def test_guardable_protocol(self) -> None:
        """Test para protocol Guardable."""
        guardable: Guardable = MockGuardable(True)
        
        resultado = guardable.guardar()
        assert resultado is True
        assert guardable.guardado is True


class TestUsuarioRepositorio:
    """Tests para UsuarioRepositorio."""
    
    def setup_method(self) -> None:
        """Configuración inicial para cada test."""
        self.repositorio = UsuarioRepositorio()
    
    def test_guardar_usuario_sin_id(self) -> None:
        """Test para guardar usuario sin ID (se asigna automáticamente)."""
        datos = {"nombre": "Juan", "email": "juan@example.com"}
        resultado = self.repositorio.guardar(datos)
        
        assert resultado is True
        assert "id" in datos
        assert datos["id"] == 1
    
    def test_guardar_usuario_con_id(self) -> None:
        """Test para guardar usuario con ID específico."""
        datos = {"id": 999, "nombre": "María", "email": "maria@example.com"}
        resultado = self.repositorio.guardar(datos)
        
        assert resultado is True
        assert self.repositorio.obtener(999) is not None
    
    def test_obtener_usuario_existente(self) -> None:
        """Test para obtener usuario existente."""
        datos = {"nombre": "Test", "email": "test@example.com"}
        self.repositorio.guardar(datos)
        
        usuario = self.repositorio.obtener(1)
        assert usuario is not None
        assert usuario["nombre"] == "Test"
    
    def test_obtener_usuario_inexistente(self) -> None:
        """Test para obtener usuario inexistente."""
        usuario = self.repositorio.obtener(999)
        assert usuario is None
    
    def test_obtener_usuario_con_string_id(self) -> None:
        """Test para obtener usuario con ID como string."""
        datos = {"nombre": "Test", "email": "test@example.com"}
        self.repositorio.guardar(datos)
        
        usuario = self.repositorio.obtener("1")
        assert usuario is not None
        assert usuario["id"] == 1
    
    def test_listar_vacio(self) -> None:
        """Test para listar cuando no hay usuarios."""
        usuarios = self.repositorio.listar()
        assert usuarios == []
    
    def test_listar_con_datos(self) -> None:
        """Test para listar con usuarios existentes."""
        self.repositorio.guardar({"nombre": "User1", "email": "user1@example.com"})
        self.repositorio.guardar({"nombre": "User2", "email": "user2@example.com"})
        
        usuarios = self.repositorio.listar()
        assert len(usuarios) == 2
    
    def test_eliminar_usuario_existente(self) -> None:
        """Test para eliminar usuario existente."""
        datos = {"nombre": "Test", "email": "test@example.com"}
        self.repositorio.guardar(datos)
        
        resultado = self.repositorio.eliminar(1)
        assert resultado is True
        assert self.repositorio.obtener(1) is None
    
    def test_eliminar_usuario_inexistente(self) -> None:
        """Test para eliminar usuario inexistente."""
        resultado = self.repositorio.eliminar(999)
        assert resultado is False


class TestPedidoServicio:
    """Tests para PedidoServicio."""
    
    def setup_method(self) -> None:
        """Configuración inicial para cada test."""
        self.mock_repositorio = Mock(spec=RepositorioBase)
        self.servicio = PedidoServicio(self.mock_repositorio)
    
    def test_crear_pedido_basico(self) -> None:
        """Test para crear pedido básico."""
        self.mock_repositorio.listar.return_value = []
        self.mock_repositorio.guardar.return_value = True
        
        productos = [{"id": 1, "cantidad": 2, "precio": 10.0}]
        pedido = self.servicio.crear_pedido(1, productos, 20.0)
        
        assert pedido["usuario_id"] == 1
        assert pedido["productos"] == productos
        assert pedido["total"] == 20.0
        assert pedido["estado"] == "pendiente"
        self.mock_repositorio.guardar.assert_called_once()
    
    def test_crear_pedido_con_string_id(self) -> None:
        """Test para crear pedido con ID como string."""
        self.mock_repositorio.listar.return_value = []
        self.mock_repositorio.guardar.return_value = True
        
        productos = [{"id": 1, "cantidad": 1}]
        pedido = self.servicio.crear_pedido("123", productos, 10.0)
        
        assert pedido["usuario_id"] == 123  # Debe convertir a int
    
    def test_actualizar_estado_pedido(self) -> None:
        """Test para actualizar estado de pedido."""
        pedido_existente = {
            "id": 1,
            "usuario_id": 1,
            "productos": [],
            "total": 10.0,
            "estado": "pendiente",
            "fecha_pedido": "2024-01-01"
        }
        
        self.mock_repositorio.obtener.return_value = pedido_existente
        self.mock_repositorio.guardar.return_value = True
        
        resultado = self.servicio.actualizar_estado(1, "procesando")
        
        assert resultado is True
        assert pedido_existente["estado"] == "procesando"
        self.mock_repositorio.guardar.assert_called_once()
    
    def test_actualizar_estado_pedido_inexistente(self) -> None:
        """Test para actualizar estado de pedido inexistente."""
        self.mock_repositorio.obtener.return_value = None
        
        resultado = self.servicio.actualizar_estado(999, "entregado")
        
        assert resultado is False
        self.mock_repositorio.guardar.assert_not_called()
    
    def test_pedidos_por_estado(self) -> None:
        """Test para filtrar pedidos por estado."""
        pedidos = [
            {"id": 1, "estado": "pendiente"},
            {"id": 2, "estado": "procesando"},
            {"id": 3, "estado": "pendiente"},
            {"id": 4, "estado": "entregado"}
        ]
        
        self.mock_repositorio.listar.return_value = pedidos
        
        pendientes = self.servicio.pedidos_por_estado("pendiente")
        
        assert len(pendientes) == 2
        assert all(p["estado"] == "pendiente" for p in pendientes)


class TestProcesadorPedidos:
    """Tests para ProcesadorPedidos."""
    
    def setup_method(self) -> None:
        """Configuración inicial para cada test."""
        self.mock_servicio = Mock(spec=PedidoServicio)
        self.procesador = ProcesadorPedidos(self.mock_servicio)
    
    def test_procesar_pedidos_pendientes(self) -> None:
        """Test para procesar pedidos pendientes."""
        pedidos_pendientes = [
            {"id": 1, "estado": "pendiente"},
            {"id": 2, "estado": "pendiente"}
        ]
        
        self.mock_servicio.pedidos_por_estado.return_value = pedidos_pendientes
        self.mock_servicio.actualizar_estado.return_value = True
        
        resultado = self.procesador.procesar()
        
        assert "Se procesaron 2 pedidos pendientes" in resultado
        assert self.mock_servicio.actualizar_estado.call_count == 2
    
    def test_procesar_sin_pedidos_pendientes(self) -> None:
        """Test para procesar cuando no hay pedidos pendientes."""
        self.mock_servicio.pedidos_por_estado.return_value = []
        
        resultado = self.procesador.procesar()
        
        assert "Se procesaron 0 pedidos pendientes" in resultado
        self.mock_servicio.actualizar_estado.assert_not_called()

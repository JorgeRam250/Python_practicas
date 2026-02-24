"""
Servicios con Protocol y tipos avanzados
"""

from typing import Protocol, List, Dict, Any, Union, Optional
from abc import ABC, abstractmethod
from .models import Usuario, Producto, Pedido, EstadoPedido


class Procesable(Protocol):
    """Protocol para objetos que pueden ser procesados."""
    
    def procesar(self) -> str:
        """Procesa el objeto y retorna un resultado."""
        ...


class Guardable(Protocol):
    """Protocol para objetos que pueden ser guardados."""
    
    def guardar(self) -> bool:
        """Guarda el objeto y retorna si fue exitoso."""
        ...


class RepositorioBase(ABC):
    """Clase base abstracta para repositorios."""
    
    @abstractmethod
    def guardar(self, datos: Dict[str, Any]) -> bool:
        """Guarda datos en el repositorio."""
        pass
    
    @abstractmethod
    def obtener(self, id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Obtiene datos por ID."""
        pass
    
    @abstractmethod
    def listar(self) -> List[Dict[str, Any]]:
        """Lista todos los datos."""
        pass


class UsuarioRepositorio(RepositorioBase):
    """Repositorio para gestionar usuarios."""
    
    def __init__(self) -> None:
        self._datos: Dict[int, Dict[str, Any]] = {}
        self._siguiente_id: int = 1
    
    def guardar(self, datos: Dict[str, Any]) -> bool:
        """Guarda un usuario en el repositorio."""
        try:
            if "id" not in datos:
                datos["id"] = self._siguiente_id
                self._siguiente_id += 1
            
            self._datos[datos["id"]] = datos.copy()
            return True
        except Exception:
            return False
    
    def obtener(self, id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Obtiene un usuario por ID."""
        return self._datos.get(int(id))
    
    def listar(self) -> List[Dict[str, Any]]:
        """Lista todos los usuarios."""
        return list(self._datos.values())
    
    def eliminar(self, id: Union[int, str]) -> bool:
        """Elimina un usuario por ID."""
        return self._datos.pop(int(id), None) is not None


class PedidoServicio:
    """Servicio para gestionar pedidos con type hints avanzados."""
    
    def __init__(self, repositorio: RepositorioBase) -> None:
        self.repositorio = repositorio
    
    def crear_pedido(
        self,
        usuario_id: Union[int, str],
        productos: List[Dict[str, Union[int, float]]],
        total: float
    ) -> Dict[str, Any]:
        """
        Crea un nuevo pedido con validación de tipos.
        
        Args:
            usuario_id: ID del usuario que realiza el pedido
            productos: Lista de productos con id y cantidad
            total: Total del pedido
            
        Returns:
            Dict: Pedido creado con estado inicial 'pendiente'
        """
        pedido: Dict[str, Any] = {
            "id": len(self.repositorio.listar()) + 1,
            "usuario_id": int(usuario_id),
            "productos": productos,
            "total": float(total),
            "estado": "pendiente",
            "fecha_pedido": "2024-01-01"  # Simplificado para el ejemplo
        }
        
        self.repositorio.guardar(pedido)
        return pedido
    
    def actualizar_estado(
        self, 
        pedido_id: Union[int, str], 
        nuevo_estado: EstadoPedido
    ) -> bool:
        """
        Actualiza el estado de un pedido.
        
        Args:
            pedido_id: ID del pedido a actualizar
            nuevo_estado: Nuevo estado (valores predefinidos)
            
        Returns:
            bool: True si se actualizó correctamente
        """
        pedido = self.repositorio.obtener(pedido_id)
        if pedido:
            pedido["estado"] = nuevo_estado
            return self.repositorio.guardar(pedido)
        return False
    
    def pedidos_por_estado(self, estado: EstadoPedido) -> List[Dict[str, Any]]:
        """
        Filtra pedidos por estado.
        
        Args:
            estado: Estado a filtrar
            
        Returns:
            List[Dict]: Lista de pedidos con el estado especificado
        """
        return [
            pedido for pedido in self.repositorio.listar()
            if pedido.get("estado") == estado
        ]


class ProcesadorPedidos:
    """Clase que implementa el protocol Procesable."""
    
    def __init__(self, pedido_servicio: PedidoServicio) -> None:
        self.pedido_servicio = pedido_servicio
    
    def procesar(self) -> str:
        """Procesa todos los pedidos pendientes."""
        pendientes = self.pedido_servicio.pedidos_por_estado("pendiente")
        
        for pedido in pendientes:
            self.pedido_servicio.actualizar_estado(pedido["id"], "procesando")
        
        return f"Se procesaron {len(pendientes)} pedidos pendientes"

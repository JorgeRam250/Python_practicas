#!/usr/bin/env python3
"""
Ejemplo 2: Protocol y Tipos Avanzados
Conceptos: Protocol, TypedDict complejos, repositorios
"""

from typing import Dict, Any, List
from src.services import (
    UsuarioRepositorio, PedidoServicio, ProcesadorPedidos,
    Procesable, Guardable
)
from src.models import EstadoPedido


class ProcesadorPersonalizado:
    """Clase que implementa el protocol Procesable."""
    
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.procesados = 0
    
    def procesar(self) -> str:
        """Implementación del método procesar."""
        self.procesados += 1
        return f"{self.nombre} ha procesado {self.procesados} elementos"


class LoggerSimple:
    """Clase que implementa el protocol Guardable."""
    
    def __init__(self) -> None:
        self.logs: List[str] = []
    
    def guardar(self) -> bool:
        """Implementación del método guardar."""
        self.logs.append(f"Log guardado: {len(self.logs) + 1}")
        return True


def main() -> None:
    """Función principal que demuestra tipos avanzados."""
    
    print("🎯 Ejemplo 2: Protocol y Tipos Avanzados")
    print("=" * 50)
    
    # 1. Demostrar Protocol con clases personalizadas
    print("\n🔧 Demostración de Protocol:")
    
    # Usar las clases como si fueran del mismo tipo
    procesador1 = ProcesadorPersonalizado("Procesador A")
    procesador2 = ProcesadorPersonalizado("Procesador B")
    
    logger = LoggerSimple()
    
    # Función que acepta cualquier objeto que implemente Procesable
    def ejecutar_procesamiento(procesable: Procesable) -> str:
        return procesable.procesar()
    
    # Función que acepta cualquier objeto que implemente Guardable
    def guardar_datos(guardable: Guardable) -> bool:
        return guardable.guardar()
    
    print(f"  {ejecutar_procesamiento(procesador1)}")
    print(f"  {ejecutar_procesamiento(procesador2)}")
    print(f"  {ejecutar_procesamiento(procesador1)}")
    
    print(f"  Guardado exitoso: {guardar_datos(logger)}")
    print(f"  Logs registrados: {len(logger.logs)}")
    
    # 2. Demostrar repositorio y servicios
    print("\n🗄️ Demostración de Repositorio:")
    
    # Crear repositorio de usuarios
    repo_usuarios = UsuarioRepositorio()
    
    # Guardar usuarios
    usuarios_data = [
        {"nombre": "Juan Pérez", "email": "juan@example.com", "edad": 30},
        {"nombre": "María García", "email": "maria@example.com", "edad": 25},
        {"nombre": "Pedro López", "email": "pedro@example.com"}  # Sin edad
    ]
    
    usuarios_guardados = []
    for usuario_data in usuarios_data:
        if repo_usuarios.guardar(usuario_data):
            usuarios_guardados.append(usuario_data)
            print(f"  ✅ Usuario guardado: {usuario_data['nombre']}")
    
    # Listar todos los usuarios
    print(f"\n  📋 Total usuarios guardados: {len(repo_usuarios.listar())}")
    
    # 3. Demostrar servicio de pedidos
    print("\n🛒 Demostración de Servicio de Pedidos:")
    
    # Crear repositorio para pedidos (usamos el mismo de usuarios para simplificar)
    repo_pedidos = UsuarioRepositorio()
    servicio_pedidos = PedidoServicio(repo_pedidos)
    
    # Crear pedidos
    pedidos_data = [
        (1, [{"id": 1, "cantidad": 2, "precio": 50.0}], 100.0),
        (2, [{"id": 2, "cantidad": 1, "precio": 75.5}], 75.5),
        (1, [{"id": 3, "cantidad": 3, "precio": 25.0}], 75.0)
    ]
    
    for usuario_id, productos, total in pedidos_data:
        pedido = servicio_pedidos.crear_pedido(usuario_id, productos, total)
        print(f"  📦 Pedido {pedido['id']} creado para usuario {pedido['usuario_id']}")
    
    # 4. Demostrar actualización de estados
    print("\n🔄 Actualización de Estados:")
    
    # Obtener pedidos pendientes
    pendientes = servicio_pedidos.pedidos_por_estado("pendiente")
    print(f"  📋 Pedidos pendientes: {len(pendientes)}")
    
    # Actualizar algunos pedidos
    if pendientes:
        # Actualizar primer pedido a procesando
        primer_pedido = pendientes[0]
        servicio_pedidos.actualizar_estado(primer_pedido["id"], "procesando")
        print(f"  ⚡ Pedido {primer_pedido['id']} actualizado a 'procesando'")
        
        # Actualizar segundo pedido a enviado
        if len(pendientes) > 1:
            segundo_pedido = pendientes[1]
            servicio_pedidos.actualizar_estado(segundo_pedido["id"], "enviado")
            print(f"  📤 Pedido {segundo_pedido['id']} actualizado a 'enviado'")
    
    # 5. Demostrar ProcesadorPedidos
    print("\n🤖 Demostración de ProcesadorPedidos:")
    
    procesador = ProcesadorPedidos(servicio_pedidos)
    resultado = procesador.procesar()
    print(f"  🔄 {resultado}")
    
    # Mostrar resumen final de estados
    print("\n📊 Resumen Final de Estados:")
    estados: List[EstadoPedido] = ["pendiente", "procesando", "enviado", "entregado", "cancelado"]
    
    for estado in estados:
        cantidad = len(servicio_pedidos.pedidos_por_estado(estado))
        if cantidad > 0:
            print(f"  {estado}: {cantidad} pedidos")
    
    print("\n✅ Ejemplo 2 completado exitosamente!")


if __name__ == "__main__":
    main()

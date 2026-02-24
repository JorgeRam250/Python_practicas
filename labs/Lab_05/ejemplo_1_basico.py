#!/usr/bin/env python3
"""
Ejemplo 1: Type Hints Básicos y Validación
Conceptos: Union, Optional, TypedDict básicos
"""

from typing import Union, Optional, Dict, Any
from src.models import crear_usuario, crear_producto, validar_email


def main() -> None:
    """Función principal que demuestra type hints básicos."""
    
    print("🎯 Ejemplo 1: Type Hints Básicos y Validación")
    print("=" * 50)
    
    # 1. Crear usuarios con diferentes tipos de ID
    print("\n📝 Creando usuarios:")
    
    usuario1 = crear_usuario(1, "Ana García", "ana@example.com", 28)
    print(f"Usuario 1: {usuario1['nombre']} (ID: {usuario1['id']})")
    
    usuario2 = crear_usuario("456", "Carlos López", "carlos@empresa.org")
    print(f"Usuario 2: {usuario2['nombre']} (ID: {usuario2['id']})")
    
    # 2. Validar emails
    print("\n✅ Validación de emails:")
    emails_para_validar = [
        "usuario@dominio.com",
        "invalido@",
        "test.email@sub.domain.org",
        "sin-arroba.com"
    ]
    
    for email in emails_para_validar:
        es_valido = validar_email(email)
        print(f"  {email}: {'✅ Válido' if es_valido else '❌ Inválido'}")
    
    # 3. Crear productos con diferentes categorías
    print("\n📦 Creando productos:")
    
    productos_data = [
        (101, "Laptop Gamer", 1200.50, "electrónica", 15),
        (102, "Camiseta Algodón", 25, "ropa", 100),
        (103, "Libro Python", 45.99, "libros", 30),
        (104, "Manzanas", 3.50, "alimentos", 200)
    ]
    
    for id_prod, nombre, precio, categoria, stock in productos_data:
        producto = crear_producto(id_prod, nombre, precio, categoria, stock)
        disponible = "✅ Disponible" if producto["disponible"] else "❌ Agotado"
        print(f"  {producto['nombre']}: ${producto['precio']:.2f} - {disponible}")
    
    # 4. Demostrar Union types
    print("\n🔄 Demostración de Union types:")
    
    def procesar_id(id_mixto: Union[int, str]) -> str:
        """Función que acepta tanto int como str."""
        return f"ID procesado: {int(id_mixto):06d}"
    
    ids_mixtos = [1, "42", 999, "7"]
    for id_val in ids_mixtos:
        print(f"  {id_val} -> {procesar_id(id_val)}")
    
    # 5. Demostrar Optional
    print("\n❓ Demostración de Optional:")
    
    def mostrar_edad(usuario: Dict[str, Any]) -> str:
        """Función que maneja edad opcional."""
        edad = usuario.get("edad")
        if edad is not None:
            return f"{usuario['nombre']} tiene {edad} años"
        else:
            return f"{usuario['nombre']} no especificó su edad"
    
    print(f"  {mostrar_edad(usuario1)}")
    print(f"  {mostrar_edad(usuario2)}")
    
    print("\n✅ Ejemplo 1 completado exitosamente!")


if __name__ == "__main__":
    main()

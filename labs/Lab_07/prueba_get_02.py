#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EJEMPLO 1: Cliente HTTP Optimizado con httpx
============================================
"""

import httpx
from typing import Any, Dict, Optional

# Es una buena práctica extraer las URLs a constantes o variables de configuración
BASE_URL = "https://jsonplaceholder.typicode.com"

def obtener_usuario(client: httpx.Client, user_id: int) -> Optional[Dict[str, Any]]:
    """
    Realiza una petición GET para obtener los datos de un usuario específico.
    Utiliza una sesión de cliente inyectada para reutilizar conexiones.
    """
    url = f"{BASE_URL}/users/{user_id}"
    
    try:
        # Siempre se debe definir un timeout explícito en peticiones de red
        response = client.get(url, timeout=5.0)
        
        # raise_for_status() lanza una excepción automáticamente si el status es 4xx o 5xx
        response.raise_for_status()
        
        return response.json()
        
    except httpx.HTTPStatusError as e:
        print(f"❌ Error HTTP: El servidor devolvió {e.response.status_code} para la URL {e.request.url}")
    except httpx.RequestError as e:
        print(f"❌ Error de red o conexión al solicitar {e.request.url}: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        
    return None

def ejemplo_get_sencillo() -> None:
    print("🔍 Ejemplo 1.1: Petición GET optimizada")
    print("-" * 40)
    
    # El Context Manager (with) asegura que el pool de conexiones se cierre correctamente
    with httpx.Client() as client:
        usuario = obtener_usuario(client, 1)
        
        if usuario:
            print("✅ Petición exitosa!")
            print(f"Status Code: 200 OK") # Si llegamos aquí, sabemos que fue exitosa
            
            print(f"\n👤 Usuario encontrado:")
            # Uso de .get() para evitar KeyErrors si la estructura del JSON cambia
            print(f"  Nombre: {usuario.get('name', 'No disponible')}")
            print(f"  Email: {usuario.get('email', 'No disponible')}")
            
            # Acceso seguro a diccionarios anidados
            direccion = usuario.get('address', {})
            print(f"  Ciudad: {direccion.get('city', 'No disponible')}")

def main() -> None:
    print("🐍 Laboratorio HTTP con httpx - Optimizado")
    print("=" * 60)
    ejemplo_get_sencillo()
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
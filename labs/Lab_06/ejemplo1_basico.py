#!/usr/bin/env python3
"""
EJEMPLO 1: Ingesta básica de CSV
Este es el ejemplo más simple para principiantes
"""

import csv
from pathlib import Path

def leer_csv_simple():
    """
    Función que lee un archivo CSV y lo muestra en pantalla
    """
    print("Ejemplo 1: Lectura basica de CSV")
    print("=" * 40)
    
    # Usamos pathlib para manejar la ruta de forma segura
    ruta_archivo = Path("datos_ejemplo.csv")
    
    # Verificamos que el archivo exista
    if not ruta_archivo.exists():
        print(f"Error: No existe el archivo {ruta_archivo}")
        return
    
    try:
        # Abrimos el archivo y lo leemos
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            lector_csv = csv.reader(archivo)
            
            # Leemos la primera fila (encabezados)
            encabezados = next(lector_csv)
            print("Encabezados:", encabezados)
            print()
            
            # Leemos el resto de los datos
            print("Datos:")
            contador = 1
            for fila in lector_csv:
                print(f"  Fila {contador}: {fila}")
                contador += 1
                
        print(f"\nSe leyeron {contador-1} registros correctamente")
        
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

if __name__ == "__main__":
    leer_csv_simple()

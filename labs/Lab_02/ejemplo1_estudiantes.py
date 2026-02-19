#!/usr/bin/env python3
"""
Ejemplo 1: Procesamiento de datos de estudiantes
Lee un JSON con información de estudiantes, filtra por aprobados y calcula estadísticas
"""

import json
import sys
from typing import Dict, List, Any

def leer_archivo_json(ruta_archivo: str) -> Dict[str, Any]:
    """
    Lee un archivo JSON y maneja errores de archivo y formato
    
    Args:
        ruta_archivo: Ruta del archivo JSON a leer
        
    Returns:
        Dict con los datos del JSON
        
    Raises:
        FileNotFoundError: Si el archivo no existe
        json.JSONDecodeError: Si el formato JSON es inválido
        PermissionError: Si no hay permisos para leer el archivo
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            print(f"[OK] Archivo '{ruta_archivo}' leído correctamente")
            return datos
    except FileNotFoundError:
        print(f"[ERROR] Error: El archivo '{ruta_archivo}' no existe")
        raise
    except json.JSONDecodeError as e:
        print(f"[ERROR] Error: Formato JSON inválido en '{ruta_archivo}': {e}")
        raise
    except PermissionError:
        print(f"[ERROR] Error: No tienes permisos para leer '{ruta_archivo}'")
        raise
    except Exception as e:
        print(f"[ERROR] Error inesperado al leer '{ruta_archivo}': {e}")
        raise

def filtrar_estudiantes_aprobados(estudiantes: List[Dict]) -> List[Dict]:
    """
    Filtra estudiantes con calificación >= 70
    
    Args:
        estudiantes: Lista de diccionarios con datos de estudiantes
        
    Returns:
        Lista de estudiantes aprobados
    """
    aprobados = []
    for estudiante in estudiantes:
        try:
            calificacion = estudiante.get('calificacion', 0)
            if calificacion >= 70:
                aprobados.append(estudiante)
        except (TypeError, AttributeError):
            print(f"[ADVERTENCIA] Estudiante con formato inválido: {estudiante}")
            continue
    
    print(f"[INFO] Estudiantes aprobados: {len(aprobados)}/{len(estudiantes)}")
    return aprobados

def calcular_estadisticas(estudiantes: List[Dict]) -> Dict[str, float]:
    """
    Calcula estadísticas básicas de calificaciones
    
    Args:
        estudiantes: Lista de estudiantes
        
    Returns:
        Diccionario con estadísticas
    """
    if not estudiantes:
        return {"promedio": 0, "maximo": 0, "minimo": 0}
    
    calificaciones = []
    for estudiante in estudiantes:
        calif = estudiante.get('calificacion', 0)
        if isinstance(calif, (int, float)):
            calificaciones.append(calif)
    
    if not calificaciones:
        return {"promedio": 0, "maximo": 0, "minimo": 0}
    
    estadisticas = {
        "promedio": sum(calificaciones) / len(calificaciones),
        "maximo": max(calificaciones),
        "minimo": min(calificaciones),
        "total_estudiantes": len(calificaciones)
    }
    
    return estadisticas

def procesar_datos_estudiantes(ruta_archivo: str) -> None:
    """
    Función principal que procesa los datos de estudiantes
    
    Args:
        ruta_archivo: Ruta del archivo JSON con datos de estudiantes
    """
    try:
        # Leer archivo JSON
        datos = leer_archivo_json(ruta_archivo)
        
        # Validar estructura
        if 'estudiantes' not in datos:
            print(f"[ERROR] Error: El JSON debe contener la clave 'estudiantes'")
            return
        
        estudiantes = datos['estudiantes']
        if not isinstance(estudiantes, list):
            print(f"[ERROR] Error: 'estudiantes' debe ser una lista")
            return
        
        print(f"[INFO] Total de estudiantes: {len(estudiantes)}")
        
        # Filtrar aprobados
        aprobados = filtrar_estudiantes_aprobados(estudiantes)
        
        # Calcular estadísticas generales
        stats_generales = calcular_estadisticas(estudiantes)
        print(f"\n[INFO] Estadísticas generales:")
        print(f"   Promedio: {stats_generales['promedio']:.2f}")
        print(f"   Máximo: {stats_generales['maximo']}")
        print(f"   Mínimo: {stats_generales['minimo']}")
        
        # Calcular estadísticas de aprobados
        stats_aprobados = calcular_estadisticas(aprobados)
        print(f"\n[INFO] Estadísticas de aprobados:")
        print(f"   Promedio: {stats_aprobados['promedio']:.2f}")
        print(f"   Máximo: {stats_aprobados['maximo']}")
        print(f"   Mínimo: {stats_aprobados['minimo']}")
        
        # Mostrar lista de aprobados
        print(f"\n[OK] Lista de estudiantes aprobados:")
        for i, estudiante in enumerate(aprobados, 1):
            nombre = estudiante.get('nombre', 'N/A')
            calificacion = estudiante.get('calificacion', 0)
            print(f"   {i}. {nombre}: {calificacion}")
            
    except Exception as e:
        print(f"[ERROR] Error fatal en el procesamiento: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Uso del script
    if len(sys.argv) != 2:
        print("Uso: python ejemplo1_estudiantes.py <archivo_json>")
        print("Ejemplo: python ejemplo1_estudiantes.py estudiantes.json")
        sys.exit(1)
    
    ruta_archivo = sys.argv[1]
    procesar_datos_estudiantes(ruta_archivo)

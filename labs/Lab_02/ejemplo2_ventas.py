#!/usr/bin/env python3
"""
Ejemplo 2: Análisis de datos de ventas
Lee un JSON con datos de ventas, filtra por categorías y genera reportes
Usa pattern matching y expresiones regulares
"""

import json
import sys
import re
from typing import Dict, List, Any, Union
from datetime import datetime

def leer_y_validar_json(ruta_archivo: str) -> Dict[str, Any]:
    """
    Lee y valida un archivo JSON con manejo robusto de errores
    
    Args:
        ruta_archivo: Ruta del archivo JSON
        
    Returns:
        Diccionario con los datos validados
        
    Raises:
        FileNotFoundError: Si el archivo no existe
        json.JSONDecodeError: Si el JSON es inválido
        ValueError: Si la estructura no es válida
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            
        # Validar estructura básica
        if not isinstance(datos, dict):
            raise ValueError("El JSON debe ser un objeto/diccionario")
            
        if 'ventas' not in datos:
            print(f"[ERROR] Error: El JSON debe contener la clave 'ventas'")
            
        if not isinstance(datos['ventas'], list):
            print(f"[ERROR] Error: 'ventas' debe ser una lista")
            
        print(f"[OK] Archivo validado: {len(datos['ventas'])} registros de ventas")
        return datos
        
    except FileNotFoundError:
        print(f"[ERROR] Error: Archivo no encontrado '{ruta_archivo}'")
        raise
    except json.JSONDecodeError as e:
        print(f"[ERROR] Error: JSON inválido - {e}")
        raise
    except ValueError as e:
        print(f"[ERROR] Error de validación: {e}")
        raise
    except Exception as e:
        print(f"[ERROR] Error inesperado: {e}")
        raise

def validar_fecha(fecha_str: str) -> bool:
    """
    Valida formato de fecha usando expresiones regulares
    
    Args:
        fecha_str: String de fecha
        
    Returns:
        True si el formato es válido
    """
    patron = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(patron, fecha_str))

def procesar_venta(venta: Dict) -> Dict[str, Any]:
    """
    Procesa una venta individual usando pattern matching
    
    Args:
        venta: Diccionario con datos de venta
        
    Returns:
        Diccionario procesado o None si hay error
    """
    try:
        # Validar estructura básica primero
        if not isinstance(venta, dict):
            return None
            
        id_venta = venta.get("id")
        producto = venta.get("producto")
        categoria = venta.get("categoria")
        cantidad = venta.get("cantidad")
        precio = venta.get("precio")
        fecha = venta.get("fecha")
        
        # Validar tipos y valores
        if not all(isinstance(x, (int, float, str)) for x in [id_venta, producto, categoria, cantidad, precio, fecha]):
            return None
            
        if not isinstance(id_venta, int) or not isinstance(producto, str) or not isinstance(categoria, str):
            return None
            
        if not isinstance(cantidad, int) or cantidad <= 0:
            return None
            
        if not isinstance(precio, (int, float)) or precio <= 0:
            return None
            
        if not isinstance(fecha, str) or not validar_fecha(fecha):
            return None
        
        # Calcular total
        total = cantidad * precio
        
        # Determinar rango de precio usando if-elif-else (compatible con Python 3.8+)
        if precio < 50:
            rango_precio = "bajo"
        elif 50 <= precio < 200:
            rango_precio = "medio"
        elif precio >= 200:
            rango_precio = "alto"
        else:
            rango_precio = "desconocido"
        
        return {
            "id": id_venta,
            "producto": producto,
            "categoria": categoria,
            "cantidad": cantidad,
            "precio": precio,
            "total": total,
            "fecha": fecha,
            "rango_precio": rango_precio
        }
                
    except Exception as e:
        print(f"[ADVERTENCIA] Error procesando venta {venta.get('id', 'desconocido')}: {e}")
        return None

def filtrar_por_categoria(ventas: List[Dict], categoria: str) -> List[Dict]:
    """
    Filtra ventas por categoría específica
    
    Args:
        ventas: Lista de ventas procesadas
        categoria: Categoría a filtrar
        
    Returns:
        Lista filtrada
    """
    filtradas = [venta for venta in ventas if venta.get('categoria') == categoria]
    print(f"[INFO] Ventas en categoría '{categoria}': {len(filtradas)}")
    return filtradas

def generar_reporte(ventas: List[Dict]) -> Dict[str, Any]:
    """
    Genera reporte agregado de ventas
    
    Args:
        ventas: Lista de ventas procesadas
        
    Returns:
        Diccionario con reporte
    """
    if not ventas:
        return {"error": "No hay ventas válidas para procesar"}
    
    # Totales por categoría
    totales_categoria = {}
    for venta in ventas:
        categoria = venta.get('categoria', 'sin_categoria')
        total = venta.get('total', 0)
        totales_categoria[categoria] = totales_categoria.get(categoria, 0) + total
    
    # Totales por rango de precio
    totales_rango = {}
    for venta in ventas:
        rango = venta.get('rango_precio', 'desconocido')
        total = venta.get('total', 0)
        totales_rango[rango] = totales_rango.get(rango, 0) + total
    
    # Estadísticas generales
    total_general = sum(v.get('total', 0) for v in ventas)
    total_unidades = sum(v.get('cantidad', 0) for v in ventas)
    venta_promedio = total_general / len(ventas) if ventas else 0
    
    # Producto más vendido
    productos = {}
    for venta in ventas:
        producto = venta.get('producto', 'desconocido')
        cantidad = venta.get('cantidad', 0)
        productos[producto] = productos.get(producto, 0) + cantidad
    
    producto_top = max(productos.items(), key=lambda x: x[1]) if productos else ("N/A", 0)
    
    reporte = {
        "resumen": {
            "total_ventas": len(ventas),
            "total_ingresos": total_general,
            "total_unidades": total_unidades,
            "venta_promedio": venta_promedio,
            "producto_mas_vendido": {
                "nombre": producto_top[0],
                "unidades": producto_top[1]
            }
        },
        "por_categoria": totales_categoria,
        "por_rango_precio": totales_rango,
        "top_productos": dict(sorted(productos.items(), key=lambda x: x[1], reverse=True)[:5])
    }
    
    return reporte

def guardar_reporte_json(reporte: Dict, nombre_archivo: str = "reporte_ventas.json") -> None:
    """
    Guarda el reporte en un archivo JSON
    
    Args:
        reporte: Diccionario con el reporte
        nombre_archivo: Nombre del archivo de salida
    """
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(reporte, archivo, indent=2, ensure_ascii=False)
        print(f"[OK] Reporte guardado en '{nombre_archivo}'")
    except Exception as e:
        print(f"[ERROR] Error guardando reporte: {e}")

def main():
    """
    Función principal del programa
    """
    # Verificar argumentos
    if len(sys.argv) < 2:
        print("Uso: python ejemplo2_ventas.py <archivo_json> [categoria]")
        print("Ejemplo: python ejemplo2_ventas.py ventas.json Electrónicos")
        sys.exit(1)
    
    ruta_archivo = sys.argv[1]
    categoria_filtro = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        # Leer y validar datos
        datos = leer_y_validar_json(ruta_archivo)
        
        # Procesar ventas
        print("\nProcesando ventas...")
        ventas_procesadas = []
        for venta in datos['ventas']:
            venta_procesada = procesar_venta(venta)
            if venta_procesada:
                ventas_procesadas.append(venta_procesada)
        
        print(f"[INFO] Ventas procesadas: {len(ventas_procesadas)}/{len(datos['ventas'])}")
        
        # Filtrar por categoría si se especificó
        if categoria_filtro:
            print(f"[INFO] Filtrando por categoría: {categoria_filtro}")
            ventas_filtradas = filtrar_por_categoria(ventas_procesadas, categoria_filtro)
            ventas_analizar = ventas_filtradas
        else:
            ventas_analizar = ventas_procesadas
        
        # Generar reporte
        print("[INFO] Generando reporte...")
        print("\n[INFO] Generando reporte...")
        reporte = generar_reporte(ventas_analizar)
        
        # Mostrar resumen
        resumen = reporte.get('resumen', {})
        print(f"\n[INFO] RESUMEN DE VENTAS:")
        print(f"   Total ventas: {resumen.get('total_ventas', 0)}")
        print(f"   Total ingresos: ${resumen.get('total_ingresos', 0):.2f}")
        print(f"   Total unidades: {resumen.get('total_unidades', 0)}")
        print(f"   Venta promedio: ${resumen.get('venta_promedio', 0):.2f}")
        
        producto_top = resumen.get('producto_mas_vendido', {})
        print(f"   Producto más vendido: {producto_top.get('nombre', 'N/A')} ({producto_top.get('unidades', 0)} unidades)")
        
        # Guardar reporte
        nombre_salida = f"reporte_{'filtrado_' + categoria_filtro if categoria_filtro else 'general'}.json"
        guardar_reporte_json(reporte, nombre_salida)
        
        print(f"\n[EXITO] Proceso completado exitosamente!")
        
    except Exception as e:
        print(f"\n[ERROR] Error fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

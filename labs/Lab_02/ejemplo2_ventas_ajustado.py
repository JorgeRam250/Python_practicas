#!/usr/bin/env python3
"""
Ejemplo 2: Sistema de Ventas
Lee un JSON con datos de ventas, filtra por categorías y genera reportes
Usa expresiones regulares para validar fechas.

Ajustes solicitados:
- Salida en consola con formato de "probando ejemplo" (general / filtrado)
- Mensajes [OK]/[INFO]/[EXITO] consistentes con el ejemplo del usuario
- Validación que realmente detiene el proceso si falta 'ventas' o si no es lista
"""

from __future__ import annotations

import json
import sys
import re
from typing import Dict, List, Any, Optional


def _print_header(titulo: str) -> None:
    print("=" * 50)
    print(titulo)
    print("=" * 50)


def leer_y_validar_json(ruta_archivo: str) -> Dict[str, Any]:
    """Lee y valida un archivo JSON con manejo robusto de errores."""
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, dict):
            raise ValueError("El JSON debe ser un objeto/diccionario")

        if "ventas" not in datos:
            # Mantengo el prefijo del ejemplo, pero también detengo el flujo (antes no lo hacía).
            print("[ERROR] Error: El JSON debe contener la clave 'ventas'")
            raise ValueError("Falta la clave 'ventas'")

        if not isinstance(datos["ventas"], list):
            print("[ERROR] Error: 'ventas' debe ser una lista")
            raise ValueError("'ventas' no es lista")

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
    """Valida formato YYYY-MM-DD usando regex."""
    patron = r"^\d{4}-\d{2}-\d{2}$"
    return bool(re.match(patron, fecha_str))


def procesar_venta(venta: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Procesa una venta individual; devuelve None si la venta es inválida."""
    try:
        if not isinstance(venta, dict):
            return None

        id_venta = venta.get("id")
        producto = venta.get("producto")
        categoria = venta.get("categoria")
        cantidad = venta.get("cantidad")
        precio = venta.get("precio")
        fecha = venta.get("fecha")

        # Validaciones de tipo / valor (más estrictas para evitar basura silenciosa)
        if not isinstance(id_venta, int):
            return None
        if not isinstance(producto, str) or not producto.strip():
            return None
        if not isinstance(categoria, str) or not categoria.strip():
            return None
        if not isinstance(cantidad, int) or cantidad <= 0:
            return None
        if not isinstance(precio, (int, float)) or float(precio) <= 0:
            return None
        if not isinstance(fecha, str) or not validar_fecha(fecha):
            return None

        total = cantidad * float(precio)

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
            "precio": float(precio),
            "total": total,
            "fecha": fecha,
            "rango_precio": rango_precio,
        }

    except Exception as e:
        # No rompo el proceso completo por una venta mal formada
        print(f"[ADVERTENCIA] Error procesando venta {venta.get('id', 'desconocido')}: {e}")
        return None


def filtrar_por_categoria(ventas: List[Dict[str, Any]], categoria: str) -> List[Dict[str, Any]]:
    filtradas = [v for v in ventas if v.get("categoria") == categoria]
    print(f"[INFO] Ventas en categoría '{categoria}': {len(filtradas)}")
    return filtradas


def generar_reporte(ventas: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not ventas:
        return {"error": "No hay ventas válidas para procesar"}

    totales_categoria: Dict[str, float] = {}
    for v in ventas:
        cat = v.get("categoria", "sin_categoria")
        totales_categoria[cat] = totales_categoria.get(cat, 0.0) + float(v.get("total", 0.0))

    totales_rango: Dict[str, float] = {}
    for v in ventas:
        rango = v.get("rango_precio", "desconocido")
        totales_rango[rango] = totales_rango.get(rango, 0.0) + float(v.get("total", 0.0))

    total_ingresos = sum(float(v.get("total", 0.0)) for v in ventas)
    total_unidades = sum(int(v.get("cantidad", 0)) for v in ventas)
    venta_promedio = total_ingresos / len(ventas) if ventas else 0.0

    productos: Dict[str, int] = {}
    for v in ventas:
        p = v.get("producto", "desconocido")
        productos[p] = productos.get(p, 0) + int(v.get("cantidad", 0))

    producto_top = max(productos.items(), key=lambda x: x[1]) if productos else ("N/A", 0)

    return {
        "resumen": {
            "total_ventas": len(ventas),
            "total_ingresos": total_ingresos,
            "total_unidades": total_unidades,
            "venta_promedio": venta_promedio,
            "producto_mas_vendido": {"nombre": producto_top[0], "unidades": producto_top[1]},
        },
        "por_categoria": totales_categoria,
        "por_rango_precio": totales_rango,
        "top_productos": dict(sorted(productos.items(), key=lambda x: x[1], reverse=True)[:5]),
    }


def guardar_reporte_json(reporte: Dict[str, Any], nombre_archivo: str) -> None:
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            json.dump(reporte, archivo, indent=2, ensure_ascii=False)
        print(f"[OK] Reporte guardado en '{nombre_archivo}'")
    except Exception as e:
        print(f"[ERROR] Error guardando reporte: {e}")
        raise


def _imprimir_resumen(reporte: Dict[str, Any]) -> None:
    resumen = reporte.get("resumen", {})
    producto_top = resumen.get("producto_mas_vendido", {})

    print("\n[INFO] RESUMEN DE VENTAS:")
    print(f"   Total ventas: {resumen.get('total_ventas', 0)}")
    print(f"   Total ingresos: ${resumen.get('total_ingresos', 0):.2f}")
    print(f"   Total unidades: {resumen.get('total_unidades', 0)}")
    print(f"   Venta promedio: ${resumen.get('venta_promedio', 0):.2f}")
    print(
        f"   Producto más vendido: {producto_top.get('nombre', 'N/A')} "
        f"({producto_top.get('unidades', 0)} unidades)"
    )


def ejecutar(ruta_archivo: str, categoria_filtro: Optional[str] = None) -> Dict[str, Any]:
    """Ejecuta el flujo principal y devuelve el reporte para validaciones externas."""
    datos = leer_y_validar_json(ruta_archivo)

    print("\nProcesando ventas...")
    ventas_procesadas: List[Dict[str, Any]] = []
    for v in datos["ventas"]:
        vp = procesar_venta(v)
        if vp:
            ventas_procesadas.append(vp)

    print(f"[INFO] Ventas procesadas: {len(ventas_procesadas)}/{len(datos['ventas'])}")

    if categoria_filtro:
        print(f"[INFO] Filtrando por categoría: {categoria_filtro}")
        ventas_analizar = filtrar_por_categoria(ventas_procesadas, categoria_filtro)
    else:
        ventas_analizar = ventas_procesadas

    print("[INFO] Generando reporte...")
    print("\n[INFO] Generando reporte...")
    reporte = generar_reporte(ventas_analizar)

    _imprimir_resumen(reporte)

    nombre_salida = (
        f"reporte_filtrado_{categoria_filtro}.json" if categoria_filtro else "reporte_general.json"
    )
    guardar_reporte_json(reporte, nombre_salida)

    print("\n[EXITO] Proceso completado exitosamente!")
    return reporte


def main() -> None:
    """CLI."""
    # Modo demo: reproduce el output de ejemplo (general y filtrado)
    # Uso: python ejemplo2_ventas_ajustado.py --demo ventas.json
    if len(sys.argv) >= 3 and sys.argv[1] == "--demo":
        ruta = sys.argv[2]

        _print_header("PROBANDO EJEMPLO 2: Sistema de Ventas")
        try:
            reporte = ejecutar(ruta)
            print("\n[OK] Ejemplo 2 ejecutado exitosamente")
            print("\nSalida del programa:")  # Mantengo el literal del ejemplo

            # “Asserts” impresos como en el ejemplo
            print("\n[OK] Reporte general generado correctamente")
            resumen = reporte.get("resumen", {})
            print(f"Total ventas en reporte: {resumen.get('total_ventas', 0)}")
            print(f"Total ingresos: ${resumen.get('total_ingresos', 0):.2f}")
        except Exception as e:
            print(f"\n[ERROR] Error fatal: {e}")
            raise

        _print_header("PROBANDO EJEMPLO 2: Sistema de Ventas (Filtrado)")
        try:
            # Nota: la categoría del ejemplo es “Electrónicos”
            reporte_f = ejecutar(ruta, "Electrónicos")
            print("\n[OK] Ejemplo 2 (filtrado) ejecutado exitosamente")
            print("\nSalida del programa:")

            print("\n[OK] Reporte filtrado generado correctamente")
        except Exception as e:
            print(f"\n[ERROR] Error fatal: {e}")
            raise

        return

    # Modo normal (compatibilidad hacia atrás)
    if len(sys.argv) < 2:
        print("Uso: python ejemplo2_ventas_ajustado.py <archivo_json> [categoria]")
        print("Ejemplo: python ejemplo2_ventas_ajustado.py ventas.json Electrónicos")
        print("Demo:   python ejemplo2_ventas_ajustado.py --demo ventas.json")
        sys.exit(1)

    ruta_archivo = sys.argv[1]
    categoria = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        ejecutar(ruta_archivo, categoria)
    except Exception as e:
        print(f"\n[ERROR] Error fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

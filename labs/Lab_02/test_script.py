#!/usr/bin/env python3
"""
Script de prueba para verificar que todos los ejemplos funcionen correctamente
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def verificar_archivos():
    """Verifica que todos los archivos necesarios existan"""
    archivos_requeridos = [
        'ejemplo1_estudiantes.py',
        'ejemplo2_ventas.py',
        'estudiantes.json',
        'ventas.json',
        'ejercicios_practicos.py'
    ]
    
    print("Verificando archivos requeridos...")
    archivos_faltantes = []
    
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"   [OK] {archivo}")
        else:
            print(f"   [ERROR] {archivo} (faltante)")
            archivos_faltantes.append(archivo)
    
    if archivos_faltantes:
        print(f"\n[ERROR] Faltan {len(archivos_faltantes)} archivos requeridos")
        return False
    else:
        print(f"\n[TODOS OK] Todos los archivos requeridos estan presentes")
        return True

def probar_ejemplo1():
    """Prueba el ejemplo 1 de estudiantes"""
    print("\n" + "="*50)
    print("PROBANDO EJEMPLO 1: Sistema de Estudiantes")
    print("="*50)
    
    try:
        # Ejecutar el script
        resultado = subprocess.run([
            sys.executable, 'ejemplo1_estudiantes.py', 'estudiantes.json'
        ], capture_output=True, text=True, timeout=30)
        
        if resultado.returncode == 0:
            print("[OK] Ejemplo 1 ejecutado exitosamente")
            print("\nSalida del programa:")
            print(resultado.stdout)
        else:
            print("[ERROR] Error en la ejecucion del Ejemplo 1")
            print("Error:", resultado.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("[ERROR] El Ejemplo 1 tardo demasiado en ejecutarse")
        return False
    except Exception as e:
        print(f"[ERROR] Error ejecutando el Ejemplo 1: {e}")
        return False
    
    return True

def probar_ejemplo2():
    """Prueba el ejemplo 2 de ventas"""
    print("\n" + "="*50)
    print("PROBANDO EJEMPLO 2: Sistema de Ventas")
    print("="*50)
    
    try:
        # Ejecutar el script
        resultado = subprocess.run([
            sys.executable, 'ejemplo2_ventas.py', 'ventas.json'
        ], capture_output=True, text=True, timeout=30)
        
        if resultado.returncode == 0:
            print("[OK] Ejemplo 2 ejecutado exitosamente")
            print("\nSalida del programa:")
            print(resultado.stdout)
            
            # Verificar si se genero el reporte
            if os.path.exists('reporte_general.json'):
                print("[OK] Reporte general generado correctamente")
                
                # Leer y mostrar parte del reporte
                with open('reporte_general.json', 'r', encoding='utf-8') as f:
                    reporte = json.load(f)
                
                print(f"Total ventas en reporte: {reporte.get('resumen', {}).get('total_ventas', 0)}")
                print(f"Total ingresos: ${reporte.get('resumen', {}).get('total_ingresos', 0):.2f}")
            else:
                print("[ADVERTENCIA] No se genero el reporte esperado")
                
        else:
            print("[ERROR] Error en la ejecucion del Ejemplo 2")
            print("Error:", resultado.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("[ERROR] El Ejemplo 2 tardo demasiado en ejecutarse")
        return False
    except Exception as e:
        print(f"[ERROR] Error ejecutando el Ejemplo 2: {e}")
        return False
    
    return True

def probar_ejemplo2_filtrado():
    """Prueba el ejemplo 2 con filtrado por categoría"""
    print("\n" + "="*50)
    print("PROBANDO EJEMPLO 2: Sistema de Ventas (Filtrado)")
    print("="*50)
    
    try:
        # Ejecutar el script con filtro
        resultado = subprocess.run([
            sys.executable, 'ejemplo2_ventas.py', 'ventas.json', 'Electrónicos'
        ], capture_output=True, text=True, timeout=30)
        
        if resultado.returncode == 0:
            print("[OK] Ejemplo 2 (filtrado) ejecutado exitosamente")
            print("\nSalida del programa:")
            print(resultado.stdout)
            
            # Verificar si se genero el reporte filtrado
            if os.path.exists('reporte_filtrado_Electrónicos.json'):
                print("[OK] Reporte filtrado generado correctamente")
            else:
                print("[ADVERTENCIA] No se genero el reporte filtrado esperado")
                
        else:
            print("[ERROR] Error en la ejecucion del Ejemplo 2 (filtrado)")
            print("Error:", resultado.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("[ERROR] El Ejemplo 2 (filtrado) tardo demasiado en ejecutarse")
        return False
    except Exception as e:
        print(f"[ERROR] Error ejecutando el Ejemplo 2 (filtrado): {e}")
        return False
    
    return True

def probar_ejercicios_practicos():
    """Prueba los ejercicios prácticos"""
    print("\n" + "="*50)
    print("PROBANDO EJERCICIOS PRÁCTICOS")
    print("="*50)
    
    try:
        # Ejecutar los ejercicios en modo no interactivo
        resultado = subprocess.run([
            sys.executable, '-c', 
            '''
import sys
sys.path.append(".")
from ejercicios_practicos import demo_inventario, demo_analizador_logs, demo_encuestas

print("Ejecutando demostraciones en modo automático...")
demo_inventario()
demo_analizador_logs()
demo_encuestas()
print("Todas las demostraciones completadas.")
'''
        ], capture_output=True, text=True, timeout=60)
        
        if resultado.returncode == 0:
            print("[OK] Ejercicios practicos ejecutados exitosamente")
            print("\nResumen de la ejecucion:")
            
            # Contar lineas de salida para verificar que se ejecutaron
            lineas = resultado.stdout.strip().split('\n')
            print(f"   - Total lineas de salida: {len(lineas)}")
            
            # Verificar archivos generados
            archivos_generados = ['inventario_demo.json', 'demo.log', 'encuesta_demo.json']
            for archivo in archivos_generados:
                if os.path.exists(archivo):
                    print(f"   [OK] {archivo} generado")
                else:
                    print(f"   [ADVERTENCIA] {archivo} no encontrado")
                    
        else:
            print("[ERROR] Error en la ejecucion de los ejercicios practicos")
            print("Error:", resultado.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("[ERROR] Los ejercicios practicos tardaron demasiado en ejecutarse")
        return False
    except Exception as e:
        print(f"[ERROR] Error ejecutando los ejercicios practicos: {e}")
        return False
    
    return True

def limpiar_archivos_temporales():
    """Limpia archivos temporales generados durante las pruebas"""
    print("\nLimpiando archivos temporales...")
    
    archivos_temporales = [
        'reporte_general.json',
        'reporte_filtrado_Electrónicos.json',
        'inventario_demo.json',
        'demo.log',
        'encuesta_demo.json'
    ]
    
    for archivo in archivos_temporales:
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
                print(f"   [ELIMINADO] {archivo}")
            except Exception as e:
                print(f"   [ERROR] No se pudo eliminar {archivo}: {e}")

def mostrar_resumen(resultados):
    """Muestra un resumen de los resultados de las pruebas"""
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS")
    print("="*60)
    
    total_pruebas = len(resultados)
    pruebas_exitosas = sum(resultados.values())
    
    for prueba, resultado in resultados.items():
        estado = "[OK] EXITOSO" if resultado else "[ERROR] FALLÓ"
        print(f"   {prueba}: {estado}")
    
    print(f"\nEstadisticas:")
    print(f"   - Total pruebas: {total_pruebas}")
    print(f"   - Exitosas: {pruebas_exitosas}")
    print(f"   - Fallidas: {total_pruebas - pruebas_exitosas}")
    print(f"   - Tasa de exito: {(pruebas_exitosas/total_pruebas*100):.1f}%")
    
    if pruebas_exitosas == total_pruebas:
        print(f"\n[EXITO] Todas las pruebas pasaron exitosamente!")
        print("[OK] El laboratorio esta listo para usarse.")
    else:
        print(f"\n[ADVERTENCIA] Algunas pruebas fallaron. Revisa los errores mostrados arriba.")
        print("[INFO] Es posible que necesites ajustar algunos archivos.")

def main():
    """Función principal del script de pruebas"""
    print("SCRIPT DE PRUEBAS - LABORATORIO PYTHON")
    print("="*60)
    
    # Verificar archivos
    if not verificar_archivos():
        print("\n[ERROR] No se pueden continuar las pruebas sin todos los archivos requeridos.")
        return False
    
    # Ejecutar pruebas
    resultados = {}
    
    print("\nIniciando pruebas...")
    
    try:
        resultados['Verificación de archivos'] = True
        resultados['Ejemplo 1 (Estudiantes)'] = probar_ejemplo1()
        resultados['Ejemplo 2 (Ventas)'] = probar_ejemplo2()
        resultados['Ejemplo 2 (Filtrado)'] = probar_ejemplo2_filtrado()
        resultados['Ejercicios prácticos'] = probar_ejercicios_practicos()
        
    except KeyboardInterrupt:
        print("\n\n[INTERRUMPIDO] Pruebas interrumpidas por el usuario")
        return False
    except Exception as e:
        print(f"\n[ERROR] Error inesperado durante las pruebas: {e}")
        return False
    finally:
        # Limpiar archivos temporales
        limpiar_archivos_temporales()
    
    # Mostrar resumen
    mostrar_resumen(resultados)
    
    # Retornar si todas las pruebas fueron exitosas
    return all(resultados.values())

if __name__ == "__main__":
    exito = main()
    sys.exit(0 if exito else 1)

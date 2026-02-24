#!/usr/bin/env python3
"""
EJEMPLO 2: Métricas y exportación a JSON
Este ejemplo calcula estadísticas y exporta los resultados
"""

import csv
import json
from pathlib import Path
from datetime import datetime

def calcular_metricas_y_exportar():
    """
    Función que lee CSV, calcula métricas y exporta a JSON
    """
    print("📈 Ejemplo 2: Cálculo de métricas y exportación JSON")
    print("=" * 50)
    
    ruta_csv = Path("datos_ejemplo.csv")
    ruta_json = Path("resultados.json")
    
    if not ruta_csv.exists():
        print(f"❌ Error: No existe el archivo {ruta_csv}")
        return
    
    try:
        # Lista para guardar todos los datos
        empleados = []
        
        # Leer el CSV
        with open(ruta_csv, 'r', encoding='utf-8') as archivo:
            lector_csv = csv.DictReader(archivo)  # DictReader es más conveniente
            
            for fila in lector_csv:
                # Convertir tipos de datos
                fila['edad'] = int(fila['edad'])
                fila['salario'] = float(fila['salario'])
                fila['id'] = int(fila['id'])
                empleados.append(fila)
        
        print(f"✅ Se cargaron {len(empleados)} empleados")
        
        # Calcular métricas
        total_empleados = len(empleados)
        edad_promedio = sum(emp['edad'] for emp in empleados) / total_empleados
        salario_promedio = sum(emp['salario'] for emp in empleados) / total_empleados
        salario_total = sum(emp['salario'] for emp in empleados)
        
        # Agrupar por departamento
        departamentos = {}
        for emp in empleados:
            depto = emp['departamento']
            if depto not in departamentos:
                departamentos[depto] = {
                    'cantidad': 0,
                    'salario_total': 0,
                    'empleados': []
                }
            departamentos[depto]['cantidad'] += 1
            departamentos[depto]['salario_total'] += emp['salario']
            departamentos[depto]['empleados'].append(emp['nombre'])
        
        # Calcular promedio por departamento
        for depto in departamentos:
            depto_data = departamentos[depto]
            depto_data['salario_promedio'] = depto_data['salario_total'] / depto_data['cantidad']
        
        # Crear estructura de resultados
        resultados = {
            'fecha_procesamiento': datetime.now().isoformat(),
            'resumen_general': {
                'total_empleados': total_empleados,
                'edad_promedio': round(edad_promedio, 2),
                'salario_promedio': round(salario_promedio, 2),
                'salario_total': round(salario_total, 2)
            },
            'por_departamento': departamentos,
            'empleado_mayor_salario': max(empleados, key=lambda x: x['salario']),
            'empleado_menor_salario': min(empleados, key=lambda x: x['salario'])
        }
        
        # Exportar a JSON
        with open(ruta_json, 'w', encoding='utf-8') as archivo_json:
            json.dump(resultados, archivo_json, indent=2, ensure_ascii=False)
        
        print(f"📊 Métricas calculadas:")
        print(f"  - Total empleados: {total_empleados}")
        print(f"  - Edad promedio: {edad_promedio:.1f} años")
        print(f"  - Salario promedio: ${salario_promedio:.2f}")
        print(f"  - Salario total: ${salario_total:.2f}")
        print(f"\n📁 Resultados exportados a: {ruta_json}")
        
        return resultados
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    calcular_metricas_y_exportar()

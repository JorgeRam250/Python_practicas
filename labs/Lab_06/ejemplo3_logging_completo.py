#!/usr/bin/env python3
"""
EJEMPLO 3: Logging completo con subprocess
Este ejemplo incluye logging estructurado y automatización
"""

import csv
import json
import logging
import subprocess
from pathlib import Path
from datetime import datetime
import sys

def configurar_logging():
    """
    Configura el sistema de logging con diferentes niveles
    """
    # Crear directorio de logs si no existe
    Path("logs").mkdir(exist_ok=True)
    
    # Configurar formato de logs
    formato = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configurar logging para archivo
    logging.basicConfig(
        level=logging.DEBUG,
        format=formato,
        handlers=[
            logging.FileHandler('logs/laboratorio.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)  # También mostrar en consola
        ]
    )
    
    return logging.getLogger(__name__)

def verificar_archivo_con_subprocess(ruta):
    """
    Usa subprocess para verificar si el archivo existe
    """
    logger = logging.getLogger(__name__)
    
    try:
        # En Windows usamos 'dir', en Linux/Mac usamos 'ls'
        if sys.platform == 'win32':
            resultado = subprocess.run(['dir', str(ruta)], 
                                    capture_output=True, 
                                    text=True, 
                                    shell=True)
        else:
            resultado = subprocess.run(['ls', '-la', str(ruta)], 
                                    capture_output=True, 
                                    text=True)
        
        if resultado.returncode == 0:
            logger.info(f"✅ Archivo verificado con subprocess: {ruta}")
            return True
        else:
            logger.error(f"❌ Archivo no encontrado: {ruta}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error en subprocess: {e}")
        return False

def procesar_con_logging_completo():
    """
    Función principal con logging completo
    """
    logger = configurar_logging()
    
    logger.info("🚀 Iniciando procesamiento completo")
    logger.debug("Ejemplo 3: Logging completo con subprocess")
    
    # Rutas de archivos
    ruta_csv = Path("datos_ejemplo.csv")
    ruta_json = Path("resultados_completos.json")
    ruta_resumen = Path("resumen_procesamiento.txt")
    
    logger.info(f"📁 Archivo CSV: {ruta_csv}")
    
    # Verificar archivo con subprocess
    if not verificar_archivo_con_subprocess(ruta_csv):
        logger.critical("❌ No se puede continuar sin el archivo CSV")
        return False
    
    try:
        logger.info("📖 Iniciando lectura del CSV")
        
        empleados = []
        errores_registro = 0
        
        with open(ruta_csv, 'r', encoding='utf-8') as archivo:
            lector_csv = csv.DictReader(archivo)
            
            for num_fila, fila in enumerate(lector_csv, start=2):  # start=2 porque la fila 1 es encabezado
                try:
                    # Validar y convertir datos
                    fila['id'] = int(fila['id'])
                    fila['edad'] = int(fila['edad'])
                    fila['salario'] = float(fila['salario'])
                    
                    # Validaciones
                    if fila['edad'] < 18 or fila['edad'] > 65:
                        logger.warning(f"⚠️ Edad fuera de rango en fila {num_fila}: {fila['edad']}")
                    
                    if fila['salario'] < 0:
                        logger.error(f"❌ Salario negativo en fila {num_fila}: {fila['salario']}")
                        errores_registro += 1
                        continue
                    
                    empleados.append(fila)
                    logger.debug(f"✅ Fila {num_fila} procesada: ID {fila['id']}")
                    
                except ValueError as e:
                    logger.error(f"❌ Error de conversión en fila {num_fila}: {e}")
                    errores_registro += 1
                    continue
        
        logger.info(f"✅ CSV procesado: {len(empleados)} registros válidos, {errores_registro} errores")
        
        # Calcular métricas avanzadas
        logger.info("📊 Calculando métricas avanzadas")
        
        metricas = {
            'total_empleados': len(empleados),
            'edad_promedio': sum(emp['edad'] for emp in empleados) / len(empleados),
            'salario_promedio': sum(emp['salario'] for emp in empleados) / len(empleados),
            'salario_total': sum(emp['salario'] for emp in empleados),
            'departamentos': {}
        }
        
        # Agrupar por departamento
        for emp in empleados:
            depto = emp['departamento']
            if depto not in metricas['departamentos']:
                metricas['departamentos'][depto] = {
                    'cantidad': 0,
                    'salario_total': 0,
                    'edades': []
                }
            
            metricas['departamentos'][depto]['cantidad'] += 1
            metricas['departamentos'][depto]['salario_total'] += emp['salario']
            metricas['departamentos'][depto]['edades'].append(emp['edad'])
        
        # Calcular promedios por departamento
        for depto, datos in metricas['departamentos'].items():
            datos['salario_promedio'] = datos['salario_total'] / datos['cantidad']
            datos['edad_promedio'] = sum(datos['edades']) / len(datos['edades'])
            del datos['edades']  # Eliminar lista temporal
        
        logger.info("📈 Métricas calculadas exitosamente")
        
        # Exportar resultados a JSON
        logger.info(f"💾 Exportando resultados a {ruta_json}")
        
        resultado_completo = {
            'metadata': {
                'fecha_procesamiento': datetime.now().isoformat(),
                'script_version': '3.0',
                'registros_procesados': len(empleados),
                'errores_encontrados': errores_registro
            },
            'metricas': metricas,
            'empleados': empleados
        }
        
        with open(ruta_json, 'w', encoding='utf-8') as archivo_json:
            json.dump(resultado_completo, archivo_json, indent=2, ensure_ascii=False)
        
        logger.info("✅ JSON exportado correctamente")
        
        # Crear resumen de texto
        logger.info(f"📝 Creando resumen en {ruta_resumen}")
        
        with open(ruta_resumen, 'w', encoding='utf-8') as archivo_resumen:
            archivo_resumen.write("RESUMEN DE PROCESAMIENTO\n")
            archivo_resumen.write("=" * 40 + "\n")
            archivo_resumen.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            archivo_resumen.write(f"Total empleados: {metricas['total_empleados']}\n")
            archivo_resumen.write(f"Edad promedio: {metricas['edad_promedio']:.1f} años\n")
            archivo_resumen.write(f"Salario promedio: ${metricas['salario_promedio']:.2f}\n")
            archivo_resumen.write(f"Salario total: ${metricas['salario_total']:.2f}\n")
            archivo_resumen.write(f"Errores: {errores_registro}\n\n")
            
            archivo_resumen.write("POR DEPARTAMENTO:\n")
            archivo_resumen.write("-" * 20 + "\n")
            for depto, datos in metricas['departamentos'].items():
                archivo_resumen.write(f"{depto}:\n")
                archivo_resumen.write(f"  Empleados: {datos['cantidad']}\n")
                archivo_resumen.write(f"  Salario promedio: ${datos['salario_promedio']:.2f}\n")
                archivo_resumen.write(f"  Edad promedio: {datos['edad_promedio']:.1f} años\n\n")
        
        logger.info("✅ Resumen creado correctamente")
        
        # Usar subprocess para mostrar el contenido del JSON
        logger.info("🔍 Verificando archivo JSON creado con subprocess")
        
        if sys.platform == 'win32':
            subprocess.run(['type', str(ruta_json)], shell=True)
        else:
            subprocess.run(['cat', str(ruta_json)], shell=True)
        
        logger.info("🎉 Procesamiento completado exitosamente")
        return True
        
    except Exception as e:
        logger.critical(f"💥 Error crítico en el procesamiento: {e}")
        return False

if __name__ == "__main__":
    procesar_con_logging_completo()

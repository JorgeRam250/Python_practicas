#!/usr/bin/env python3
"""
Script para ejecutar todos los tests y generar reportes de cobertura
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n{'='*50}")
    print(f"Ejecutando: {description}")
    print(f"Comando: {command}")
    print(f"{'='*50}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print("STDOUT:")
        print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    if result.returncode != 0:
        print(f"ERROR: El comando falló con código {result.returncode}")
        return False
    
    print(f"OK {description} - EXITOSO")
    return True


def main():
    """Función principal"""
    print("Laboratorio de Pruebas y TDD - Ejecutor de Tests")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("requirements.txt"):
        print("Error: No se encuentra requirements.txt. Asegúrate de estar en el directorio del proyecto.")
        sys.exit(1)
    
    # Instalar dependencias
    if not run_command("pip install -r requirements.txt", "Instalando dependencias"):
        sys.exit(1)
    
    # Ejecutar tests básicos
    if not run_command("pytest tests/ -v", "Ejecutando tests básicos"):
        sys.exit(1)
    
    # Ejecutar tests con cobertura
    if not run_command("pytest tests/ --cov=src --cov-report=html --cov-report=term-missing", "Ejecutando tests con cobertura"):
        sys.exit(1)
    
    # Ejecutar tests por categorías
    print("\n" + "="*50)
    print("Ejecutando tests por categorías")
    print("="*50)
    
    # Tests unitarios
    run_command("pytest tests/ -m unit -v", "Tests unitarios")
    
    # Tests de integración
    run_command("pytest tests/ -m integration -v", "Tests de integración")
    
    # Tests rápidos (excluyendo los lentos)
    run_command("pytest tests/ -m 'not slow' -v", "Tests rápidos")
    
    # Generar reporte de cobertura detallado
    print("\n" + "="*50)
    print("Generando reporte de cobertura")
    print("="*50)
    
    if os.path.exists("htmlcov"):
        print("Reporte HTML generado en: htmlcov/index.html")
        print("Abre el archivo en tu navegador para ver los detalles")
    
    print("\nTodos los tests completados!")
    print("Revisa los reportes en:")
    print("   - Reporte HTML: htmlcov/index.html")
    print("   - Reporte de cobertura en terminal (arriba)")


if __name__ == "__main__":
    main()

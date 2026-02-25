"""
Script de configuración y ejecución del laboratorio FastAPI
"""

import os
import subprocess
import sys
import time
import sqlite3
import hashlib

def check_python_version():
    """Verificar versión de Python"""
    if sys.version_info < (3, 7):
        print("❌ Se requiere Python 3.7 o superior")
        return False
    print(f"✅ Python {sys.version.split()[0]} detectado")
    return True

def install_dependencies():
    """Instalar dependencias"""
    print("\n📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error al instalar dependencias")
        return False

def init_database():
    """Inicializar base de datos"""
    print("\n🗄️ Inicializando base de datos...")
    try:
        # La base de datos se crea automáticamente cuando se inicia main.py
        print("✅ Base de datos lista (se creará automáticamente al iniciar la aplicación)")
        return True
    except Exception as e:
        print(f"❌ Error al inicializar base de datos: {e}")
        return False

def start_server():
    """Iniciar el servidor FastAPI"""
    print("\n🚀 Iniciando servidor FastAPI...")
    print("El servidor estará disponible en: http://localhost:8000")
    print("Documentación Swagger: http://localhost:8000/docs")
    print("Documentación ReDoc: http://localhost:8000/redoc")
    print("\nPresiona Ctrl+C para detener el servidor")
    
    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")

def run_tests():
    """Ejecutar pruebas"""
    print("\n🧪 Ejecutando pruebas...")
    try:
        subprocess.run([sys.executable, "examples/ejemplo_testing.py"])
    except Exception as e:
        print(f"❌ Error al ejecutar pruebas: {e}")

def show_menu():
    """Mostrar menú de opciones"""
    print("\n" + "="*50)
    print("🎯 LABORATORIO FASTAPI - MENÚ PRINCIPAL")
    print("="*50)
    print("1. 🚀 Iniciar servidor FastAPI")
    print("2. 🧪 Ejecutar pruebas automatizadas")
    print("3. 📚 Ejecutar ejemplo básico")
    print("4. 🔧 Ejecutar ejemplo avanzado")
    print("5. 📋 Ver estructura del proyecto")
    print("6. ❌ Salir")
    print("="*50)

def show_project_structure():
    """Mostrar estructura del proyecto"""
    print("\n📁 ESTRUCTURA DEL PROYECTO:")
    print("""
Windsurf/
├── main.py              # Aplicación principal FastAPI
├── test_orders.py       # Pruebas con pytest
├── setup.py            # Script de configuración (este archivo)
├── requirements.txt     # Dependencias del proyecto
├── README.md           # Documentación completa
├── orders.db           # Base de datos SQLite (se crea automáticamente)
└── examples/           # Ejemplos de uso
    ├── ejemplo_basico.py    # Ejemplo simple para principiantes
    ├── ejemplo_avanzado.py  # Ejemplo con operaciones complejas
    └── ejemplo_testing.py   # Ejemplo de testing automatizado
    """)

def main():
    """Función principal"""
    print("🎓 LABORATORIO DE FASTAPI - CRUD DE ORDERS CON JWT")
    print("=" * 60)
    
    # Verificar requisitos
    if not check_python_version():
        return
    
    # Instalar dependencias
    if not install_dependencies():
        return
    
    # Inicializar base de datos
    if not init_database():
        return
    
    print("\n✅ Configuración completada exitosamente!")
    
    # Menú interactivo
    while True:
        show_menu()
        
        try:
            option = input("\nSelecciona una opción (1-6): ").strip()
            
            if option == "1":
                start_server()
            elif option == "2":
                run_tests()
            elif option == "3":
                print("\n📚 Ejecutando ejemplo básico...")
                subprocess.run([sys.executable, "examples/ejemplo_basico.py"])
            elif option == "4":
                print("\n🔧 Ejecutando ejemplo avanzado...")
                subprocess.run([sys.executable, "examples/ejemplo_avanzado.py"])
            elif option == "5":
                show_project_structure()
            elif option == "6":
                print("\n👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción inválida. Por favor selecciona 1-6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()

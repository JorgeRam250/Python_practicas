#!/usr/bin/env python3
"""
Script para ejecutar tests y generar reportes de cobertura
"""

import subprocess
import sys
from pathlib import Path


def ejecutar_tests(con_cobertura: bool = True) -> bool:
    """Ejecuta los tests del proyecto."""
    modo = "con cobertura" if con_cobertura else "básicos"
    print(f"🧪 Ejecutando tests ({modo})...")
    print("=" * 50)
    
    try:
        if con_cobertura:
            comando = [
                "pytest", 
                "tests/", 
                "-v",
                "--cov=src",
                "--cov-report=term-missing",
                "--cov-report=html:htmlcov",
                "--cov-fail-under=80"
            ]
        else:
            comando = ["pytest", "tests/", "-v"]
        
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        print("STDOUT:")
        print(resultado.stdout)
        
        if resultado.stderr:
            print("STDERR:")
            print(resultado.stderr)
        
        if resultado.returncode == 0:
            print(f"✅ Tests: Todos pasaron exitosamente")
            if con_cobertura:
                print("📊 Reporte de cobertura generado en htmlcov/index.html")
            return True
        else:
            print(f"❌ Tests: Algunos tests fallaron (código: {resultado.returncode})")
            return False
            
    except FileNotFoundError:
        print("❌ Error: pytest no está instalado")
        print("💡 Solución: pip install pytest pytest-cov")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def ejecutar_test_especifico(test_file: str) -> bool:
    """Ejecuta un archivo de test específico."""
    print(f"🎯 Ejecutando test específico: {test_file}")
    print("=" * 50)
    
    try:
        comando = [
            "pytest", 
            f"tests/{test_file}", 
            "-v",
            "--tb=short"
        ]
        
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        print("STDOUT:")
        print(resultado.stdout)
        
        if resultado.stderr:
            print("STDERR:")
            print(resultado.stderr)
        
        if resultado.returncode == 0:
            print(f"✅ Test {test_file}: Pasó exitosamente")
            return True
        else:
            print(f"❌ Test {test_file}: Falló (código: {resultado.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ Error al ejecutar test específico: {e}")
        return False


def mostrar_menu_tests() -> None:
    """Muestra menú de opciones de tests."""
    print("\n📋 Menú de Tests Disponibles:")
    print("=" * 40)
    print("1. Ejecutar todos los tests con cobertura")
    print("2. Ejecutar todos los tests (básico)")
    print("3. Ejecutar solo tests de modelos")
    print("4. Ejecutar solo tests de servicios")
    print("5. Ejecutar solo tests de utils")
    print("6. Salir")
    print("=" * 40)


def main() -> None:
    """Función principal con menú interactivo."""
    print("🎯 Ejecutor de Tests")
    print("=" * 60)
    
    # Si hay argumentos, ejecutar directamente
    if len(sys.argv) > 1:
        if sys.argv[1] == "--all":
            exito = ejecutar_tests(con_cobertura=True)
            sys.exit(0 if exito else 1)
        elif sys.argv[1] == "--basic":
            exito = ejecutar_tests(con_cobertura=False)
            sys.exit(0 if exito else 1)
        elif sys.argv[1] == "--models":
            exito = ejecutar_test_especifico("test_models.py")
            sys.exit(0 if exito else 1)
        elif sys.argv[1] == "--services":
            exito = ejecutar_test_especifico("test_services.py")
            sys.exit(0 if exito else 1)
        elif sys.argv[1] == "--utils":
            exito = ejecutar_test_especifico("test_utils.py")
            sys.exit(0 if exito else 1)
    
    # Modo interactivo
    while True:
        mostrar_menu_tests()
        
        try:
            opcion = input("\nSelecciona una opción [1-6]: ").strip()
            
            if opcion == "1":
                exito = ejecutar_tests(con_cobertura=True)
                if exito:
                    print("\n🎉 ¡Todos los tests con cobertura pasaron!")
                else:
                    print("\n❌ Algunos tests fallaron")
                break
                
            elif opcion == "2":
                exito = ejecutar_tests(con_cobertura=False)
                if exito:
                    print("\n✅ Todos los tests básicos pasaron!")
                else:
                    print("\n❌ Algunos tests fallaron")
                break
                
            elif opcion == "3":
                exito = ejecutar_test_especifico("test_models.py")
                if exito:
                    print("\n✅ Tests de modelos pasaron!")
                else:
                    print("\n❌ Tests de modelos fallaron")
                    
            elif opcion == "4":
                exito = ejecutar_test_especifico("test_services.py")
                if exito:
                    print("\n✅ Tests de servicios pasaron!")
                else:
                    print("\n❌ Tests de servicios fallaron")
                    
            elif opcion == "5":
                exito = ejecutar_test_especifico("test_utils.py")
                if exito:
                    print("\n✅ Tests de utils pasaron!")
                else:
                    print("\n❌ Tests de utils fallaron")
                    
            elif opcion == "6":
                print("\n👋 Saliendo...")
                break
                
            else:
                print("\n❌ Opción no válida. Intenta nuevamente.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Operación cancelada por el usuario")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()

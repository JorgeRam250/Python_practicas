#!/usr/bin/env python3
"""
Script para verificar type hints con mypy
"""

import subprocess
import sys
from pathlib import Path


def ejecutar_mypy() -> bool:
    """Ejecuta mypy en el código fuente."""
    print("🔍 Verificando type hints con mypy...")
    print("=" * 50)
    
    try:
        # Ejecutar mypy en el directorio src/
        resultado = subprocess.run(
            ["mypy", "src/", "--show-error-codes"],
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
            print("✅ mypy: No se encontraron errores de tipo")
            return True
        else:
            print(f"❌ mypy: Se encontraron errores (código: {resultado.returncode})")
            return False
            
    except FileNotFoundError:
        print("❌ Error: mypy no está instalado")
        print("💡 Solución: pip install mypy")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def ejecutar_mypy_en_tests() -> bool:
    """Ejecuta mypy también en los tests."""
    print("\n🧪 Verificando type hints en tests...")
    print("=" * 50)
    
    try:
        resultado = subprocess.run(
            ["mypy", "tests/", "--show-error-codes"],
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
            print("✅ mypy tests: No se encontraron errores de tipo")
            return True
        else:
            print(f"❌ mypy tests: Se encontraron errores (código: {resultado.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ Error al verificar tests: {e}")
        return False


def main() -> None:
    """Función principal."""
    print("🎯 Verificación de Type Hints con mypy")
    print("=" * 60)
    
    # Verificar código fuente
    exito_src = ejecutar_mypy()
    
    # Verificar tests
    exito_tests = ejecutar_mypy_en_tests()
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    if exito_src and exito_tests:
        print("✅ Todos los archivos pasaron la verificación de tipos")
        sys.exit(0)
    else:
        print("❌ Se encontraron errores de tipo")
        print("\n💡 Recomendaciones:")
        print("   1. Revisa los errores mostrados arriba")
        print("   2. Añade las anotaciones de tipo faltantes")
        print("   3. Corrige las incompatibilidades de tipo")
        print("   4. Vuelve a ejecutar este script")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script para verificar calidad de código con ruff, black e isort
"""

import subprocess
import sys
from pathlib import Path


def ejecutar_ruff(check_only: bool = True) -> bool:
    """Ejecuta ruff para verificar y formatear código."""
    modo = "verificación" if check_only else "formateo"
    print(f"🔍 Ejecutando ruff ({modo})...")
    print("=" * 50)
    
    try:
        comando = ["ruff", "check", "src/", "tests/"]
        if not check_only:
            comando.append("--fix")
        
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
            print(f"✅ ruff: {modo} exitoso")
            return True
        else:
            print(f"❌ ruff: Se encontraron problemas (código: {resultado.returncode})")
            return False
            
    except FileNotFoundError:
        print("❌ Error: ruff no está instalado")
        print("💡 Solución: pip install ruff")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def ejecutar_black(check_only: bool = True) -> bool:
    """Ejecuta black para verificar y formatear código."""
    modo = "verificación" if check_only else "formateo"
    print(f"\n⚫ Ejecutando black ({modo})...")
    print("=" * 50)
    
    try:
        comando = ["black", "--check", "src/", "tests/"] if check_only else ["black", "src/", "tests/"]
        
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
            print(f"✅ black: {modo} exitoso")
            return True
        else:
            print(f"❌ black: Se encontraron problemas de formato (código: {resultado.returncode})")
            return False
            
    except FileNotFoundError:
        print("❌ Error: black no está instalado")
        print("💡 Solución: pip install black")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def ejecutar_isort(check_only: bool = True) -> bool:
    """Ejecuta isort para verificar y ordenar imports."""
    modo = "verificación" if check_only else "ordenamiento"
    print(f"\n📚 Ejecutando isort ({modo})...")
    print("=" * 50)
    
    try:
        comando = ["isort", "--check-only", "src/", "tests/"] if check_only else ["isort", "src/", "tests/"]
        
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
            print(f"✅ isort: {modo} exitoso")
            return True
        else:
            print(f"❌ isort: Se encontraron problemas en imports (código: {resultado.returncode})")
            return False
            
    except FileNotFoundError:
        print("❌ Error: isort no está instalado")
        print("💡 Solución: pip install isort")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def ejecutar_pre_commit() -> bool:
    """Ejecuta pre-commit en todos los archivos."""
    print("\n🪝 Ejecutando pre-commit hooks...")
    print("=" * 50)
    
    try:
        resultado = subprocess.run(
            ["pre-commit", "run", "--all-files"],
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
            print("✅ pre-commit: Todos los hooks pasaron exitosamente")
            return True
        else:
            print(f"❌ pre-commit: Algunos hooks fallaron (código: {resultado.returncode})")
            return False
            
    except FileNotFoundError:
        print("❌ Error: pre-commit no está instalado")
        print("💡 Solución: pip install pre-commit")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def main() -> None:
    """Función principal."""
    print("🎯 Verificación de Calidad de Código")
    print("=" * 60)
    
    # Verificar solo (sin modificar archivos)
    print("📋 MODO VERIFICACIÓN (sin modificar archivos)")
    print("=" * 60)
    
    exito_ruff = ejecutar_ruff(check_only=True)
    exito_black = ejecutar_black(check_only=True)
    exito_isort = ejecutar_isort(check_only=True)
    
    # Resumen de verificación
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    if exito_ruff and exito_black and exito_isort:
        print("✅ Todas las verificaciones de calidad pasaron")
        
        # Preguntar si desea ejecutar pre-commit
        print("\n🤔 ¿Desea ejecutar pre-commit hooks completos?")
        try:
            respuesta = input("   [S/N]: ").strip().upper()
            if respuesta == 'S':
                exito_precommit = ejecutar_pre_commit()
                if exito_precommit:
                    print("\n🎉 ¡Todo está perfecto!")
                    sys.exit(0)
                else:
                    print("\n⚠️ Algunos pre-commit hooks fallaron")
                    sys.exit(1)
            else:
                print("\n✅ Verificación completada (sin ejecutar pre-commit)")
                sys.exit(0)
        except KeyboardInterrupt:
            print("\n\n👋 Operación cancelada por el usuario")
            sys.exit(0)
    else:
        print("❌ Se encontraron problemas de calidad")
        print("\n💡 Recomendaciones:")
        print("   1. Corrige los problemas de formato reportados")
        print("   2. Ordena los imports si es necesario")
        print("   3. Resuelve los problemas de estilo")
        print("   4. Vuelve a ejecutar este script")
        print("\n🔧 Para corregir automáticamente, ejecuta:")
        print("   python verificar_calidad.py --fix")
        sys.exit(1)


def main_fix() -> None:
    """Función para corregir automáticamente."""
    print("🔧 MODO CORRECCIÓN AUTOMÁTICA")
    print("=" * 60)
    print("⚠️ Este modo modificará los archivos para corregir problemas de formato")
    
    try:
        respuesta = input("   ¿Estás seguro? [S/N]: ").strip().upper()
        if respuesta != 'S':
            print("👋 Operación cancelada")
            return
    except KeyboardInterrupt:
        print("\n👋 Operación cancelada por el usuario")
        return
    
    print("\n🔧 Corrigiendo automáticamente...")
    
    exito_ruff = ejecutar_ruff(check_only=False)
    exito_black = ejecutar_black(check_only=False)
    exito_isort = ejecutar_isort(check_only=False)
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE CORRECCIÓN")
    print("=" * 60)
    
    if exito_ruff and exito_black and exito_isort:
        print("✅ Todas las correcciones se aplicaron exitosamente")
        
        # Verificar después de corregir
        print("\n🔍 Verificando después de las correcciones...")
        exito_ruff = ejecutar_ruff(check_only=True)
        exito_black = ejecutar_black(check_only=True)
        exito_isort = ejecutar_isort(check_only=True)
        
        if exito_ruff and exito_black and exito_isort:
            print("🎉 ¡Código perfectamente formateado!")
        else:
            print("⚠️ Algunos problemas persisten (requieren corrección manual)")
    else:
        print("❌ Algunas correcciones fallaron")
        print("\n💡 Revisa los errores arriba y corrige manualmente lo necesario")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--fix":
        main_fix()
    else:
        main()

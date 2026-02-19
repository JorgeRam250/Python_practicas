@echo off
echo ========================================
echo Laboratorio 01: Configuracion Python
echo ========================================
echo.

echo Paso 1: Verificando instalacion de Poetry...
poetry --version
if %errorlevel% neq 0 (
    echo Poetry no esta instalado. Por favor, instala Poetry primero:
    echo (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content ^| Invoke-Expression
    pause
    exit /b 1
)

echo.
echo Paso 2: Instalando dependencias del proyecto...
poetry install --with dev

echo.
echo Paso 3: Instalando pre-commit hooks...
poetry run pre-commit install

echo.
echo Paso 4: Analizando codigo con errores PEP 8...
echo --- Analizando con Black ---
poetry run black src/ejemplo_con_errores.py --diff

echo.
echo --- Analizando con isort ---
poetry run isort src/ejemplo_con_errores.py --diff-only

echo.
echo --- Analizando con Ruff ---
poetry run ruff check src/ejemplo_con_errores.py

echo.
echo Paso 5: Corrigiendo automaticamente...
echo --- Corrigiendo con Black ---
poetry run black src/ejemplo_con_errores.py

echo --- Corrigiendo con isort ---
poetry run isort src/ejemplo_con_errores.py

echo --- Corrigiendo con Ruff ---
poetry run ruff check --fix src/ejemplo_con_errores.py

echo.
echo Paso 6: Verificacion final...
echo --- Ejecutando todos los hooks pre-commit ---
poetry run pre-commit run --all-files

echo.
echo ========================================
echo Configuracion completada!
echo ========================================
echo.
echo Para activar el entorno virtual:
echo   poetry shell
echo.
echo Para salir del entorno virtual:
echo   exit
echo.
echo Para ejecutar el ejemplo corregido:
echo   poetry run python src/ejemplo_corregido.py
echo.

pause

# Laboratorio 01: Entorno y Herramientas de Desarrollo Python

## Objetivo del Laboratorio

Configurar un entorno de desarrollo Python profesional utilizando Poetry, herramientas de calidad de código y automatización con pre-commit hooks.

## Estructura del Proyecto

```
Lab_01/
├── pyproject.toml          # Configuración de Poetry y herramientas
├── .pre-commit-config.yaml # Configuración de hooks pre-commit
├── README.md              # Este archivo
└── src/
    ├── __init__.py        # Inicialización del paquete
    ├── ejemplo_con_errores.py    # Código con infracciones PEP 8
    └── ejemplo_corregido.py      # Código corregido siguiendo PEP 8
```

## Herramientas Utilizadas

- **Poetry**: Gestión de dependencias y entornos virtuales
- **Black**: Formateador de código (PEP 8)
- **isort**: Organizador de imports
- **Ruff**: Linter para análisis estático de código
- **pre-commit**: Hooks para automatizar validaciones

## Pasos para Completar el Laboratorio

### 1. Instalación de Poetry

```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | Invoke-Expression

# Verificar instalación
poetry --version
```

### 2. Configuración del Entorno Virtual

```bash
# Navegar al directorio del proyecto
cd Lab_01

# Crear y activar entorno virtual
poetry install

# Activar el entorno virtual
poetry shell
```

### 3. Instalación de Dependencias

Las dependencias ya están definidas en `pyproject.toml`:

```bash
# Instalar dependencias de desarrollo
poetry install --with dev
```

### 4. Configuración de Pre-commit Hooks

```bash
# Instalar hooks pre-commit
poetry run pre-commit install

# Ejecutar hooks en todos los archivos
poetry run pre-commit run --all-files
```

### 5. Corrección de Infracciones PEP 8

#### Analizar código con errores:

```bash
# Formatear con black
poetry run black src/ejemplo_con_errores.py

# Organizar imports con isort
poetry run isort src/ejemplo_con_errores.py

# Analizar con ruff
poetry run ruff check src/ejemplo_con_errores.py

# Corregir automáticamente con ruff
poetry run ruff check --fix src/ejemplo_con_errores.py
```

#### Comparar resultados:

```bash
# Ver diferencias entre archivo original y corregido
diff src/ejemplo_con_errores.py src/ejemplo_corregido.py
```

## Conceptos Clave

### PEP 8 (Style Guide for Python Code)

- **Indentación**: 4 espacios
- **Longitud de línea**: Máximo 79 caracteres (Black usa 88)
- **Imports**: Uno por línea, agrupados por tipo
- **Nomenclatura**: snake_case para variables/funciones, PascalCase para clases
- **Espacios en blanco**: Reglas específicas para operadores y funciones

### PEP 20 (Zen de Python)

Principios que guían el diseño de Python:
- Bello es mejor que feo
- Simple es mejor que complejo
- Legibilidad cuenta
- Explícito es mejor que implícito

## Comandos Útiles

```bash
# Ver estado del entorno virtual
poetry env info

# Ejecutar script en el entorno virtual
poetry run python src/ejemplo_corregido.py

# Actualizar dependencias
poetry update

# Salir del entorno virtual
exit
```

## Verificación Final

Para verificar que todo está configurado correctamente:

1. **Ejecutar todos los hooks**:
   ```bash
   poetry run pre-commit run --all-files
   ```

2. **Verificar que no hay errores de linting**:
   ```bash
   poetry run ruff check src/
   ```

3. **Confirmar que el código está formateado**:
   ```bash
   poetry run black --check src/
   ```

4. **Probar que los imports están ordenados**:
   ```bash
   poetry run isort --check-only src/
   ```

## Recursos Adicionales

- [Documentación oficial de Poetry](https://python-poetry.org/docs/)
- [Guía PEP 8](https://peps.python.org/pep-0008/)
- [Black - The uncompromising code formatter](https://black.readthedocs.io/)
- [Ruff - Extremely fast Python linter](https://docs.astral.sh/ruff/)

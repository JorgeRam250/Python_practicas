# Laboratorio 05: Type Hints y Calidad de Código en Python

## 📋 Descripción del Laboratorio

Este laboratorio se enfoca en implementar buenas prácticas de desarrollo en Python utilizando:

- **Type hints y typing avanzado** (Union, Literal, TypedDict, Protocol)
- **Verificación estática** con mypy/pyright
- **Calidad de código** con PEP 8 mediante ruff/black/isort
- **Integración continua** con pre-commit y checks en CI

## 🎯 Objetivos

1. ✅ Anotar tipos en el código existente
2. ✅ Ejecutar mypy y ruff para verificación
3. ✅ Configurar pre-commit hooks
4. ✅ Integrar linters/formatters en CI

## 📁 Estructura del Proyecto

```
Lab_05/
├── src/
│   ├── __init__.py
│   ├── models.py          # Modelos de datos con TypedDict
│   ├── services.py        # Lógica de negocio con Protocol
│   └── utils.py           # Utilidades con Union y Literal
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── .pre-commit-config.yaml
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## 🚀 Comandos Útiles

```bash
# Instalar dependencias
pip install -r requirements-dev.txt

# Instalar pre-commit hooks
pre-commit install

# Ejecutar verificación de tipos
mypy src/

# Formatear código
black src/ tests/
ruff check src/ tests/
isort src/ tests/

# Ejecutar todos los checks
pre-commit run --all-files
```

## 📚 Conceptos Clave

### Type Hints Básicos
```python
def saludar(nombre: str) -> str:
    return f"Hola, {nombre}"
```

### Union Types
```python
from typing import Union

def procesar_id(id: Union[int, str]) -> str:
    return str(id)
```

### Literal Types
```python
from typing import Literal

def set_estado(estado: Literal["activo", "inactivo", "pendiente"]) -> None:
    pass
```

### TypedDict
```python
from typing import TypedDict

class Usuario(TypedDict):
    id: int
    nombre: str
    email: str
```

### Protocol
```python
from typing import Protocol

class Procesable(Protocol):
    def procesar(self) -> str: ...
```

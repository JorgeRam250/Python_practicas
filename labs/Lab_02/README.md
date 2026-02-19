# Laboratorio de Python: Procesamiento de JSON con Manejo de Errores

## Descripción del Laboratorio

Este laboratorio te ayudará a practicar los fundamentos de Python a través del procesamiento de archivos JSON, implementando manejo robusto de errores y estructuras de control.

## Objetivos de Aprendizaje

- ✅ Sintaxis, indentación, variables y alcance
- ✅ Tipos básicos y colecciones (list, dict, set, tuple)
- ✅ Control de flujo (if, for, while)
- ✅ Errores y excepciones (try-except)
- ✅ Expresiones regulares
- ✅ Lectura y escritura de archivos JSON

## Archivos del Laboratorio

### Ejemplo 1: Sistema de Estudiantes
- **Archivo**: `ejemplo1_estudiantes.py`
- **Datos**: `estudiantes.json`
- **Funcionalidad**: Procesa calificaciones de estudiantes, filtra aprobados y genera estadísticas

### Ejemplo 2: Sistema de Ventas
- **Archivo**: `ejemplo2_ventas.py`
- **Datos**: `ventas.json`
- **Funcionalidad**: Analiza datos de ventas, filtra por categorías y genera reportes

## Pasos para Realizar el Laboratorio

### 1. Entender la Estructura del Código

Ambos ejemplos siguen la misma estructura:

1. **Lectura de JSON**: Función que lee archivos JSON con manejo de errores
2. **Procesamiento**: Funciones que filtran y transforman datos
3. **Análisis**: Funciones que calculan estadísticas y agregados
4. **Salida**: Muestra resultados y opcionalmente guarda archivos

### 2. Ejecutar los Ejemplos

#### Ejemplo 1 - Estudiantes:
```bash
python ejemplo1_estudiantes.py estudiantes.json
```

#### Ejemplo 2 - Ventas:
```bash
# Análisis general
python ejemplo2_ventas.py ventas.json

# Filtrar por categoría específica
python ejemplo2_ventas.py ventas.json Electrónicos
```

### 3. Analizar el Código

Presta atención a:

- **Manejo de Excepciones**: `try-except` para diferentes tipos de errores
- **Validación de Datos**: Comprobación de tipos y valores
- **Estructuras de Control**: Uso de `if`, `for`, `while`
- **Colecciones**: Manipulación de listas y diccionarios
- **Funciones**: Definición y uso de funciones con parámetros

### 4. Modificar y Experimentar

Una vez que entiendas el código, intenta:

1. **Agregar nuevos filtros** (ej: filtrar por rango de edad)
2. **Crear nuevas estadísticas** (ej: mediana, moda)
3. **Manejar más tipos de errores**
4. **Agregar validaciones adicionales**

## Conceptos Clave Explicados

### 1. Manejo de Excepciones

```python
try:
    # Código que puede fallar
    with open(archivo, 'r') as f:
        datos = json.load(f)
except FileNotFoundError:
    print("El archivo no existe")
except json.JSONDecodeError:
    print("Formato JSON inválido")
except Exception as e:
    print(f"Error inesperado: {e}")
```

### 2. Estructuras de Control

```python
# Condicional
if calificacion >= 70:
    print("Aprobado")
else:
    print("Reprobado")

# Bucle for
for estudiante in estudiantes:
    print(estudiante['nombre'])

# List comprehension
aprobados = [e for e in estudiantes if e['calificacion'] >= 70]
```

### 3. Tipos de Datos y Colecciones

```python
# Lista (mutable, ordenada)
numeros = [1, 2, 3, 4, 5]

# Diccionario (clave-valor)
persona = {"nombre": "Ana", "edad": 20}

# Tupla (inmutable, ordenada)
coordenadas = (10, 20)

# Set (único, desordenado)
categorias = {"Electrónicos", "Libros", "Muebles"}
```

### 4. Expresiones Regulares

```python
import re

# Validar formato de fecha
patron = r'^\d{4}-\d{2}-\d{2}$'
if re.match(patron, fecha_str):
    print("Fecha válida")
```

## Errores Comunes y Soluciones

### 1. IndentationError
**Problema**: Espacios inconsistentes
**Solución**: Usar siempre 4 espacios o configurar tu editor

### 2. KeyError
**Problema**: Acceder a clave que no existe
**Solución**: Usar `.get()` con valor por defecto
```python
# Incorrecto
nombre = estudiante['nombre']  # Puede fallar

# Correcto
nombre = estudiante.get('nombre', 'Desconocido')
```

### 3. TypeError
**Problema**: Operación con tipos incompatibles
**Solución**: Validar tipos antes de operar
```python
if isinstance(edad, int) and edad > 0:
    # Procesar edad
```

## Buenas Prácticas

1. **Nombres descriptivos**: Usa nombres claros para variables y funciones
2. **Comentarios**: Documenta el código complejo
3. **Validación**: Siempre valida datos de entrada
4. **Manejo de errores**: Anticipa y maneja posibles errores
5. **Modularidad**: Divide el código en funciones pequeñas y reutilizables

## Ejercicios Adicionales

1. **Crear un sistema de inventario** que maneje stock y alertas
2. **Implementar un sistema de calificaciones** con diferentes ponderaciones
3. **Desarrollar un analizador de logs** que extraiga patrones específicos
4. **Construir un procesador de encuestas** con diferentes tipos de preguntas

## Recursos Adicionales

- [Documentación oficial de Python](https://docs.python.org/3/)
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/)

---

**¡Feliz aprendizaje!** 🐍✨

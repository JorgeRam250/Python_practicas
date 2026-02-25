# Laboratorio de Python: Funciones y Programación "Pythonic"

## Descripción del Laboratorio

Este laboratorio te ayudará a entender y aplicar conceptos avanzados de Python relacionados con funciones y programación "pythonic". Aprenderás a:

- **Decoradores**: Implementar reintentos automáticos con backoff exponencial
- **Generadores**: Crear generadores por lotes para procesamiento eficiente de datos
- **Context Managers**: Medir tiempo de ejecución y manejar recursos de forma segura

## Objetivos de Aprendizaje

Al finalizar este laboratorio, serás capaz de:

1. Diseñar APIs de funciones claras y expresivas
2. Implementar decoradores y generadores útiles
3. Crear context managers para recursos
4. Combinar todos los conceptos en soluciones prácticas

## Estructura de Archivos

```
Lab_03
├── README.md                # Este archivo - Guía completa
├── decoradores.py           # Decorador de reintentos con backoff
├── generadores.py           # Generadores por lotes y otros útiles
├── context_managers.py      # Context managers de temporización
├── ejemplos_practicos.py    # Ejemplos completos y avanzados
├── ejemplo_simple.py        # Ejemplos simplificados para principiantes
└── requirements.txt         # Dependencias del proyecto
```

## Guía Paso a Paso

### Paso 1: Entender los Conceptos Básicos

#### **Decoradores**
Un decorador es una función que modifica el comportamiento de otra función. Piensa en ello como un "envoltorio" que añade funcionalidad.

```python
@decorador
def mi_funcion():
    pass
```

#### **Generadores**
Un generador es una función que produce valores uno a uno, en lugar de crearlos todos a la vez. Es más eficiente en memoria.

```python
def mi_generador():
    yield 1
    yield 2
    yield 3
```

#### **Context Managers**
Un context manager maneja recursos automáticamente (como archivos o conexiones) usando `with`.

```python
with mi_context_manager():
    # El recurso se maneja automáticamente
    pass
```

### Paso 2: Ejecutar los Ejemplos

#### Para Principiantes: `ejemplo_simple.py`
```bash
python ejemplo_simple.py
```

Este archivo contiene ejemplos simplificados con explicaciones detalladas.

#### Para Usuarios Avanzados: `ejemplos_practicos.py`
```bash
python ejemplos_practicos.py
```

Este archivo muestra implementaciones más completas y profesionales.

### Paso 3: Estudiar el Código

#### **Decorador de Reintentos** (`decoradores.py`)
```python
@retry_con_backoff(max_retries=3, delay=1, backoff_factor=2)
def funcion_inestable():
    # Puede fallar, se reintentará automáticamente
    pass
```

**Características:**
- Reintenta automáticamente si la función falla
- Usa backoff exponencial (espera más tiempo entre reintentos)
- Permite configurar número máximo de reintentos
- Maneja diferentes tipos de excepciones

#### **Generador por Lotes** (`generadores.py`)
```python
for lote in batch_generator(datos_grandes, tamaño_lote=100):
    # Procesar cada lote individualmente
    procesar_lote(lote)
```

**Características:**
- Divide datos grandes en lotes más pequeños
- Ahorra memoria al no cargar todo a la vez
- Ideal para procesar archivos grandes o APIs

#### ⏱ **Context Manager de Temporización** (`context_managers.py`)
```python
with Timer("Procesamiento de datos"):
    # Código cuyo tiempo queremos medir
    procesar_datos()
```

**Características:**
- Mide automáticamente el tiempo de ejecución
- Muestra mensajes informativos
- Maneja excepciones correctamente

## Ejemplos Prácticos

### Ejemplo 1: API con Reintentos Automáticos
```python
@retry_con_backoff(max_retries=3, delay=2)
def llamar_api_externa():
    response = requests.get("https://api.ejemplo.com/datos")
    response.raise_for_status()
    return response.json()
```

### Ejemplo 2: Procesamiento de Archivos Grandes
```python
def procesar_archivo_grande(ruta_archivo):
    with Timer("Procesamiento de archivo"):
        for lote in batch_generator(leer_archivo(ruta_archivo), 1000):
            procesar_lote(lote)
```

### Ejemplo 3: Descarga con Reintentos y Temporización
```python
@retry_con_backoff(max_retries=5, delay=1)
def descargar_con_temporizacion(url, destino):
    with Timer(f"Descarga desde {url}"):
        # Lógica de descarga
        pass
```

## Instalación de Dependencias

```bash
pip install -r requirements.txt
```

Las dependencias incluyen:
- `psutil`: Para medición de memoria
- Otras utilidades para los ejemplos

## Explicación Detallada de Conceptos

### Decoradores

Un decorador es una función que:
1. Recibe otra función como parámetro
2. Retorna una nueva función modificada
3. Se aplica usando el símbolo `@`

**¿Por qué usar decoradores?**
- Reutilización de código
- Separación de responsabilidades
- Sintaxis limpia y legible

### Generadores

Un generador:
1. Usa `yield` en lugar de `return`
2. Pausa su ejecución y la reanuda más tarde
3. Es más eficiente en memoria

**¿Por qué usar generadores?**
- Procesamiento de datos grandes
- Streams de datos infinitos
- Ahorro de memoria

### Context Managers

Un context manager:
1. Implementa `__enter__` y `__exit__`
2. Se usa con la palabra clave `with`
3. Garantiza limpieza de recursos

**¿Por qué usar context managers?**
- Manejo automático de recursos
- Prevención de fugas de memoria
- Código más seguro y legible



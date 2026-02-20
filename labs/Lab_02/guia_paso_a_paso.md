# Guía Paso a Paso para el Laboratorio de Python

## 🎯 Objetivo
Completar el laboratorio de procesamiento de JSON con manejo de errores, aprendiendo los fundamentos de Python.

## 📋 Requisitos Previos
- Python 3.8 o superior instalado
- Editor de código (VS Code, PyCharm, etc.)
- Conocimientos básicos de programación (variables, bucles)

---

## 🚀 PASO 1: Configuración del Entorno

### 1.1 Verificar instalación de Python
```bash
python --version
# o
python3 --version
```

### 1.2 Crear carpeta de trabajo
```bash
mkdir laboratorio_python
cd laboratorio_python
```

### 1.3 Descargar los archivos del laboratorio
Asegúrate de tener todos los archivos:
- `ejemplo1_estudiantes.py`
- `ejemplo2_ventas.py`
- `estudiantes.json`
- `ventas.json`
- `README.md`
- `guia_paso_a_paso.md`

---

## 📚 PASO 2: Entender la Estructura de los Archivos

### 2.1 Analizar el archivo JSON de estudiantes
Abre `estudiantes.json` y observa:
- Es un objeto con una clave `"estudiantes"`
- El valor es una lista de objetos
- Cada estudiante tiene: id, nombre, edad, calificacion, carrera

### 2.2 Analizar el archivo JSON de ventas
Abre `ventas.json` y observa:
- Estructura similar al anterior
- Cada venta tiene: id, producto, categoria, cantidad, precio, fecha

---

## 🔍 PASO 3: Estudiar el Código (Ejemplo 1)

### 3.1 Abrir `ejemplo1_estudiantes.py`

#### Función `leer_archivo_json(ruta_archivo)`
```python
def leer_archivo_json(ruta_archivo: str) -> Dict[str, Any]:
```
**¿Qué hace?**: Lee un archivo JSON y maneja errores

**Conceptos aprendidos**:
- **Type hints**: `ruta_archivo: str` indica que el parámetro es un string
- **Return type**: `-> Dict[str, Any]` indica que retorna un diccionario
- **Manejo de excepciones**: `try-except` para diferentes errores
- **Context manager**: `with open()` asegura que el archivo se cierre

#### Función `filtrar_estudiantes_aprobados(estudiantes)`
```python
def filtrar_estudiantes_aprobados(estudiantes: List[Dict]) -> List[Dict]:
```
**¿Qué hace?**: Filtra estudiantes con calificación >= 70

**Conceptos aprendidos**:
- **List comprehension**: Crear listas de forma concisa
- **Métodos de diccionario**: `.get()` para acceder seguro a valores
- **Bucles for**: Iterar sobre listas

#### Función `calcular_estadisticas(estudiantes)`
```python
def calcular_estadisticas(estudiantes: List[Dict]) -> Dict[str, float]:
```
**¿Qué hace?**: Calcula promedio, máximo y mínimo de calificaciones

**Conceptos aprendidos**:
- **Funciones built-in**: `sum()`, `max()`, `min()`, `len()`
- **Diccionarios**: Crear y retornar estructuras de datos
- **Validación**: Comprobar listas vacías

---

## 🛠️ PASO 4: Ejecutar y Probar

### 4.1 Ejecutar el Ejemplo 1
```bash
python ejemplo1_estudiantes.py estudiantes.json
```

**Salida esperada**:
```
✅ Archivo 'estudiantes.json' leído correctamente
📋 Total de estudiantes: 8
📊 Estudiantes aprobados: 5/8

📈 Estadísticas generales:
   Promedio: 75.62
   Máximo: 95
   Mínimo: 45

🎯 Estadísticas de aprobados:
   Promedio: 87.00
   Máximo: 95
   Mínimo: 75

✅ Lista de estudiantes aprobados:
   1. Ana García: 85
   2. Carlos López: 92
   3. Juan Martínez: 75
   4. Pedro Díaz: 88
   5. Sofía Hernández: 95
```

### 4.2 Probar con errores
Intenta ejecutar con archivos que no existen para ver el manejo de errores:
```bash
python ejemplo1_estudiantes.py no_existe.json
```

---

## 🔧 PASO 5: Modificar el Código (Práctica Guiada)

### 5.1 Agregar un nuevo filtro
Vamos a agregar una función para filtrar por carrera:

```python
def filtrar_por_carrera(estudiantes: List[Dict], carrera: str) -> List[Dict]:
    """
    Filtra estudiantes por carrera específica
    
    Args:
        estudiantes: Lista de estudiantes
        carrera: Carrera a filtrar
        
    Returns:
        Lista de estudiantes de la carrera especificada
    """
    filtrados = []
    for estudiante in estudiantes:
        if estudiante.get('carrera') == carrera:
            filtrados.append(estudiante)
    
    print(f"📊 Estudiantes de '{carrera}': {len(filtrados)}")
    return filtrados
```

### 5.2 Integrar el nuevo filtro
Modifica la función `procesar_datos_estudiantes` para usar el nuevo filtro:

```python
# Agrega después de calcular estadísticas generales
carrera_filtro = "Ingeniería"  # Puedes cambiar esto
estudiantes_ingenieria = filtrar_por_carrera(estudiantes, carrera_filtro)

if estudiantes_ingenieria:
    stats_ingenieria = calcular_estadisticas(estudiantes_ingenieria)
    print(f"\n🎯 Estadísticas de {carrera_filtro}:")
    print(f"   Promedio: {stats_ingenieria['promedio']:.2f}")
    print(f"   Máximo: {stats_ingenieria['maximo']}")
    print(f"   Mínimo: {stats_ingenieria['minimo']}")
```

### 5.3 Probar las modificaciones
Ejecuta nuevamente el script para ver los cambios.

---

## 🎯 PASO 6: Practicar con el Ejemplo 2

### 6.1 Entender las diferencias
El Ejemplo 2 introduce conceptos adicionales:
- **Expresiones regulares** para validación de fechas
- **Agregaciones más complejas**
- **Generación de reportes en JSON**
- **Filtrado por categorías**

### 6.2 Ejecutar el Ejemplo 2
```bash
# Análisis general
python ejemplo2_ventas.py ventas.json

# Filtrar por categoría
python ejemplo2_ventas.py ventas.json Electrónicos
```

### 6.3 Analizar la salida
Observa cómo se genera un reporte JSON adicional con los resultados.

---

## 💡 PASO 7: Ejercicios Prácticos

### Ejercicio 1: Agregar Validación
Modifica el Ejemplo 1 para validar que:
- La edad esté entre 18 y 100 años
- La calificación esté entre 0 y 100
- El nombre no esté vacío

### Ejercicio 2: Crear Nuevas Estadísticas
Agrega funciones para calcular:
- Mediana de calificaciones
- Moda (carrera más común)
- Desviación estándar

### Ejercicio 3: Mejorar el Manejo de Errores
Agrega manejo para:
- Datos duplicados
- Campos faltantes
- Tipos de datos incorrectos

### Ejercicio 4: Exportar Resultados
Modifica el Ejemplo 1 para guardar los resultados en un nuevo archivo JSON.

---

## 🔍 PASO 8: Análisis del Código

### 8.1 Identificar Patrones
Busca estos patrones en el código:

1. **Validación de entrada**:
   ```python
   if not isinstance(datos, dict):
       raise ValueError("El JSON debe ser un objeto")
   ```

2. **Manejo seguro de diccionarios**:
   ```python
   nombre = estudiante.get('nombre', 'Desconocido')
   ```

3. **Procesamiento con list comprehension**:
   ```python
   aprobados = [e for e in estudiantes if e.get('calificacion', 0) >= 70]
   ```

4. **Manejo robusto de errores**:
   ```python
   try:
       # Código que puede fallar
   except SpecificError as e:
       # Manejo específico
   except Exception as e:
       # Manejo general
   ```

### 8.2 Entender el Flujo
Dibuja un diagrama de flujo del programa:
1. Inicio → Leer argumentos
2. Validar archivo → Leer JSON
3. Procesar datos → Filtrar
4. Calcular estadísticas → Mostrar resultados
5. Fin

---

## ✅ PASO 9: Verificación Final

### 9.1 Checklist de Conceptos Aprendidos
- [ ] Sintaxis y indentación de Python
- [ ] Variables y tipos de datos
- [ ] Listas y diccionarios
- [ ] Control de flujo (if, for, while)
- [ ] Funciones y parámetros
- [ ] Manejo de excepciones (try-except)
- [ ] Lectura/escritura de archivos
- [ ] Procesamiento JSON
- [ ] Expresiones regulares básicas

### 9.2 Autoevaluación
Responde estas preguntas:
1. ¿Qué es el type hinting y por qué es útil?
2. ¿Cuándo usarías `.get()` vs `[]` para acceder a diccionarios?
3. ¿Por qué es importante el manejo de excepciones?
4. ¿Qué ventajas tienen las list comprehensions?
5. ¿Cómo validarías datos de entrada en Python?

---

## 🚀 PASO 10: Siguientes Pasos

### 10.1 Proyectos Sugeridos
1. **Sistema de inventario**: Maneja stock, productos, proveedores
2. **Analizador de logs**: Extrae información de archivos de log
3. **Procesador de encuestas**: Analiza resultados de cuestionarios
4. **Sistema de reservas**: Maneja fechas, disponibilidad, confirmaciones

### 10.2 Temas Avanzados
- Programación orientada a objetos
- Módulos y paquetes
- Testing con pytest
- Virtual environments
- APIs y web scraping

---

## 📞 Ayuda y Soporte

Si tienes problemas:
1. Revisa la sintaxis y indentación
2. Verifica los mensajes de error
3. Consulta la documentación oficial
4. Practica con ejemplos más simples
5. No dudes en experimentar

**¡Recuerda**: La práctica constante es la clave para dominar Python. 🐍✨

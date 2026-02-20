# Gu铆a Paso a Paso para el Laboratorio de Python

## 馃幆 Objetivo
Completar el laboratorio de procesamiento de JSON con manejo de errores, aprendiendo los fundamentos de Python.

## 馃搵 Requisitos Previos
- Python 3.8 o superior instalado
- Editor de c贸digo (VS Code, PyCharm, etc.)
- Conocimientos b谩sicos de programaci贸n (variables, bucles)

---

## 馃殌 PASO 1: Configuraci贸n del Entorno

### 1.1 Verificar instalaci贸n de Python
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
Aseg煤rate de tener todos los archivos:
- `Sistema ventas`
- `ventas.json`
- `README.md`
- `guia_paso_a_paso.md`

---

## 馃摎 PASO 2: Entender la Estructura de los Archivos

### 2.1 Analizar el archivo JSON de ventas
Abre `ventas.json` y observa:
- Estructura similar al anterior
- Cada venta tiene: id, producto, categoria, cantidad, precio, fecha

---

## 馃幆 PASO 3: Practicar con el ejemplo Sistema_ventas

### 3.1 Entender las diferencias
El Sistema_ventas introduce conceptos adicionales:
- **Expresiones regulares** para validaci贸n de fechas
- **Agregaciones m谩s complejas**
- **Generaci贸n de reportes en JSON**
- **Filtrado por categor铆as**

### 3.2 Ejecutar el Sistema_ventas
```bash
# An谩lisis general
python ejemplo2_ventas.py ventas.json

# Filtrar por categor铆a
python ejemplo2_ventas.py ventas.json Electr贸nicos
```

### 3.3 Analizar la salida
Observa c贸mo se genera un reporte JSON adicional con los resultados.

---

---

## 馃攳 PASO 4: An谩lisis del C贸digo

Dibuja un diagrama de flujo del programa:
1. Inicio 鈫?Leer argumentos
2. Validar archivo 鈫?Leer JSON
3. Procesar datos 鈫?Filtrar
4. Calcular estad铆sticas 鈫?Mostrar resultados
5. Fin

---

## 鉁?PASO 5: Verificaci贸n Final

### 5.1 Checklist de Conceptos Aprendidos
- [ ] Sintaxis y indentaci贸n de Python
- [ ] Variables y tipos de datos
- [ ] Listas y diccionarios
- [ ] Control de flujo (if, for, while)
- [ ] Funciones y par谩metros
- [ ] Manejo de excepciones (try-except)
- [ ] Lectura/escritura de archivos
- [ ] Procesamiento JSON
- [ ] Expresiones regulares b谩sicas

### 5.2 Autoevaluaci贸n
Responde estas preguntas:
1. 驴Qu茅 es el type hinting y por qu茅 es 煤til?
2. 驴Cu谩ndo usar铆as `.get()` vs `[]` para acceder a diccionarios?
3. 驴Por qu茅 es importante el manejo de excepciones?
4. 驴Qu茅 ventajas tienen las list comprehensions?
5. 驴C贸mo validar铆as datos de entrada en Python?

---

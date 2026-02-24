# Laboratorio: HTTP y Consumo de APIs con Python

## 🎯 Objetivos del Laboratorio

Este laboratorio te enseñará a construir clientes HTTP robustos en Python utilizando la librería `httpx`. Aprenderás a:

- Realizar peticiones HTTP GET, POST, PUT, DELETE
- Configurar timeouts para evitar esperas infinitas
- Implementar reintentos automáticos para manejar fallos
- Descargar archivos grandes usando streaming (sin agotar la memoria)
- Manejar errores de forma profesional

## 📚 Conceptos Clave

### 1. ¿Qué es HTTPx?
`httpx` es una librería HTTP moderna para Python que soporta:
- HTTP/1.1 y HTTP/2
- Síncrono y asíncrono
- Cliente y servidor
- Tiene una API muy similar a `requests` pero más potente

### 2. Timeouts
Los timeouts evitan que tu programa se quede esperando indefinidamente:
- **Connect timeout**: Tiempo máximo para establecer conexión
- **Read timeout**: Tiempo máximo para recibir respuesta
- **Write timeout**: Tiempo máximo para enviar datos

### 3. Reintentos
Los reintentos automáticos ayudan cuando:
- La red es inestable
- El servidor está temporalmente sobrecargado
- Hay intermitencias en la conexión

### 4. Streaming
El streaming permite descargar archivos grandes:
- Sin cargar todo el archivo en memoria
- Procesando el archivo por partes (chunks)
- Ideal para videos, imágenes grandes, datasets, etc.

## 🛠️ Instalación

```bash
pip install httpx
```

## 📁 Estructura del Proyecto

```
Windsurf/
├── README.md                 # Este archivo
├── requirements.txt          # Dependencias
├── ejemplo1_basico.py        # Ejemplo 1: Cliente básico
├── ejemplo2_reintentos.py    # Ejemplo 2: Con reintentos y timeouts
├── ejemplo3_streaming.py     # Ejemplo 3: Streaming de archivos
└── utils/                    # Utilidades reutilizables
    ├── __init__.py
    ├── http_client.py        # Cliente HTTP reutilizable
    └── exceptions.py         # Excepciones personalizadas
```

## 🚀 Ejemplos del Laboratorio

### Ejemplo 1: Cliente HTTP Básico
Aprende los fundamentos de httpx con peticiones simples.

### Ejemplo 2: Cliente con Reintentos y Timeouts
Construye un cliente robusto que maneja errores automáticamente.

### Ejemplo 3: Streaming de Archivos Grandes
Descarga archivos pesados sin consumir toda la memoria RAM.

## 📋 Pasos para Completar el Laboratorio

1. **Instalar dependencias**: `pip install -r requirements.txt`
2. **Estudiar Ejemplo 1**: Entiende los conceptos básicos
3. **Analizar Ejemplo 2**: Aprende sobre resiliencia
4. **Practicar Ejemplo 3**: Domina el streaming
5. **Experimentar**: Modifica los códigos y prueba diferentes APIs

## 🔧 Requisitos Previos

- Python 3.7 o superior
- Conexión a internet
- Editor de código (VS Code, PyCharm, etc.)

## 📖 Recursos Adicionales

- [Documentación oficial de httpx](https://www.python-httpx.org/)
- [HTTP Status Codes](https://developer.mozilla.org/es/docs/Web/HTTP/Status)
- [APIs públicas para practicar](https://github.com/public-apis/public-apis)

---

**¡Comencemos!** 🚀 Sigue los ejemplos en orden para mejor comprensión.

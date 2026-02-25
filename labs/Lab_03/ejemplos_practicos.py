"""
Ejemplos prácticos del laboratorio de Python
Demostración de decoradores, generadores y context managers
"""

import time
import random
from decoradores import retry_con_backoff, funcion_inestable, procesar_datos
from generadores import batch_generator, fibonacci_generator, rango_infinito, generador_primos
from context_managers import Timer, temporizador_simple, medicion_memoria, ArchivoSeguro, conexion_bd_simulada


def ejemplo_decorador_reintentos():
    """
    Ejemplo 1: Uso del decorador de reintentos con backoff
    """
    print("=" * 60)
    print("🚀 EJEMPLO 1: Decorador de Reintentos con Backoff")
    print("=" * 60)
    
    # Ejemplo con función inestable
    print("\n📡 Probando función inestable:")
    try:
        resultado = funcion_inestable(probabilidad_fallo=0.4)
        print(f"Resultado: {resultado}")
    except Exception as e:
        print(f"Error final: {e}")
    
    # Ejemplo con procesamiento de datos
    print("\n📊 Probando procesamiento de datos:")
    try:
        datos = [1, 2, 3, 4, 5]
        resultado = procesar_datos(datos)
        print(f"Datos procesados: {resultado}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Ejemplo con datos inválidos
    print("\n❌ Probando con datos inválidos:")
    try:
        resultado = procesar_datos("no soy una lista")
    except Exception as e:
        print(f"Error esperado: {e}")


def ejemplo_generador_lotes():
    """
    Ejemplo 2: Uso del generador por lotes
    """
    print("\n" + "=" * 60)
    print("🚀 EJEMPLO 2: Generador por Lotes")
    print("=" * 60)
    
    # Datos de ejemplo
    datos = list(range(1, 21))  # Números del 1 al 20
    tamaño_lote = 5
    
    print(f"\n📦 Procesando {len(datos)} elementos en lotes de {tamaño_lote}:")
    
    for i, lote in enumerate(batch_generator(datos, tamaño_lote), 1):
        print(f"Lote {i}: {lote}")
        # Simular procesamiento
        time.sleep(0.1)
    
    # Ejemplo con Fibonacci
    print(f"\n🔢 Primer 10 números de Fibonacci:")
    for i, num in enumerate(fibonacci_generator(10), 1):
        print(f"F({i-1}) = {num}")
    
    # Ejemplo con números primos
    print(f"\n🔢 Números primos hasta 30:")
    primos = list(generador_primos(30))
    print(primos)


def ejemplo_context_managers():
    """
    Ejemplo 3: Uso de context managers
    """
    print("\n" + "=" * 60)
    print("🚀 EJEMPLO 3: Context Managers")
    print("=" * 60)
    
    # Timer básico
    print("\n⏱️  Medición de tiempo con Timer:")
    with Timer("Procesamiento de datos"):
        # Simular trabajo
        datos = [random.random() for _ in range(1000000)]
        suma = sum(datos)
        print(f"Suma calculada: {suma:.2f}")
    
    # Temporizador simple
    print("\n⏱️  Temporizador simple:")
    with temporizador_simple():
        time.sleep(0.5)
        print("Trabajo en progreso...")
    
    # Medición de memoria
    print("\n🧠 Medición de memoria:")
    with medicion_memoria():
        # Crear lista grande
        lista_grande = [i for i in range(1000000)]
        print(f"Lista creada con {len(lista_grande)} elementos")
    
    # Archivo seguro
    print("\n📁 Manejo seguro de archivos:")
    with ArchivoSeguro("ejemplo.txt", "w") as f:
        f.write("Este es un archivo de ejemplo\n")
        f.write("Creado con el context manager seguro\n")
    
    # Leer el archivo
    with ArchivoSeguro("ejemplo.txt", "r") as f:
        contenido = f.read()
        print(f"Contenido del archivo:\n{contenido}")
    
    # Conexión a base de datos simulada
    print("\n🗄️  Conexión a base de datos simulada:")
    with conexion_bd_simulada("mi_base.db") as conn:
        resultado = conn.query("SELECT * FROM usuarios")
        print(f"Resultado: {resultado}")


def ejemplo_combinado():
    """
    Ejemplo 4: Combinando todos los conceptos
    """
    print("\n" + "=" * 60)
    print("🚀 EJEMPLO 4: Combinación de Todos los Conceptos")
    print("=" * 60)
    
    # Función con decorador que usa generadores y se mide con context manager
    @retry_con_backoff(max_retries=2, delay=0.5)
    def procesar_lotes_con_reintentos(datos, tamaño_lote=3):
        """
        Función que procesa datos por lotes y puede fallar
        """
        if random.random() < 0.3:  # 30% probabilidad de fallo
            raise RuntimeError("Error aleatorio en procesamiento")
        
        resultados = []
        for lote in batch_generator(datos, tamaño_lote):
            # Simular procesamiento intensivo
            time.sleep(0.1)
            resultado_lote = [x * 2 for x in lote]
            resultados.extend(resultado_lote)
        
        return resultados
    
    # Usar todo junto
    print("\n🔄 Procesamiento completo con reintentos, lotes y temporización:")
    
    with Timer("Procesamiento completo"):
        try:
            datos = list(range(1, 16))
            resultado = procesar_lotes_con_reintentos(datos, tamaño_lote=4)
            print(f"✅ Resultado final: {resultado}")
        except Exception as e:
            print(f"❌ Error en procesamiento: {e}")


if __name__ == "__main__":
    print("🐍 LABORATORIO DE PYTHON: Funciones y Programación Pythonic")
    print("=" * 80)
    
    # Ejecutar todos los ejemplos
    ejemplo_decorador_reintentos()
    ejemplo_generador_lotes()
    ejemplo_context_managers()
    ejemplo_combinado()
    
    print("\n" + "=" * 80)
    print("🎉 ¡Laboratorio completado!")
    print("=" * 80)

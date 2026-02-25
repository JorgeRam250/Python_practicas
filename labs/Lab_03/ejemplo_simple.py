"""
Ejemplo simple y directo para entender los conceptos básicos
Ideal para principiantes
"""

import time
import random


# ===============================================================
# EJEMPLO 1: DECORADOR DE REINTENTOS (Versión simplificada)
# ===============================================================

def reintento_simple(max_reintentos=3):
    """
    Decorador simple que reintenta una función si falla
    """
    def decorador(funcion):
        def nueva_funcion(*args, **kwargs):
            for intento in range(max_reintentos):
                try:
                    return funcion(*args, **kwargs)
                except Exception as e:
                    print(f"Intento {intento + 1} fallido: {e}")
                    if intento == max_reintentos - 1:
                        print("Maximo de reintentos alcanzado")
                        raise
                    print(f"Esperando 1 segundo antes de reintentar...")
                    time.sleep(1)
        return nueva_funcion
    return decorador


@reintento_simple(max_reintentos=3)
def conectar_servidor():
    """
    Función que simula conectar a un servidor (falla a veces)
    """
    if random.random() < 0.5:  # 50% probabilidad de fallo
        raise ConnectionError("No se puede conectar al servidor")
    return "Conectado exitosamente"


# ===============================================================
# EJEMPLO 2: GENERADOR POR LOTES (Versión simplificada)
# ===============================================================

def dividir_en_lotes(lista, tamaño_lote):
    """
    Generador que divide una lista en lotes más pequeños
    """
    lote_actual = []
    for elemento in lista:
        lote_actual.append(elemento)
        if len(lote_actual) == tamaño_lote:
            yield lote_actual
            lote_actual = []
    
    # Devolver el último lote si no está vacío
    if lote_actual:
        yield lote_actual


# ===============================================================
# EJEMPLO 3: CONTEXT MANAGER DE TEMPORIZACIÓN (Versión simplificada)
# ===============================================================

class Temporizador:
    """
    Context manager para medir tiempo de ejecución
    """
    def __init__(self, nombre="Tarea"):
        self.nombre = nombre
        self.inicio = None
        
    def __enter__(self):
        self.inicio = time.time()
        print(f"Iniciando: {self.nombre}")
        return self
        
    def __exit__(self, tipo_error, valor_error, traza_error):
        fin = time.time()
        duracion = fin - self.inicio
        print(f"{self.nombre} completada en {duracion:.2f} segundos")
        return False  # No suprimir errores


# ===============================================================
# FUNCIONES PARA DEMOSTRAR LOS EJEMPLOS
# ===============================================================

def demostrar_decorador():
    """
    Demostración del decorador de reintentos
    """
    print("\n" + "="*50)
    print("DEMO 1: Decorador de Reintentos")
    print("="*50)
    
    try:
        resultado = conectar_servidor()
        print(f"Resultado: {resultado}")
    except Exception as e:
        print(f"Error final: {e}")


def demostrar_generador():
    """
    Demostración del generador por lotes
    """
    print("\n" + "="*50)
    print("DEMO 2: Generador por Lotes")
    print("="*50)
    
    # Lista de números del 1 al 15
    numeros = list(range(1, 16))
    print(f"Numeros a procesar: {numeros}")
    
    print("\nProcesando en lotes de 4:")
    for i, lote in enumerate(dividir_en_lotes(numeros, 4), 1):
        print(f"Lote {i}: {lote}")
        # Simular trabajo
        time.sleep(0.2)


def demostrar_temporizador():
    """
    Demostración del context manager de temporización
    """
    print("\n" + "="*50)
    print("DEMO 3: Temporizador")
    print("="*50)
    
    # Medir tiempo de una operación
    with Temporizador("Cálculo matemático"):
        # Simular trabajo intensivo
        resultado = sum(i**2 for i in range(100000))
        print(f"Resultado del calculo: {resultado}")
    
    # Medir otra operación
    with Temporizador("Procesamiento de texto"):
        texto = "hola " * 10000
        palabras = texto.split()
        print(f"Procesadas {len(palabras)} palabras")


def demostrar_combinado():
    """
    Demostración combinando todos los conceptos
    """
    print("\n" + "="*50)
    print("DEMO 4: Todos los conceptos juntos")
    print("="*50)
    
    @reintento_simple(max_reintentos=2)
    def procesar_datos_con_lotes(datos):
        """
        Función que procesa datos por lotes y puede fallar
        """
        if random.random() < 0.4:  # 40% probabilidad de fallo
            raise RuntimeError("Error en procesamiento")
        
        resultados = []
        for lote in dividir_en_lotes(datos, 3):
            time.sleep(0.1)  # Simular trabajo
            resultados.extend([x * 2 for x in lote])
        
        return resultados
    
    # Usar todo junto
    with Temporizador("Procesamiento completo"):
        try:
            datos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            resultado = procesar_datos_con_lotes(datos)
            print(f"Datos procesados: {resultado}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    print("EJEMPLOS SIMPLES DE PYTHON")
    print("Conceptos: Decoradores, Generadores, Context Managers")
    print("="*60)
    
    # Ejecutar todas las demostraciones
    demostrar_decorador()
    demostrar_generador()
    demostrar_temporizador()
    demostrar_combinado()
    
    print("\n" + "="*60)
    print("Fin de los ejemplos!")
    print("="*60)

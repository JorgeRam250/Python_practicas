"""
Decoradores para el laboratorio de Python
Decorador de reintentos con backoff exponencial
"""

import time
import random
from functools import wraps


def retry_con_backoff(max_retries=3, delay=1, backoff_factor=2, exceptions=(Exception,)):
    """
    Decorador que reintenta una función con backoff exponencial
    
    Args:
        max_retries: Número máximo de reintentos (default: 3)
        delay: Tiempo inicial de espera en segundos (default: 1)
        backoff_factor: Factor multiplicativo del delay (default: 2)
        exceptions: Tupla de excepciones a capturar (default: Exception)
    
    Returns:
        Función decorada con capacidad de reintento
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        print(f"❌ Fallo después de {max_retries} intentos. Error: {e}")
                        raise
                    
                    print(f"⚠️  Intento {attempt + 1} falló. Reintentando en {current_delay:.2f}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff_factor
                    
                    # Añadir jitter para evitar thundering herd
                    current_delay += random.uniform(0, 0.1)
            
        return wrapper
    return decorator


# Ejemplo de función que falla para probar el decorador
@retry_con_backoff(max_retries=3, delay=0.5, backoff_factor=2)
def funcion_inestable(probabilidad_fallo=0.7):
    """
    Función que simula una operación inestable
    """
    import random
    if random.random() < probabilidad_fallo:
        raise ConnectionError("Conexión fallida simulada")
    return "✅ Operación exitosa"


@retry_con_backoff(max_retries=2, delay=1, exceptions=(ValueError, TypeError))
def procesar_datos(datos):
    """
    Función que procesa datos y puede fallar con ValueError o TypeError
    """
    if not isinstance(datos, (list, tuple)):
        raise TypeError("Los datos deben ser una lista o tupla")
    
    if not datos:
        raise ValueError("Los datos no pueden estar vacíos")
    
    return [x * 2 for x in datos]

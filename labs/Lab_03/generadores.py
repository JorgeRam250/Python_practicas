"""
Generadores para el laboratorio de Python
Generador por lotes y otros generadores útiles
"""

from typing import Iterator, List, Any, Iterable


def batch_generator(data: Iterable[Any], batch_size: int) -> Iterator[List[Any]]:
    """
    Generador que divide los datos en lotes más pequeños
    
    Args:
        data: Iterable de datos a procesar
        batch_size: Tamaño de cada lote
    
    Yields:
        Listas con los datos divididos en lotes
    
    Example:
        >>> for batch in batch_generator([1,2,3,4,5,6,7,8,9], 3):
        ...     print(batch)
        [1, 2, 3]
        [4, 5, 6]
        [7, 8, 9]
    """
    batch = []
    for item in data:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    
    # Yield el último batch si no está vacío
    if batch:
        yield batch


def rango_infinito(start: int = 0, step: int = 1) -> Iterator[int]:
    """
    Generador que produce números infinitamente
    
    Args:
        start: Número inicial (default: 0)
        step: Incremento (default: 1)
    
    Yields:
        Números consecutivos infinitamente
    """
    current = start
    while True:
        yield current
        current += step


def fibonacci_generator(n: int) -> Iterator[int]:
    """
    Generador de la secuencia de Fibonacci
    
    Args:
        n: Número de términos a generar
    
    Yields:
        Números de la secuencia de Fibonacci
    """
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def leer_archivo_por_lineas(ruta_archivo: str) -> Iterator[str]:
    """
    Generador que lee un archivo línea por línea de forma eficiente
    
    Args:
        ruta_archivo: Ruta al archivo a leer
    
    Yields:
        Cada línea del archivo sin el salto de línea
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as file:
            for line in file:
                yield line.strip()
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {ruta_archivo}")
        return


def generador_primos(limit: int) -> Iterator[int]:
    """
    Generador de números primos hasta un límite
    
    Args:
        limit: Límite máximo para generar primos
    
    Yields:
        Números primos
    """
    def es_primo(n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    for num in range(2, limit + 1):
        if es_primo(num):
            yield num

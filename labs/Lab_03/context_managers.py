"""
Context Managers para el laboratorio de Python
Context manager de temporización y otros útiles
"""

import time
from contextlib import contextmanager
from typing import Generator, Tuple


class Timer:
    """
    Context manager para medir tiempo de ejecución
    
    Example:
        >>> with Timer() as t:
        ...     time.sleep(1)
        >>> print(f"Tiempo: {t.elapsed:.2f}s")
        Tiempo: 1.00s
    """
    
    def __init__(self, description: str = "Operación"):
        self.description = description
        self.start_time = None
        self.end_time = None
        self.elapsed = None
    
    def __enter__(self):
        self.start_time = time.time()
        print(f"⏱️  Iniciando: {self.description}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.elapsed = self.end_time - self.start_time
        print(f"✅ Completado: {self.description} en {self.elapsed:.4f} segundos")
        return False  # No suprimir excepciones


@contextmanager
def temporizador_simple() -> Generator[Tuple[float, float], None, None]:
    """
    Context manager simple que retorna el tiempo de inicio y fin
    
    Yields:
        Tupla con (tiempo_inicio, tiempo_fin)
    """
    inicio = time.time()
    try:
        yield (inicio, None)
    finally:
        fin = time.time()
        duracion = fin - inicio
        print(f"⏱️  Duración: {duracion:.4f} segundos")


@contextmanager
def medicion_memoria():
    """
    Context manager para medir uso de memoria (simulado)
    """
    import psutil
    import os
    
    proceso = psutil.Process(os.getpid())
    memoria_inicial = proceso.memory_info().rss / 1024 / 1024  # MB
    
    print(f"🧠 Memoria inicial: {memoria_inicial:.2f} MB")
    
    try:
        yield memoria_inicial
    finally:
        memoria_final = proceso.memory_info().rss / 1024 / 1024  # MB
        diferencia = memoria_final - memoria_inicial
        print(f"🧠 Memoria final: {memoria_final:.2f} MB")
        print(f"📊 Diferencia: {diferencia:+.2f} MB")


class ArchivoSeguro:
    """
    Context manager para manejo seguro de archivos con backup
    """
    
    def __init__(self, ruta_archivo: str, modo: str = 'r', encoding: str = 'utf-8'):
        self.ruta_archivo = ruta_archivo
        self.modo = modo
        self.encoding = encoding
        self.file = None
        self.backup_creado = False
    
    def __enter__(self):
        if 'w' in self.modo or 'a' in self.modo:
            # Crear backup si vamos a escribir
            try:
                import shutil
                backup_ruta = f"{self.ruta_archivo}.backup"
                shutil.copy2(self.ruta_archivo, backup_ruta)
                self.backup_creado = True
                print(f"💾 Backup creado: {backup_ruta}")
            except FileNotFoundError:
                pass  # No hay archivo original, no hay backup
        
        self.file = open(self.ruta_archivo, self.modo, encoding=self.encoding)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        
        if exc_type is not None and self.backup_creado:
            # Restaurar backup si hubo error
            import shutil
            backup_ruta = f"{self.ruta_archivo}.backup"
            shutil.copy2(backup_ruta, self.ruta_archivo)
            print(f"🔄 Backup restaurado debido a error")
        
        return False  # No suprimir excepciones


@contextmanager
def conexion_bd_simulada(nombre_db: str = "test.db"):
    """
    Context manager que simula una conexión a base de datos
    """
    print(f"🔌 Conectando a la base de datos: {nombre_db}")
    
    class ConexionSimulada:
        def __init__(self, nombre):
            self.nombre = nombre
            self.conectada = False
        
        def query(self, sql):
            if not self.conectada:
                raise RuntimeError("No conectado a la base de datos")
            return f"Resultado simulado para: {sql}"
        
        def close(self):
            self.conectada = False
            print(f"🔌 Desconectado de: {self.nombre}")
    
    conexion = ConexionSimulada(nombre_db)
    conexion.conectada = True
    
    try:
        yield conexion
    finally:
        conexion.close()

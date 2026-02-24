#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EJEMPLO 3: Streaming de Archivos Grandes
=========================================

Este ejemplo te enseña a descargar archivos grandes usando streaming:
- Descargar archivos sin cargarlos completamente en memoria
- Procesar archivos por partes (chunks)
- Mostrar progreso de descarga con barras de progreso
- Reanudar descargas interrumpidas
- Descargar múltiples archivos en paralelo

Autor: Programador Python Experto
Nivel: Avanzado
"""

import httpx
import os
import sys
import io
from pathlib import Path
from typing import Optional, Callable
from tqdm import tqdm
import time
from utils.exceptions import DownloadError

# Configurar codificación para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class StreamingDownloader:
    """
    Descargador de archivos con streaming y progreso
    """
    
    def __init__(self, chunk_size: int = 8192, timeout: float = 30.0):
        """
        Inicializa el descargador
        
        Args:
            chunk_size: Tamaño de cada chunk en bytes (default: 8KB)
            timeout: Timeout para las descargas
        """
        self.chunk_size = chunk_size
        self.timeout = timeout
        self.client = httpx.Client(timeout=httpx.Timeout(timeout))
        
        print(f"📥 StreamingDownloader configurado:")
        print(f"  Tamaño de chunk: {chunk_size:,} bytes")
        print(f"  Timeout: {timeout} segundos")

    def download_with_progress(self, 
                             url: str, 
                             destination: str,
                             progress_callback: Optional[Callable[[int, int], None]] = None) -> str:
        """
        Descarga un archivo mostrando progreso
        
        Args:
            url: URL del archivo a descargar
            destination: Ruta donde guardar el archivo
            progress_callback: Función callback para progreso personalizado
            
        Returns:
            str: Ruta del archivo descargado
            
        Raises:
            DownloadError: Si hay error en la descarga
        """
        print(f"📥 Iniciando descarga: {url}")
        print(f"💾 Destino: {destination}")
        
        try:
            # Iniciar petición streaming
            with self.client.stream('GET', url) as response:
                response.raise_for_status()
                
                # Obtener tamaño total del archivo
                total_size = int(response.headers.get('content-length', 0))
                
                # Crear directorio si no existe
                Path(destination).parent.mkdir(parents=True, exist_ok=True)
                
                # Descargar con barra de progreso
                with open(destination, 'wb') as file, \
                     tqdm(total=total_size, unit='B', unit_scale=True, desc="Descargando") as pbar:
                    
                    downloaded = 0
                    
                    for chunk in response.iter_bytes(chunk_size=self.chunk_size):
                        if chunk:
                            file.write(chunk)
                            downloaded += len(chunk)
                            pbar.update(len(chunk))
                            
                            # Llamar al callback personalizado si existe
                            if progress_callback:
                                progress_callback(downloaded, total_size)
                
                print(f"✅ Descarga completada: {destination}")
                print(f"📊 Tamaño final: {downloaded:,} bytes")
                
                return destination
                
        except httpx.RequestError as e:
            raise DownloadError(f"Error de conexión: {e}")
        except Exception as e:
            # Limpiar archivo parcial si hay error
            if os.path.exists(destination):
                os.remove(destination)
            raise DownloadError(f"Error en descarga: {e}")

    def download_with_resume(self, 
                           url: str, 
                           destination: str,
                           max_retries: int = 3) -> str:
        """
        Descarga con capacidad de reanudar descargas interrumpidas
        
        Args:
            url: URL del archivo
            destination: Ruta de destino
            max_retries: Máximo de reintentos
            
        Returns:
            str: Ruta del archivo descargado
        """
        print(f"🔄 Descarga con reanudo: {url}")
        
        for attempt in range(max_retries + 1):
            try:
                # Verificar si ya existe un archivo parcial
                downloaded_bytes = 0
                if os.path.exists(destination):
                    downloaded_bytes = os.path.getsize(destination)
                    print(f"📁 Archivo parcial encontrado: {downloaded_bytes:,} bytes")
                
                # Headers para reanudar descarga
                headers = {}
                if downloaded_bytes > 0:
                    headers['Range'] = f'bytes={downloaded_bytes}-'
                
                with self.client.stream('GET', url, headers=headers) as response:
                    response.raise_for_status()
                    
                    # Verificar si el servidor soporta reanudo
                    if response.status_code == 206:  # Partial Content
                        print("✅ Servidor soporta reanudo de descarga")
                        mode = 'ab'  # Append binary
                    else:
                        print("⚠️ Servidor no soporta reanudo, descargando desde inicio")
                        mode = 'wb'  # Write binary
                        downloaded_bytes = 0
                    
                    # Obtener tamaño total
                    total_size = int(response.headers.get('content-length', 0))
                    if response.status_code == 206:
                        # Ajustar tamaño total para descargas parciales
                        range_header = response.headers.get('content-range', '')
                        if '/' in range_header:
                            total_size = int(range_header.split('/')[-1])
                    
                    # Descargar
                    with open(destination, mode) as file, \
                         tqdm(total=total_size, initial=downloaded_bytes, 
                              unit='B', unit_scale=True, desc="Reanudando") as pbar:
                        
                        for chunk in response.iter_bytes(chunk_size=self.chunk_size):
                            if chunk:
                                file.write(chunk)
                                pbar.update(len(chunk))
                
                print(f"✅ Descarga completada: {destination}")
                return destination
                
            except Exception as e:
                print(f"❌ Intento {attempt + 1} falló: {e}")
                if attempt == max_retries:
                    raise DownloadError(f"Descarga falló después de {max_retries} reintentos")
                
                time.sleep(2 ** attempt)  # Backoff exponencial

    def download_multiple(self, 
                         urls: list[tuple[str, str]], 
                         max_concurrent: int = 3) -> list[str]:
        """
        Descarga múltiples archivos en paralelo
        
        Args:
            urls: Lista de tuplas (url, destination)
            max_concurrent: Máximo de descargas simultáneas
            
        Returns:
            list: Lista de rutas de archivos descargados
        """
        print(f"📦 Descargando {len(urls)} archivos (máx. {max_concurrent} concurrentes)")
        
        downloaded_files = []
        
        # Descargar secuencialmente (httpx no soporta streaming paralelo fácilmente)
        for i, (url, destination) in enumerate(urls, 1):
            try:
                print(f"\n📥 Archivo {i}/{len(urls)}")
                result = self.download_with_progress(url, destination)
                downloaded_files.append(result)
            except Exception as e:
                print(f"❌ Error descargando {url}: {e}")
        
        print(f"\n✅ Completadas {len(downloaded_files)}/{len(urls)} descargas")
        return downloaded_files

    def close(self):
        """Cierra el cliente HTTP"""
        self.client.close()

def ejemplo_descarga_basica():
    """
    Ejemplo 3.1: Descarga básica con streaming
    """
    print("📥 Ejemplo 3.1: Descarga básica con streaming")
    print("-" * 50)
    
    # URL de una imagen de prueba (tamaño mediano)
    url = "https://picsum.photos/seed/python123/1920/1080.jpg"
    destination = "downloads/imagen_streaming.jpg"
    
    downloader = StreamingDownloader(chunk_size=4096)  # Chunks de 4KB
    
    try:
        result = downloader.download_with_progress(url, destination)
        print(f"✅ Archivo guardado en: {result}")
        
        # Verificar tamaño
        if os.path.exists(result):
            size = os.path.getsize(result)
            print(f"📊 Tamaño del archivo: {size:,} bytes")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        downloader.close()

def ejemplo_descarga_grande():
    """
    Ejemplo 3.2: Descargar un archivo grande
    """
    print("\n📥 Ejemplo 3.2: Descarga de archivo grande")
    print("-" * 50)
    
    # URL de un archivo de prueba más grande
    url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    destination = "downloads/archivo_grande.pdf"
    
    downloader = StreamingDownloader(chunk_size=16384)  # Chunks de 16KB
    
    def progress_callback(downloaded: int, total: int):
        """Callback personalizado para mostrar progreso"""
        if total > 0:
            percent = (downloaded / total) * 100
            print(f"\r⏳ Progreso: {percent:.1f}% ({downloaded:,}/{total:,} bytes)", end="")
    
    try:
        result = downloader.download_with_progress(url, destination, progress_callback)
        print(f"\n✅ Archivo grande descargado: {result}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        downloader.close()

def ejemplo_reanudo_descarga():
    """
    Ejemplo 3.3: Reanudar descarga interrumpida
    """
    print("\n🔄 Ejemplo 3.3: Reanudo de descarga")
    print("-" * 50)
    
    # URL que soporta reanudo (la mayoría de los servidores modernos)
    url = "https://proof.ovh.net/files/100Mio.dat"  # Archivo de 100MB
    destination = "downloads/archivo_100mb.dat"
    
    downloader = StreamingDownloader(chunk_size=32768)  # Chunks de 32KB
    
    try:
        result = downloader.download_with_resume(url, destination, max_retries=2)
        print(f"✅ Descarga completada: {result}")
        
        if os.path.exists(result):
            size = os.path.getsize(result)
            print(f"📊 Tamaño final: {size:,} bytes ({size/1024/1024:.1f} MB)")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        downloader.close()

def ejemplo_descargas_multiples():
    """
    Ejemplo 3.4: Descargar múltiples archivos
    """
    print("\n📦 Ejemplo 3.4: Descargas múltiples")
    print("-" * 50)
    
    # Lista de archivos a descargar
    urls = [
        ("https://picsum.photos/seed/img1/800/600.jpg", "downloads/multiples/imagen1.jpg"),
        ("https://picsum.photos/seed/img2/800/600.jpg", "downloads/multiples/imagen2.jpg"),
        ("https://picsum.photos/seed/img3/800/600.jpg", "downloads/multiples/imagen3.jpg"),
    ]
    
    downloader = StreamingDownloader(chunk_size=8192)
    
    try:
        downloaded = downloader.download_multiple(urls, max_concurrent=2)
        print(f"\n✅ Archivos descargados:")
        for file_path in downloaded:
            size = os.path.getsize(file_path)
            print(f"  📁 {file_path} ({size:,} bytes)")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        downloader.close()

def ejemplo_streaming_procesamiento():
    """
    Ejemplo 3.5: Procesar archivo mientras se descarga
    """
    print("\n⚙️ Ejemplo 3.5: Procesamiento durante streaming")
    print("-" * 50)
    
    # URL de un archivo de texto grande
    url = "https://www.gutenberg.org/files/11/11-0.txt"  # Alicia en el País de las Maravillas
    destination = "downloads/alicia_en_el_pais.txt"
    
    downloader = StreamingDownloader(chunk_size=1024)  # Chunks pequeños para procesamiento
    
    try:
        print("📥 Descargando y procesando archivo...")
        
        with downloader.client.stream('GET', url) as response:
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            processed_chars = 0
            word_count = 0
            
            with open(destination, 'wb') as file, \
                 tqdm(total=total_size, unit='B', unit_scale=True, desc="Procesando") as pbar:
                
                for chunk in response.iter_bytes(chunk_size=downloader.chunk_size):
                    if chunk:
                        file.write(chunk)
                        pbar.update(len(chunk))
                        
                        # Procesar el chunk (contar palabras)
                        try:
                            text_chunk = chunk.decode('utf-8', errors='ignore')
                            words = text_chunk.split()
                            word_count += len(words)
                            processed_chars += len(text_chunk)
                        except:
                            pass
        
        print(f"\n✅ Archivo procesado: {destination}")
        print(f"📊 Estadísticas:")
        print(f"  Caracteres procesados: {processed_chars:,}")
        print(f"  Palabras contadas: {word_count:,}")
        print(f"  Tamaño del archivo: {os.path.getsize(destination):,} bytes")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        downloader.close()

def main():
    """
    Función principal que ejecuta todos los ejemplos
    """
    print("🐍 Laboratorio HTTP con httpx - Ejemplo 3: Streaming de Archivos")
    print("=" * 70)
    print("Aprende a descargar archivos grandes usando streaming eficiente\n")
    
    # Crear directorio de descargas
    os.makedirs("downloads", exist_ok=True)
    os.makedirs("downloads/multiples", exist_ok=True)
    
    # Ejecutar todos los ejemplos
    ejemplo_descarga_basica()
    ejemplo_descarga_grande()
    ejemplo_reanudo_descarga()
    ejemplo_descargas_multiples()
    ejemplo_streaming_procesamiento()
    
    print("\n" + "=" * 70)
    print("🎉 Ejemplo 3 completado!")
    print("📚 Conceptos aprendidos:")
    print("  ✓ Streaming de archivos sin agotar memoria")
    print("  ✓ Barras de progreso con tqdm")
    print("  ✓ Reanudo de descargas interrumpidas")
    print("  ✓ Descargas múltiples concurrentes")
    print("  ✓ Procesamiento de datos durante la descarga")
    print("  ✓ Manejo eficiente de memoria con chunks")
    print("\n🚀 ¡Felicidades! Has completado todos los ejemplos del laboratorio")

if __name__ == "__main__":
    main()

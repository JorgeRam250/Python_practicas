"""
Cliente HTTP reutilizable con todas las funcionalidades del laboratorio
"""

import httpx
import time
from typing import Optional, Dict, Any, Callable
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm import tqdm
import os
from pathlib import Path

class UniversalHTTPClient:
    """
    Cliente HTTP universal que combina todas las funcionalidades:
    - Reintentos automáticos
    - Timeouts configurables
    - Streaming de archivos
    - Progreso de descarga
    - Manejo robusto de errores
    """
    
    def __init__(self,
                 timeout_connect: float = 5.0,
                 timeout_read: float = 30.0,
                 timeout_write: float = 10.0,
                 max_retries: int = 3,
                 retry_delay: float = 1.0,
                 chunk_size: int = 8192):
        """
        Inicializa el cliente universal con todas las configuraciones
        """
        self.timeouts = httpx.Timeout(
            connect=timeout_connect,
            read=timeout_read,
            write=timeout_write,
            pool=timeout_connect
        )
        
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.chunk_size = chunk_size
        
        self.client = httpx.Client(timeout=self.timeouts)
        
        print(f"🔧 UniversalHTTPClient inicializado:")
        print(f"  Timeouts: C={timeout_connect}s, R={timeout_read}s, W={timeout_write}s")
        print(f"  Reintentos: {max_retries}")
        print(f"  Chunk size: {chunk_size:,} bytes")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.TimeoutException))
    )
    def get(self, url: str, params: Optional[Dict] = None) -> httpx.Response:
        """GET con reintentos automáticos"""
        return self.client.get(url, params=params)
    
    def post(self, url: str, data: Dict[str, Any], json_data: bool = True) -> httpx.Response:
        """POST con reintentos manuales"""
        for attempt in range(self.max_retries + 1):
            try:
                if json_data:
                    response = self.client.post(url, json=data)
                else:
                    response = self.client.post(url, data=data)
                response.raise_for_status()
                return response
            except httpx.RequestError as e:
                if attempt == self.max_retries:
                    raise
                time.sleep(self.retry_delay * (2 ** attempt))
    
    def download_stream(self, url: str, destination: str) -> str:
        """Descarga con streaming y progreso"""
        try:
            with self.client.stream('GET', url) as response:
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                Path(destination).parent.mkdir(parents=True, exist_ok=True)
                
                with open(destination, 'wb') as file, \
                     tqdm(total=total_size, unit='B', unit_scale=True, desc="Descargando") as pbar:
                    
                    for chunk in response.iter_bytes(chunk_size=self.chunk_size):
                        if chunk:
                            file.write(chunk)
                            pbar.update(len(chunk))
                
                return destination
                
        except Exception as e:
            if os.path.exists(destination):
                os.remove(destination)
            raise e
    
    def close(self):
        """Cierra el cliente"""
        self.client.close()

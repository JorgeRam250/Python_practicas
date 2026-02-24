"""
Excepciones personalizadas para el cliente HTTP
"""

class HTTPClientError(Exception):
    """Excepción base para errores del cliente HTTP"""
    pass

class TimeoutError(HTTPClientError):
    """Error cuando se excede el tiempo de espera"""
    pass

class RetryExhaustedError(HTTPClientError):
    """Error cuando se agotan los reintentos"""
    pass

class DownloadError(HTTPClientError):
    """Error durante la descarga de archivos"""
    pass

"""
Modelos de datos para el sistema de usuarios
"""

import time


class Usuario:
    """Clase que representa un usuario"""
    
    def __init__(self, id=None, nombre=None, email=None):
        """
        Inicializa un usuario
        
        Args:
            id: ID del usuario (opcional)
            nombre: Nombre del usuario
            email: Email del usuario
        """
        self.nombre = nombre
        self.email = email
        self.creado_en = int(time.time())
        self.id = id if id is not None else self._generar_id()
    
    def _generar_id(self):
        """Genera un ID único para el usuario"""
        return hash(f"{self.nombre}{self.email}{self.creado_en}") % 1000000
    
    def __eq__(self, other):
        """Compara dos usuarios"""
        if not isinstance(other, Usuario):
            return False
        return self.id == other.id
    
    def __repr__(self):
        """Representación string del usuario"""
        return f"Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}')"

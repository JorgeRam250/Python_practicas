"""
Clase Validador con métodos para validar diferentes tipos de datos
"""

import re


class Validador:
    """Clase que contiene métodos de validación"""
    
    def __init__(self):
        """Inicializa el validador"""
        self.email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def es_email_valido(self, email):
        """
        Valida si un email tiene formato correcto
        
        Args:
            email (str): Email a validar
            
        Returns:
            bool: True si el email es válido, False otherwise
        """
        if not isinstance(email, str):
            return False
        
        # Patrón que acepta dominios internacionales incluyendo punycode
        # xn-- es el prefijo para dominios internacionalizados (punycode)
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z\-\-]{2,}$')
        
        # Verificar formato básico
        if not email_pattern.match(email):
            return False
        
        # Verificaciones adicionales
        parts = email.split('@')
        if len(parts) != 2:
            return False
        
        local, domain = parts
        if not local or not domain:
            return False
        
        # Verificar que el dominio tenga al menos un punto o sea punycode
        if '.' not in domain and not domain.startswith('xn--'):
            return False
        
        return True
    
    def es_edad_valida(self, edad):
        """
        Valida si una edad está en un rango razonable (0-120)
        
        Args:
            edad (int): Edad a validar
            
        Returns:
            bool: True si la edad es válida, False otherwise
        """
        if not isinstance(edad, int):
            return False
        
        return 0 <= edad <= 120
    
    def sumar_lista(self, numeros):
        """
        Suma todos los números de una lista
        
        Args:
            numeros (list): Lista de números
            
        Returns:
            int/float: Suma de todos los números
        """
        if not isinstance(numeros, list):
            raise ValueError("Se espera una lista")
        
        return sum(numeros)
    
    def es_password_longitud_valida(self, password):
        """
        Valida si un password tiene longitud adecuada (8-20 caracteres)
        
        Args:
            password (str): Password a validar
            
        Returns:
            bool: True si la longitud es válida, False otherwise
        """
        if not isinstance(password, str):
            return False
        
        return 8 <= len(password) <= 20
    
    def es_nombre_valido(self, nombre):
        """
        Valida si un nombre es válido (al menos 3 caracteres, alfanuméricos y espacios)
        
        Args:
            nombre (str): Nombre a validar
            
        Returns:
            bool: True si el nombre es válido, False otherwise
        """
        if not isinstance(nombre, str):
            return False
        
        # Eliminar espacios y verificar longitud mínima
        nombre_sin_espacios = nombre.replace(" ", "")
        if len(nombre_sin_espacios) < 3:
            return False
        
        # Verificar que solo contenga caracteres alfanuméricos y espacios
        return all(c.isalnum() or c.isspace() for c in nombre)
    
    def es_usuario_valido(self, nombre, edad):
        """
        Valida si un usuario es válido (nombre y edad válidos)
        
        Args:
            nombre (str): Nombre del usuario
            edad (int): Edad del usuario
            
        Returns:
            bool: True si el usuario es válido, False otherwise
        """
        return self.es_nombre_valido(nombre) and self.es_edad_valida(edad)
    
    def promedio_lista(self, numeros):
        """
        Calcula el promedio de una lista de números
        
        Args:
            numeros (list): Lista de números
            
        Returns:
            float: Promedio de los números
            
        Raises:
            ValueError: Si la lista está vacía
        """
        if not numeros:
            raise ValueError("Lista vacía")
        
        return sum(numeros) / len(numeros)
    
    def es_telefono_valido(self, telefono):
        """
        Valida si un teléfono tiene formato válido (solo números, guiones y paréntesis)
        
        Args:
            telefono (str): Teléfono a validar
            
        Returns:
            bool: True si el teléfono es válido, False otherwise
        """
        if not isinstance(telefono, str):
            return False
        
        # Eliminar espacios y verificar caracteres permitidos
        telefono_limpio = telefono.replace(" ", "")
        if not telefono_limpio:
            return False
        
        # Permitir números, guiones y paréntesis
        caracteres_permitidos = set('0123456789-()')
        return all(c in caracteres_permitidos for c in telefono_limpio) and len(telefono_limpio) >= 8

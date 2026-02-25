"""
Servicio de gestión de usuarios con dependencias externas
"""

import time
from .models import Usuario


def enviar_email(email, mensaje):
    """
    Función que simula el envío de un email
    En un caso real, esto conectaría con un servicio externo
    """
    print(f"Enviando email a {email}: {mensaje}")
    return True


class UsuarioService:
    """Servicio para gestionar usuarios"""
    
    def __init__(self, db):
        """
        Inicializa el servicio con una base de datos
        
        Args:
            db: Objeto de base de datos mockeado
        """
        self.db = db
    
    def crear_usuario(self, nombre, email):
        """
        Crea un nuevo usuario
        
        Args:
            nombre: Nombre del usuario
            email: Email del usuario
            
        Returns:
            Usuario: El usuario creado
            
        Raises:
            ValueError: Si el email ya existe
        """
        # Verificar si el email ya existe
        if self.db.existe_email(email):
            raise ValueError("Email ya existe")
        
        # Crear el usuario
        usuario = Usuario(nombre=nombre, email=email)
        
        # Guardar en la base de datos
        if not self.db.guardar_usuario(usuario):
            raise ValueError("No se pudo guardar el usuario")
        
        # Enviar email de bienvenida
        enviar_email(email, f"¡Bienvenida {nombre}!")
        
        return usuario
    
    def obtener_usuario(self, usuario_id):
        """
        Obtiene un usuario por su ID
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            Usuario o None si no existe
        """
        return self.db.obtener_usuario_por_id(usuario_id)
    
    def actualizar_usuario(self, usuario_id, nombre=None, email=None):
        """
        Actualiza los datos de un usuario
        
        Args:
            usuario_id: ID del usuario
            nombre: Nuevo nombre (opcional)
            email: Nuevo email (opcional)
            
        Returns:
            bool: True si se actualizó correctamente
            
        Raises:
            ValueError: Si el usuario no existe
        """
        # Obtener usuario existente
        usuario = self.db.obtener_usuario_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        # Actualizar datos si se proporcionan
        if nombre:
            usuario.nombre = nombre
        if email:
            # Verificar si el nuevo email ya existe
            if self.db.existe_email(email) and email != usuario.email:
                raise ValueError("Email ya existe")
            usuario.email = email
        
        # Guardar cambios
        return self.db.actualizar_usuario(usuario)
    
    def eliminar_usuario(self, usuario_id):
        """
        Elimina un usuario
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            bool: True si se eliminó correctamente
        """
        return self.db.eliminar_usuario(usuario_id)

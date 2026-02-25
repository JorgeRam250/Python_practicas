"""
Tests para el servicio de usuarios usando mocking
Demostración de cómo simular dependencias externas
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.usuario_service import UsuarioService
from src.models import Usuario


class TestUsuarioService:
    """Clase de tests para UsuarioService con mocking"""
    
    def setup_method(self):
        """Fixture que se ejecuta antes de cada test"""
        # Creamos un mock para la base de datos
        self.mock_db = Mock()
        self.service = UsuarioService(self.mock_db)
        
        # Configurar comportamiento por defecto para evitar falsos positivos
        self.mock_db.existe_email.return_value = False
        self.mock_db.guardar_usuario.return_value = True
    
    def test_crear_usuario_exitoso(self):
        """Test: crear un usuario exitosamente"""
        # Configuramos el mock
        self.mock_db.guardar_usuario.return_value = True
        
        # Ejecutamos el test
        usuario = self.service.crear_usuario("juan", "juan@email.com")
        
        # Verificamos
        assert usuario.nombre == "juan"
        assert usuario.email == "juan@email.com"
        assert usuario.id is not None
        self.mock_db.guardar_usuario.assert_called_once()
    
    def test_crear_usuario_email_duplicado(self):
        """Test: intentar crear usuario con email duplicado"""
        # Configuramos el mock para simular email duplicado
        self.mock_db.existe_email.return_value = True
        
        # Ejecutamos y verificamos que lanza excepción
        with pytest.raises(ValueError, match="Email ya existe"):
            self.service.crear_usuario("juan", "juan@email.com")
        
        # Verificamos que no se llamó a guardar_usuario
        self.mock_db.guardar_usuario.assert_not_called()
    
    def test_obtener_usuario_existente(self):
        """Test: obtener un usuario existente"""
        # Creamos un usuario de prueba
        usuario_mock = Usuario(1, "juan", "juan@email.com")
        self.mock_db.obtener_usuario_por_id.return_value = usuario_mock
        
        # Ejecutamos
        usuario = self.service.obtener_usuario(1)
        
        # Verificamos
        assert usuario.id == 1
        assert usuario.nombre == "juan"
        self.mock_db.obtener_usuario_por_id.assert_called_once_with(1)
    
    def test_obtener_usuario_no_existente(self):
        """Test: obtener un usuario que no existe"""
        # Configuramos el mock
        self.mock_db.obtener_usuario_por_id.return_value = None
        
        # Ejecutamos
        usuario = self.service.obtener_usuario(999)
        
        # Verificamos
        assert usuario is None
        self.mock_db.obtener_usuario_por_id.assert_called_once_with(999)
    
    @patch('src.usuario_service.enviar_email')
    def test_enviar_bienvenida_usuario_nuevo(self, mock_email):
        """Test: enviar email de bienvenida usando patch"""
        # Configuramos los mocks
        mock_email.return_value = True
        self.mock_db.guardar_usuario.return_value = True
        
        # Ejecutamos
        usuario = self.service.crear_usuario("maria", "maria@email.com")
        
        # Verificamos que se envió el email
        mock_email.assert_called_once_with(
            "maria@email.com", 
            "¡Bienvenida maria!"
        )
    
    @patch('src.usuario_service.time.time')
    def test_timestamp_creacion_usuario(self, mock_time):
        """Test: verificar timestamp de creación usando mock de time"""
        # Configuramos el mock
        mock_time.return_value = 1640995200  # Timestamp fijo
        
        # Ejecutamos
        self.mock_db.guardar_usuario.return_value = True
        usuario = self.service.crear_usuario("test", "test@email.com")
        
        # Verificamos
        assert usuario.creado_en == 1640995200
    
    def test_actualizar_usuario_con_datos_validos(self):
        """Test: actualizar usuario con datos válidos"""
        # Usuario existente
        usuario_existente = Usuario(1, "juan", "juan@email.com")
        self.mock_db.obtener_usuario_por_id.return_value = usuario_existente
        self.mock_db.actualizar_usuario.return_value = True
        
        # Ejecutamos
        resultado = self.service.actualizar_usuario(1, "juan_actualizado", "nuevo@email.com")
        
        # Verificamos
        assert resultado is True
        self.mock_db.actualizar_usuario.assert_called_once()
    
    def test_actualizar_usuario_no_existente(self):
        """Test: intentar actualizar usuario que no existe"""
        # Configuramos el mock
        self.mock_db.obtener_usuario_por_id.return_value = None
        
        # Ejecutamos y verificamos
        with pytest.raises(ValueError, match="Usuario no encontrado"):
            self.service.actualizar_usuario(999, "nuevo", "email@email.com")
        
        self.mock_db.actualizar_usuario.assert_not_called()
    
    def test_eliminar_usuario(self):
        """Test: eliminar un usuario"""
        # Configuramos el mock
        self.mock_db.eliminar_usuario.return_value = True
        
        # Ejecutamos
        resultado = self.service.eliminar_usuario(1)
        
        # Verificamos
        assert resultado is True
        self.mock_db.eliminar_usuario.assert_called_once_with(1)
    
    @pytest.mark.integration
    def test_flujo_completo_usuario(self):
        """Test de integración: flujo completo de usuario"""
        # Configuramos todos los mocks necesarios
        self.mock_db.existe_email.return_value = False
        self.mock_db.guardar_usuario.return_value = True
        self.mock_db.obtener_usuario_por_id.return_value = Usuario(1, "test", "test@email.com")
        self.mock_db.eliminar_usuario.return_value = True
        
        # Ejecutamos el flujo completo
        with patch('src.usuario_service.enviar_email') as mock_email:
            mock_email.return_value = True
            
            # Crear usuario
            usuario = self.service.crear_usuario("test", "test@email.com")
            
            # Obtener usuario
            usuario_obtenido = self.service.obtener_usuario(1)
            
            # Eliminar usuario
            eliminado = self.service.eliminar_usuario(1)
        
        # Verificaciones
        assert usuario.nombre == "test"
        assert usuario_obtenido.id == 1
        assert eliminado is True
        mock_email.assert_called_once()

"""
Tests para el validador de datos usando Hypothesis (Property-based testing)
Hypothesis genera automáticamente casos de prueba para verificar propiedades
"""

import pytest
from hypothesis import given, strategies as st
from src.validador import Validador


class TestValidador:
    """Clase de tests para Validador usando Hypothesis"""
    
    def setup_method(self):
        """Fixture que se ejecuta antes de cada test"""
        self.validador = Validador()
    
    def test_email_valido_simple(self):
        """Test tradicional: email válido simple"""
        assert self.validador.es_email_valido("usuario@dominio.com")
    
    def test_email_invalido_simple(self):
        """Test tradicional: email inválido simple"""
        assert not self.validador.es_email_valido("email_invalido")
        assert not self.validador.es_email_valido("")
        assert not self.validador.es_email_valido("@dominio.com")
    
    @given(st.from_regex(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'))
    def test_emails_generados_son_validos(self, email):
        """
        Property-based test: Emails generados con regex
        deben ser considerados válidos por nuestro validador
        """
        assert self.validador.es_email_valido(email)
    
    @given(st.text(min_size=1))
    def test_textos_aleatorios_pueden_ser_invalidos(self, texto):
        """
        Property-based test: Textos aleatorios pueden ser emails inválidos
        (pero no todos, algunos pueden ser válidos por coincidencia)
        """
        resultado = self.validador.es_email_valido(texto)
        # No podemos asegurar que sea False, pero podemos verificar
        # que si es True, cumple ciertas propiedades
        if resultado:
            assert "@" in texto
            assert "." in texto.split("@")[-1]
    
    @given(st.integers(min_value=0, max_value=100))
    def test_edad_valida_rango(self, edad):
        """
        Property-based test: Edades en rango 0-100 deben ser válidas
        """
        assert self.validador.es_edad_valida(edad)
    
    @given(st.integers(min_value=-1000, max_value=-1))
    def test_edades_negativas_invalidas(self, edad):
        """
        Property-based test: Edades negativas deben ser inválidas
        """
        assert not self.validador.es_edad_valida(edad)
    
    @given(st.integers(min_value=150, max_value=1000))
    def test_edades_muy_altas_invalidas(self, edad):
        """
        Property-based test: Edades mayores a 140 deben ser inválidas
        """
        assert not self.validador.es_edad_valida(edad)
    
    @given(st.lists(st.integers(min_value=1, max_value=100), min_size=1))
    def test_suma_lista_propiedad_conmutativa(self, lista):
        """
        Property-based test: La suma es conmutativa
        El orden de los elementos no afecta el resultado
        """
        resultado_original = self.validador.sumar_lista(lista)
        lista_reversa = list(reversed(lista))
        resultado_reversa = self.validador.sumar_lista(lista_reversa)
        assert resultado_original == resultado_reversa
    
    @given(st.lists(st.integers(), min_size=0))
    def test_suma_lista_propiedad_asociativa(self, lista):
        """
        Property-based test: La suma es asociativa
        (a + b) + c = a + (b + c)
        """
        if len(lista) >= 3:
            # Dividimos la lista en tres partes
            a = lista[0]
            b = lista[1]
            c = lista[2:]
            
            # (a + b) + c
            resultado1 = self.validador.sumar_lista([a + b] + c)
            
            # a + (b + c)
            suma_bc = self.validador.sumar_lista([b] + c)
            resultado2 = self.validador.sumar_lista([a, suma_bc])
            
            assert resultado1 == resultado2
    
    @given(st.lists(st.integers(min_value=0, max_value=1000), min_size=0))
    def test_suma_lista_propiedad_identidad(self, lista):
        """
        Property-based test: La suma con 0 es la identidad
        """
        resultado_original = self.validador.sumar_lista(lista)
        resultado_con_cero = self.validador.sumar_lista([0] + lista)
        assert resultado_original == resultado_con_cero
    
    @given(st.text(min_size=8, max_size=20))
    def test_password_longitud_valida(self, password):
        """
        Property-based test: Passwords con longitud 8-20 deben tener longitud válida
        """
        assert self.validador.es_password_longitud_valida(password)
    
    @given(st.text(min_size=0, max_size=7))
    def test_password_corto_invalido(self, password):
        """
        Property-based test: Passwords con menos de 8 caracteres deben ser inválidos
        """
        assert not self.validador.es_password_longitud_valida(password)
    
    @given(st.text(min_size=21, max_size=50))
    def test_password_largo_invalido(self, password):
        """
        Property-based test: Passwords con más de 20 caracteres deben ser inválidos
        """
        assert not self.validador.es_password_longitud_valida(password)
    
    @given(st.lists(st.characters(whitelist_categories=('L', 'Nd')), min_size=3))
    def test_nombre_propiedad_longitud(self, caracteres):
        """
        Property-based test: Nombres con al menos 3 caracteres alfanuméricos
        """
        nombre = "".join(caracteres)
        assert self.validador.es_nombre_valido(nombre)
    
    @given(st.tuples(st.text(), st.integers(min_value=0, max_value=120)))
    def test_validacion_usuario_completa(self, datos_usuario):
        """
        Property-based test: Validación completa de usuario
        """
        nombre, edad = datos_usuario
        
        # Si el nombre es válido y la edad es válida, el usuario debe ser válido
        nombre_valido = len(nombre) >= 3 and nombre.replace(" ", "").isalnum()
        edad_valida = 0 <= edad <= 120
        
        resultado = self.validador.es_usuario_valido(nombre, edad)
        
        if nombre_valido and edad_valida:
            assert resultado
        elif not nombre_valido or not edad_valida:
            # Puede ser False o True dependiendo de otras reglas
            # Pero al menos verificamos que no lanza excepción
            assert isinstance(resultado, bool)
    
    @given(st.lists(st.integers(min_value=1, max_value=100)))
    def test_promedio_lista_propiedad_rango(self, lista):
        """
        Property-based test: El promedio debe estar entre min y max de la lista
        """
        if lista:  # Solo si la lista no está vacía
            promedio = self.validador.promedio_lista(lista)
            minimo = min(lista)
            maximo = max(lista)
            assert minimo <= promedio <= maximo
    
    @given(st.lists(st.integers()))
    def test_promedio_lista_vacia_lanza_excepcion(self, lista):
        """
        Property-based test: Lista vacía debe lanzar ValueError
        """
        if not lista:
            with pytest.raises(ValueError, match="Lista vacía"):
                self.validador.promedio_lista(lista)

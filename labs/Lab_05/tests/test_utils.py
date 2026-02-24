"""
Tests para las utilidades con Union, Literal y tipos avanzados
"""

import pytest
from src.utils import (
    procesar_dato, obtener_tipo_operacion, validar_formato_fecha,
    filtrar_lista_por_tipo, calcular_estadisticas, formatear_mensaje,
    safe_division
)


class TestProcesarDato:
    """Tests para la función procesar_dato."""
    
    def test_procesar_string(self) -> None:
        """Test para procesar datos tipo string."""
        resultado = procesar_dato("  hola mundo  ")
        assert resultado == "HOLA MUNDO"
    
    def test_procesar_entero(self) -> None:
        """Test para procesar datos tipo entero."""
        resultado = procesar_dato(42)
        assert resultado == "NUMERO: 42"
    
    def test_procesar_flotante(self) -> None:
        """Test para procesar datos tipo flotante."""
        resultado = procesar_dato(3.1416)
        assert resultado == "NUMERO: 3.1416"
    
    def test_procesar_tipo_no_reconocido(self) -> None:
        """Test para procesar tipo no reconocido."""
        resultado = procesar_dato([1, 2, 3])  # type: ignore
        assert resultado == "TIPO_NO_RECONOCIDO"


class TestObtenerTipoOperacion:
    """Tests para la función obtener_tipo_operacion."""
    
    def test_obtener_suma(self) -> None:
        """Test para obtener operación suma."""
        operacion = obtener_tipo_operacion("suma")
        assert operacion(5, 3) == 8
    
    def test_obtener_resta(self) -> None:
        """Test para obtener operación resta."""
        operacion = obtener_tipo_operacion("resta")
        assert operacion(5, 3) == 2
    
    def test_obtener_multiplicacion(self) -> None:
        """Test para obtener operación multiplicación."""
        operacion = obtener_tipo_operacion("multiplicacion")
        assert operacion(5, 3) == 15
    
    def test_obtener_division(self) -> None:
        """Test para obtener operación división."""
        operacion = obtener_tipo_operacion("division")
        assert operacion(10, 2) == 5.0
    
    def test_division_por_cero(self) -> None:
        """Test para división por cero."""
        operacion = obtener_tipo_operacion("division")
        assert operacion(10, 0) == 0.0


class TestValidarFormatoFecha:
    """Tests para la función validar_formato_fecha."""
    
    def test_formato_ddmmyyyy_valido(self) -> None:
        """Test para formato DD/MM/YYYY válido."""
        assert validar_formato_fecha("25/12/2024", "DD/MM/YYYY") is True
        assert validar_formato_fecha("01/01/2024", "DD/MM/YYYY") is True
    
    def test_formato_ddmmyyyy_invalido(self) -> None:
        """Test para formato DD/MM/YYYY inválido."""
        assert validar_formato_fecha("25-12-2024", "DD/MM/YYYY") is False
        assert validar_formato_fecha("25/12/24", "DD/MM/YYYY") is False
        assert validar_formato_fecha("25/12/2024/extra", "DD/MM/YYYY") is False
    
    def test_formato_yyyymmdd_valido(self) -> None:
        """Test para formato YYYY-MM-DD válido."""
        assert validar_formato_fecha("2024-12-25", "YYYY-MM-DD") is True
        assert validar_formato_fecha("2024-01-01", "YYYY-MM-DD") is True
    
    def test_formato_yyyymmdd_invalido(self) -> None:
        """Test para formato YYYY-MM-DD inválido."""
        assert validar_formato_fecha("25-12-2024", "YYYY-MM-DD") is False
        assert validar_formato_fecha("2024/12/25", "YYYY-MM-DD") is False
    
    def test_formato_ddmmyyyy_con_guion_valido(self) -> None:
        """Test para formato DD-MM-YYYY válido."""
        assert validar_formato_fecha("25-12-2024", "DD-MM-YYYY") is True
        assert validar_formato_fecha("01-01-2024", "DD-MM-YYYY") is True


class TestFiltrarListaPorTipo:
    """Tests para la función filtrar_lista_por_tipo."""
    
    def test_filtrar_strings(self) -> None:
        """Test para filtrar solo strings."""
        lista = ["hola", 42, 3.14, True, "mundo"]
        resultado = filtrar_lista_por_tipo(lista, "str")
        assert resultado == ["hola", "mundo"]
    
    def test_filtrar_enteros(self) -> None:
        """Test para filtrar solo enteros."""
        lista = ["hola", 42, 3.14, True, 100]
        resultado = filtrar_lista_por_tipo(lista, "int")
        assert resultado == [42, 100]
    
    def test_filtrar_flotantes(self) -> None:
        """Test para filtrar solo flotantes."""
        lista = ["hola", 42, 3.14, 2.5, True]
        resultado = filtrar_lista_por_tipo(lista, "float")
        assert resultado == [3.14, 2.5]
    
    def test_filtrar_booleanos(self) -> None:
        """Test para filtrar solo booleanos."""
        lista = ["hola", 42, 3.14, True, False]
        resultado = filtrar_lista_por_tipo(lista, "bool")
        assert resultado == [True, False]
    
    def test_filtrar_lista_vacia(self) -> None:
        """Test para filtrar lista vacía."""
        resultado = filtrar_lista_por_tipo([], "str")
        assert resultado == []
    
    def test_filtrar_sin_coincidencias(self) -> None:
        """Test para filtrar cuando no hay coincidencias."""
        lista = [1, 2, 3, 4.5]
        resultado = filtrar_lista_por_tipo(lista, "str")
        assert resultado == []


class TestCalcularEstadisticas:
    """Tests para la función calcular_estadisticas."""
    
    def test_estadisticas_lista_vacia(self) -> None:
        """Test para calcular estadísticas de lista vacía."""
        resultado = calcular_estadisticas([])
        
        assert resultado["promedio"] == 0.0
        assert resultado["maximo"] == 0
        assert resultado["minimo"] == 0
        assert resultado["suma"] == 0.0
        assert resultado["cantidad"] == 0
    
    def test_estadisticas_solo_enteros(self) -> None:
        """Test para calcular estadísticas con solo enteros."""
        resultado = calcular_estadisticas([1, 2, 3, 4, 5])
        
        assert resultado["promedio"] == 3.0
        assert resultado["maximo"] == 5.0
        assert resultado["minimo"] == 1.0
        assert resultado["suma"] == 15.0
        assert resultado["cantidad"] == 5
    
    def test_estadisticas_solo_flotantes(self) -> None:
        """Test para calcular estadísticas con solo flotantes."""
        resultado = calcular_estadisticas([1.5, 2.5, 3.5])
        
        assert resultado["promedio"] == 2.5
        assert resultado["maximo"] == 3.5
        assert resultado["minimo"] == 1.5
        assert resultado["suma"] == 7.5
        assert resultado["cantidad"] == 3
    
    def test_estadisticas_mixtos(self) -> None:
        """Test para calcular estadísticas con enteros y flotantes."""
        resultado = calcular_estadisticas([1, 2.5, 3, 4.5])
        
        assert resultado["promedio"] == 2.75
        assert resultado["maximo"] == 4.5
        assert resultado["minimo"] == 1.0
        assert resultado["suma"] == 11.0
        assert resultado["cantidad"] == 4


class TestFormatearMensaje:
    """Tests para la función formatear_mensaje."""
    
    def test_formatear_mensaje_info(self) -> None:
        """Test para formatear mensaje con nivel info."""
        resultado = formatear_mensaje(
            "Hola {nombre}, tienes {mensajes} mensajes",
            {"nombre": "Juan", "mensajes": 5},
            "info"
        )
        
        assert resultado == "[INFO] Hola Juan, tienes 5 mensajes"
    
    def test_formatear_mensaje_warning(self) -> None:
        """Test para formatear mensaje con nivel warning."""
        resultado = formatear_mensaje(
            "Advertencia: {alerta}",
            {"alerta": "Espacio bajo en disco"},
            "warning"
        )
        
        assert resultado == "[WARNING] Advertencia: Espacio bajo en disco"
    
    def test_formatear_mensaje_error(self) -> None:
        """Test para formatear mensaje con nivel error."""
        resultado = formatear_mensaje(
            "Error: {error}",
            {"error": "Conexión fallida"},
            "error"
        )
        
        assert resultado == "[ERROR] Error: Conexión fallida"
    
    def test_formatear_mensaje_nivel_defecto(self) -> None:
        """Test para formatear mensaje con nivel por defecto."""
        resultado = formatear_mensaje(
            "Mensaje: {texto}",
            {"texto": "Hola mundo"}
        )
        
        assert resultado == "[INFO] Mensaje: Hola mundo"
    
    def test_formatear_mensaje_clave_faltante(self) -> None:
        """Test para formatear mensaje con clave faltante."""
        resultado = formatear_mensaje(
            "Hola {nombre}",
            {"apellido": "Pérez"}
        )
        
        assert "[ERROR] Error al formatear mensaje: clave no encontrada" in resultado


class TestSafeDivision:
    """Tests para la función safe_division."""
    
    def test_division_normal(self) -> None:
        """Test para división normal."""
        resultado = safe_division(10, 2)
        assert resultado == 5.0
    
    def test_division_por_cero_con_defecto(self) -> None:
        """Test para división por cero con valor por defecto."""
        resultado = safe_division(10, 0)
        assert resultado == 0.0
    
    def test_division_por_cero_con_defecto_personalizado(self) -> None:
        """Test para división por cero con valor por defecto personalizado."""
        resultado = safe_division(10, 0, -1.0)
        assert resultado == -1.0
    
    def test_division_con_strings_numericos(self) -> None:
        """Test para división con strings que representan números."""
        resultado = safe_division("10", "2")
        assert resultado == 5.0
    
    def test_division_con_datos_invalidos(self) -> None:
        """Test para división con datos no numéricos."""
        resultado = safe_division("abc", "xyz")
        assert resultado == 0.0
    
    def test_division_con_defecto_personalizado_invalido(self) -> None:
        """Test para división con valor por defecto no numérico."""
        resultado = safe_division(10, 0, "invalido")  # type: ignore
        assert resultado == 0.0

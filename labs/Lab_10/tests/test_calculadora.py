"""
Tests para la clase Calculadora usando TDD (Test-Driven Development)
Estos tests se escriben ANTES de implementar el código.
"""

import pytest
from src.calculadora import Calculadora


class TestCalculadora:
    """Clase de tests para la Calculadora"""
    
    def setup_method(self):
        """Fixture que se ejecuta antes de cada test"""
        self.calc = Calculadora()
    
    def test_sumar_numeros_positivos(self):
        """Test: sumar dos números positivos"""
        resultado = self.calc.sumar(2, 3)
        assert resultado == 5
    
    def test_sumar_numeros_negativos(self):
        """Test: sumar dos números negativos"""
        resultado = self.calc.sumar(-2, -3)
        assert resultado == -5
    
    def test_sumar_cero(self):
        """Test: sumar con cero"""
        assert self.calc.sumar(5, 0) == 5
        assert self.calc.sumar(0, 5) == 5
        assert self.calc.sumar(0, 0) == 0
    
    def test_restar_numeros_positivos(self):
        """Test: restar dos números positivos"""
        resultado = self.calc.restar(5, 3)
        assert resultado == 2
    
    def test_restar_numeros_negativos(self):
        """Test: restar dos números negativos"""
        resultado = self.calc.restar(-2, -3)
        assert resultado == 1
    
    def test_multiplicar_numeros_positivos(self):
        """Test: multiplicar dos números positivos"""
        resultado = self.calc.multiplicar(3, 4)
        assert resultado == 12
    
    def test_multiplicar_por_cero(self):
        """Test: multiplicar por cero"""
        assert self.calc.multiplicar(5, 0) == 0
        assert self.calc.multiplicar(0, 5) == 0
    
    def test_dividir_numeros_positivos(self):
        """Test: dividir dos números positivos"""
        resultado = self.calc.dividir(10, 2)
        assert resultado == 5
    
    def test_dividir_por_cero_lanza_excepcion(self):
        """Test: dividir por cero debe lanzar ValueError"""
        with pytest.raises(ValueError, match="No se puede dividir por cero"):
            self.calc.dividir(5, 0)
    
    def test_dividir_resultado_decimal(self):
        """Test: división que resulta en decimal"""
        resultado = self.calc.dividir(7, 2)
        assert resultado == 3.5
    
    @pytest.mark.parametrize("a,b,esperado", [
        (1, 2, 3),
        (-1, 1, 0),
        (0, 0, 0),
        (100, 200, 300),
        (-50, -30, -80)
    ])
    def test_sumar_parametrizado(self, a, b, esperado):
        """Test parametrizado para sumar"""
        resultado = self.calc.sumar(a, b)
        assert resultado == esperado
    
    @pytest.mark.parametrize("a,b,esperado", [
        (10, 2, 5),
        (8, 4, 2),
        (9, 3, 3),
        (1, 1, 1),
        (-6, 2, -3)
    ])
    def test_dividir_parametrizado(self, a, b, esperado):
        """Test parametrizado para dividir"""
        resultado = self.calc.dividir(a, b)
        assert resultado == esperado
    
    @pytest.mark.slow
    def test_operacion_compleja(self):
        """Test marcado como lento"""
        resultado = self.calc.sumar(
            self.calc.multiplicar(2, 3),
            self.calc.dividir(10, 2)
        )
        assert resultado == 11

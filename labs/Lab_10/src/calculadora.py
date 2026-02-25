"""
Clase Calculadora implementada usando TDD
Esta clase se implementa PARA HACER PASAR LOS TESTS
"""

class Calculadora:
    """Clase que implementa operaciones matemáticas básicas"""
    
    def __init__(self):
        """Inicializa la calculadora"""
        pass
    
    def sumar(self, a, b):
        """
        Suma dos números
        
        Args:
            a: Primer número
            b: Segundo número
            
        Returns:
            La suma de a y b
        """
        return a + b
    
    def restar(self, a, b):
        """
        Resta dos números
        
        Args:
            a: Minuendo
            b: Sustraendo
            
        Returns:
            La diferencia de a y b
        """
        return a - b
    
    def multiplicar(self, a, b):
        """
        Multiplica dos números
        
        Args:
            a: Primer número
            b: Segundo número
            
        Returns:
            El producto de a y b
        """
        return a * b
    
    def dividir(self, a, b):
        """
        Divide dos números
        
        Args:
            a: Dividendo
            b: Divisor
            
        Returns:
            El cociente de a y b
            
        Raises:
            ValueError: Si b es cero
        """
        if b == 0:
            raise ValueError("No se puede dividir por cero")
        return a / b

"""
Este archivo muestra el código corregido aplicando PEP 8 y buenas prácticas.
"""

import json
import os
import sys


def calcular_suma(lista_numeros):
    """Calcula la suma de una lista de números.

    Args:
        lista_numeros: Lista de números a sumar.

    Returns:
        La suma total de los números.
    """
    resultado = 0
    for num in lista_numeros:
        resultado += num
    return resultado


def procesar_datos(datos):
    """Procesa una lista de datos aplicando transformaciones.

    Args:
        datos: Lista de números enteros a procesar.

    Returns:
        Lista con los datos procesados. Los números pares se multiplican por 2,
        los impares se incrementan en 1.
    """
    if len(datos) > 0:
        print(f"Procesando {len(datos)} elementos")
        datos_procesados = []
        for item in datos:
            if item % 2 == 0:
                datos_procesados.append(item * 2)
            else:
                datos_procesados.append(item + 1)
        return datos_procesados
    else:
        return []


class CalculadoraAvanzada:
    """Clase que representa una calculadora con historial de operaciones."""

    def __init__(self, precision=2):
        """Inicializa la calculadora.

        Args:
            precision: Número de decimales para redondear resultados.
        """
        self.precision = precision
        self.historial = []

    def sumar(self, a, b):
        """Suma dos números y registra la operación.

        Args:
            a: Primer operando.
            b: Segundo operando.

        Returns:
            Resultado de la suma redondeado a la precisión configurada.
        """
        resultado = round(a + b, self.precision)
        self.historial.append(f"{a}+{b}={resultado}")
        return resultado

    def multiplicar(self, a, b):
        """Multiplica dos números y registra la operación.

        Args:
            a: Primer operando.
            b: Segundo operando.

        Returns:
            Resultado de la multiplicación redondeado a la precisión configurada.
        """
        resultado = round(a * b, self.precision)
        self.historial.append(f"{a}*{b}={resultado}")
        return resultado

    def obtener_historial(self):
        """Retorna el historial de operaciones realizadas.

        Returns:
            Lista con las operaciones registradas.
        """
        return self.historial


def main():
    """Función principal que demuestra el uso de las funciones y clases."""
    numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    suma_total = calcular_suma(numeros)
    print(f"La suma total es: {suma_total}")

    datos_procesados = procesar_datos(numeros)
    print(f"Datos procesados: {datos_procesados}")

    calc = CalculadoraAvanzada()
    print(calc.sumar(5, 3))
    print(calc.multiplicar(4, 2.5))
    print(calc.obtener_historial())


if __name__ == "__main__":
    main()

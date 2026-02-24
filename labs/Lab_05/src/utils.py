"""
Utilidades con Union, Literal y tipos avanzados
"""

from typing import Union, Literal, List, Dict, Any, Optional, Callable
from datetime import datetime
import re


def procesar_dato(dato: Union[str, int, float]) -> str:
    """
    Procesa diferentes tipos de datos y los convierte a string.
    
    Args:
        dato: Puede ser string, entero o flotante
        
    Returns:
        str: Representación en string del dato procesado
    """
    if isinstance(dato, str):
        return dato.strip().upper()
    elif isinstance(dato, (int, float)):
        return f"NUMERO: {dato}"
    else:
        return "TIPO_NO_RECONOCIDO"


def obtener_tipo_operacion(tipo: Literal["suma", "resta", "multiplicacion", "division"]) -> Callable[[float, float], float]:
    """
    Retorna una función de operación según el tipo especificado.
    
    Args:
        tipo: Tipo de operación matemática
        
    Returns:
        Callable: Función que realiza la operación
    """
    operaciones: Dict[Literal["suma", "resta", "multiplicacion", "division"], Callable[[float, float], float]] = {
        "suma": lambda x, y: x + y,
        "resta": lambda x, y: x - y,
        "multiplicacion": lambda x, y: x * y,
        "division": lambda x, y: x / y if y != 0 else 0.0
    }
    
    return operaciones[tipo]


def validar_formato_fecha(fecha_str: str, formato: Literal["DD/MM/YYYY", "YYYY-MM-DD", "DD-MM-YYYY"]) -> bool:
    """
    Valida si una fecha tiene el formato especificado.
    
    Args:
        fecha_str: String de fecha a validar
        formato: Formato esperado (valores predefinidos)
        
    Returns:
        bool: True si el formato es correcto
    """
    patrones: Dict[Literal["DD/MM/YYYY", "YYYY-MM-DD", "DD-MM-YYYY"], str] = {
        "DD/MM/YYYY": r"^\d{2}/\d{2}/\d{4}$",
        "YYYY-MM-DD": r"^\d{4}-\d{2}-\d{2}$",
        "DD-MM-YYYY": r"^\d{2}-\d{2}-\d{4}$"
    }
    
    return bool(re.match(patrones[formato], fecha_str))


def filtrar_lista_por_tipo(
    lista: List[Any], 
    tipo_deseado: Literal["str", "int", "float", "bool"]
) -> List[Any]:
    """
    Filtra una lista manteniendo solo los elementos del tipo especificado.
    
    Args:
        lista: Lista de elementos mixtos
        tipo_deseado: Tipo de elementos a mantener
        
    Returns:
        List: Lista filtrada con solo el tipo deseado
    """
    tipos: Dict[Literal["str", "int", "float", "bool"], type] = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool
    }
    
    return [elem for elem in lista if isinstance(elem, tipos[tipo_deseado])]


def calcular_estadisticas(numeros: List[Union[int, float]]) -> Dict[str, Union[float, int]]:
    """
    Calcula estadísticas básicas de una lista de números.
    
    Args:
        numeros: Lista de números enteros o flotantes
        
    Returns:
        Dict: Diccionario con estadísticas (promedio, max, min, suma, cantidad)
    """
    if not numeros:
        return {
            "promedio": 0.0,
            "maximo": 0,
            "minimo": 0,
            "suma": 0.0,
            "cantidad": 0
        }
    
    numeros_float = [float(n) for n in numeros]
    
    return {
        "promedio": sum(numeros_float) / len(numeros_float),
        "maximo": max(numeros_float),
        "minimo": min(numeros_float),
        "suma": sum(numeros_float),
        "cantidad": len(numeros_float)
    }


def formatear_mensaje(
    plantilla: str,
    valores: Dict[str, Union[str, int, float]],
    nivel: Literal["info", "warning", "error"] = "info"
) -> str:
    """
    Formatea un mensaje usando una plantilla y valores.
    
    Args:
        plantilla: Plantilla con marcadores {clave}
        valores: Diccionario con valores a reemplazar
        nivel: Nivel del mensaje para prefijo
        
    Returns:
        str: Mensaje formateado con prefijo de nivel
    """
    prefijos: Dict[Literal["info", "warning", "error"], str] = {
        "info": "[INFO]",
        "warning": "[WARNING]",
        "error": "[ERROR]"
    }
    
    try:
        mensaje = plantilla.format(**valores)
        return f"{prefijos[nivel]} {mensaje}"
    except KeyError as e:
        return f"{prefijos['error']} Error al formatear mensaje: clave no encontrada {e}"


def safe_division(
    numerador: Union[int, float], 
    denominador: Union[int, float],
    valor_defecto: Union[int, float] = 0.0
) -> float:
    """
    Realiza una división segura manejando división por cero.
    
    Args:
        numerador: Número a dividir
        denominador: Divisor
        valor_defecto: Valor a retornar si hay división por cero
        
    Returns:
        float: Resultado de la división o valor por defecto
    """
    try:
        if denominador == 0:
            return float(valor_defecto)
        return float(numerador) / float(denominador)
    except (TypeError, ValueError):
        return float(valor_defecto)

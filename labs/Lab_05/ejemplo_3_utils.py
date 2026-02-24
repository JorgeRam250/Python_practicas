#!/usr/bin/env python3
"""
Ejemplo 3: Utilidades con Union y Literal
Conceptos: Union, Literal, funciones genéricas, manejo de tipos
"""

from typing import List, Dict, Any, Union
from src.utils import (
    procesar_dato, obtener_tipo_operacion, validar_formato_fecha,
    filtrar_lista_por_tipo, calcular_estadisticas, formatear_mensaje,
    safe_division
)


def main() -> None:
    """Función principal que demuestra utilidades con tipos avanzados."""
    
    print("🎯 Ejemplo 3: Utilidades con Union y Literal")
    print("=" * 50)
    
    # 1. Demostrar procesamiento de datos mixtos
    print("\n🔄 Procesamiento de Datos Mixtos:")
    
    datos_mixtos = [
        "  hola mundo  ",
        42,
        3.14159,
        "  python types  ",
        100,
        [1, 2, 3]  # Este no será reconocido
    ]
    
    print("  Datos originales:")
    for i, dato in enumerate(datos_mixtos, 1):
        print(f"    {i}. {dato} ({type(dato).__name__})")
    
    print("\n  Datos procesados:")
    for i, dato in enumerate(datos_mixtos, 1):
        resultado = procesar_dato(dato)  # type: ignore
        print(f"    {i}. {resultado}")
    
    # 2. Demostrar operaciones matemáticas con Literal
    print("\n🧮 Operaciones Matemáticas (Literal types):")
    
    operaciones = ["suma", "resta", "multiplicacion", "division"]
    numeros = [(10, 5), (7, 3), (12, 4)]
    
    for a, b in numeros:
        print(f"\n  Operaciones con {a} y {b}:")
        for op in operaciones:
            funcion = obtener_tipo_operacion(op)  # type: ignore
            resultado = funcion(a, b)
            print(f"    {op}: {a} {get_simbolo(op)} {b} = {resultado}")
    
    # 3. Demostrar validación de fechas con Literal
    print("\n📅 Validación de Fechas:")
    
    fechas = [
        ("25/12/2024", "DD/MM/YYYY"),
        ("2024-12-25", "YYYY-MM-DD"),
        ("25-12-2024", "DD-MM-YYYY"),
        ("25/12/24", "DD/MM/YYYY"),  # Inválido
        ("2024/12/25", "YYYY-MM-DD"),  # Inválido
    ]
    
    for fecha, formato in fechas:
        es_valida = validar_formato_fecha(fecha, formato)  # type: ignore
        estado = "✅ Válido" if es_valida else "❌ Inválido"
        print(f"  {fecha} ({formato}): {estado}")
    
    # 4. Demostrar filtrado por tipo
    print("\n🔍 Filtrado por Tipo:")
    
    lista_mixta = [
        "texto1", "texto2", 42, 100, 3.14, 2.71, True, False, "texto3"
    ]
    
    print(f"  Lista original: {lista_mixta}")
    
    tipos_a_filtrar = ["str", "int", "float", "bool"]
    for tipo in tipos_a_filtrar:
        filtrados = filtrar_lista_por_tipo(lista_mixta, tipo)  # type: ignore
        print(f"  {tipo}: {filtrados}")
    
    # 5. Demostrar cálculo de estadísticas
    print("\n📊 Cálculo de Estadísticas:")
    
    conjuntos_numeros = [
        [1, 2, 3, 4, 5],
        [10.5, 20.3, 30.7],
        [100, 200.5, 300, 400.2, 500],
        []  # Lista vacía
    ]
    
    for i, numeros in enumerate(conjuntos_numeros, 1):
        print(f"\n  Conjunto {i}: {numeros}")
        stats = calcular_estadisticas(numeros)
        print(f"    Promedio: {stats['promedio']:.2f}")
        print(f"    Máximo: {stats['maximo']}")
        print(f"    Mínimo: {stats['minimo']}")
        print(f"    Suma: {stats['suma']:.2f}")
        print(f"    Cantidad: {stats['cantidad']}")
    
    # 6. Demostrar formateo de mensajes
    print("\n💬 Formateo de Mensajes:")
    
    mensajes = [
        ("Hola {nombre}, bienvenido al sistema", {"nombre": "Ana"}, "info"),
        ("Error: {error_code} - {mensaje}", {"error_code": 404, "mensaje": "Página no encontrada"}, "error"),
        ("Advertencia: {alerta}", {"alerta": "Contraseña débil"}, "warning"),
        ("Usuario {user} tiene {count} mensajes", {"user": "Juan", "count": 5}, "info"),
        ("Clave faltante: {inexistente}", {"existente": "valor"}, "error")  # Error
    ]
    
    for plantilla, valores, nivel in mensajes:
        resultado = formatear_mensaje(plantilla, valores, nivel)  # type: ignore
        print(f"  {resultado}")
    
    # 7. Demostrar división segura
    print("\n⚡ División Segura:")
    
    divisiones = [
        (10, 2),
        (15, 3),
        (10, 0),  # División por cero
        (25, 5),
        ("20", "4"),  # Strings numéricos
        ("abc", "xyz"),  # No numéricos
        (100, 0, -1)  # Con valor por defecto personalizado
    ]
    
    for i, division in enumerate(divisiones, 1):
        if len(division) == 2:
            a, b = division
            resultado = safe_division(a, b)
            defecto = "0.0"
        else:
            a, b, defecto_valor = division
            resultado = safe_division(a, b, defecto_valor)
            defecto = str(defecto_valor)
        
        print(f"  {i}. {a} ÷ {b} = {resultado} (defecto: {defecto})")
    
    # 8. Demostrar uso práctico combinado
    print("\n🎯 Ejemplo Práctico Combinado:")
    
    # Simular datos de sensores
    datos_sensores = [
        {"sensor": "temperatura", "valor": 25.5, "unidad": "°C"},
        {"sensor": "humedad", "valor": 60, "unidad": "%"},
        {"sensor": "presion", "valor": 1013.25, "unidad": "hPa"},
        {"sensor": "viento", "valor": 15, "unidad": "km/h"}
    ]
    
    # Extraer valores numéricos
    valores_numericos = [d["valor"] for d in datos_sensores]
    
    # Calcular estadísticas
    stats = calcular_estadisticas(valores_numericos)
    
    # Formatear mensaje de resumen
    mensaje = formatear_mensaje(
        "Resumen de sensores - Promedio: {promedio:.2f}, Rango: {minimo:.2f}-{maximo:.2f}",
        {
            "promedio": stats["promedio"],
            "minimo": stats["minimo"],
            "maximo": stats["maximo"]
        },
        "info"
    )
    
    print(f"  📡 {mensaje}")
    print(f"  📋 Total sensores: {len(datos_sensores)}")
    
    print("\n✅ Ejemplo 3 completado exitosamente!")


def get_simbolo(operacion: str) -> str:
    """Retorna el símbolo matemático para una operación."""
    simbolos = {
        "suma": "+",
        "resta": "-",
        "multiplicacion": "×",
        "division": "÷"
    }
    return simbolos.get(operacion, "?")


if __name__ == "__main__":
    main()

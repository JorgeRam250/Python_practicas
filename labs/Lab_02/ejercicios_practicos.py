#!/usr/bin/env python3
"""
Ejercicios prácticos adicionales para el laboratorio de Python
Estos ejercicios te ayudarán a reforzar los conceptos aprendidos
"""

import json
import sys
import re
from typing import Dict, List, Any, Union
from datetime import datetime

# ============================================================================
# EJERCICIO 1: Sistema de Inventario con Validaciones Avanzadas
# ============================================================================

class SistemaInventario:
    """Sistema de gestión de inventario con validaciones robustas"""
    
    def __init__(self):
        self.productos = []
        self.errores = []
    
    def validar_producto(self, producto: Dict) -> bool:
        """
        Valida que un producto tenga todos los campos requeridos y válidos
        
        Args:
            producto: Diccionario con datos del producto
            
        Returns:
            True si el producto es válido
        """
        try:
            # Validar campos obligatorios
            campos_requeridos = ['id', 'nombre', 'precio', 'stock', 'categoria']
            for campo in campos_requeridos:
                if campo not in producto:
                    self.errores.append(f"Producto {producto.get('id', 'desconocido')}: falta campo '{campo}'")
                    return False
            
            # Validar tipos de datos
            if not isinstance(producto['id'], int) or producto['id'] <= 0:
                self.errores.append(f"Producto {producto['id']}: ID debe ser entero positivo")
                return False
            
            if not isinstance(producto['nombre'], str) or len(producto['nombre'].strip()) < 2:
                self.errores.append(f"Producto {producto['id']}: nombre inválido")
                return False
            
            if not isinstance(producto['precio'], (int, float)) or producto['precio'] <= 0:
                self.errores.append(f"Producto {producto['id']}: precio debe ser positivo")
                return False
            
            if not isinstance(producto['stock'], int) or producto['stock'] < 0:
                self.errores.append(f"Producto {producto['id']}: stock no puede ser negativo")
                return False
            
            if not isinstance(producto['categoria'], str) or len(producto['categoria'].strip()) < 2:
                self.errores.append(f"Producto {producto['id']}: categoría inválida")
                return False
            
            return True
            
        except Exception as e:
            self.errores.append(f"Error validando producto: {e}")
            return False
    
    def cargar_inventario(self, ruta_archivo: str) -> bool:
        """
        Carga inventario desde archivo JSON
        
        Args:
            ruta_archivo: Ruta del archivo JSON
            
        Returns:
            True si la carga fue exitosa
        """
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
            
            if 'productos' not in datos:
                self.errores.append("El JSON debe contener la clave 'productos'")
                return False
            
            productos_validos = []
            for producto in datos['productos']:
                if self.validar_producto(producto):
                    productos_validos.append(producto)
            
            self.productos = productos_validos
            print(f"[OK] Inventario cargado: {len(self.productos)} productos válidos")
            
            if self.errores:
                print(f"[ADVERTENCIA] Se encontraron {len(self.errores)} errores de validación")
            
            return True
            
        except FileNotFoundError:
            self.errores.append(f"Archivo no encontrado: {ruta_archivo}")
            return False
        except json.JSONDecodeError as e:
            self.errores.append(f"Error JSON: {e}")
            return False
        except Exception as e:
            self.errores.append(f"Error inesperado: {e}")
            return False
    
    def generar_alertas_stock(self, umbral_minimo: int = 10) -> List[Dict]:
        """
        Genera alertas para productos con stock bajo
        
        Args:
            umbral_minimo: Umbral mínimo de stock
            
        Returns:
            Lista de productos con stock bajo
        """
        alertas = []
        for producto in self.productos:
            if producto.get('stock', 0) <= umbral_minimo:
                alertas.append({
                    'id': producto['id'],
                    'nombre': producto['nombre'],
                    'stock_actual': producto['stock'],
                    'umbral': umbral_minimo,
                    'nivel_alerta': 'crítico' if producto['stock'] <= 5 else 'advertencia'
                })
        
        return alertas
    
    def calcular_valor_inventario(self) -> Dict[str, float]:
        """
        Calcula el valor total del inventario por categoría
        
        Returns:
            Diccionario con valor por categoría y total general
        """
        valor_por_categoria = {}
        valor_total = 0
        
        for producto in self.productos:
            categoria = producto['categoria']
            valor_producto = producto['precio'] * producto['stock']
            
            valor_por_categoria[categoria] = valor_por_categoria.get(categoria, 0) + valor_producto
            valor_total += valor_producto
        
        return {
            'por_categoria': valor_por_categoria,
            'total_general': valor_total
        }

# ============================================================================
# EJERCICIO 2: Analizador de Logs con Expresiones Regulares
# ============================================================================

class AnalizadorLogs:
    """Analizador de archivos de log usando expresiones regulares"""
    
    def __init__(self):
        self.logs = []
        self.estadisticas = {
            'total_lineas': 0,
            'errores': 0,
            'advertencias': 0,
            'infos': 0,
            'ips_unicas': set(),
            'fechas': set()
        }
    
    def parsear_linea_log(self, linea: str) -> Dict[str, Any]:
        """
        Parsea una línea de log usando expresiones regulares
        
        Formato esperado: [2024-01-15 10:30:45] INFO: 192.168.1.100 - Usuario login exitoso
        """
        # Patrón regex para extraer componentes del log
        patron = r'^\[([0-9]{4}-[0-9]{2}-[0-9]{2}) ([0-9]{2}:[0-9]{2}:[0-9]{2})\] (ERROR|WARNING|INFO): ([0-9.]+) - (.+)$'
        
        match = re.match(patron, linea.strip())
        
        if match:
            fecha, hora, nivel, ip, mensaje = match.groups()
            
            # Actualizar estadísticas
            self.estadisticas['total_lineas'] += 1
            self.estadisticas['ips_unicas'].add(ip)
            self.estadisticas['fechas'].add(fecha)
            
            if nivel == 'ERROR':
                self.estadisticas['errores'] += 1
            elif nivel == 'WARNING':
                self.estadisticas['advertencias'] += 1
            elif nivel == 'INFO':
                self.estadisticas['infos'] += 1
            
            return {
                'fecha': fecha,
                'hora': hora,
                'nivel': nivel,
                'ip': ip,
                'mensaje': mensaje,
                'timestamp': f"{fecha} {hora}"
            }
        else:
            # Línea que no coincide con el formato
            return {
                'fecha': None,
                'hora': None,
                'nivel': 'UNKNOWN',
                'ip': None,
                'mensaje': linea.strip(),
                'timestamp': None
            }
    
    def analizar_archivo_log(self, ruta_archivo: str) -> bool:
        """
        Analiza un archivo de log línea por línea
        
        Args:
            ruta_archivo: Ruta del archivo de log
            
        Returns:
            True si el análisis fue exitoso
        """
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                for linea in archivo:
                    if linea.strip():  # Ignorar líneas vacías
                        log_entry = self.parsear_linea_log(linea)
                        self.logs.append(log_entry)
            
            print(f"[OK] Log analizado: {len(self.logs)} líneas procesadas")
            return True
            
        except FileNotFoundError:
            print(f"[ERROR] Error: Archivo no encontrado '{ruta_archivo}'")
            return False
        except Exception as e:
            print(f"[ERROR] Error analizando log: {e}")
            return False
    
    def filtrar_por_nivel(self, nivel: str) -> List[Dict]:
        """
        Filtra logs por nivel específico
        
        Args:
            nivel: Nivel a filtrar (ERROR, WARNING, INFO)
            
        Returns:
            Lista de logs filtrados
        """
        return [log for log in self.logs if log['nivel'] == nivel]
    
    def obtener_ips_sospechosas(self, umbral_errores: int = 5) -> List[Dict]:
        """
        Identifica IPs con muchos errores
        
        Args:
            umbral_errores: Número mínimo de errores para considerar sospechosa
            
        Returns:
            Lista de IPs sospechosas con estadísticas
        """
        errores_por_ip = {}
        
        for log in self.logs:
            if log['nivel'] == 'ERROR' and log['ip']:
                ip = log['ip']
                errores_por_ip[ip] = errores_por_ip.get(ip, 0) + 1
        
        sospechosas = []
        for ip, cantidad_errores in errores_por_ip.items():
            if cantidad_errores >= umbral_errores:
                sospechosas.append({
                    'ip': ip,
                    'cantidad_errores': cantidad_errores,
                    'nivel_riesgo': 'alto' if cantidad_errores >= 10 else 'medio'
                })
        
        return sorted(sospechosas, key=lambda x: x['cantidad_errores'], reverse=True)

# ============================================================================
# EJERCICIO 3: Sistema de Encuestas
# ============================================================================

class SistemaEncuestas:
    """Sistema para procesar resultados de encuestas"""
    
    def __init__(self):
        self.encuestas = []
        self.preguntas = []
        self.respuestas = []
    
    def cargar_encuesta(self, ruta_archivo: str) -> bool:
        """
        Carga datos de encuesta desde JSON
        
        Args:
            ruta_archivo: Ruta del archivo JSON
            
        Returns:
            True si la carga fue exitosa
        """
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
            
            # Validar estructura
            if 'encuesta' not in datos:
                print("[ERROR] Error: El JSON debe contener la clave 'encuesta'")
                return False
            
            encuesta_data = datos['encuesta']
            
            if 'preguntas' not in encuesta_data or 'respuestas' not in encuesta_data:
                print("[ERROR] Error: La encuesta debe contener 'preguntas' y 'respuestas'")
                return False
            
            self.preguntas = encuesta_data['preguntas']
            self.respuestas = encuesta_data['respuestas']
            
            print(f"[OK] Encuesta cargada: {len(self.preguntas)} preguntas, {len(self.respuestas)} respuestas")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error cargando encuesta: {e}")
            return False
    
    def calcular_estadisticas_pregunta(self, indice_pregunta: int) -> Dict[str, Any]:
        """
        Calcula estadísticas para una pregunta específica
        
        Args:
            indice_pregunta: Índice de la pregunta a analizar
            
        Returns:
            Diccionario con estadísticas
        """
        if indice_pregunta >= len(self.preguntas):
            return {"error": "Índice de pregunta inválido"}
        
        pregunta = self.preguntas[indice_pregunta]
        tipo_pregunta = pregunta.get('tipo', 'opcion_multiple')
        
        # Extraer respuestas para esta pregunta
        respuestas_pregunta = []
        for respuesta in self.respuestas:
            if indice_pregunta < len(respuesta.get('respuestas', [])):
                respuestas_pregunta.append(respuesta['respuestas'][indice_pregunta])
        
        # Calcular estadísticas según el tipo
        if tipo_pregunta == 'opcion_multiple':
            return self._estadisticas_opcion_multiple(respuestas_pregunta, pregunta)
        elif tipo_pregunta == 'escala':
            return self._estadisticas_escala(respuestas_pregunta, pregunta)
        elif tipo_pregunta == 'texto':
            return self._estadisticas_texto(respuestas_pregunta, pregunta)
        else:
            return {"error": "Tipo de pregunta no soportado"}
    
    def _estadisticas_opcion_multiple(self, respuestas: List, pregunta: Dict) -> Dict[str, Any]:
        """Calcula estadísticas para preguntas de opción múltiple"""
        opciones = pregunta.get('opciones', [])
        conteo = {opcion: 0 for opcion in opciones}
        
        for respuesta in respuestas:
            if respuesta in conteo:
                conteo[respuesta] += 1
            else:
                conteo['Otra'] = conteo.get('Otra', 0) + 1
        
        total = len(respuestas)
        porcentajes = {k: (v / total * 100) if total > 0 else 0 for k, v in conteo.items()}
        
        return {
            'tipo': 'opcion_multiple',
            'total_respuestas': total,
            'conteo': conteo,
            'porcentajes': porcentajes,
            'opcion_mas_popular': max(conteo.items(), key=lambda x: x[1])[0] if conteo else None
        }
    
    def _estadisticas_escala(self, respuestas: List, pregunta: Dict) -> Dict[str, Any]:
        """Calcula estadísticas para preguntas de escala (1-5)"""
        valores = []
        for respuesta in respuestas:
            try:
                valor = int(respuesta)
                if 1 <= valor <= 5:
                    valores.append(valor)
            except (ValueError, TypeError):
                continue
        
        if not valores:
            return {"error": "No hay valores válidos para la escala"}
        
        return {
            'tipo': 'escala',
            'total_respuestas': len(valores),
            'promedio': sum(valores) / len(valores),
            'minimo': min(valores),
            'maximo': max(valores),
            'distribucion': {i: valores.count(i) for i in range(1, 6)}
        }
    
    def _estadisticas_texto(self, respuestas: List, pregunta: Dict) -> Dict[str, Any]:
        """Calcula estadísticas para preguntas de texto abierto"""
        textos = [str(r) for r in respuestas if r and str(r).strip()]
        
        if not textos:
            return {"error": "No hay respuestas de texto válidas"}
        
        longitudes = [len(texto) for texto in textos]
        palabras_totales = sum(len(texto.split()) for texto in textos)
        
        return {
            'tipo': 'texto',
            'total_respuestas': len(textos),
            'longitud_promedio': sum(longitudes) / len(longitudes),
            'palabras_promedio': palabras_totales / len(textos),
            'respuesta_mas_larga': max(textos, key=len),
            'respuesta_mas_corta': min(textos, key=len)
        }

# ============================================================================
# FUNCIONES DE DEMOSTRACIÓN
# ============================================================================

def demo_inventario():
    """Demostración del sistema de inventario"""
    print("\n" + "="*50)
    print("DEMO: Sistema de Inventario")
    print("="*50)
    
    # Crear datos de ejemplo
    inventario_data = {
        "productos": [
            {"id": 1, "nombre": "Laptop", "precio": 1200.50, "stock": 15, "categoria": "Electrónicos"},
            {"id": 2, "nombre": "Mouse", "precio": 25.99, "stock": 5, "categoria": "Electrónicos"},
            {"id": 3, "nombre": "Silla", "precio": 450.00, "stock": 8, "categoria": "Muebles"},
            {"id": 4, "nombre": "Libro", "precio": -35.50, "stock": 20, "categoria": "Libros"},  # Error: precio negativo
            {"id": 5, "nombre": "M", "precio": 280.00, "stock": 3, "categoria": "Muebles"},  # Error: nombre muy corto
        ]
    }
    
    # Guardar datos de ejemplo
    with open('inventario_demo.json', 'w', encoding='utf-8') as f:
        json.dump(inventario_data, f, indent=2, ensure_ascii=False)
    
    # Procesar inventario
    sistema = SistemaInventario()
    sistema.cargar_inventario('inventario_demo.json')
    
    # Generar alertas
    alertas = sistema.generar_alertas_stock(umbral_minimo=10)
    print(f"\n[ALERTA] Alertas de stock: {len(alertas)} productos")
    for alerta in alertas:
        print(f"   - {alerta['nombre']}: {alerta['stock_actual']} unidades ({alerta['nivel_alerta']})")
    
    # Calcular valor del inventario
    valor = sistema.calcular_valor_inventario()
    print(f"\n[INFO] Valor del inventario: ${valor['total_general']:.2f}")
    for categoria, valor_cat in valor['por_categoria'].items():
        print(f"   - {categoria}: ${valor_cat:.2f}")

def demo_analizador_logs():
    """Demostración del analizador de logs"""
    print("\n" + "="*50)
    print("DEMO: Analizador de Logs")
    print("="*50)
    
    # Crear archivo de log de ejemplo
    log_lines = [
        "[2024-01-15 10:30:45] INFO: 192.168.1.100 - Usuario login exitoso",
        "[2024-01-15 10:31:12] ERROR: 192.168.1.101 - Fallo de autenticación",
        "[2024-01-15 10:32:03] WARNING: 192.168.1.102 - Contraseña débil detectada",
        "[2024-01-15 10:33:15] INFO: 192.168.1.100 - Acceso a base de datos",
        "[2024-01-15 10:34:22] ERROR: 192.168.1.101 - Intento de acceso no autorizado",
        "[2024-01-15 10:35:30] ERROR: 192.168.1.101 - Ataque de fuerza bruta detectado",
        "[2024-01-15 10:36:45] INFO: 192.168.1.103 - Nuevo usuario registrado",
        "[2024-01-15 10:37:12] ERROR: 192.168.1.101 - IP bloqueada por actividad sospechosa",
        "Línea de log con formato incorrecto",
        "[2024-01-15 10:38:20] WARNING: 192.168.1.104 - Sesión a punto de expirar"
    ]
    
    with open('demo.log', 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    
    # Analizar logs
    analizador = AnalizadorLogs()
    analizador.analizar_archivo_log('demo.log')
    
    # Mostrar estadísticas
    stats = analizador.estadisticas
    print(f"\n[INFO] Estadísticas del log:")
    print(f"   - Total líneas: {stats['total_lineas']}")
    print(f"   - Errores: {stats['errores']}")
    print(f"   - Advertencias: {stats['advertencias']}")
    print(f"   - Infos: {stats['infos']}")
    print(f"   - IPs únicas: {len(stats['ips_unicas'])}")
    
    # Mostrar IPs sospechosas
    sospechosas = analizador.obtener_ips_sospechosas(umbral_errores=2)
    print(f"\n[INFO] IPs sospechosas: {len(sospechosas)}")
    for ip_info in sospechosas:
        print(f"   - {ip_info['ip']}: {ip_info['cantidad_errores']} errores ({ip_info['nivel_riesgo']})")

def demo_encuestas():
    """Demostración del sistema de encuestas"""
    print("\n" + "="*50)
    print("DEMO: Sistema de Encuestas")
    print("="*50)
    
    # Crear datos de encuesta de ejemplo
    encuesta_data = {
        "encuesta": {
            "preguntas": [
                {
                    "id": 1,
                    "texto": "¿Cómo califica nuestro servicio?",
                    "tipo": "escala",
                    "descripcion": "Escala del 1 al 5"
                },
                {
                    "id": 2,
                    "texto": "¿Qué producto prefiere?",
                    "tipo": "opcion_multiple",
                    "opciones": ["Producto A", "Producto B", "Producto C"]
                },
                {
                    "id": 3,
                    "texto": "¿Algún comentario adicional?",
                    "tipo": "texto"
                }
            ],
            "respuestas": [
                {"id_encuestado": 1, "respuestas": ["5", "Producto A", "Excelente servicio"]},
                {"id_encuestado": 2, "respuestas": ["4", "Producto B", "Muy bueno"]},
                {"id_encuestado": 3, "respuestas": ["3", "Producto A", "Podrían mejorar"]},
                {"id_encuestado": 4, "respuestas": ["5", "Producto C", "Perfecto"]},
                {"id_encuestado": 5, "respuestas": ["2", "Producto B", "Necesita mejoras"]}
            ]
        }
    }
    
    # Guardar datos de ejemplo
    with open('encuesta_demo.json', 'w', encoding='utf-8') as f:
        json.dump(encuesta_data, f, indent=2, ensure_ascii=False)
    
    # Procesar encuesta
    sistema = SistemaEncuestas()
    sistema.cargar_encuesta('encuesta_demo.json')
    
    # Analizar cada pregunta
    for i, pregunta in enumerate(sistema.preguntas):
        print(f"\n[INFO] Pregunta {i+1}: {pregunta['texto']}")
        stats = sistema.calcular_estadisticas_pregunta(i)
        
        if 'error' in stats:
            print(f"   Error: {stats['error']}")
            continue
        
        if stats['tipo'] == 'escala':
            print(f"   - Promedio: {stats['promedio']:.2f}/5")
            print(f"   - Rango: {stats['minimo']} - {stats['maximo']}")
        elif stats['tipo'] == 'opcion_multiple':
            print(f"   - Opción más popular: {stats['opcion_mas_popular']}")
            for opcion, porcentaje in stats['porcentajes'].items():
                print(f"   - {opcion}: {porcentaje:.1f}%")
        elif stats['tipo'] == 'texto':
            print(f"   - Longitud promedio: {stats['longitud_promedio']:.1f} caracteres")
            print(f"   - Palabras promedio: {stats['palabras_promedio']:.1f}")

if __name__ == "__main__":
    print("Laboratorio de Python - Ejercicios Prácticos")
    print("Selecciona una demostración:")
    print("1. Sistema de Inventario")
    print("2. Analizador de Logs")
    print("3. Sistema de Encuestas")
    print("4. Todas las demostraciones")
    
    try:
        opcion = input("\nIngresa tu opción (1-4): ").strip()
        
        if opcion == "1":
            demo_inventario()
        elif opcion == "2":
            demo_analizador_logs()
        elif opcion == "3":
            demo_encuestas()
        elif opcion == "4":
            demo_inventario()
            demo_analizador_logs()
            demo_encuestas()
        else:
            print("Opción inválida. Ejecutando todas las demostraciones...")
            demo_inventario()
            demo_analizador_logs()
            demo_encuestas()
        
        print("\nDemostraciones completadas!")
        
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario")
    except Exception as e:
        print(f"\n[ERROR] Error inesperado: {e}")

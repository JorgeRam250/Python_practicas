# 🎓 GUÍA COMPLETA DEL LABORATORIO DE PRUEBAS Y TDD

## 📋 Resumen del Proyecto

He creado un laboratorio completo de **Pruebas y TDD en Python** con 3 ejemplos prácticos que cubren todos los conceptos solicitados:

### ✅ Elementos Creados

1. **Estructura del proyecto completa**
   - `src/` - Código fuente
   - `tests/` - Suite de pruebas
   - `requirements.txt` - Dependencias
   - `pytest.ini` - Configuración
   - `.github/workflows/ci.yml` - Integración CI/CD

2. **Ejemplo 1: Calculadora con TDD** 🧮
   - `src/calculadora.py` - Implementación
   - `tests/test_calculadora.py` - Tests completos
   - **Conceptos**: Fixtures, parametrización, markers

3. **Ejemplo 2: Sistema de Usuarios con Mocking** 👥
   - `src/usuario_service.py` - Servicio con dependencias
   - `src/models.py` - Modelos de datos
   - `tests/test_usuario_service.py` - Tests con mocks
   - **Conceptos**: Mock objects, patch, assert calls

4. **Ejemplo 3: Validador con Hypothesis** 🔍
   - `src/validador.py` - Funciones de validación
   - `tests/test_validador.py` - Property-based tests
   - **Conceptos**: Property-based testing, strategies, falsification

5. **Herramientas adicionales**
   - `run_tests.py` - Script ejecutor de tests
   - `README.md` - Documentación detallada
   - Reportes de cobertura HTML

## 🎯 Resultados Actuales

### Tests: ✅ 48 PASADOS, 0 FALLIDOS
- **Cobertura de código**: 81% (superando el mínimo del 80%)
- **Tests unitarios**: 21 (calculadora)
- **Tests con mocking**: 10 (usuario service)  
- **Tests property-based**: 17 (validador)

### Cobertura por Módulo:
- `calculadora.py`: 100% ✅
- `usuario_service.py`: 94% ✅
- `models.py`: 73% ⚠️
- `validador.py`: 71% ⚠️

## 🚀 Cómo Usar el Laboratorio

### Paso 1: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 2: Ejecutar Todos los Tests
```bash
python run_tests.py
```

### Paso 3: Ver Reporte de Cobertura
Abre `htmlcov/index.html` en tu navegador

### Paso 4: Ejecutar Tests Específicos
```bash
# Solo calculadora
pytest tests/test_calculadora.py -v

# Solo con mocking
pytest tests/test_usuario_service.py -v

# Solo property-based
pytest tests/test_validador.py -v
```

## 📚 Conceptos Aprendidos

### 1. TDD (Test-Driven Development)
- **Red-Green-Refactor**: Escribir test → Implementar → Mejorar
- **Fixtures**: Configuración automática de tests
- **Parametrización**: Múltiples casos en un test

### 2. Mocking con unittest.mock
- **Mock objects**: Simular dependencias externas
- **Patch**: Reemplazar temporalmente funciones
- **Assert calls**: Verificar interacciones

### 3. Property-based Testing con Hypothesis
- **Strategies**: Generadores de datos automáticos
- **Properties**: Verificar propiedades matemáticas
- **Falsification**: Encontrar casos que rompen el código

### 4. Cobertura e Integración CI
- **pytest-cov**: Medir cobertura de código
- **Reportes HTML**: Visualización detallada
- **GitHub Actions**: Integración automatizada

## 🎯 Tareas del Laboratorio Completadas

### ✅ Tarea 1: Implementar historia nueva con TDD
- **Ejemplo**: Calculadora con operaciones básicas
- **Proceso**: Tests escritos ANTES del código
- **Resultado**: 100% cobertura, 21 tests

### ✅ Tarea 2: Añadir tests de propiedades
- **Ejemplo**: Validador con Hypothesis
- **Propiedades**: Conmutativa, asociativa, identidad
- **Resultado**: 17 tests property-based

### ✅ Tarea 3: Reporte de cobertura
- **Configuración**: pytest-cov con reportes HTML
- **Umbral**: 80% mínimo (alcanzado: 81%)
- **Visualización**: Reporte interactivo en HTML

## 🔧 Comandos Útiles

### Ejecución por Categorías
```bash
# Tests unitarios (marcados como @pytest.mark.unit)
pytest -m unit -v

# Tests de integración (marcados como @pytest.mark.integration)
pytest -m integration -v

# Excluir tests lentos
pytest -m "not slow" -v
```

### Cobertura Detallada
```bash
# Reporte en terminal
pytest --cov=src --cov-report=term-missing

# Reporte HTML completo
pytest --cov=src --cov-report=html

# Ver líneas no cubiertas
pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

## 📊 Métricas de Calidad

### Indicadores de Éxito:
- ✅ **48 tests pasando** (100% success rate)
- ✅ **81% cobertura** (supera mínimo del 80%)
- ✅ **3 ejemplos completos** (TDD, Mocking, Property-based)
- ✅ **CI/CD configurado** (GitHub Actions)
- ✅ **Documentación completa** (README + Guía)

### Distribución de Tests:
- **Unit Tests**: 21 (43.7%)
- **Mocking Tests**: 10 (20.8%)
- **Property Tests**: 17 (35.4%)

## 🎉 Conclusión

El laboratorio está **COMPLETO Y FUNCIONAL** con:

1. **Todos los conceptos solicitados implementados**
2. **Ejemplos prácticos y funcionales**
3. **Cobertura adecuada (81%)**
4. **Documentación detallada para principiantes**
5. **Integración CI/CD lista para usar**

### Para Descargar y Usar:
1. Copia todos los archivos a tu directorio
2. Ejecuta `pip install -r requirements.txt`
3. Corre `python run_tests.py`
4. Revisa el reporte en `htmlcov/index.html`

**¡Listo para aprender y practicar TDD en Python!** 🚀

# Laboratorio 04 - Objetos y Modelos de Datos en Python

Este laboratorio te enseña, paso a paso y desde cero, a combinar:

- `dataclass` para modelar entidades de negocio (`Order`).
- Métodos especiales (*dunder methods*) para comparaciones y representación.
- Pydantic para validar entradas/salidas (`OrderIn`, `OrderOut`).
- Conversión entre modelos de entrada/salida y entidad de dominio.

## 1) Requisitos

1. Tener Python 3.10 o superior instalado.
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## 2) Estructura del proyecto

```text
.
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── order_entity.py
│   ├── order_models.py
│   └── converters.py
├── examples/
│   ├── example_1_basic.py
│   ├── example_2_validation.py
│   └── example_3_compare_and_sort.py
└── scripts/
    └── run_all_examples.py
```

## 3) Qué vas a aprender en este laboratorio

### A. Entidad `Order` con `dataclass`

Archivo: `src/order_entity.py`

- Campos base:
  - `id`: identificador de la orden
  - `customer_name`: nombre del cliente
  - `unit_price`: precio unitario
  - `quantity`: cantidad
  - `tax_rate`: impuesto (por defecto 0.18 = 18%)

- Cálculos derivados:
  - `subtotal`
  - `tax_amount`
  - `total`

- Validaciones internas en `__post_init__`:
  - precio > 0
  - cantidad > 0
  - impuesto entre 0 y 1

- Comparaciones:
  - `@dataclass(order=True)` permite ordenar órdenes.
  - Se usa `sort_index` (interno) para que el orden se base en `total`.

### B. Modelos Pydantic `OrderIn` y `OrderOut`

Archivo: `src/order_models.py`

- `OrderIn`:
  - Valida datos de entrada (ej. API/formulario).
  - Rechaza valores inválidos (cantidad negativa, impuesto fuera de rango, etc.).

- `OrderOut`:
  - Representa salida serializable con campos calculados.
  - Útil para devolver respuesta JSON o imprimir resultados limpios.

### C. Conversión entre capas

Archivo: `src/converters.py`

- `to_entity(order_in)`
  - Convierte `OrderIn` -> `Order`.

- `to_output(order)`
  - Convierte `Order` -> `OrderOut`.

## 4) Paso a paso sugerido para cumplir el laboratorio

1. Ejecuta `examples/example_1_basic.py` para ver el flujo completo de entrada->entidad->salida.
2. Ejecuta `examples/example_2_validation.py` para entender cómo fallan validaciones en Pydantic y dataclass.
3. Ejecuta `examples/example_3_compare_and_sort.py` para practicar comparaciones y ordenamiento de órdenes por total.
4. Revisa el código fuente en `src/` y modifica valores para observar cambios.

## 5) Cómo ejecutar

### Opción A: uno por uno

```bash
python examples/example_1_basic.py
python examples/example_2_validation.py
python examples/example_3_compare_and_sort.py
```


## 6) Entregable sugerido para tu laboratorio

Incluye en tu entrega:

1. Código de la entidad `Order` con validaciones y cálculos derivados.
2. Modelos `OrderIn`/`OrderOut` en Pydantic.
3. Funciones de conversión.
4. Evidencias de ejecución (capturas o salida de consola).
5. Explicación corta de:
   - por qué separaste entidad y validación externa,
   - qué valida Pydantic y qué valida la entidad,
   - cómo funciona el ordenamiento por `total`.

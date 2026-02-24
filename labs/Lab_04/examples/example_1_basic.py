from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.converters import to_entity, to_output
from src.order_models import OrderIn


def main() -> None:
    print("== Ejemplo 1: Flujo basico ==")

    raw_data = {
        "id": 1,
        "customer_name": "Ana Lopez",
        "unit_price": 50,
        "quantity": 3,
        "tax_rate": 0.18,
    }

    order_in = OrderIn(**raw_data)
    order_entity = to_entity(order_in)
    order_out = to_output(order_entity)

    print("Entrada validada (OrderIn):")
    print(order_in.model_dump())

    print("\nEntidad de dominio (Order):")
    print(order_entity)

    print("\nSalida serializable (OrderOut):")
    print(order_out.model_dump())


if __name__ == "__main__":
    main()

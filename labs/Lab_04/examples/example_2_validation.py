from __future__ import annotations

import sys
from pathlib import Path

from pydantic import ValidationError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.order_entity import Order
from src.order_models import OrderIn


def main() -> None:
    print("== Ejemplo 2: Validaciones ==")

    invalid_input = {
        "id": 2,
        "customer_name": "",
        "unit_price": -10,
        "quantity": 0,
        "tax_rate": 1.5,
    }

    print("\n1) Error de validacion en Pydantic (OrderIn):")
    try:
        OrderIn(**invalid_input)
    except ValidationError as err:
        print(err)

    print("\n2) Error de validacion en la entidad dataclass (Order):")
    try:
        Order(id=3, customer_name="Pedro", unit_price=20, quantity=1, tax_rate=2)
    except ValueError as err:
        print(err)


if __name__ == "__main__":
    main()

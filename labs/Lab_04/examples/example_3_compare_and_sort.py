from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.order_entity import Order


def main() -> None:
    print("== Ejemplo 3: Comparar y ordenar por total ==")

    order_a = Order(id=10, customer_name="Carla", unit_price=100, quantity=1)
    order_b = Order(id=11, customer_name="Luis", unit_price=40, quantity=3)
    order_c = Order(id=12, customer_name="Rosa", unit_price=25, quantity=2)

    orders = [order_a, order_b, order_c]

    print("\nOrdenes originales:")
    for order in orders:
        print(order)

    print("\nOrdenes ordenadas por total (menor -> mayor):")
    for order in sorted(orders):
        print(order)

    print("\nComparaciones directas:")
    print(f"order_a > order_c ? {order_a > order_c}")
    print(f"order_b == order_a ? {order_b == order_a}")


if __name__ == "__main__":
    main()

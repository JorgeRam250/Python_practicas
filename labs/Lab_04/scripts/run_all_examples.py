from __future__ import annotations

import subprocess
import sys


EXAMPLES = [
    "examples/example_1_basic.py",
    "examples/example_2_validation.py",
    "examples/example_3_compare_and_sort.py",
]


def main() -> None:
    print("== Ejecutando todos los ejemplos ==")
    for path in EXAMPLES:
        print(f"\n--- {path} ---")
        result = subprocess.run([sys.executable, path], check=False)
        if result.returncode != 0:
            print(f"Fallo en {path} con codigo {result.returncode}")


if __name__ == "__main__":
    main()

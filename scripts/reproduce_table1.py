"""Reproduce la Tabla 1 del paper de Broadie y Glasserman (1997).

La tabla original usa n = 100 réplicas, b = 50 ramas y cuatro fechas de
ejercicio (d = 3). La opción es un call americano con K = 100, r = 0.05,
delta = 0.10, T = 1 y sigma = 0.2. Los valores "verdad" son los del paper.

Uso:
    python scripts/reproduce_table1.py --branches 50 --replications 100
"""

from __future__ import annotations

import argparse

from bg_pricing.model import Market, Option
from bg_pricing.pricing import price_american

PAPER_TRUE_VALUES = {
    70.0: 0.121,
    80.0: 0.670,
    90.0: 2.303,
    100.0: 5.731,
    110.0: 11.341,
    120.0: 20.000,
    130.0: 30.000,
}


def main() -> int:
    """Corre la tabla y devuelve el código de salida."""
    parser = argparse.ArgumentParser(description="Reproduce la Tabla 1 del paper.")
    parser.add_argument("--branches", type=int, default=50, help="ramas por nodo b")
    parser.add_argument("--replications", type=int, default=100, help="cantidad de árboles n")
    parser.add_argument("--seed", type=int, default=20261017, help="semilla del generador")
    args = parser.parse_args()

    replications, branching = args.replications, args.branches

    header = (
        f"{'S0':>6} {'bajo':>9} {'alto':>9} "
        f"{'IC 90%':>20} {'punto':>9} {'verdad':>9} {'error rel.':>11}"
    )
    print(f"n = {replications}, b = {branching}, d = 3, semilla = {args.seed}")
    print(header)
    print("-" * len(header))
    for spot, true_value in PAPER_TRUE_VALUES.items():
        market = Market(spot=spot, rate=0.05, dividend=0.10, volatility=0.20)
        option = Option(strike=100.0, maturity=1.0, kind="call")
        result = price_american(
            market,
            option,
            steps=3,
            branching=branching,
            replications=replications,
            confidence=0.90,
            seed=args.seed,
        )
        error = abs(result.point - true_value) / true_value
        interval = f"[{result.ci_low:.3f}, {result.ci_high:.3f}]"
        print(
            f"{spot:6.1f} {result.low_mean:9.3f} {result.high_mean:9.3f} "
            f"{interval:>20} {result.point:9.3f} {true_value:9.3f} {100.0 * error:10.2f}%"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

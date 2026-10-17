"""Interfaz de línea de comandos."""

from __future__ import annotations

import argparse

from .model import Market, Option
from .pricing import price_american


def build_parser() -> argparse.ArgumentParser:
    """Construye el parser de argumentos."""
    parser = argparse.ArgumentParser(
        prog="bg-pricing",
        description="Precio de una opción americana con el método de Broadie-Glasserman.",
    )
    parser.add_argument("--spot", type=float, default=100.0, help="precio inicial S(0)")
    parser.add_argument("--strike", type=float, default=100.0, help="precio de ejercicio K")
    parser.add_argument("--rate", type=float, default=0.05, help="tasa libre de riesgo r")
    parser.add_argument(
        "--dividend",
        type=float,
        default=0.10,
        help="tasa de dividendos continua delta",
    )
    parser.add_argument("--volatility", type=float, default=0.20, help="volatilidad sigma")
    parser.add_argument("--maturity", type=float, default=1.0, help="madurez T en años")
    parser.add_argument("--steps", type=int, default=3, help="pasos entre fechas de ejercicio d")
    parser.add_argument("--branches", type=int, default=3, help="ramas por nodo b")
    parser.add_argument("--replications", type=int, default=100, help="cantidad de árboles n")
    parser.add_argument(
        "--confidence",
        type=float,
        default=0.90,
        help="nivel de confianza del intervalo",
    )
    parser.add_argument(
        "--control-variate",
        action="store_true",
        help="usar el valor europeo del mismo árbol como control",
    )
    parser.add_argument("--put", action="store_true", help="valorar un put en lugar de un call")
    parser.add_argument("--seed", type=int, default=None, help="semilla del generador")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Ejecuta la interfaz y devuelve el código de salida."""
    args = build_parser().parse_args(argv)
    market = Market(
        spot=args.spot,
        rate=args.rate,
        dividend=args.dividend,
        volatility=args.volatility,
    )
    option = Option(
        strike=args.strike,
        maturity=args.maturity,
        kind="put" if args.put else "call",
    )
    result = price_american(
        market,
        option,
        steps=args.steps,
        branching=args.branches,
        replications=args.replications,
        confidence=args.confidence,
        control_variate=args.control_variate,
        seed=args.seed,
    )

    kind = "put" if args.put else "call"
    print(f"Broadie-Glasserman: {kind} americano")
    print(
        f"  b = {result.branching} ramas, "
        f"d = {result.steps} pasos, "
        f"n = {result.replications} réplicas"
    )
    print(f"  confianza = {100.0 * result.confidence:.0f}%")
    print(f"  estimador bajo = {result.low_mean:.4f}  (error estándar {result.low_stderr:.4f})")
    print(f"  estimador alto = {result.high_mean:.4f}  (error estándar {result.high_stderr:.4f})")
    print(f"  intervalo = [{result.ci_low:.4f}, {result.ci_high:.4f}]")
    print(f"  precio puntual = {result.point:.4f}")
    if result.control_variate:
        print(
            f"  europeo en el árbol = {result.european_mean:.4f} "
            f"(valor exacto {result.european_true:.4f})"
        )
    return 0

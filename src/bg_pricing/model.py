"""Modelo de mercado y de opción para el método de Broadie-Glasserman."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log, sqrt
from statistics import NormalDist
from typing import Literal

import numpy as np

OptionKind = Literal["call", "put"]

_NORMAL = NormalDist()


@dataclass(frozen=True)
class Market:
    """Parámetros de mercado con movimiento geométrico browniano.

    El precio del activo sigue

        S(t + dt) = S(t) exp((r - delta - sigma^2 / 2) dt + sigma sqrt(dt) Z)

    con Z normal estándar bajo la medida neutral al riesgo.

    spot: precio inicial S(0).
    rate: tasa libre de riesgo anual r.
    dividend: tasa de dividendos continua anual delta.
    volatility: volatilidad anual sigma.
    """

    spot: float
    rate: float
    dividend: float = 0.0
    volatility: float = 0.2

    def __post_init__(self) -> None:
        if self.spot <= 0.0:
            raise ValueError("spot tiene que ser positivo")
        if self.volatility < 0.0:
            raise ValueError("volatility no puede ser negativa")


@dataclass(frozen=True)
class Option:
    """Opción americana o europea sobre un solo activo.

    strike: precio de ejercicio K.
    maturity: madurez T en años.
    kind: "call" o "put".
    """

    strike: float
    maturity: float
    kind: OptionKind = "call"

    def __post_init__(self) -> None:
        if self.strike <= 0.0:
            raise ValueError("strike tiene que ser positivo")
        if self.maturity < 0.0:
            raise ValueError("maturity no puede ser negativa")
        if self.kind not in ("call", "put"):
            raise ValueError("kind tiene que ser 'call' o 'put'")


def payoff(spot: float | np.ndarray, option: Option) -> np.ndarray | np.floating:
    """Payoff de ejercicio en una fecha, h(t, s) en la notación del paper."""
    prices = np.asarray(spot, dtype=float)
    if option.kind == "call":
        return np.maximum(prices - option.strike, 0.0)
    return np.maximum(option.strike - prices, 0.0)


def black_scholes_european(market: Market, option: Option) -> float:
    """Precio europeo de Black-Scholes con dividendos continuos.

    Se usa como valor de referencia del control variate. Exige volatilidad y
    madurez positivas.
    """
    if option.maturity <= 0.0:
        raise ValueError("maturity tiene que ser positiva")
    if market.volatility <= 0.0:
        raise ValueError("volatility tiene que ser positiva")

    root_t = sqrt(option.maturity)
    d1 = (
        log(market.spot / option.strike)
        + (market.rate - market.dividend + 0.5 * market.volatility**2) * option.maturity
    ) / (market.volatility * root_t)
    d2 = d1 - market.volatility * root_t

    if option.kind == "call":
        return (
            market.spot * exp(-market.dividend * option.maturity) * _NORMAL.cdf(d1)
            - option.strike * exp(-market.rate * option.maturity) * _NORMAL.cdf(d2)
        )
    return (
        option.strike * exp(-market.rate * option.maturity) * _NORMAL.cdf(-d2)
        - market.spot * exp(-market.dividend * option.maturity) * _NORMAL.cdf(-d1)
    )

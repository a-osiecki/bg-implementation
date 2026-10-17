"""Árbol simulado y estimadores alto y bajo."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp

import numpy as np
from numpy.random import Generator

from .model import Market, Option, payoff


@dataclass(frozen=True)
class TreeEstimate:
    """Estimadores de una réplica del árbol.

    high: estimador alto, sesgado hacia arriba.
    low: estimador bajo, sesgado hacia abajo.
    european: valor europeo sobre el mismo árbol, para el control variate.
    """

    high: float
    low: float
    european: float


def simulate_levels(
    market: Market,
    option: Option,
    steps: int,
    branching: int,
    rng: Generator,
) -> list[np.ndarray]:
    """Simula los precios del árbol, un nivel por vez.

    El nivel 0 tiene el precio inicial. El nivel t + 1 tiene branching veces
    más nodos que el nivel t. Las ramas de un nodo son independientes entre sí
    y siguen la distribución condicional del movimiento geométrico browniano.
    El árbol no recombina: dos nodos con el mismo precio son nodos distintos.

    Devuelve una lista de steps + 1 arreglos con los precios de cada nivel.
    """
    if steps < 0:
        raise ValueError("steps no puede ser negativo")
    if branching < 2:
        raise ValueError("branching tiene que ser al menos 2 para el estimador bajo")

    levels = [np.array([market.spot], dtype=float)]
    if steps == 0:
        return levels

    dt = option.maturity / steps
    drift = (market.rate - market.dividend - 0.5 * market.volatility**2) * dt
    volatility = market.volatility * np.sqrt(dt)

    states = levels[0]
    for _ in range(steps):
        shocks = rng.standard_normal((states.size, branching))
        states = (states[:, None] * np.exp(drift + volatility * shocks)).ravel()
        levels.append(states)
    return levels


def tree_estimates(
    levels: list[np.ndarray],
    market: Market,
    option: Option,
    branching: int,
) -> TreeEstimate:
    """Aplica las recursiones del paper a un árbol ya simulado.

    levels[0] contiene un solo precio y levels[t] contiene branching**t precios.
    Las fórmulas son las ecuaciones (2) a (6) del paper.
    """
    steps = len(levels) - 1
    if steps == 0:
        value = float(payoff(levels[0][0], option))
        return TreeEstimate(high=value, low=value, european=value)

    expected_sizes = [branching**t for t in range(steps + 1)]
    actual_sizes = [int(level.size) for level in levels]
    if actual_sizes != expected_sizes:
        raise ValueError(
            "los tamaños de los niveles no coinciden con branching**t: "
            f"esperado {expected_sizes}, recibido {actual_sizes}"
        )

    dt = option.maturity / steps
    discount = exp(-market.rate * dt)

    high = np.asarray(payoff(levels[steps], option), dtype=float)
    low = high.copy()
    european = high.copy()

    for t in range(steps - 1, -1, -1):
        intrinsic = np.asarray(payoff(levels[t], option), dtype=float)

        # Estimador alto: máximo entre ejercer y el promedio de los hijos.
        high_children = high.reshape(-1, branching)
        high = np.maximum(intrinsic, discount * high_children.mean(axis=1))

        # Estimador bajo: cada rama j valora la continuación y las otras
        # ramas b - 1 deciden si conviene ejercer.
        low_children = discount * low.reshape(-1, branching)
        decision = (low_children.sum(axis=1, keepdims=True) - low_children) / (branching - 1)
        low = np.where(
            intrinsic[:, None] >= decision,
            intrinsic[:, None],
            low_children,
        ).mean(axis=1)

        european = discount * european.reshape(-1, branching).mean(axis=1)

    return TreeEstimate(
        high=float(high[0]),
        low=float(low[0]),
        european=float(european[0]),
    )

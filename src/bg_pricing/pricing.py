"""Precio de la opción con n réplicas y intervalo de confianza."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from statistics import NormalDist

import numpy as np

from .model import Market, Option, black_scholes_european, payoff
from .tree import simulate_levels, tree_estimates


@dataclass(frozen=True)
class BGResult:
    """Resultado de una corrida de Broadie-Glasserman.

    low_mean y high_mean promedian n árboles independientes. ci_low y ci_high
    forman el intervalo conservador de la ecuación (9) del paper. point es el
    promedio de los dos estimadores, truncado por el ejercicio inmediato.
    """

    low_mean: float
    high_mean: float
    low_stderr: float
    high_stderr: float
    ci_low: float
    ci_high: float
    point: float
    confidence: float
    replications: int
    steps: int
    branching: int
    control_variate: bool
    european_mean: float
    european_true: float

    @property
    def halfwidth(self) -> float:
        """Semiancho del intervalo de confianza."""
        return 0.5 * (self.ci_high - self.ci_low)

    @property
    def relative_halfwidth(self) -> float:
        """Semiancho dividido por el precio puntual."""
        if self.point == 0.0:
            return float("inf")
        return self.halfwidth / self.point


def _apply_control_variate(
    values: np.ndarray,
    europeans: np.ndarray,
    european_true: float,
) -> np.ndarray:
    """Ajusta las réplicas con el valor europeo del mismo árbol.

        X_i_ajustado = X_i - beta (E_i - E_exacto)

    con beta = Cov(X, E) / Var(E). Si la varianza europea es cero, devuelve
    los valores sin cambios.
    """
    variance = float(europeans.var(ddof=1))
    if variance == 0.0:
        return values.copy()
    covariance = float(np.cov(values, europeans, ddof=1)[0, 1])
    beta = covariance / variance
    return values - beta * (europeans - european_true)


def price_american(
    market: Market,
    option: Option,
    *,
    steps: int,
    branching: int,
    replications: int,
    confidence: float = 0.90,
    control_variate: bool = False,
    seed: int | None = None,
) -> BGResult:
    """Estima el precio de una opción americana con Broadie-Glasserman.

    steps: cantidad de pasos entre fechas de ejercicio, d en el paper.
    branching: ramas por nodo, b en el paper.
    replications: cantidad de árboles independientes, n en el paper.
    confidence: nivel de confianza del intervalo, por ejemplo 0.90.
    control_variate: usa el valor europeo del mismo árbol como control.
    seed: semilla del generador aleatorio.
    """
    if steps < 0:
        raise ValueError("steps no puede ser negativo")
    if branching < 2:
        raise ValueError("branching tiene que ser al menos 2 para el estimador bajo")
    if replications < 2:
        raise ValueError("replications tiene que ser al menos 2 para estimar la varianza")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence tiene que estar entre 0 y 1")

    rng = np.random.default_rng(seed)
    highs = np.empty(replications)
    lows = np.empty(replications)
    europeans = np.empty(replications)

    for i in range(replications):
        levels = simulate_levels(market, option, steps, branching, rng)
        estimate = tree_estimates(levels, market, option, branching)
        highs[i] = estimate.high
        lows[i] = estimate.low
        europeans[i] = estimate.european

    european_true = black_scholes_european(market, option)
    if control_variate:
        highs = _apply_control_variate(highs, europeans, european_true)
        lows = _apply_control_variate(lows, europeans, european_true)

    low_mean = float(lows.mean())
    high_mean = float(highs.mean())
    low_stderr = float(lows.std(ddof=1) / sqrt(replications))
    high_stderr = float(highs.std(ddof=1) / sqrt(replications))

    z = NormalDist().inv_cdf(1.0 - (1.0 - confidence) / 2.0)
    intrinsic = float(payoff(market.spot, option))
    ci_low = max(intrinsic, low_mean - z * low_stderr)
    ci_high = high_mean + z * high_stderr
    point = 0.5 * max(intrinsic, low_mean) + 0.5 * high_mean

    return BGResult(
        low_mean=low_mean,
        high_mean=high_mean,
        low_stderr=low_stderr,
        high_stderr=high_stderr,
        ci_low=ci_low,
        ci_high=ci_high,
        point=point,
        confidence=confidence,
        replications=replications,
        steps=steps,
        branching=branching,
        control_variate=control_variate,
        european_mean=float(europeans.mean()),
        european_true=european_true,
    )

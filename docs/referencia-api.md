# Referencia de la API

El paquete `bg_pricing` expone los tipos y las funciones siguientes:

```python
from bg_pricing import (
    BGResult,
    Market,
    Option,
    TreeEstimate,
    black_scholes_european,
    payoff,
    price_american,
    simulate_levels,
    tree_estimates,
)
```

## Tipos

### `Market`

Dataclass inmutable con los parámetros del mercado. Lanza `ValueError` si `spot` no es positivo o si `volatility` es negativa. `spot` y `rate` son obligatorios. `dividend` vale `0.0` y `volatility` vale `0.2` por defecto.

| Campo | Significado |
| --- | --- |
| `spot` | precio inicial del activo `S(0)` |
| `rate` | tasa libre de riesgo anual `r`, en forma continua |
| `dividend` | tasa de dividendos anual `delta`, en forma continua |
| `volatility` | volatilidad anual `sigma` |

### `Option`

Dataclass inmutable con los términos del contrato. Lanza `ValueError` si `strike` no es positivo, si `maturity` es negativa o si `kind` no es `"call"` ni `"put"`. `strike` y `maturity` son obligatorios. `kind` vale `"call"` por defecto.

| Campo | Significado |
| --- | --- |
| `strike` | precio de ejercicio `K` |
| `maturity` | madurez `T`, en años |
| `kind` | `"call"` o `"put"` |

### `TreeEstimate`

Resultado de una réplica del árbol.

| Campo | Significado |
| --- | --- |
| `high` | estimador alto, sesgado hacia arriba |
| `low` | estimador bajo, sesgado hacia abajo |

### `BGResult`

Resultado de una corrida de `price_american`.

| Campo | Significado |
| --- | --- |
| `low_mean` | media del estimador bajo sobre las réplicas |
| `high_mean` | media del estimador alto sobre las réplicas |
| `low_stderr` | error estándar de `low_mean` |
| `high_stderr` | error estándar de `high_mean` |
| `ci_low`, `ci_high` | límite inferior y superior del intervalo de confianza. `ci_low` está truncado en el payoff de ejercicio inmediato |
| `point` | promedio de los dos estimadores, con el mismo truncamiento |
| `confidence` | nivel de confianza de la corrida |
| `replications` | cantidad de árboles independientes, `n` |
| `steps` | cantidad de pasos entre fechas de ejercicio, `d` |
| `branching` | cantidad de ramas por nodo, `b` |
| `control_variate` | indica si se usó el valor europeo como control |
| `european_mean` | media del valor europeo sobre los árboles. Se calcula con `control_variate=True` |
| `european_true` | valor europeo exacto de Black-Scholes. Se calcula con `control_variate=True` |

## Funciones

### `payoff(spot, option)`

Devuelve el payoff de ejercicio en una fecha. Acepta un número o un arreglo de numpy y devuelve un escalar o un arreglo de la misma forma. Para un call devuelve `max(spot - K, 0)` y para un put, `max(K - spot, 0)`. `K` es el strike de `option`.

### `black_scholes_european(market, option)`

Devuelve el precio europeo de `option` por Black-Scholes con dividendos continuos. Es el valor exacto que `price_american` usa como control cuando `control_variate=True`. Lanza `ValueError` si `market.volatility` no es positiva o si `option.maturity` no es positiva.

### `simulate_levels(market, option, steps, branching, rng)`

Simula el árbol de precios nivel por nivel. Devuelve una lista de `steps + 1` arreglos de numpy. El nivel `t`, con `t` de 0 a `steps`, tiene `branching**t` precios. `rng` es un generador de numpy, por ejemplo `numpy.random.default_rng(seed)`. Lanza `ValueError` si `steps` es menor que 1 o si `branching` es menor que 2.

### `tree_estimates(levels, market, option, branching)`

Aplica las recursiones del paper a un árbol ya simulado. `levels` es la lista que devuelve `simulate_levels`. Devuelve un `TreeEstimate`. Lanza `ValueError` si `levels` no tiene al menos dos niveles o si los tamaños no coinciden con `branching**t`.

### `price_american(market, option, *, steps, branching, replications, confidence=0.90, control_variate=False, seed=None)`

Simula `replications` árboles independientes y devuelve un `BGResult` con las medias, los errores estándar, el intervalo de confianza y el precio puntual.

| Argumento | Significado |
| --- | --- |
| `market` | parámetros del mercado |
| `option` | términos del contrato |
| `steps` | cantidad de pasos entre fechas de ejercicio, `d` |
| `branching` | cantidad de ramas por nodo, `b` |
| `replications` | cantidad de árboles independientes, `n` |
| `confidence` | nivel de confianza del intervalo, por defecto `0.90` |
| `control_variate` | usa el valor europeo del mismo árbol como control, por defecto `False` |
| `seed` | semilla del generador aleatorio, por defecto `None` |

`market` y `option` se pasan por posición. Los demás argumentos se pasan por nombre.

El valor europeo del árbol se calcula solo con `control_variate=True`. La función lanza `ValueError` si `steps` es menor que 1, si `branching` es menor que 2, si `replications` es menor que 2 o si `confidence` no está entre 0 y 1.

# Guía de implementación

## Instalación

Desde la raíz del repositorio:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

El paquete depende de numpy. Las dependencias de desarrollo son pytest y ruff.

## Uso desde la línea de comandos

```bash
bg-pricing --steps 3 --branches 3 --replications 100 --seed 42
```

La tabla de argumentos:

| Argumento | Valor por defecto | Significado |
| --- | --- | --- |
| `--spot` | 100.0 | precio inicial `S(0)` |
| `--strike` | 100.0 | precio de ejercicio `K` |
| `--rate` | 0.05 | tasa libre de riesgo `r` |
| `--dividend` | 0.10 | tasa de dividendos continua `delta` |
| `--volatility` | 0.20 | volatilidad `sigma` |
| `--maturity` | 1.0 | madurez `T` en años |
| `--steps` | 3 | pasos entre fechas de ejercicio `d` |
| `--branches` | 3 | ramas por nodo `b` |
| `--replications` | 100 | cantidad de árboles `n` |
| `--confidence` | 0.90 | nivel de confianza del intervalo |
| `--control-variate` | apagado | usa el valor europeo del mismo árbol |
| `--put` | apagado | valora un put en lugar de un call |
| `--seed` | ninguno | semilla del generador aleatorio |

También podés ejecutar el módulo con `python -m bg_pricing`.

## Uso desde Python

```python
from bg_pricing import Market, Option, price_american

market = Market(spot=100.0, rate=0.05, dividend=0.10, volatility=0.20)
option = Option(strike=100.0, maturity=1.0, kind="call")

result = price_american(
    market,
    option,
    steps=3,
    branching=3,
    replications=100,
    confidence=0.90,
    seed=42,
)

print(result.low_mean, result.high_mean)
print(result.ci_low, result.ci_high)
print(result.point, result.relative_halfwidth)
```

## Referencia de la API

### `Market`

Dataclass inmutable con los parámetros de mercado: `spot`, `rate`, `dividend` y `volatility`. Valida que `spot` sea positivo y que `volatility` no sea negativa.

### `Option`

Dataclass inmutable con `strike`, `maturity` y `kind`. `kind` es `"call"` o `"put"`. Valida que el strike sea positivo, que la madurez no sea negativa y que el tipo sea válido.

### `payoff(spot, option)`

Devuelve el payoff de ejercicio. Acepta un número o un arreglo de numpy. Para un call devuelve `max(spot - K, 0)`, para un put `max(K - spot, 0)`.

### `black_scholes_european(market, option)`

Devuelve el precio europeo con dividendos continuos. Sirve como valor exacto del control variate. Con volatilidad cero devuelve el payoff descontado del precio terminal.

### `simulate_levels(market, option, steps, branching, rng)`

Simula el árbol nivel por nivel y devuelve una lista con `steps + 1` arreglos. El nivel `t` tiene `branching**t` precios. `rng` es un generador de numpy, por ejemplo `numpy.random.default_rng(seed)`. Lanza `ValueError` si `steps` es negativo o si `branching` es menor que 2.

### `tree_estimates(levels, market, option, branching)`

Aplica las recursiones del paper a un árbol ya simulado y devuelve un `TreeEstimate` con los campos `high`, `low` y `european`. `levels` tiene que respetar los tamaños `branching**t`; si no, lanza `ValueError`.

### `price_american(market, option, *, steps, branching, replications, confidence=0.90, control_variate=False, seed=None)`

Simula `replications` árboles independientes, calcula las medias, los errores estándar, el intervalo de confianza y el precio puntual. Devuelve un `BGResult`. Lanza `ValueError` si `steps` es negativo, si `branching` es menor que 2, si `replications` es menor que 2 o si `confidence` no está entre 0 y 1.

### `BGResult`

| Campo | Significado |
| --- | --- |
| `low_mean`, `high_mean` | medias de los estimadores bajo y alto |
| `low_stderr`, `high_stderr` | errores estándar de las medias |
| `ci_low`, `ci_high` | intervalo de confianza, con el límite inferior truncado |
| `point` | promedio de los dos estimadores |
| `confidence` | nivel de confianza usado |
| `replications`, `steps`, `branching` | parámetros de la corrida |
| `control_variate` | indica si se usó el control |
| `european_mean` | media del valor europeo sobre los árboles |
| `european_true` | valor europeo exacto |
| `halfwidth` | semiancho del intervalo |
| `relative_halfwidth` | semiancho dividido por el precio puntual |

## Cómo se recorre el árbol

`simulate_levels` genera los precios por niveles. Primero dibuja todos los shocks del nivel 1, después los del nivel 2 y así hasta la madurez. Cada fila de shocks produce los `b` hijos de un nodo. El resultado por nivel es un vector de `b^t` precios.

`tree_estimates` recorre los niveles al revés. En la madurez calcula el payoff. En cada nivel anterior reconstruye la matriz de hijos con `reshape(-1, branching)`, calcula el promedio de los hijos y aplica las fórmulas del estimador alto y del estimador bajo. La operación de numpy `where` aplica la decisión de ejercicio de las `b` pasadas del estimador bajo a la vez.

Esta estrategia guarda `O(b^d)` precios y hace operaciones vectorizadas. El Apéndice C del paper usa un recorrido en profundidad con `O(b d)` memoria. Para los tamaños de este trabajo práctico la memoria no es un problema, y la versión vectorizada es mucho más rápida en Python. Si necesitás árboles muy grandes, cambiá `simulate_levels` y `tree_estimates` por una recursión en profundidad.

## Reproducir la Tabla 1

```bash
python scripts/reproduce_table1.py
```

El script recorre `S(0)` de 70 a 130, usa `K = 100`, `r = 0.05`, `delta = 0.10`, `T = 1`, `sigma = 0.2`, cuatro fechas de ejercicio y la configuración del paper: `n = 100` y `b = 50`. Imprime las dos medias, el intervalo del 90 por ciento, el precio puntual, el valor verdadero del paper y el error relativo. Con la semilla por defecto, los valores quedan cerca de los de la Tabla 1 pero no son idénticos, porque los números aleatorios son otros. La opción `--quick` corre con `n = 20` y `b = 10` para una prueba rápida.

## Tests

```bash
python -m pytest
```

Los tests cubren:

- El payoff de calls y puts, con valores escalares y vectoriales.
- Valores conocidos de Black-Scholes y la paridad put-call.
- Un árbol de un paso con valores calculados a mano para los dos estimadores.
- El Teorema 5 del paper: `L <= H` en cada realización, para diez semillas.
- Un put muy dentro del dinero, que se ejerce de inmediato y da el payoff intrínseco.
- Volatilidad cero, donde el call americano coincide con el europeo.
- La reducción del error estándar con el control variate.
- Los errores de validación de argumentos.

## Extensiones

Para cambiar el payoff, editá `payoff` en `model.py` o agregá un campo a `Option`. Los estimadores no dependen de la forma del payoff.

Para agregar otro modelo de precio, reemplazá la simulación de `simulate_levels`. La recursión de `tree_estimates` solo necesita la lista de niveles.

Para varios activos, el estado de cada nodo pasa a ser un vector y cada rama simula el vector completo. La cantidad de nodos terminales sigue siendo `b^d`, así que el costo no crece con la cantidad de activos. Esa es la ventaja del método frente a las grillas.

Para reducir la varianza hay tres caminos que el paper menciona: el control variate europeo que ya está implementado, el muestreo por hipercubo latino y la poda del árbol con valores europeos conocidos.

Para estimar el ejercicio continuo, calcá `C(1)`, `C(2)` y `C(3)` con `b` grande y extrapolá con la regla de Richardson, como en la sección 4.2 del paper.

Para paralelizar, repartí los `n` árboles entre procesos. Cada árbol es independiente y solo devuelve dos números.

# Broadie-Glasserman

Repositorio de estudio del método de [Broadie y Glasserman (1997)](https://doi.org/10.1016/S0165-1889(97)00029-8) para valorar opciones americanas con simulación. Incluye una implementación en Python, la explicación del algoritmo, un script que reproduce la Tabla 1 del paper y una lista de lecturas con los PDF guardados en `references/`.

- [El método](docs/metodo.md): explicación del algoritmo, las fórmulas y las propiedades.
- [Referencia de la API](docs/referencia-api.md): tipos, funciones, argumentos y campos del resultado.
- [Recursos](docs/recursos.md): papers, libros y notas del curso, con enlaces y copias locales.

## Empezar

Necesitás Python 3.11 o superior. Desde la raíz del repositorio:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest
```

El paquete depende de numpy. Las dependencias de desarrollo son pytest y ruff. Los tests cubren el payoff, el valor europeo, los dos estimadores, el intervalo de confianza y el control variate.

## Reproducir la Tabla 1

```bash
python scripts/reproduce_table1.py --branches 50 --replications 100
```

El script recorre `S(0)` de 70 a 130 con los parámetros del paper: `K = 100`, `r = 0.05`, `delta = 0.10`, `T = 1`, `sigma = 0.2` y `d = 3`. `--branches` fija la cantidad de ramas por nodo y `--replications` fija la cantidad de árboles. Imprime una fila por precio inicial con el estimador bajo, el estimador alto, el intervalo del 90 por ciento, el precio puntual, el valor verdadero del paper y el error relativo. Los valores quedan cerca de los de la Tabla 1, pero no son idénticos: el script genera sus propios caminos aleatorios.

## Precio desde Python

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

print(result.low_mean, result.high_mean, result.ci_low, result.ci_high)
```

La descripción de cada argumento y de cada campo del resultado está en `docs/referencia-api.md`.

## Estructura

| Ruta | Contenido |
| --- | --- |
| `src/bg_pricing/` | implementación del árbol, los estimadores y el intervalo |
| `docs/metodo.md` | explicación del algoritmo, las fórmulas y las propiedades |
| `docs/referencia-api.md` | referencia de la API |
| `docs/recursos.md` | lecturas comentadas con enlaces y copias locales |
| `references/` | papers y notas del curso en PDF |
| `scripts/reproduce_table1.py` | reproducción de la Tabla 1 del paper |

## Licencia

El código está bajo licencia MIT. Los PDF de `references/` mantienen la licencia de sus autores y editoriales y se incluyen solo para estudio personal.

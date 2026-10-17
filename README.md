# Broadie-Glasserman

Repositorio de estudio del método de Broadie y Glasserman (1997) para valorar opciones americanas con simulación. Incluye una implementación en Python, la explicación del algoritmo, un script que reproduce la Tabla 1 del paper y una lista de lecturas con los PDF guardados en `references/`.

## Qué hace el método

Una opción americana se puede ejercer en cualquier fecha hasta la madurez. La simulación avanza en el tiempo, así que no puede decidir hacia atrás cuándo convenía ejercer. Broadie y Glasserman resuelven el problema con dos estimadores sobre un árbol simulado de `b` ramas por nodo:

- El estimador alto aplica programación dinámica al árbol. Usa información del futuro simulado, así que sobreestima el precio.
- El estimador bajo separa las ramas de cada nodo. Unas ramas deciden si conviene ejercer y la rama restante valora la continuación. La decisión puede ser subóptima, así que subestima el precio.

Los dos estimadores son consistentes cuando `b` crece. Para un `b` finito, el precio verdadero queda entre los dos. Con las medias y los errores estándar de `n` árboles independientes se arma un intervalo de confianza conservador.

## Empezar

Necesitás Python 3.11 o superior. Desde la raíz del repositorio:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest
```

Una corrida de ejemplo:

```bash
bg-pricing --steps 3 --branches 3 --replications 100 --seed 42
```

La salida tiene esta forma:

```
Broadie-Glasserman: call americano
  b = 3 ramas, d = 3 pasos, n = 100 réplicas
  confianza = 90%
  estimador bajo = 2.2908  (error estándar 0.3555)
  estimador alto = 5.7622  (error estándar 0.3915)
  intervalo = [1.7060, 6.4062]
  precio puntual = 4.0265
```

Con `b = 3` el sesgo de los dos estimadores es grande y el intervalo queda ancho. Subí `--branches` para achicarlo.

Para reproducir la Tabla 1 del paper:

```bash
python scripts/reproduce_table1.py --quick
```

La opción `--quick` usa 20 réplicas y 10 ramas. Sin ella, el script usa la configuración del paper (n = 100, b = 50, d = 3) y tarda unos segundos.

## Estructura

| Ruta | Contenido |
| --- | --- |
| `src/bg_pricing/` | implementación del árbol, los estimadores y el intervalo |
| `docs/metodo.md` | explicación del algoritmo, las fórmulas y las propiedades |
| `docs/implementacion.md` | uso de la API, reproducción de la tabla y extensiones |
| `docs/recursos.md` | lecturas comentadas con enlaces y copias locales |
| `references/` | papers y notas del curso en PDF |
| `scripts/reproduce_table1.py` | reproducción de la Tabla 1 del paper |

## Alcance

La implementación cubre un activo con movimiento geométrico browniano, calls y puts, cantidad finita de fechas de ejercicio, estimadores alto y bajo, intervalo de confianza y control variate europeo. No cubre varios activos, tasas estocásticas, dividendos discretos ni ejercicio continuo.

## Referencia principal

Broadie, M. y Glasserman, P. (1997). Pricing American-style securities using simulation. *Journal of Economic Dynamics and Control* 21(8-9), 1323-1352. DOI: [10.1016/S0165-1889(97)00029-8](https://doi.org/10.1016/S0165-1889(97)00029-8). Copia local: `references/broadie-glasserman-1997.pdf`.

## Licencia

El código está bajo licencia MIT. Los PDF de `references/` mantienen la licencia de sus autores y editoriales y se incluyen solo para estudio personal.

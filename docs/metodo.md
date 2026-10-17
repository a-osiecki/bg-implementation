# El método de Broadie-Glasserman

## Notación

| Símbolo | Significado |
| --- | --- |
| `S(t)` | precio del activo en la fecha de ejercicio `t`, bajo la medida neutral al riesgo |
| `S(0)` | precio inicial del activo, un dato conocido |
| `K` | precio de ejercicio (strike) |
| `r` | tasa libre de riesgo anual, en forma continua |
| `delta` | tasa de dividendos anual, en forma continua |
| `sigma` | volatilidad anual del activo |
| `T` | madurez de la opción |
| `d` | cantidad de pasos entre fechas de ejercicio |
| `t` | índice de la fecha de ejercicio, de `0` a `d` |
| `b` | cantidad de ramas por nodo del árbol simulado |
| `h(t, s)` | payoff de ejercer en `t` si el activo vale `s` |
| `f(t, s)` | valor de la opción en `t` si el activo vale `s` |
| `g(t, s)` | valor de continuación en `t` si el activo vale `s` |
| `D` | factor de descuento de un paso, `exp(-r (T / d))` |
| `n` | cantidad de árboles independientes |
| `H`, `L` | estimadores alto y bajo de una repetición del árbol |
| `H_barra`, `L_barra` | medias de `H` y `L` sobre las `n` repeticiones |
| `s_H`, `s_L` | desviaciones estándar muestrales de `H` y `L` |
| `E` | valor europeo exacto de la opción, por Black-Scholes |
| `z` | cuantil normal que corresponde al nivel de confianza |

Las fórmulas usan `promedio` sobre las ramas del árbol. Por ejemplo, `promedio_j x_j` es la suma de los `x_j` dividida por `b`.

## El problema

Una opción americana permite ejercer en cualquier fecha hasta la madurez. El modelo discreto fija las fechas de ejercicio en `0 = t_0 < t_1 < ... < t_d = T`. El precio es el máximo, sobre todas las reglas de ejercicio, del payoff esperado y descontado:

```
f(0, S(0)) = max_tau E[ D(tau) h(tau, S(tau)) ]
```

La regla de ejercicio `tau` elige una fecha de ejercicio y puede depender de lo que pasó hasta esa fecha. En cada fecha `t` la decisión es ejercer ahora, con valor `h(t, s)`, o continuar, con valor `g(t, s)`. El precio de la opción es `f(t, s) = max(h(t, s), g(t, s))`.

Resolver esto requiere programación dinámica hacia atrás, porque la decisión óptima en `t` depende del valor de la opción en `t + 1`. La simulación avanza hacia adelante. Esa tensión es el problema central del paper.

## Por qué la simulación directa no alcanza

Un primer intento es simular un camino de precios y calcular el máximo descuento del payoff sobre las fechas de ejercicio. Ese estimador usa el mejor momento del camino simulado, como si el inversor conociera el futuro. Se lo llama solución de previsión perfecta y cumple

```
max_t D(t) h(t, S(t)) >= D(tau) h(tau, S(tau))
```

para cualquier regla de ejercicio. Por lo tanto su esperanza es mayor que el precio verdadero. Simular más caminos no elimina ese sesgo, solo reduce la varianza. El Apéndice B del paper formaliza el resultado: bajo condiciones razonables no existe un estimador insesgado del precio de una opción americana con esfuerzo finito.

El método de Broadie y Glasserman esquiva el problema con dos estimadores, uno sesgado hacia arriba y otro hacia abajo. Los dos son consistentes cuando crece la cantidad de ramas.

## El árbol simulado

En cada nodo del árbol el proceso se ramifica en `b` ramas. Cada rama es una observación independiente de `S(t + 1)` condicional en el precio `S(t)` del nodo. Para un movimiento geométrico browniano con `dt = T / d`,

```
S(t + 1) = S(t) exp( (r - delta - sigma^2 / 2) dt + sigma sqrt(dt) Z )
```

con `Z` normal estándar.

El árbol no recombina. Dos nodos pueden compartir el mismo precio y aun así ser nodos distintos, porque descienden de padres distintos. La Figura 2 del paper muestra el caso `b = 3`. La cantidad de nodos terminales es `b^d`, y todo el cálculo se hace sobre el árbol simulado.

La elección de `b` controla el sesgo de los dos estimadores. La elección de `n`, la cantidad de árboles, controla la varianza de las medias.

## Estimador alto

El estimador alto `H` aplica programación dinámica al árbol. En la madurez vale el payoff. En cada fecha anterior toma el máximo entre ejercer y el promedio descontado de los hijos:

```
H(d, s) = h(d, s)
H(t, s) = max( h(t, s), D * promedio_j H(t + 1, s_j) )
```

El valor en la raíz, `H(0, S(0))`, es el estimador alto de esa repetición.

El sesgo es positivo porque el árbol es una muestra finita. La programación dinámica aprovecha cualquier rama que haya resultado favorable y evita las desfavorables. Por la desigualdad de Jensen,

```
E[ max( h, X ) ] >= max( h, E[X] )
```

cuando `X` es insesgado para el valor de continuación. El sesgo desaparece cuando `b` crece, porque el promedio de los hijos se concentra alrededor de `g(t, s)`. El Teorema 1 del paper prueba esa convergencia.

La Figura 4 del paper da un ejemplo con `S(0) = 101`, `K = 100`, `T = 1`, `r = 0` y dos pasos: el estimador vale 11.9.

## Estimador bajo

El estimador bajo `L` separa las ramas en cada nodo. Una rama valora la continuación y las otras `b - 1` deciden si conviene ejercer. La versión más simple usa una sola rama para valorar y las restantes para decidir. El paper mejora esa versión: repite el procedimiento `b` veces, deja una rama distinta afuera cada vez, y promedia los `b` resultados.

Para cada rama `j`:

```
Y(t, s, j) = h(t, s)                                  si h(t, s) >= D * promedio_{i != j} L(t + 1, s_i)
Y(t, s, j) = D * L(t + 1, s_j)                        si h(t, s) <  D * promedio_{i != j} L(t + 1, s_i)
```

y entonces

```
L(t, s) = promedio_j Y(t, s, j)
```

La decisión usa las ramas `i != j` y el valor de continuación usa la rama `j`. La rama que decide no es la misma que valora. Esa separación rompe el sesgo hacia arriba, pero introduce un sesgo hacia abajo.

El sesgo es negativo porque la decisión se toma con información finita. Con probabilidad positiva la decisión es subóptima, y el valor asociado a una decisión subóptima es menor que el valor óptimo. El Teorema 4 del paper prueba el signo y el Teorema 3 prueba la consistencia cuando `b` crece. El Teorema 5 prueba algo más fuerte: en cada realización del árbol, `L <= H` en todos los nodos.

El ejemplo de la Figura 6 del paper usa el nodo inferior de la primera fecha. El ejercicio vale 15 y la continuación estimada con dos ramas vale 32.5, así que conviene continuar. Las tres pasadas dan valores 0, 16 y 15, y el promedio es 10.3. La pasada que valora con la primera rama obtiene 0 por el mal resultado de esa rama, aunque la decisión haya sido correcta.

## Intervalo de confianza

Se simulan `n` árboles independientes. Cada árbol produce una pareja `(L_i, H_i)`. Con las medias `L_barra` y `H_barra` y los errores estándar muestrales `s_L` y `s_H`, el intervalo de la ecuación (9) del paper es

```
[ max( h(0, S(0)), L_barra - z * s_L / sqrt(n) ),  H_barra + z * s_H / sqrt(n) ]
```

donde `z` es el cuantil `1 - alpha / 2` de la normal estándar y el nivel de confianza es `1 - alpha`. Para un 90 por ciento, `z = 1.645`. El límite inferior se trunca en el payoff de ejercicio inmediato, que es una cota inferior del precio.

El intervalo es conservador. El límite inferior usa el sesgo hacia abajo y el límite superior usa el sesgo hacia arriba, y cada uno es un límite unilateral. Por eso la cobertura real supera a la nominal. La sección 4 del paper lo muestra con 1000 corridas. Un intervalo calculado con `z = 0.5`, que corresponde a un 38 por ciento nominal, contiene el valor verdadero en más del 90 por ciento de los casos.

El precio puntual que sugiere el paper es el promedio de los dos estimadores, con el mismo truncamiento:

```
punto = 0.5 * max( h(0, S(0)), L_barra ) + 0.5 * H_barra
```

## Costo computacional

El árbol tiene `b^d` nodos terminales. El trabajo crece exponencialmente con la cantidad de fechas de ejercicio, no con la cantidad de factores de riesgo. Esa es la ventaja del método frente a las grillas cuando hay varios factores. Una corrida con `b = 50` y `d = 3` tiene 125000 nodos terminales por árbol.

El método se paraleliza: cada árbol es independiente de los demás.

## Cómo recorre el árbol esta implementación

La función `simulate_levels(market, option, steps, branching, rng)` genera los precios por niveles. Primero dibuja todos los shocks del nivel 1, después los del nivel 2, y así hasta la madurez. Cada fila de shocks produce las `b` ramas de un nodo. El nivel `t`, con `t` de 0 a `d`, queda como un arreglo de `b^t` precios.

La función `tree_estimates(levels, market, option, branching)` recorre los niveles al revés. En la madurez calcula el payoff. En cada nivel anterior reconstruye la matriz de hijos, calcula el promedio de las ramas y aplica las fórmulas del estimador alto y del estimador bajo. La operación `where` de numpy aplica la decisión de ejercicio de las `b` pasadas del estimador bajo a la vez.

Esta estrategia guarda los precios de todos los niveles, `O(b^d)` en total, y a cambio vectoriza con numpy y evita la llamada a función por nodo que tendría una recursión en Python. El recorrido en profundidad del Apéndice C usa `O(b d)` memoria, mucho menos que esos `O(b^d)` precios, pero en Python es más lento por el costo de cada llamada a función. Para los tamaños de este trabajo práctico la memoria no es un problema. Con `b = 50` y `d = 3` hay 127551 nodos en total y alrededor de 1 MB en flotantes. El script `scripts/reproduce_table1.py` reproduce la Tabla 1 del paper en segundos. Queda como mejora futura pasar a un recorrido en profundidad si `d` crece o la memoria aprieta.

La descripción de cada función está en `docs/referencia-api.md`.

## Control variate

El valor europeo de la opción se calcula sobre el mismo árbol simulado: en la madurez es el payoff y en las fechas anteriores es el promedio descontado de los hijos, sin decisión de ejercicio. Ese valor tiene una fórmula exacta, la de Black-Scholes con dividendos continuos. Su error respecto del valor exacto está correlacionado con el error de los estimadores americano alto y bajo, porque comparten las mismas ramas.

Con las réplicas europeas `E_i` y el valor exacto `E`, el ajuste es

```
X_i_ajustado = X_i - beta * (E_i - E)
beta = Cov(X, E) / Var(E)
```

El ajuste no cambia el valor esperado y reduce el error estándar. La Tabla 2 del paper muestra la reducción: el error estándar del estimador bajo en `S(0) = 100` pasa de 0.076 a 0.013. La reducción es menor para opciones muy dentro del dinero, porque ahí el payoff americano y el europeo están menos correlacionados.

## Ejercicio continuo

Los estimadores usan una cantidad finita de fechas de ejercicio. Para aproximar el valor con ejercicio continuo el paper propone extrapolar los valores `C(1), C(2), C(3), ...` con la regla de Richardson, la misma que usa Geske y Johnson (1984). Por ejemplo, con estimaciones `C(1)`, `C(2)` y `C(3)` se puede ajustar un polinomio en `1 / d` y evaluarlo en `d` infinito. Esta implementación no incluye la extrapolación.

## Qué no cubre esta implementación

- Opciones sobre varios activos. El estado sería un vector y cada rama simularía el vector completo.
- Tasas de interés estocásticas y volatilidad estocástica.
- Dividendos discretos. El paper menciona cómo ajustar la simulación para el caso de dividendos en fechas fijas.
- Ejercicio continuo por extrapolación.
- Las mejoras de poda y bootstrap del paper de 1995, y las técnicas de reducción de varianza del paper de 1997 con Jain.

## Cómo leer el paper

| Sección | Contenido |
| --- | --- |
| 1. Introducción | motivación, historia de Tilley, Barraquand y Martineau |
| 2. Overview | intuición de los dos estimadores, Figuras 1 a 6 |
| 3. Analysis | notación precisa, Teoremas 1 a 5 |
| 4. Numerical results | Tablas 1 a 6, control variate y ejercicio continuo |
| 5. Conclusions | extensiones posibles |
| Apéndice A | demostraciones |
| Apéndice B | no existe un estimador insesgado general |
| Apéndice C | pseudocódigo en profundidad, memoria `O(b d)` |

Un orden de lectura posible que combina el paper con los demás recursos:

1. El paper de 1997, secciones 1 y 2.
2. Este documento y una corrida de `python scripts/reproduce_table1.py`.
3. El paper de 1997, sección 3 y Apéndice A.
4. El paper de 1997, sección 4 y Broadie, Glasserman y Jain (1997), para el control variate.
5. Longstaff y Schwartz (2001), para comparar con el método de regresión.
6. El capítulo 8 de Glasserman (2003), para una exposición de texto.
7. Broadie y Glasserman (2004), para la malla estocástica en dimensión alta.

La consigna del trabajo práctico pide `b = 3`. Con ese valor el sesgo de los dos estimadores es grande y el intervalo queda ancho. Sirve como punto de partida y para mostrar la convergencia al aumentar `b`.

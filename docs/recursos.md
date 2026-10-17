# Recursos

Esta lista reúne el paper original, los trabajos de los mismos autores, los métodos que compiten con Broadie-Glasserman y el material de fondo. Las copias locales están en `references/` y solo se incluyen para estudio personal.

## El paper original

**Broadie, M. y Glasserman, P. (1997). Pricing American-style securities using simulation. Journal of Economic Dynamics and Control 21(8-9), 1323-1352.**

- Copia local: `../references/broadie-glasserman-1997.pdf`
- DOI: [10.1016/S0165-1889(97)00029-8](https://doi.org/10.1016/S0165-1889(97)00029-8)
- Espejo en el sitio de Axel Kind: [broadie_glasserman_1997_jedc.pdf](http://www.axelkind.com/teaching/financial_derivatives/papers/broadie_glasserman_1997_jedc.pdf)

La sección 2 explica la intuición con las Figuras 1 a 6. La sección 3 fija la notación y enuncia los Teoremas 1 a 5. La sección 4 tiene las Tablas 1 a 6 y el control variate. El Apéndice C trae el pseudocódigo del recorrido en profundidad.

## Papers de los mismos autores

**Broadie, M. y Glasserman, P. (1995). A pruned and bootstrapped American option simulator. Proceedings of the 1995 Winter Simulation Conference, 212-219.**

- Enlace: [1995_0032.pdf](https://informs-sim.org/wsc95papers/1995_0032.pdf)

Cuenta las mejoras prácticas del método: podar ramas cuando el valor europeo se conoce o cuando el ejercicio es claramente subóptimo, y usar bootstrap para estimar y corregir el sesgo. Es la versión corta de las ideas que después aparecen en el paper de 1997.

**Broadie, M., Glasserman, P. y Jain, G. (1997). Enhanced Monte Carlo estimates for American option prices. The Journal of Derivatives 5(1), 25-44.**

- DOI: [10.3905/jod.1997.407983](https://doi.org/10.3905/jod.1997.407983)
- Resumen y descarga en SSRN: [abstract_id=11257](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=11257)

Estudia el control variate europeo, el muestreo por hipercubo latino y la extrapolación de Richardson para pasar de fechas finitas a ejercicio continuo. Las Tablas 2, 4 y 6 del paper de 1997 usan estas técnicas.

**Boyle, P., Broadie, M. y Glasserman, P. (1997). Monte Carlo methods for security pricing. Journal of Economic Dynamics and Control 21(8-9), 1267-1321.**

- DOI: [10.1016/S0165-1889(97)00028-6](https://doi.org/10.1016/S0165-1889(97)00028-6)

Es un relevamiento general de simulación en finanzas. Ubica a Broadie-Glasserman entre los demás métodos de la época y cubre reducción de varianza, números cuasi aleatorios y sensibilidad de precios.

**Broadie, M. y Glasserman, P. (2004). A stochastic mesh method for pricing high-dimensional American options. Journal of Computational Finance 7(4), 35-72.**

- Enlace: [v7n4a3_Broadie.pdf](http://www.columbia.edu/~mnb2/broadie/Assets/v7n4a3_Broadie.pdf)

Reemplaza el árbol por una malla de estados simulados. Cada nodo se conecta con todos los nodos del nivel siguiente con pesos, así que la cantidad de conexiones deja de crecer exponencialmente. Es la extensión del método a dimensión alta.

## Métodos alternativos

**Longstaff, F. y Schwartz, E. (2001). Valuing American options by simulation: a simple least-squares approach. Review of Financial Studies 14(1), 113-147.**

- Copia local: `../references/longstaff-schwartz-2001.pdf`
- DOI: [10.1093/rfs/14.1.113](https://doi.org/10.1093/rfs/14.1.113)
- PDF de la ETH: [LongstaffSchwartzAmericanOptionsLeastSquareMonteCarlo.pdf](https://people.math.ethz.ch/~hjfurrer/teaching/LongstaffSchwartzAmericanOptionsLeastSquareMonteCarlo.pdf)

El método de regresión por mínimos cuadrados. En lugar de un árbol, estima el valor de continuación con una regresión sobre los caminos. Maneja muchas fechas de ejercicio sin costo exponencial. El paper compara sus valores con las cotas de Broadie-Glasserman.

**Tilley, J. (1993). Valuing American options in a path simulation model. Transactions of the Society of Actuaries 45, 83-104.**

- PDF en ResearchGate: [Valuing American Options in a Path Simulation Model](https://www.researchgate.net/profile/James-Tilley-4/publication/237326444_111_Valuing_American_Options_in_a_Path_Simulation_Model/links/5cc33b84299bf12097827fb1/111-Valuing-American-Options-in-a-Path-Simulation-Model.pdf)

El primer intento de valorar opciones americanas con simulación. Agrupa caminos por precio y estima una decisión de ejercicio por grupo. Tiene problemas de convergencia y de almacenamiento, y el paper de 1997 los discute en la introducción.

**Barraquand, J. y Martineau, D. (1995). Numerical valuation of high dimensional multivariate American securities. Journal of Financial and Quantitative Analysis 30(3), 383-405.**

- DOI: [10.2307/2331347](https://doi.org/10.2307/2331347)

Método de estratificación para dimensión alta. Compite con el árbol simulado en la misma clase de problemas.

**Carriere, J. (1996). Valuation of the early-exercise price for options using simulations and nonparametric regression. Insurance: Mathematics and Economics 19(1), 19-30.**

- DOI: [10.1016/S0167-6687(96)00004-2](https://doi.org/10.1016/S0167-6687(96)00004-2)

Estima el valor de continuación con splines. Es un antecedente de la regresión de Longstaff y Schwartz.

## Libros

**Glasserman, P. (2003). Monte Carlo Methods in Financial Engineering. Springer.**

- DOI: [10.1007/978-0-387-21617-1](https://doi.org/10.1007/978-0-387-21617-1)

El capítulo 8 cubre las opciones americanas por simulación: árbol aleatorio, estimadores alto y bajo, reducción de varianza y formulaciones duales.

**Hull, J. (2021). Options, Futures, and Other Derivatives. Pearson.**

- Página del libro: [pearson.com](https://www.pearson.com/en-us/subject-catalog/p/options-futures-and-other-derivatives/P200000005938)

Cubre opciones americanas, árboles binomiales y procedimientos numéricos en general.

**Baxter, M. y Rennie, A. (1996). Financial Calculus: An Introduction to Derivative Pricing. Cambridge University Press.**

- Página del libro: [cambridge.org](https://www.cambridge.org/us/universitypress/subjects/mathematics/mathematical-finance/financial-calculus-introduction-derivative-pricing)

Introducción a la valoración neutral al riesgo y a las martingalas.

## Tesis, notas y material del curso

**Larsson, K. (2007). Pricing American Options using Simulation. Tesis de maestría, Uppsala University.**

- Enlace: [DIVA fulltext](https://www.diva-portal.org/smash/get/diva2:479155/FULLTEXT01.pdf)
- Registro: [diva2:479155](https://www.diva-portal.org/smash/record.jsf?pid=diva2%3A479155)

Explica el árbol aleatorio paso a paso y lo compara numéricamente con otros métodos.

**Wieslander, P. (2013). On Monte Carlo approximation of the Snell envelope with application to the pricing of American options. Tesis de maestría, Lund University.**

- Copia local: `../references/wieslander-2013-snell-envelope.pdf`
- Enlace: [student-papers/record/4618206](https://lup.lub.lu.se/student-papers/record/4618206)

Presenta el método desde la envolvente de Snell y deriva los estimadores alto y bajo dentro de ese marco.

**Notas de Modelos Matemáticos en Finanzas Cuantitativas (2026).**

- Copia local: `../references/curso/notas-finanzas-cuantitativas-2026.pdf`

Material del curso. Sirven de fondo las páginas 20, 24, 37, 40 y 58 para opciones americanas, la página 63 para simulación de Monte Carlo y las páginas 74 a 80 para el modelo trinomial discreto y las medidas de martingala. El trinomial del curso recombina y se construye con un modelo discreto; el árbol de Broadie-Glasserman no recombina y se genera simulando el movimiento geométrico browniano. Esa diferencia es la que pide la consigna.

**Matemática Financiera (2010). Colección Las Ciencias Naturales y la Matemática, Ministerio de Educación de Argentina.**

- Copia local: `../references/curso/matematica-financiera.pdf`

Libro de distribución gratuita. El capítulo 10.3 cubre opciones de compra y venta como introducción.

**Consigna del trabajo práctico.**

- Copia local: `../references/consigna-tp.pdf`

Pide estudiar el método para `b = 3`, valorar opciones americanas por simulación e implementar el algoritmo para estimar un intervalo de confianza.

## Implementaciones

- `cantaro86/Financial-Models-Numerical-Methods`: [repositorio](https://github.com/cantaro86/Financial-Models-Numerical-Methods). Cuadernos de métodos numéricos en Python. Tiene un cuaderno de opciones americanas con Longstaff-Schwartz, útil para comparar.
- QuantLib: [quantlib.org](https://www.quantlib.org/). Biblioteca en C++ con árboles binomiales y trinomiales. No implementa el árbol aleatorio, pero sirve como referencia de precios.
- GitHub topic `american-options`: [github.com/topics/american-options](https://github.com/topics/american-options).

## Videos y cursos

- *American Monte-Carlo, Bermudan Options (1/2)*: [youtube.com/watch?v=Q4vfoDUkTsM](https://www.youtube.com/watch?v=Q4vfoDUkTsM). Sesión sobre Monte Carlo americano y opciones bermudas. No sigue el paper, pero cubre el mismo problema.
- Búsqueda en YouTube: [Broadie Glasserman American option simulation](https://www.youtube.com/results?search_query=broadie+glasserman+american+option+simulation).

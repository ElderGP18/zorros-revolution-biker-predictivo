# Capítulo IV – Presentación y Análisis de Resultados

Este capítulo presenta los datos obtenidos durante la fase de validación técnica del sistema y los interpreta en relación con el problema, los objetivos específicos y las bases teóricas del Capítulo II. Conviene delimitar desde el inicio su alcance: durante esta fase no se dispuso de acceso a los registros históricos de Zorros Revolution Biker, por lo que los instrumentos de recolección de carácter cualitativo definidos en el Capítulo III —entrevista semiestructurada, cuestionario de usabilidad y observación directa— quedan en estado de diseño, listos para su aplicación en la fase de prueba piloto. Los resultados que aquí se reportan provienen del componente cuantitativo: la ficha de perfilamiento de datos y los registros de evaluación que el propio sistema genera al comparar los modelos de pronóstico.

Los datos sobre los que operó el sistema son **simulados**. No representan ventas de la empresa y ninguna cifra de este capítulo debe leerse como un hallazgo sobre su operación. Lo que la simulación permite validar es el procedimiento: que el motor de pronóstico calcula las métricas correctas, compara los candidatos bajo el protocolo exigido por el marco teórico y aplica el criterio de publicación tal como fue diseñado. En cada tabla se indica explícitamente esta procedencia.

## 4.1 Presentación de resultados

### 4.1.1 Estado de aplicación de los instrumentos

La Tabla 13 resume qué instrumentos del Capítulo III se aplicaron en esta fase y cuáles quedan pendientes, con el motivo.

| Instrumento (Cap. III) | Estado | Observación |
|---|---|---|
| 3.3.1 Entrevista semiestructurada | Diseñado, no aplicado | Requiere acceso a la gerencia de la empresa; programado para la prueba piloto |
| 3.3.2 Cuestionario de usabilidad (Likert) | Diseñado, no aplicado | Se aplicará sobre el MVP desplegado, con las tareas observables del RNF-05 |
| 3.3.3 Observación directa | No aplicado | Requiere una sesión de preparación de ventas en la empresa |
| 3.3.4 Revisión documental | Parcial | Se revisó la información pública de la empresa; no se accedió a reportes internos |
| 3.3.5 Ficha de perfilamiento de datos | Aplicada sobre datos simulados | El sistema calcula el perfil de cada serie de forma automática (sección 4.1.3) |
| Registros del sistema (evaluación de modelos) | Aplicados sobre datos simulados | Métricas, ventanas de validación y decisión de publicación (secciones 4.1.5 a 4.1.7) |

Tabla 13. Estado de aplicación de los instrumentos de recolección de datos. Fuente: Elaboración propia.

### 4.1.2 Naturaleza de los datos utilizados

Para validar el sistema se construyó un simulador de ventas que genera doce meses de transacciones sobre el catálogo de 25 productos del prototipo. El simulador se diseñó para reproducir las propiedades que el marco teórico identifica como determinantes en el comercio minorista de accesorios: demanda intermitente por producto (Syntetos, Boylan y Croston, 2005), estacionalidad ligada al calendario guatemalteco (quincenas, Bono 14, aguinaldo, Caravana del Zorro y feriados), promociones de corta duración y, de manera central, la demanda censurada por inventario descrita en la sección 2.1: cuando un producto se agota, la venta se pierde y no queda registrada.

Un requisito de diseño del simulador fue no compartir ninguna función con las variables que el modelo recibe como entrada. Un generador que use las mismas funciones de calendario que las características del modelo le entrega la respuesta por construcción, y cualquier métrica obtenida resulta circular. La sección 4.1.7 presenta el efecto medido de esta decisión. El conjunto resultante se resume en la Tabla 14.

| Característica | Valor |
|---|---|
| Periodo | 18 de septiembre de 2025 al 18 de septiembre de 2026 (366 días) |
| Productos con ventas | 25 |
| Tickets registrados | 1,607 |
| Unidades vendidas | 2,492 |
| Unidades demandadas no atendidas por falta de existencia | 424 (14.5 % de la demanda simulada) |
| Días con al menos una venta | 359 de 366 |
| Ingreso total simulado | Q 1,610,560 |
| Ticket promedio simulado | Q 1,002.22 |

Tabla 14. Características del conjunto de datos simulado utilizado en la validación técnica. Fuente: Elaboración propia a partir de los registros del sistema (datos simulados).

### 4.1.3 Resultados del perfilamiento de series

El sistema calcula para cada producto, a partir de sus unidades vendidas por día, los tres estadísticos que la sección 2.2.3 exige antes de entrenar: la proporción de días sin venta, el intervalo promedio entre demandas (ADI, por sus siglas en inglés) y el coeficiente de variación al cuadrado de las cantidades positivas (CV²). Con ellos clasifica cada serie según el esquema de Syntetos, Boylan y Croston (2005), con los cortes ADI = 1.32 y CV² = 0.49. La Tabla 15 presenta los estadísticos del catálogo completo y la Figura 7 la distribución de la proporción de días sin venta.

| Estadístico | Mínimo | Mediana | Media | Máximo |
|---|---|---|---|---|
| Proporción de días sin venta | 59.1 % | 79.1 % | 77.3 % | 88.6 % |
| Intervalo promedio entre demandas (ADI, días) | 2.45 | — | 5.15 | 8.73 |
| CV² de las cantidades positivas | 0.023 | — | 0.130 | 0.291 |
| Clasificación resultante | Intermitente: 25 de 25 productos (100 %) | | | |

Tabla 15. Perfil de intermitencia de las 25 series de demanda (n = 25). Fuente: Elaboración propia a partir de los registros del sistema (datos simulados).

![Figura 7. Distribución de la proporción de días sin venta por producto (n = 25).](figura7_dias_sin_venta.png)

Figura 7. Distribución de la proporción de días sin venta por producto (n = 25). Fuente: Elaboración propia a partir de los registros del sistema (datos simulados).

Ningún producto alcanzó el umbral de ADI < 1.32 que caracteriza a una serie regular. El producto con mayor rotación (espejos retrovisores, 189 unidades en el periodo) registró ventas en el 40.2 % de los días; el de menor rotación (botas urbanas, 42 unidades), en el 11.5 %. La Tabla 16 muestra los cinco productos de mayor y los cinco de menor volumen.

| Producto (SKU) | Unidades | Días sin venta | ADI (días) | CV² | Clasificación |
|---|---|---|---|---|---|
| ACC-ESPEJOS | 189 | 59.8 % | 2.49 | 0.20 | Intermitente |
| CAS-VISOR | 186 | 59.1 % | 2.45 | 0.18 | Intermitente |
| GTE-VERANO | 165 | 66.4 % | 2.98 | 0.23 | Intermitente |
| ACC-CANDADO | 162 | 65.5 % | 2.90 | 0.24 | Intermitente |
| CHQ-VMAX-PRO | 150 | 68.4 % | 3.17 | 0.19 | Intermitente |
| … | | | | | |
| CAS-XR700 | 56 | 85.4 % | 6.85 | 0.06 | Intermitente |
| ACC-PORTA | 52 | 87.0 % | 7.67 | 0.09 | Intermitente |
| ACC-COVER | 47 | 87.5 % | 7.98 | 0.04 | Intermitente |
| CHQ-LLUVIA | 46 | 88.1 % | 8.43 | 0.07 | Intermitente |
| BOT-URBANA | 42 | 88.5 % | 8.73 | 0.02 | Intermitente |

Tabla 16. Perfil de los cinco productos de mayor y de menor volumen. Fuente: Elaboración propia a partir de los registros del sistema (datos simulados).

### 4.1.4 Serie agregada de ventas

El modelo de pronóstico de esta fase opera sobre el total diario de ventas en quetzales. La Figura 8 presenta la serie de 366 días con su media móvil de siete días y los periodos de temporada alta señalados, y la Tabla 17 los totales mensuales.

![Figura 8. Serie diaria simulada de ventas con los periodos de temporada alta señalados.](figura8_serie_diaria.png)

Figura 8. Serie diaria simulada de ventas con los periodos de temporada alta señalados. Fuente: Elaboración propia a partir de los registros del sistema (datos simulados).

| Mes | Tickets | Ingreso (Q) | Mes | Tickets | Ingreso (Q) |
|---|---|---|---|---|---|
| Sep. 2025 (13 días) | 59 | 62,490 | Abr. 2026 | 130 | 137,520 |
| Oct. 2025 | 130 | 120,870 | May. 2026 | 148 | 163,660 |
| Nov. 2025 | 72 | 78,780 | Jun. 2026 | 140 | 136,250 |
| Dic. 2025 | 168 | 175,590 | Jul. 2026 | 171 | 155,180 |
| Ene. 2026 | 111 | 124,280 | Ago. 2026 | 156 | 162,480 |
| Feb. 2026 | 118 | 108,970 | Sep. 2026 (18 días) | 68 | 60,860 |
| Mar. 2026 | 136 | 123,630 | **Total** | **1,607** | **1,610,560** |

Tabla 17. Ventas simuladas por mes. Fuente: Elaboración propia a partir de los registros del sistema (datos simulados).

Diciembre concentró el mayor ingreso mensual (Q 175,590) y julio el mayor número de tickets (171). Noviembre presentó el menor volumen de un mes completo (72 tickets).

![Figura 9. Ingreso mensual simulado.](figura9_ventas_mensuales.png)

Figura 9. Ingreso mensual simulado. Fuente: Elaboración propia a partir de los registros del sistema (datos simulados).

### 4.1.5 Resultados de la evaluación de modelos

El sistema evaluó siete candidatos bajo el protocolo de la sección 2.5: validación temporal con origen móvil, cinco ventanas sucesivas de 30 días y reentrenamiento en cada corte con únicamente el pasado disponible. Los seis primeros son los métodos de referencia exigidos por la sección 2.2.2; el séptimo es el modelo de aprendizaje automático (árboles potenciados por gradiente) con variables de calendario, rezagos y medias móviles. Las ventanas de validación tuvieron cortes en los días 216, 246, 276, 306 y 336 de la serie, de modo que el entrenamiento más corto contó con 216 observaciones y el más largo con 336. La Tabla 18 reporta el promedio de las seis métricas de la Tabla 2 en las cinco ventanas.

| Candidato | MAE (Q) | RMSE (Q) | WAPE (%) | sMAPE (%) | Sesgo (Q/día) | MASE |
|---|---|---|---|---|---|---|
| Gradient boosting (modelo) | 2,126.3 | 2,738.1 | 43.99 | 47.88 | −754.3 | **0.8030** |
| Suavizamiento exponencial | 2,198.3 | 2,796.6 | 46.06 | 47.99 | −130.1 | 0.8305 |
| ARIMA (1,1,1) | 2,226.1 | 2,823.4 | 46.57 | 48.61 | −178.4 | 0.8410 |
| Holt-Winters aditivo | 2,253.7 | 2,792.4 | 46.55 | 52.45 | −707.1 | 0.8505 |
| Media móvil (7 días) | 2,346.2 | 2,979.2 | 48.85 | 51.28 | −310.6 | 0.8861 |
| Naïve estacional (referencia) | 2,736.0 | 3,354.4 | 56.95 | 64.53 | −331.9 | 1.0341 |
| Naïve | 2,773.6 | 3,492.4 | 57.97 | 70.08 | −1,505.2 | 1.0499 |

Tabla 18. Métricas promedio de los siete candidatos en cinco ventanas de origen móvil (horizonte de 30 días). Fuente: Elaboración propia a partir de los registros del sistema (datos simulados).

El modelo de aprendizaje automático obtuvo el menor error en las seis métricas, con un MASE promedio de 0.8030 frente a 1.0341 del naïve estacional. La distancia respecto del segundo candidato, el suavizamiento exponencial simple, fue de 0.0275 unidades de MASE. La Tabla 19 desagrega el MASE por ventana y la Figura 10 compara el modelo con la referencia.

| Candidato | Ventana 1 | Ventana 2 | Ventana 3 | Ventana 4 | Ventana 5 | Media |
|---|---|---|---|---|---|---|
| Gradient boosting (modelo) | 0.817 | 0.976 | 0.804 | 0.826 | 0.592 | 0.803 |
| Suavizamiento exponencial | 0.828 | 0.909 | 0.693 | 0.915 | 0.808 | 0.831 |
| ARIMA (1,1,1) | 0.826 | 0.948 | 0.704 | 0.920 | 0.807 | 0.841 |
| Holt-Winters aditivo | 0.760 | 1.056 | 0.934 | 0.860 | 0.642 | 0.851 |
| Media móvil (7 días) | 0.819 | 1.056 | 0.791 | 0.965 | 0.799 | 0.886 |
| Naïve estacional (referencia) | 1.056 | 1.297 | 0.777 | 1.121 | 0.918 | 1.034 |
| Naïve | 1.396 | 0.888 | 0.718 | 1.444 | 0.804 | 1.050 |

Tabla 19. MASE por ventana de validación. Fuente: Elaboración propia a partir de los registros del sistema (datos simulados).

![Figura 10. MASE por ventana de validación: modelo frente a la referencia naïve estacional.](figura10_mase_por_ventana.png)

Figura 10. MASE por ventana de validación: modelo frente a la referencia naïve estacional. Fuente: Elaboración propia a partir de los registros del sistema (datos simulados).

El modelo superó a la referencia en cuatro de las cinco ventanas. En la ventana 3 el naïve estacional obtuvo un MASE de 0.777 frente a 0.804 del modelo. La Tabla 20 presenta el sesgo y el WAPE del modelo en cada ventana.

| Ventana | Corte (día) | Observaciones de entrenamiento | Sesgo (Q/día) | WAPE (%) |
|---|---|---|---|---|
| 1 | 216 | 216 | −662.0 | 46.89 |
| 2 | 246 | 246 | −1,654.6 | 47.27 |
| 3 | 276 | 276 | −1,300.4 | 43.94 |
| 4 | 306 | 306 | −668.4 | 41.97 |
| 5 | 336 | 336 | +513.7 | 39.86 |

Tabla 20. Sesgo y WAPE del modelo por ventana de validación. Fuente: Elaboración propia a partir de los registros del sistema (datos simulados).

El sesgo fue negativo en cuatro ventanas, es decir, el modelo subestimó las ventas, y el WAPE disminuyó de forma sostenida desde 46.89 % en la primera ventana hasta 39.86 % en la quinta, a medida que el conjunto de entrenamiento creció.

### 4.1.6 Resultado del criterio de publicación

Tras la evaluación, el sistema aplicó el criterio de aceptación de la sección 2.5.1. La Tabla 21 muestra el resultado de cada condición.

| Condición (sección 2.5.1) | Umbral | Valor obtenido | Resultado |
|---|---|---|---|
| Mejora del error escalado sobre el naïve estacional | ≥ 10 % | 22.35 % | Cumple |
| Sesgo relativo al volumen medio del periodo | ≤ 20 % | 19.06 % | Cumple |
| Consistencia (ventanas en que supera la referencia) | > 50 % | 80 % (4 de 5) | Cumple |
| Decisión | | Modelo publicado | |

Tabla 21. Resultado del criterio de publicación aplicado por el sistema. Fuente: Elaboración propia a partir de los registros del sistema (datos simulados).

### 4.1.7 Efecto del generador de datos sobre la evaluación

Antes de construir el simulador descrito en 4.1.2, el sistema se evaluó sobre un conjunto generado por un procedimiento anterior que utilizaba las mismas tres funciones de calendario que el modelo recibe como características. La Tabla 22 compara ambas evaluaciones bajo el mismo protocolo.

| Indicador | Generador anterior (comparte funciones con el modelo) | Simulador actual (sin funciones compartidas) |
|---|---|---|
| MASE del modelo | 0.6992 | 0.8030 |
| MASE del naïve estacional | 1.0762 | 1.0341 |
| Mejora sobre la referencia | 35.0 % | 22.4 % |
| Distancia al mejor método simple (MASE) | 0.119 | 0.028 |
| Sesgo relativo | 8.9 % | 19.1 % |
| Demanda censurada por inventario | No simulada | 14.5 % de la demanda |

Tabla 22. Comparación de la evaluación del modelo según el procedimiento de generación de datos. Fuente: Elaboración propia a partir de los registros del sistema (datos simulados).

### 4.1.8 Resultados de las pruebas del sistema y del despliegue

Además de la evaluación del modelo, el sistema cuenta con 128 pruebas automatizadas que verifican las fórmulas de las métricas contra valores calculados a mano, la ausencia de fuga de información temporal en la validación, el perfilamiento de series, la simulación y la gestión de usuarios (Tabla 23). El despliegue en producción se midió en un servidor de un núcleo: el proceso de la API consume entre 331 y 355 MB de memoria, la base de datos 47 MB, y el ciclo completo de evaluación de los siete candidatos en cinco ventanas tarda entre 3 y 5 segundos.

| Módulo verificado | Pruebas | Resultado |
|---|---|---|
| Métricas de evaluación (MASE, WAPE, MAE, RMSE, sMAPE, sesgo) | 19 | 19 aprobadas |
| Líneas base y validación de origen móvil | 32 | 32 aprobadas |
| Perfilamiento de series | 20 | 20 aprobadas |
| Simulador de ventas | 30 | 30 aprobadas |
| Usuarios, roles y contraseñas | 27 | 27 aprobadas |
| **Total** | **128** | **128 aprobadas** |

Tabla 23. Pruebas automatizadas del sistema por módulo. Fuente: Elaboración propia a partir de los registros del sistema.

## 4.2 Análisis e interpretación de resultados

### 4.2.1 La intermitencia del catálogo determina la estrategia de modelado

El resultado de la sección 4.1.3 —25 de 25 series clasificadas como intermitentes, con un 77 % de días sin venta en promedio y un intervalo medio de 5.2 días entre demandas— responde al primer paso que el marco teórico exige antes de entrenar (sección 2.2.3) y tiene una consecuencia directa de diseño. Una serie con más de tres de cada cuatro días en cero no admite un regresor diario por producto: el modelo aprendería que la mejor predicción es cero y las métricas porcentuales quedarían indefinidas, tal como advierten Hyndman y Koehler (2006). Esta es la razón por la que el motor de esta fase pronostica el total diario del negocio y no cada producto, y por la que el paso siguiente del proyecto es la agregación temporal por producto o un método específico de demanda intermitente (Croston, 1972; Syntetos y Boylan, 2005). El hallazgo coincide con lo anticipado en la sección 2.3.3 a partir de Mejía y Aguilar (2024): los productos de un catálogo de accesorios no comparten un único comportamiento y requieren una estrategia por tipo de serie. Aunque el dato proviene de la simulación, su implicación metodológica es independiente del origen: un catálogo real con tallas, colores y diseños será, con toda probabilidad, todavía más disperso.

### 4.2.2 El modelo de aprendizaje automático supera a las referencias, pero por un margen estrecho

El marco teórico establece que un modelo de inteligencia artificial solo agrega valor si supera de forma consistente a los métodos de referencia (sección 2.2.2). Los resultados de la Tabla 18 lo confirman en el sentido literal: el modelo obtuvo el menor error en las seis métricas y le ganó al naïve estacional en cuatro de cinco ventanas, con una reducción media del MASE de 22.4 %. Sin embargo, la Tabla 19 obliga a matizar la lectura. El suavizamiento exponencial simple, un método con un único parámetro, quedó a 0.028 unidades de MASE del modelo, y en las ventanas 2 y 3 lo superó. La diferencia entre el modelo y el conjunto de métodos simples (suavizamiento, ARIMA, Holt-Winters) es mucho menor que la diferencia entre ese conjunto y el naïve. Esto es coherente con la evidencia de la competencia M5 (Makridakis, Spiliotis y Assimakopoulos, 2022) y con la advertencia de Swami, Shah y Ray (2020): la complejidad del modelo no garantiza por sí sola una mejora, y el valor de los métodos de aprendizaje automático depende de la calidad de las variables y de la cantidad de historia disponible. En términos del objetivo específico 3, el sistema cumple con comparar los modelos bajo un mismo protocolo y con hacerlo verificable; en términos del objetivo específico 6, el criterio de aceptación operó como se diseñó.

### 4.2.3 El sesgo negativo y la ventana de doce meses

El modelo subestimó las ventas en cuatro de las cinco ventanas (Tabla 20), con un sesgo relativo del 19.1 % que quedó a menos de un punto del límite del 20 % fijado en el criterio de publicación. La interpretación más plausible no está en el algoritmo sino en la longitud del historial. Con doce meses de datos, cada evento anual aparece una sola vez en la serie, y las ventanas de validación cubren de finales de abril a septiembre de 2026; la tercera ventana (21 de junio a 20 de julio) contiene el Bono 14. Para el modelo, ese pico ocurre por primera vez en el conjunto de prueba: no existe en su entrenamiento ningún julio anterior del cual aprender la magnitud del efecto. La ventana 5, la única con sesgo positivo, es también la única cuyo entrenamiento ya incluye el pico de julio completo. El resultado ilustra de forma concreta la afirmación de la sección 1.6.4 de que una ventana de veinticuatro meses es la ideal para observar ciclos anuales: con doce meses, el sistema puede modelar la estacionalidad semanal y la tendencia, pero no puede anticipar un evento anual que no ha visto.

### 4.2.4 La circularidad del generador anterior explica la diferencia entre 35 % y 22 %

La Tabla 22 documenta un hallazgo metodológico que el equipo considera el más importante de la fase. Bajo el generador anterior, el modelo reportaba una mejora del 35 % sobre la referencia y una distancia de 0.119 unidades de MASE respecto del mejor método simple. Al reemplazarlo por un simulador que no comparte ninguna función con las variables del modelo, la mejora descendió a 22 % y la distancia a 0.028. La explicación es directa: si el proceso que genera los datos utiliza las mismas funciones que el modelo recibe como entrada, el modelo recupera por construcción la señal que se le inyectó, y la evaluación mide la coincidencia entre generador y modelo, no la capacidad de pronóstico. Este tipo de fuga de información es una de las advertencias centrales de la sección 2.3 y de la literatura sobre evaluación de series temporales (Bergmeir y Benítez, 2012; Tashman, 2000). La consecuencia práctica es que el 22 % es la cifra defendible del sistema en su estado actual y el 35 % no lo era. Se incluyen ambas precisamente porque el contraste demuestra que el protocolo de evaluación es sensible a la fuga y la detecta.

### 4.2.5 Relación entre resultados: demanda censurada, sesgo y perfil

Los resultados no son independientes entre sí. El simulador perdió el 14.5 % de la demanda por falta de existencia (Tabla 14), un fenómeno que la sección 2.1 describe como demanda censurada por inventario: las unidades vendidas subestiman la demanda potencial cuando el producto se agota. Un modelo entrenado sobre ventas observadas aprende, por tanto, una demanda menor a la real, lo que contribuye al sesgo negativo de la Tabla 20 junto con el efecto de la ventana de doce meses. A su vez, el perfil intermitente de la Tabla 15 es en parte producto de esos quiebres: los días sin existencia son también días sin venta. La cadena perfil → agregación → sesgo muestra por qué la sección 2.4 (Tabla 1) incluye la existencia y los días sin stock entre las características candidatas del modelo, y por qué su incorporación es una de las mejoras previstas.

### 4.2.6 Cierre parcial por objetivo específico

En conjunto, los datos permiten afirmar lo siguiente respecto de los objetivos específicos de la sección 1.5.2, con la salvedad de que provienen de una validación técnica sobre datos simulados:

- **Objetivo 2** (proceso reproducible de integración y validación de datos): no evaluable en esta fase; el sistema aún no dispone de un importador de históricos.
- **Objetivo 3** (comparar modelos de referencia y de inteligencia artificial mediante validación temporal con origen móvil y métricas apropiadas): cumplido en cuanto al procedimiento. Seis referencias y un modelo de aprendizaje automático se evaluaron en cinco ventanas con MASE, WAPE, MAE, RMSE, sMAPE y sesgo.
- **Objetivo 4** (arquitectura web para consultar pronósticos, métricas y alertas): cumplido parcialmente; se consultan pronósticos, métricas y alertas, pero no intervalos derivados del modelo ni explicaciones.
- **Objetivo 6** (criterios de aceptación para publicar un modelo solo cuando supere la línea base): cumplido; el criterio operó automáticamente y su decisión quedó registrada.

## 4.3 Comprobación de hipótesis

### 4.3.1 Formulación

El Capítulo I plantea una interrogante de investigación y no una hipótesis formal, dado el alcance descriptivo y correlacional declarado en la sección 3.1. No obstante, el criterio técnico de la sección 2.5.1 contiene una afirmación comprobable que el diseño no experimental de esta fase sí permite contrastar: que el modelo de aprendizaje automático produce un error escalado menor que el método de referencia naïve estacional. De ella se derivan los enunciados siguientes, donde d<sub>i</sub> es la diferencia MASE<sub>modelo</sub> − MASE<sub>referencia</sub> en la ventana i y μ<sub>d</sub> su media.

- H<sub>0</sub>: μ<sub>d</sub> ≥ 0 (el modelo no reduce el error escalado respecto del naïve estacional).
- H<sub>1</sub>: μ<sub>d</sub> < 0 (el modelo reduce el error escalado respecto del naïve estacional).

De manera complementaria, el umbral de mejora mínima del 10 % de la sección 2.5.1 permite formular una segunda prueba más exigente:

- H<sub>0</sub>': MASE<sub>modelo</sub> ≥ 0.90 × MASE<sub>referencia</sub> (la mejora no alcanza el 10 %).
- H<sub>1</sub>': MASE<sub>modelo</sub> < 0.90 × MASE<sub>referencia</sub> (la mejora supera el 10 %).

### 4.3.2 Prueba seleccionada y nivel de significancia

Las cinco ventanas de validación son las mismas para el modelo y para la referencia, de modo que las observaciones están emparejadas. La prueba adecuada es la t de Student para muestras relacionadas, unilateral, con α = 0.05 (Hernández Sampieri, Fernández Collado y Baptista Lucio, 2014). Dado que con n = 5 no es posible verificar de forma robusta el supuesto de normalidad de las diferencias, se reporta además la prueba no paramétrica de rangos con signo de Wilcoxon (1945) y el tamaño del efecto d de Cohen (1988). Con más ventanas disponibles, la prueba de referencia en la literatura para comparar la precisión de dos pronósticos es la de Diebold y Mariano (1995), que se propone para la fase con datos reales.

### 4.3.3 Resultados

La Tabla 24 resume las diferencias por ventana y los estadísticos obtenidos.

| Ventana | MASE modelo | MASE referencia | Diferencia d<sub>i</sub> |
|---|---|---|---|
| 1 | 0.8174 | 1.0564 | −0.2391 |
| 2 | 0.9757 | 1.2971 | −0.3214 |
| 3 | 0.8041 | 0.7775 | +0.0267 |
| 4 | 0.8258 | 1.1214 | −0.2956 |
| 5 | 0.5921 | 0.9183 | −0.3263 |
| Media de las diferencias | | | −0.2311 |
| Desviación estándar de las diferencias | | | 0.1482 |

Tabla 24. Diferencias de MASE por ventana entre el modelo y la referencia naïve estacional. Fuente: Elaboración propia a partir de los registros del sistema (datos simulados).

| Prueba | Estadístico | Valor p (unilateral) | Decisión (α = 0.05) |
|---|---|---|---|
| t de Student pareada (H<sub>0</sub>: μ<sub>d</sub> ≥ 0) | t(4) = −3.487 | 0.013 | Se rechaza H<sub>0</sub> |
| Wilcoxon de rangos con signo (H<sub>0</sub>: μ<sub>d</sub> ≥ 0) | W = 1 | 0.063 | No se rechaza H<sub>0</sub> |
| Tamaño del efecto | d de Cohen = −1.56 | — | Efecto grande |
| t de Student pareada contra el umbral del 10 % (H<sub>0</sub>') | t(4) = −2.121 | 0.051 | No se rechaza H<sub>0</sub>' |

Tabla 25. Resultados de la comprobación de hipótesis. Fuente: Elaboración propia a partir de los registros del sistema (datos simulados).

### 4.3.4 Conclusión de la prueba

Con la prueba t pareada, el valor p de 0.013 es menor que α = 0.05, por lo que se rechaza H<sub>0</sub>: existe evidencia estadística de que el modelo de aprendizaje automático reduce el error escalado respecto del naïve estacional en el conjunto evaluado, con un tamaño del efecto grande (d = −1.56). La prueba de Wilcoxon no alcanza la significancia al 5 % (p = 0.063), lo que se explica por el tamaño de la muestra: con cinco pares, el menor valor p unilateral posible es 0.031 y solo se obtiene cuando las cinco diferencias tienen el mismo signo; con cuatro de cinco, el resultado es exactamente 0.0625. La discrepancia entre ambas pruebas no refleja un desacuerdo sobre la dirección del efecto sino la escasa potencia que cinco observaciones otorgan a la prueba no paramétrica.

La segunda prueba es más exigente y su resultado más matizado. La mejora media observada, 22.35 %, supera el umbral del 10 % de la sección 2.5.1; sin embargo, el valor p de 0.051 no permite rechazar H<sub>0</sub>' al 5 %, por un margen de una milésima. Es decir, los datos son compatibles con que el modelo supere el umbral, pero cinco ventanas no bastan para afirmarlo con la confianza exigida. Esta conclusión es coherente con las secciones 4.2.3 y 4.2.4: el sistema aplica el criterio del 10 % sobre el promedio de las ventanas, tal como se diseñó, pero la certeza estadística sobre ese umbral requiere más historia —y por tanto más ventanas de validación— que la disponible en doce meses.

Corresponde reiterar el alcance de estas pruebas. Los datos son simulados, de modo que lo comprobado es que el procedimiento del sistema —su protocolo de validación, sus métricas y su criterio de publicación— distingue correctamente entre un modelo que mejora la referencia y uno que no. La respuesta a la interrogante de investigación de la sección 1.4, referida a la precisión y oportunidad de la información frente a los métodos actualmente empleados en la empresa, queda condicionada a la aplicación del mismo protocolo sobre los registros reales de Zorros Revolution Biker en la fase de prueba piloto.

<!-- Contenido nuevo de los Capítulos I a III, incorporado por reestructurar_docx.py según las
observaciones de la revisión. Cada bloque se inserta en el lugar que indica su nombre.
Las referencias "Tabla N" y "Figura N" usan la numeración de las fuentes (Word de agosto y
capítulos en Markdown); el pipeline las renumera según el orden final del documento. -->

<!-- bloque: pregunta -->
De este planteamiento se desprende la pregunta de investigación que orienta el resto del documento: ¿en qué medida un sistema web predictivo basado en inteligencia artificial, entrenado y evaluado con los datos históricos de Zorros Revolution Biker, puede mejorar la precisión y oportunidad de la información utilizada para la gestión de ventas frente a los métodos de estimación actualmente empleados?

<!-- bloque: objetivos -->
1. Diagnosticar el proceso actual de registro, consolidación y planificación de ventas de Zorros Revolution Biker, incluido el método con que hoy se estiman las ventas, así como las necesidades de información de los usuarios responsables.
2. Desarrollar un sistema web de arquitectura modular que integre los datos históricos con trazabilidad, compare modelos de referencia y de inteligencia artificial mediante validación temporal con origen móvil, publique solo los que superen la línea base acordada y permita consultar pronósticos, métricas y alertas sin exponer datos sensibles innecesarios.
3. Evaluar la mejora en la precisión del pronóstico que aporta el sistema frente al método de estimación vigente en la empresa, mediante la comparación del error escalado en las mismas ventanas de validación y una prueba estadística para muestras relacionadas.

<!-- bloque: limites -->
### 1.5.6 Límites

Para delimitar con precisión el compromiso del proyecto, se declaran expresamente las exclusiones siguientes:

- No se desarrollan recomendadores de productos, segmentación individual de clientes ni optimización automática de precios.
- No se integra el sistema de forma directa con el punto de venta ni con la tienda en línea de la empresa; la integración queda preparada como extensión mediante la API, sujeta a que la empresa disponga de una interfaz para sus sistemas.
- El sistema no emite facturas ni documentos tributarios: su registro de ventas es interno y no sustituye la factura electrónica en línea de la Superintendencia de Administración Tributaria ni la contabilidad de la empresa.
- Las recomendaciones de reabastecimiento son un insumo para la decisión de compra; el sistema no genera ni envía pedidos a proveedores de forma automática.
- No se tratan datos personales de clientes. Los únicos datos personales que el sistema almacena son el nombre y el correo de los empleados con cuenta de acceso.
- No se construyen modelos de aprendizaje profundo, como LSTM o transformadores, en esta fase; quedan como experimento posterior si los datos demuestran que aportan una mejora estable (sección 2.2.3.2).
- No se desarrollan aplicaciones móviles nativas; el acceso al sistema es mediante navegador web.
- Durante esta fase, la validación técnica del motor de pronóstico se realiza con datos simulados. La evaluación sobre los registros reales de la empresa y la aplicación de los instrumentos dirigidos a personas quedan sujetas al acceso que la empresa autorice en la prueba piloto.

<!-- bloque: hipotesis -->
## 1.6 Hipótesis

El proyecto incorpora un componente investigativo verificable, por lo que la formulación de una hipótesis sí aplica. La pregunta de investigación de la sección 1.2 indaga si el sistema mejora la precisión de la información frente a los métodos de estimación vigentes, y la sección 2.2.5.1 fija un criterio cuantificable para juzgarlo: una reducción de al menos 10 % del error escalado respecto del método de referencia. Ambos elementos conforman una afirmación comprobable, que puede contrastarse con mediciones repetidas del error en varios periodos de prueba (sección 3.1).

**Variable independiente:** el método de pronóstico, con dos niveles: el modelo de aprendizaje automático que el sistema selecciona y publica, y el método de estimación de referencia.

**Variable dependiente:** la precisión del pronóstico de ventas, medida mediante el error escalado absoluto medio (MASE) en cada ventana de validación de origen móvil de 30 días (sección 2.3).

Mientras los instrumentos de la sección 3.3 no documenten el procedimiento con que la empresa estima hoy sus ventas, el método vigente se representa con el naïve estacional, que formaliza la regla de estimación más elemental —esperar para cada día lo vendido el mismo día de la semana anterior— y que la sección 2.2.5.1 adopta como referencia del criterio de publicación. Si la entrevista y la revisión documental identifican un procedimiento distinto, este se incorporará como referencia adicional y se evaluará con el mismo protocolo.

- **Hipótesis de trabajo** (H<sub>1</sub>): el modelo de aprendizaje automático publicado por el sistema reduce en más de 10 % el error escalado del pronóstico de ventas respecto del método de referencia, evaluados ambos en las mismas ventanas de validación de origen móvil; es decir, MASE<sub>modelo</sub> < 0.90 × MASE<sub>referencia</sub>.
- **Hipótesis nula** (H<sub>0</sub>): el modelo no reduce el error escalado en más de 10 % respecto del método de referencia; es decir, MASE<sub>modelo</sub> ≥ 0.90 × MASE<sub>referencia</sub>.

La hipótesis se contrasta con la prueba t de Student para muestras relacionadas, unilateral y con un nivel de significancia α = 0.05, sobre la diferencia entre el error del modelo y el 90 % del error de la referencia en cada ventana; se complementa con la prueba de rangos con signo de Wilcoxon y con el tamaño del efecto (sección 4.3). Se vincula directamente con el objetivo específico 3, que evalúa la mejora frente al método vigente, y con el objetivo específico 2, que incluye el protocolo de comparación y el criterio de aceptación. En esta fase se contrasta sobre datos simulados para validar el procedimiento; su comprobación con los registros de la empresa corresponde a la prueba piloto.

<!-- bloque: bases-teoricas -->
## 2.2 Bases Teóricas

Las bases teóricas que sustentan la solución se organizan de lo general a lo particular. Primero se aborda la gestión de ventas en el comercio minorista, que define el problema de negocio (sección 2.2.1); luego, los fundamentos del pronóstico de series de tiempo (sección 2.2.2) y los métodos de inteligencia artificial aplicados a él (sección 2.2.3); después, la preparación de datos (sección 2.2.4), la evaluación de pronósticos (sección 2.2.5) y la explicabilidad (sección 2.2.6); y, por último, la arquitectura de los sistemas predictivos (sección 2.2.7), que traslada esos fundamentos a un sistema de información. Cada apartado indica cómo se aplica la teoría en el proyecto.

<!-- bloque: definicion-terminos -->
## 2.3 Definición de Términos

Los términos siguientes se emplean a lo largo del documento con el significado que aquí se precisa. Se presentan en orden alfabético; para cada uno se da su definición conceptual y, cuando el término se mide o se concreta en el sistema, su definición operacional.

**ADI (intervalo promedio entre demandas).** Promedio de periodos que transcurren entre dos ocurrencias de demanda positiva; junto con el CV², permite clasificar el patrón de demanda de una serie (Syntetos, Boylan y Croston, 2005). Operacionalmente, es el número de días observados de un producto, contados desde su primera venta, dividido entre el número de días en que registró ventas: un ADI de 5 indica, en promedio, un día con venta de cada cinco.

**Árboles potenciados por gradiente.** Técnica de aprendizaje automático que construye árboles de decisión de forma secuencial, de modo que cada árbol corrige el error residual de los anteriores (Friedman, 2001). Operacionalmente, es el modelo candidato del sistema: el regresor de árboles potenciados de scikit-learn, con hiperparámetros fijos y registrados en cada ejecución, que pronostica el total diario de ventas a partir de variables de calendario, rezagos y medias móviles.

**Criterio de publicación.** Regla de aceptación que determina si un modelo candidato reemplaza al modelo vigente (sección 2.2.5.1). Operacionalmente, el sistema publica el modelo de aprendizaje automático solo si cumple tres condiciones en la validación de origen móvil: su MASE medio es al menos 10 % menor que el del naïve estacional, su sesgo relativo no excede el 20 % y obtiene un MASE menor que el de la referencia en más de la mitad de las ventanas.

**CV² (coeficiente de variación al cuadrado).** Medida de la variabilidad del tamaño de la demanda, igual al cuadrado del cociente entre la desviación estándar y la media (Syntetos, Boylan y Croston, 2005). Operacionalmente, se calcula solo sobre las cantidades vendidas en los días con venta, de modo que mide la dispersión del tamaño de cada venta y no la de la serie con sus días en cero.

**Datos simulados.** Registros generados artificialmente para reproducir propiedades conocidas de un fenómeno cuando los datos reales no están disponibles. Operacionalmente, son las transacciones de doce meses producidas por el simulador del sistema (sección 4.1.2), que no comparte funciones con las variables del modelo; sirven exclusivamente para validar el procedimiento técnico, y ninguna cifra obtenida con ellos describe la operación de la empresa.

**Demanda censurada.** Parte de la demanda que no se convierte en venta porque la falta de existencia impide atender al cliente, de modo que las ventas registradas subestiman la demanda potencial (sección 2.2.1). Operacionalmente, en el simulador son las unidades demandadas que no se vendieron por falta de existencia; en los registros reales no es observable de forma directa, por lo que el modelo de datos conserva la existencia y sus movimientos para identificar los periodos sin inventario.

**Demanda intermitente.** Patrón de demanda con periodos frecuentes sin venta, separados por ocurrencias positivas de tamaño variable (Croston, 1972; Syntetos, Boylan y Croston, 2005). Operacionalmente, la serie diaria de un producto se clasifica como intermitente cuando su ADI es mayor o igual que 1.32 y su CV² menor que 0.49; con ADI mayor o igual que 1.32 y CV² mayor o igual que 0.49 se clasifica como grumosa, y con ADI menor que 1.32, como regular o errática según el mismo corte del CV².

**Fuga de información.** Uso, al construir o evaluar un modelo, de información que no estaría disponible en el momento de emitir el pronóstico, lo que produce una estimación optimista de su desempeño (Bergmeir y Benítez, 2012). Operacionalmente, el sistema la evita desplazando un periodo todos los rezagos y medias móviles, de modo que ninguna característica del día t utiliza datos de t o posteriores, y reentrenando cada candidato solo con el pasado de cada ventana de validación.

**Horizonte de pronóstico.** Número de periodos futuros para los que se emite una predicción a partir de una fecha de corte (Hyndman y Athanasopoulos, 2021). Operacionalmente, la evaluación de modelos utiliza un horizonte de 30 días, el mismo que consume el centro de control; la consulta de pronósticos admite horizontes de 7, 30, 90 y 180 días.

**Línea base.** Método de pronóstico simple contra el cual se mide si un modelo más complejo agrega valor; también se denomina método de referencia (Hyndman y Athanasopoulos, 2021). Operacionalmente, el sistema evalúa seis líneas base: naïve, naïve estacional de periodo 7, media móvil, suavizamiento exponencial simple, Holt-Winters aditivo y ARIMA(1,1,1).

**MASE (error escalado absoluto medio).** Métrica que divide el error absoluto medio de un pronóstico entre el error absoluto medio de un método naïve dentro de la muestra de entrenamiento, lo que la hace comparable entre series de distinta escala (Hyndman y Koehler, 2006). Operacionalmente, es el error absoluto medio del pronóstico en cada ventana de 30 días dividido entre el del naïve estacional de periodo 7 calculado sobre el conjunto de entrenamiento de esa ventana; un valor menor que 1 indica un error inferior al de esa referencia. Es la métrica primaria del sistema y la variable dependiente de la hipótesis (sección 1.6).

**MVP (producto mínimo viable).** Versión de un producto con la funcionalidad mínima necesaria para que sus usuarios lo utilicen y lo evalúen. Operacionalmente, es la versión del sistema desplegada en esta fase, cuyas funciones se identifican con el estado «Implementado» en la Tabla 35.

**Naïve estacional.** Método que pronostica cada periodo con el valor observado en el mismo punto del ciclo anterior (Hyndman y Athanasopoulos, 2021). Operacionalmente, con un ciclo semanal, el pronóstico de cada día es la venta del mismo día de la semana anterior. Es la referencia del criterio de publicación y, mientras no se documente el método vigente de la empresa, la del contraste de la hipótesis.

**Punto de reorden.** Nivel de existencia en el que debe emitirse un pedido para que la mercadería llegue antes de agotarse. Operacionalmente, es la demanda diaria media de los últimos 60 días —incrementada en 40 % cuando un evento de temporada cae dentro del tiempo de importación— multiplicada por la suma del tiempo de importación del producto y diez días de seguridad.

**Recalibración.** Proceso mediante el cual el sistema reentrena, evalúa y, si corresponde, publica una nueva versión del modelo. Operacionalmente, comprende la evaluación de los siete candidatos en cinco ventanas de origen móvil, la aplicación del criterio de publicación y el registro de la ejecución con sus métricas y su decisión (Figura 14).

**Sesgo del pronóstico.** Error medio con signo, que indica si un método tiende a sobreestimar o a subestimar. Operacionalmente, es el promedio del pronóstico menos la venta real, en quetzales por día: un valor negativo indica subestimación. El sesgo relativo, que utiliza el criterio de publicación, es su valor absoluto dividido entre la venta diaria media del periodo evaluado.

**SHAP (explicaciones aditivas de Shapley).** Método que asigna a cada variable de entrada una contribución al valor de una predicción, de modo que la suma de las contribuciones explica la diferencia respecto del valor medio (Lundberg y Lee, 2017). Operacionalmente, es el mecanismo previsto para mostrar los factores principales de cada pronóstico (requerimiento RF-12); el MVP aún no lo implementa, de modo que el sistema muestra la versión del modelo y sus métricas, pero no factores explicativos.

**Validación de origen móvil.** Procedimiento de evaluación de series de tiempo en el que el origen del pronóstico avanza de forma sucesiva: en cada corte, el modelo se entrena con el pasado y se evalúa sobre el periodo siguiente (Tashman, 2000). Operacionalmente, el sistema utiliza cinco ventanas consecutivas de 30 días con un mínimo de 60 días de entrenamiento; en cada ventana, todos los candidatos se reentrenan con el historial anterior al corte y pronostican los 30 días siguientes.

**WAPE (error porcentual absoluto ponderado).** Suma de los errores absolutos dividida entre la suma de los valores reales, expresada en porcentaje; a diferencia del error porcentual medio, no se indefine en los días sin venta y pondera el error según el volumen. Operacionalmente, se calcula sobre cada ventana de 30 días y se reporta como indefinido, no como cero, cuando el periodo no tuvo ventas.

<!-- bloque: diseno-comparativo -->
Para contrastar la hipótesis de la sección 1.6, el diseño incorpora un componente comparativo: el modelo de aprendizaje automático y el método de referencia se evalúan sobre las mismas ventanas de validación de origen móvil, de modo que sus errores forman observaciones emparejadas que se comparan mediante una prueba estadística para muestras relacionadas (sección 4.3). Esta comparación no requiere intervenir en la operación de la empresa, porque se realiza sobre los registros históricos y con el mismo protocolo para ambos métodos.

<!-- bloque: validacion-instrumento -->
## 3.4 Validación del Instrumento

Antes de su aplicación definitiva, cada instrumento de la sección 3.3 se somete a un procedimiento de validación acorde con su tipo, con el fin de comprobar que mide lo que pretende medir (validez) y que lo hace de manera consistente en aplicaciones repetidas (confiabilidad). La Tabla 46 resume el procedimiento previsto para cada instrumento.

| Instrumento | Validez | Confiabilidad | Criterio de aceptación |
|---|---|---|---|
| Guía de entrevista semiestructurada (3.3.1) | Juicio de tres expertos sobre claridad, pertinencia y coherencia de cada pregunta | Prueba piloto con personas de perfil similar, no incluidas en la muestra | V de Aiken ≥ 0.80 en cada pregunta |
| Cuestionario de usabilidad con escala Likert (3.3.2) | Juicio de tres expertos | Prueba piloto y alfa de Cronbach | V de Aiken ≥ 0.80 en cada ítem; α ≥ 0.70 |
| Guía de observación directa (3.3.3) | Juicio de tres expertos | Registro simultáneo por dos observadores y contraste de sus anotaciones | V de Aiken ≥ 0.80 en cada aspecto observado |
| Lista de cotejo para la revisión documental (3.3.4) | Juicio de tres expertos | Verificación de la lista con la gerencia antes de aplicarla | V de Aiken ≥ 0.80 en cada elemento |
| Ficha de perfilamiento de datos (3.3.5) | Pruebas automatizadas contra valores calculados a mano | Repetibilidad del cálculo con los mismos datos | Todas las pruebas aprobadas |

Tabla 46. Procedimiento de validación previsto para cada instrumento de recolección de datos. Fuente: Elaboración propia a partir de Hernández Sampieri, Fernández Collado y Baptista Lucio (2014).

### 3.4.1 Juicio de expertos

La validez de contenido de la guía de entrevista, el cuestionario de usabilidad, la guía de observación y la lista de cotejo documental se verifica mediante el juicio de tres expertos con perfiles complementarios: un ingeniero en sistemas con experiencia en desarrollo de software o en analítica de datos, un profesional del área comercial o de inventarios del comercio minorista y un docente de metodología de la investigación. Cada experto recibe un formato de validación en el que califica cada ítem de 1 a 4 en claridad, pertinencia y coherencia con el objetivo o la variable que mide, y anota sus observaciones (Hernández Sampieri, Fernández Collado y Baptista Lucio, 2014).

El grado de acuerdo entre los expertos se cuantifica con el coeficiente V de Aiken (1985), que varía entre 0 y 1 y se calcula como V = S / [n (c − 1)], donde S es la suma, sobre los jueces, de la diferencia entre la calificación asignada y el valor mínimo de la escala; n, el número de jueces, y c, el número de valores de la escala. Con tres jueces y una escala de 1 a 4, un ítem calificado con 4, 4 y 3 obtiene V = (3 + 3 + 2) / (3 × 3) = 0.89. Se conservan los ítems con V ≥ 0.80 en los tres criterios; los demás se reformulan según las observaciones y se someten a una segunda ronda, o se eliminan si no alcanzan el umbral.

### 3.4.2 Prueba piloto y confiabilidad

Una vez incorporados los ajustes del juicio de expertos, la guía de entrevista y el cuestionario de usabilidad se aplican a un grupo piloto con características similares a las de la muestra, pero no incluido en ella: personal de ventas o de administración de otro comercio minorista. Como la muestra cualitativa es de cinco a ocho participantes (sección 3.2.2), el 10 % a 15 % que suele recomendarse equivaldría a menos de una persona; por ello, el grupo piloto se fija en un mínimo de tres personas. En la prueba se registran el tiempo de aplicación, las preguntas que generan dudas o respuestas ambiguas y las tareas del cuestionario que no se comprenden, y cada problema detectado da lugar a un ajuste documentado del instrumento.

La confiabilidad del cuestionario de usabilidad se estima con el alfa de Cronbach (1951) sobre sus ítems Likert y se considera aceptable a partir de 0.70. Con un grupo piloto tan reducido, el valor obtenido en el piloto se interpreta solo como un indicador preliminar; el coeficiente se recalcula con las respuestas de la aplicación definitiva y se reporta junto con su interpretación.

### 3.4.3 Validación de los instrumentos técnicos

La ficha de perfilamiento de datos y los registros de evaluación de modelos no dependen del juicio de un informante, sino de cálculos que realiza el sistema, por lo que su validación es técnica. Su validez se verifica con pruebas automatizadas que comparan cada estadístico y cada métrica con valores calculados a mano fuera del código que se prueba (casos CP-07 a CP-11 de la Tabla 44), y su confiabilidad, con la repetibilidad: el mismo conjunto de datos y la misma semilla producen siempre el mismo perfil y las mismas métricas.

### 3.4.4 Registro de resultados y ajustes

Los formatos de validación completados, la V de Aiken de cada ítem, el alfa de Cronbach y la lista de ajustes realizados a cada instrumento se documentarán y se incluirán como anexos del documento final, junto con la versión definitiva de cada instrumento. A la fecha de este informe, los instrumentos técnicos están validados y los instrumentos dirigidos a personas están diseñados; su validación es requisito previo para aplicarlos en la prueba piloto (Tabla 13).

<!-- bloque: metodologia-desarrollo -->
## 3.5 Metodología de Desarrollo del Proyecto

La metodología de desarrollo define cómo se construye el producto de software y es independiente de la metodología de investigación de la sección 3.1: aquella determina cómo se obtienen y analizan los datos; esta, cómo se organiza el trabajo técnico del equipo.

### 3.5.1 Selección del marco de trabajo

Se contrastaron dos enfoques. El modelo en cascada organiza el desarrollo en fases secuenciales —requerimientos, diseño, construcción, pruebas e implantación— y conviene cuando los requerimientos son estables y están definidos desde el inicio (Sommerville, 2016). Scrum organiza el trabajo en iteraciones de duración fija, llamadas sprints, que producen incrementos utilizables y permiten ajustar el backlog con la retroalimentación del cliente (Schwaber y Sutherland, 2020).

Las condiciones del proyecto favorecen el enfoque ágil. Los requerimientos no podían fijarse al inicio: el levantamiento preliminar debía validarse con la empresa (sección 6.2.2), y durante la construcción surgieron requerimientos que no figuraban en el backlog, como la administración de cuentas y el registro de ventas en el propio sistema (sección 6.2.3). El motor de pronóstico exige, además, experimentar y medir antes de comprometer un diseño, lo que se ajusta a ciclos cortos con un resultado verificable. Por estas razones se adoptó Scrum, adaptado a un equipo de tres integrantes con dedicación parcial.

### 3.5.2 Roles del equipo

- **Product Owner:** la gerencia de Zorros Revolution Biker, que representa al negocio, valida el backlog y acepta los incrementos. Mientras no se dispone de acceso a la empresa, un integrante del equipo actúa como Product Owner delegado: prioriza el backlog a partir del planteamiento del problema y de los objetivos, y deja las decisiones de negocio sujetas a la validación de la gerencia en la prueba piloto.
- **Scrum Master:** Elder Estuardo Garcia Pacheco, quien facilita los eventos del sprint, da seguimiento a los impedimentos y vela por que cada cambio cumpla la definición de terminado.
- **Equipo de desarrollo:** Gabriel Enrique Pérez Meza y Luis Pedro Ordoñez Chutan, junto con el Scrum Master. El equipo es multifuncional y comparte el análisis, la construcción del sistema y del motor de pronóstico, las pruebas y la documentación.

### 3.5.3 Eventos, artefactos y definición de terminado

Cada sprint dura dos semanas, de modo que el semestre de dieciséis semanas comprende ocho sprints. Cada uno inicia con una planificación en la que el equipo selecciona los elementos del backlog y fija la meta del sprint, y cierra con una revisión del incremento y una retrospectiva. Por la dedicación parcial del equipo, la reunión diaria se sustituye por una sincronización breve por mensajería y por reuniones virtuales cuando un impedimento lo requiere.

El backlog del producto parte de las historias de usuario del levantamiento preliminar (sección 6.2.2) y se gestiona como incidencias del repositorio. Un elemento se considera terminado cuando su código está en una rama propia, cuenta con pruebas automatizadas que se aprueban, fue revisado e integrado mediante un pull request y puede desplegarse con un comando reproducible; en el caso de los entregables documentales, cuando quedan integrados en el documento del proyecto.

### 3.5.4 Sprints y vinculación con los objetivos

La Tabla 47 presenta los sprints, su entregable principal y el objetivo específico que atiende cada uno. Los sprints 3 a 6 agrupan las iteraciones de construcción descritas en la sección 6.4.2 (Tabla 43); los sprints 7 y 8 corresponden a la prueba piloto con la empresa.

| Sprint (semanas) | Entregable principal | Objetivo específico | Estado |
|---|---|---|---|
| 1 (1 y 2) | Antecedentes, planteamiento del problema, objetivos y diseño de los instrumentos de recolección | 1 | Completado |
| 2 (3 y 4) | Backlog inicial con historias de usuario, requerimientos preliminares, arquitectura, modelo de datos y prototipos de baja fidelidad | 2 | Completado |
| 3 (5 y 6) | Auditoría de alineación, corrección de defectos críticos y despliegue en contenedores con PostgreSQL (iteraciones 1 a 4) | 2 | Completado |
| 4 (7 y 8) | Perfilamiento de series, líneas base, validación de origen móvil, métricas y criterio de publicación (iteraciones 5 y 6) | 2 | Completado |
| 5 (9 y 10) | Administración de usuarios y roles, y rediseño de la interfaz (iteraciones 7 y 8) | 2 | Completado |
| 6 (11 y 12) | Simulador de ventas, validación técnica, comprobación de la hipótesis sobre datos simulados y manual de usuario (iteraciones 9 y 10) | 2 y 3 | Completado |
| 7 (13 y 14) | Importador de históricos con validación y trazabilidad de cargas; validación de los instrumentos y diagnóstico del proceso actual en la empresa | 1 y 2 | Planificado |
| 8 (15 y 16) | Prueba piloto con los registros reales: evaluación frente al método vigente, cuestionario de usabilidad y ajustes | 3 | Planificado |

Tabla 47. Sprints del proyecto, entregable principal y objetivo específico que atiende cada uno. Fuente: Elaboración propia.

### 3.5.5 Herramientas de gestión y seguimiento

La gestión y el seguimiento del proyecto se apoyan en GitHub: el backlog se registra como incidencias del repositorio, cada cambio se desarrolla en una rama propia y se integra mediante un pull request revisado, y el historial de cambios sirve de evidencia verificable de cada incremento. La comunicación del equipo se realiza por WhatsApp para la sincronización diaria y por Google Meet o Microsoft Teams para la planificación, la revisión y la retrospectiva de cada sprint. Las herramientas de construcción del sistema —Python, FastAPI, pytest y Docker Compose, entre otras— se describen en la sección 6.4.1 (Tabla 42).

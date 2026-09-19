# Capítulo V – Estudio de Factibilidad

El estudio de factibilidad examina si el sistema propuesto puede desarrollarse, implantarse y sostenerse en las condiciones reales de Zorros Revolution Biker. Se analizan siete dimensiones —modelo de negocio, transformación digital, legal, ambiental, operativa, técnica y económica— con la evidencia disponible en esta fase: la información pública de la empresa, el estado del prototipo desplegado y las mediciones obtenidas en su infraestructura. Donde una dimensión depende de datos que solo la empresa posee, se declara el supuesto utilizado en lugar de presentarlo como un hecho.

## 5.1 Modelo de negocio

Para situar el sistema en la lógica de valor de la empresa se utiliza el Business Model Canvas de Osterwalder y Pigneur (2010), completado a partir de la información pública descrita en la sección 1.1.1 y del problema planteado en la sección 1.3. La Tabla 26 presenta los nueve bloques y señala en cuáles interviene la solución.

| Bloque | Descripción para Zorros Revolution Biker | Intervención del sistema |
|---|---|---|
| Segmentos de clientes | Motociclistas de Guatemala que adquieren equipo de protección, indumentaria, consumibles y accesorios; atendidos en sucursales físicas y en línea | Indirecta: mayor disponibilidad de producto en temporada |
| Propuesta de valor | Catálogo especializado de accesorios para motocicleta, con presencia en varias ubicaciones del país y canal en línea | Directa: reduce faltantes en los periodos de mayor demanda (diciembre, Bono 14, Caravana del Zorro) |
| Canales | Sucursales en Antigua Guatemala, Bosques de San Nicolás, C. C. Metronorte, Cobán, Kiosko Metronorte y San Juan zona 4; tienda en línea | Ninguna en esta fase; el pronóstico por sucursal es una extensión prevista |
| Relación con clientes | Atención en mostrador y en línea | Ninguna directa |
| Fuentes de ingreso | Venta de productos al detalle | Indirecta: ventas que hoy se pierden por quiebre de existencia |
| Recursos clave | Inventario importado, sucursales, personal de ventas, catálogo | Directa: el inventario pasa a gestionarse con información prospectiva |
| Actividades clave | Compra e importación desde China (lead time de aproximadamente 60 días), almacenamiento, venta, reabastecimiento | Directa: la decisión de cuánto y cuándo pedir se apoya en el pronóstico y el punto de reorden |
| Socios clave | Proveedores en China, operadores logísticos de importación, plataforma de venta en línea | Ninguna directa |
| Estructura de costos | Compra de mercadería, transporte e importación, arrendamiento de locales, personal, capital inmovilizado en inventario | Directa: menor capital inmovilizado por sobrepedido y menores ventas perdidas por faltante |

Tabla 26. Business Model Canvas de Zorros Revolution Biker con los bloques en que interviene la solución. Fuente: Elaboración propia a partir de Osterwalder y Pigneur (2010) y de la información pública de la empresa.

El sistema no modifica el negocio: incide sobre la actividad clave de reabastecimiento y, a través de ella, sobre dos rubros de la estructura de costos que el planteamiento del problema identifica como la consecuencia de decidir por experiencia. Un pedido excesivo inmoviliza capital durante un ciclo de importación de dos meses; un pedido escaso produce faltantes justamente cuando la demanda es mayor. El valor de la solución reside en acercar ambas decisiones a la demanda esperada, no en sustituir el criterio comercial de la gerencia, como se establece en la sección 1.3.

## 5.2 Transformación digital

**Estado de partida.** Según el planteamiento de la sección 1.3, la planificación de compras de la empresa se apoya en la experiencia del personal y en la revisión manual de registros. No se dispone, en esta fase, de una descripción verificada del sistema transaccional que la empresa utiliza; la sección 1.1.1 deja explícito que ese antecedente debe completarse mediante entrevista. Por tanto, el estado de partida se caracteriza con lo que sí se conoce: las decisiones de reabastecimiento no cuentan con un pronóstico sistemático ni con una medición del error de las estimaciones.

**Estado deseado.** Una operación en la que las ventas se registran de forma estructurada, cada producto tiene un perfil de demanda conocido, el pronóstico se genera y evalúa con un protocolo reproducible, y las alertas de reabastecimiento consideran el tiempo de importación desde China. La sección 2.8.1 lo formula como conectar la predicción con la gestión de ventas sin perder trazabilidad.

**Capacidades que habilita el MVP.** El prototipo desplegado aporta cuatro capacidades que no existían: registro transaccional con descuento automático de inventario; perfilamiento de cada serie de demanda; comparación de modelos de pronóstico con criterio de publicación; y alertas de reabastecimiento que anticipan los eventos de temporada dentro de la ventana de envío. Todas son accesibles desde cualquier navegador con control de acceso por roles.

**Impacto en procesos, personas y cultura.** El cambio más profundo no es tecnológico sino de criterio: la decisión de compra pasa de basarse en la memoria de temporadas anteriores a apoyarse en una estimación con error conocido. Ello exige dos cosas del personal: disciplina en el registro de cada venta y cada recepción de mercadería, porque la calidad del pronóstico depende de ella, y disposición a contrastar la recomendación del sistema con su propio juicio, en lugar de aceptarla o descartarla en bloque. La sección 5.5 aborda cómo gestionar esa transición. Es importante no sobredimensionar el alcance: el sistema no transforma la relación con el cliente ni los canales de venta; transforma una decisión interna de abastecimiento.

## 5.3 Factibilidad legal

### 5.3.1 Normativa aplicable

Guatemala no cuenta con una ley general de protección de datos personales. Ello no significa ausencia de obligaciones: la Tabla 27 identifica las normas que inciden en el proyecto y la forma en que se atienden.

| Norma | Contenido relevante | Atención en el proyecto |
|---|---|---|
| Constitución Política de la República de Guatemala, artículos 24 y 31 (Asamblea Nacional Constituyente, 1985) | Inviolabilidad de la correspondencia, documentos y libros; derecho de acceso a los archivos y registros que contengan datos de la persona | Los datos de las cuentas de usuario se tratan como información confidencial de la empresa; cada usuario puede consultar sus propios datos |
| Código Penal, Decreto 17-73, artículos 274 "A" a 274 "G", adicionados por el Decreto 33-96 (Congreso de la República de Guatemala, 1996) | Tipifica la destrucción y alteración de registros informáticos, la reproducción no autorizada de programas, los registros prohibidos, la manipulación de información y los programas destructivos | Control de acceso por roles, contraseñas cifradas, registro de quién realiza cada operación y respaldos de la base de datos |
| Ley de Derecho de Autor y Derechos Conexos, Decreto 33-98 (Congreso de la República de Guatemala, 1998) | Protege los programas de ordenador como obras literarias; regula la titularidad del software desarrollado | El código es obra del equipo; se propone acordar por escrito con la empresa las condiciones de uso y titularidad antes de la implantación |
| Ley de Acceso a la Información Pública, Decreto 57-2008 (Congreso de la República de Guatemala, 2008) | Define los datos personales y los datos sensibles y establece el principio de que solo pueden tratarse con consentimiento; aplica a sujetos obligados del sector público, pero constituye la referencia normativa nacional de esas categorías | Se adoptan sus definiciones: el sistema no recolecta datos sensibles y minimiza los personales al nombre y correo de los empleados usuarios |
| Código de Comercio, Decreto 2-70 (Congreso de la República de Guatemala, 1970) | Obligación del comerciante de llevar contabilidad y conservar sus registros | El sistema es una herramienta de gestión y no sustituye los libros contables ni la facturación |
| Régimen de Factura Electrónica en Línea, Acuerdo de Directorio 13-2018 (Superintendencia de Administración Tributaria, 2018) | Obliga a emitir facturas electrónicas a través de la plataforma FEL | El sistema no emite facturas ni documentos tributarios; su registro de ventas es interno y no reemplaza la FEL |

Tabla 27. Normativa guatemalteca aplicable y su atención en el proyecto. Fuente: Elaboración propia.

Como referencia de buenas prácticas, el proyecto adopta los principios de minimización, limitación de finalidad y seguridad del Reglamento General de Protección de Datos de la Unión Europea (Parlamento Europeo y Consejo de la Unión Europea, 2016) y los controles de acceso y de gestión de contraseñas de la norma ISO/IEC 27001 (International Organization for Standardization, 2022a), en los términos que la propia guía metodológica recomienda para contextos en que la legislación local aún se desarrolla.

### 5.3.2 Datos personales tratados

El requerimiento no funcional RNF-04 establece excluir los datos personales innecesarios. La Tabla 28 inventaría los que el sistema efectivamente almacena.

| Dato | Titular | Finalidad | Medida de protección |
|---|---|---|---|
| Nombre y correo electrónico | Empleados con cuenta de usuario | Identificación y control de acceso | Acceso restringido al rol de administrador; cifrado en tránsito (HTTPS) |
| Contraseña | Empleados con cuenta de usuario | Autenticación | Nunca se almacena en claro: hash bcrypt con factor de costo 12; política de longitud y composición; cambio exigiendo la contraseña actual |
| Identificador del cajero en cada venta | Empleados | Trazabilidad de la operación | Visible solo para usuarios autenticados |
| Datos de clientes finales | — | No se recolectan | No aplica |

Tabla 28. Inventario de datos personales tratados por el sistema y medidas de protección. Fuente: Elaboración propia.

El sistema no registra datos de clientes: el pronóstico se construye sobre transacciones agregadas, en línea con la sección 1.6.3. Las cuentas de demostración creadas durante el desarrollo generan contraseñas aleatorias que solo se muestran una vez y no se almacenan en el código fuente ni en la configuración.

### 5.3.3 Licenciamiento del software

Todos los componentes son de código abierto. La Tabla 29 detalla la licencia de cada uno y su implicación (Open Source Initiative, s. f.).

| Componente | Función | Licencia | Implicación |
|---|---|---|---|
| Python | Lenguaje del backend | PSF License | Permisiva |
| FastAPI, Pydantic, Gunicorn, SQLAlchemy, python-jose | API, validación, servidor, acceso a datos, tokens | MIT | Permisiva; solo exige conservar el aviso de copyright |
| Uvicorn, scikit-learn, statsmodels, pandas, NumPy, passlib | Servidor ASGI, aprendizaje automático, series temporales, datos, hash de contraseñas | BSD de 3 cláusulas | Permisiva |
| psycopg (driver de PostgreSQL) | Conexión a la base de datos | LGPL 3.0 (Free Software Foundation, 2007) | Copyleft débil: permite su uso como biblioteca sin afectar la licencia del sistema, siempre que no se modifique el driver |
| PostgreSQL | Base de datos | PostgreSQL License | Permisiva |
| Docker Engine | Contenedores | Apache 2.0 (Apache Software Foundation, 2004) | Permisiva; exige conservar avisos |
| Nginx | Proxy inverso | BSD de 2 cláusulas | Permisiva |
| Chart.js | Gráficas en el navegador | MIT | Permisiva |
| Let's Encrypt | Certificados TLS | Servicio gratuito | Sin costo de licencia |

Tabla 29. Licencias de los componentes del sistema. Fuente: Elaboración propia a partir de Open Source Initiative (s. f.).

Ningún componente tiene licencia comercial ni de copyleft fuerte que obligue a publicar el código del sistema. El único componente bajo LGPL se utiliza sin modificaciones, con lo que se cumplen sus condiciones. El costo de licenciamiento es cero.

### 5.3.4 Confidencialidad

La sección 3.4 prevé que la recolección de datos se realice con autorización de la empresa y en un entorno restringido. Se propone formalizar, antes de la carga de registros reales, un acuerdo de confidencialidad que cubra la información comercial de Zorros Revolution Biker, el acceso al servidor y las condiciones de uso del software, en concordancia con el Decreto 33-98.

## 5.4 Factibilidad ambiental

El impacto ambiental directo del sistema es bajo. No requiere hardware dedicado: se ejecuta en un servidor privado virtual compartido de un solo núcleo, con un consumo medido de alrededor de 400 MB de memoria entre la aplicación y la base de datos, y los usuarios lo utilizan desde equipos con los que la empresa ya cuenta. No genera residuos electrónicos propios ni impresiones: toda la operación es en pantalla.

El impacto indirecto es potencialmente positivo aunque no se cuantifica en esta fase. Un pronóstico que reduzca el sobrepedido disminuye el inventario que termina obsoleto, y un reabastecimiento mejor planificado reduce la necesidad de envíos de emergencia desde el proveedor, que suelen realizarse por vía aérea con una huella de carbono muy superior a la del transporte marítimo habitual. Ambos efectos se alinean con el Objetivo de Desarrollo Sostenible 12, producción y consumo responsables (Organización de las Naciones Unidas, 2015). Como medida de mitigación del consumo energético se optó por un servidor compartido con recursos ajustados, en lugar de infraestructura dedicada, y por un modelo cuyo reentrenamiento completo tarda segundos, no horas.

## 5.5 Factibilidad operativa

**Disposición de los usuarios.** No fue posible medirla en esta fase con el cuestionario de la sección 3.3.2, que se aplicará durante la prueba piloto. Se anticipa una aceptación favorable con base en el Modelo de Aceptación de Tecnología de Davis (1989): la utilidad percibida es alta porque el sistema aborda una decisión que hoy consume tiempo y genera pérdidas, y la facilidad de uso percibida se cuidó en el diseño con flujos de pocos pasos y validación en la propia pantalla. La principal fuente de resistencia previsible es la disciplina de registro que el sistema exige.

**Competencias y capacitación.** El personal de ventas requiere las competencias de un punto de venta convencional: registrar una transacción y una recepción de mercadería. La gerencia requiere, además, interpretar el pronóstico y sus métricas. Se cuenta con un manual de usuario (versión 0.2) alineado con el sistema desplegado y se prevé una capacitación de dos sesiones: una para el personal de caja y otra para los administradores, centrada en la lectura del pronóstico y de las alertas de reabastecimiento.

**Cambios en los procesos.** Dos procesos cambian: el registro de ventas, que debe hacerse en el momento y con todos los productos del ticket, y la decisión de compra, que incorpora la recomendación del sistema como un insumo a contrastar. La sección 9 del manual de usuario propone un flujo diario, semanal y mensual.

**Soporte y sostenibilidad.** Durante el proyecto, el equipo de desarrollo atiende el soporte. Para la operación posterior se requiere designar en la empresa a un responsable de primer nivel y acordar quién administra el servidor. La solución está contenerizada y documentada para que su despliegue sea reproducible por un tercero, lo que reduce la dependencia del equipo original. Con esas condiciones, el proyecto se considera operativamente factible; sin un responsable designado, la sostenibilidad quedaría comprometida.

## 5.6 Factibilidad técnica

### 5.6.1 Infraestructura

El sistema está desplegado y en operación en un servidor privado virtual con las características de la Tabla 30, lo que constituye evidencia directa de factibilidad: no se trata de una estimación sino de una medición.

| Recurso | Disponible | Utilizado por el sistema | Observación |
|---|---|---|---|
| Procesador | 1 núcleo | Compartido con otros servicios del servidor | El entrenamiento completo tarda entre 3 y 5 segundos |
| Memoria | 3.8 GB (≈ 1.9 GB libres) | API: 331–355 MB; base de datos: 27–47 MB | Se fijaron dos procesos de trabajo para no exceder la memoria |
| Almacenamiento | 48 GB | Del orden de 2 GB (imágenes de contenedores, base de datos, modelos) | Los modelos entrenados se conservan versionados |
| Red | Dominio con certificado TLS | HTTPS con renovación automática | Nginx del servidor como proxy inverso |
| Cliente | Navegador actual con conexión a internet | Sin instalación | Interfaz adaptable a pantalla de teléfono |

Tabla 30. Infraestructura del despliegue y mediciones obtenidas. Fuente: Elaboración propia a partir de las mediciones en el servidor.

### 5.6.2 Herramientas y madurez tecnológica

La plataforma se construyó con tecnologías maduras, con soporte activo y documentación abundante: FastAPI sobre Python para la API; PostgreSQL como base de datos, tal como especifica la Tabla 10 del diseño preliminar; scikit-learn y statsmodels para el motor de pronóstico; Docker Compose para el despliegue reproducible, en cumplimiento del RNF-12; y HTML, CSS y JavaScript sin dependencias de framework para la interfaz. La elección de PostgreSQL sobre MySQL, contemplado inicialmente por restricciones de hospedaje, fue posible al disponer de un servidor propio y se realizó sin cambios en el código de aplicación gracias a la capa de abstracción de SQLAlchemy.

### 5.6.3 Competencias del equipo

El equipo domina Python, SQL y desarrollo web, y adquirió durante la fase las competencias específicas del motor de pronóstico: métricas de evaluación de series temporales, validación de origen móvil y métodos de referencia. La existencia de 128 pruebas automatizadas que verifican las fórmulas contra valores calculados a mano es evidencia de ese dominio y, a la vez, una salvaguarda frente a errores de implementación como el que se detectó y corrigió en el cálculo del MASE durante la fase.

### 5.6.4 Riesgos técnicos identificados

Tres riesgos permanecen abiertos y se documentan con su mitigación prevista: el entrenamiento se ejecuta dentro de la petición web, lo que con un histórico mayor podría exceder los tiempos de espera (mitigación: tarea asíncrona); el esquema de la base de datos no cuenta con migraciones versionadas (mitigación: incorporar Alembic); y el servidor es compartido con otros proyectos, lo que exige disciplina en los cambios de configuración. Ninguno impide la operación actual. El proyecto es técnicamente factible y, de hecho, está en operación.

## 5.7 Factibilidad económica

### 5.7.1 Costos

La Tabla 31 desglosa los costos del proyecto en su primer año y en los dos siguientes. Se distingue el desembolso efectivo del costo sombra del desarrollo, que corresponde al trabajo del equipo valorado a una tarifa de mercado aunque no represente un pago.

| Concepto | Supuesto | Año 1 (Q) | Años 2 y 3 (Q por año) |
|---|---|---|---|
| Desarrollo (costo sombra) | 4 integrantes × 10 h/semana × 16 semanas = 640 h, a Q 60/h | 38,400 | 0 |
| Servidor privado virtual | Q 80 mensuales | 960 | 960 |
| Dominio y certificado TLS | DuckDNS y Let's Encrypt, sin costo | 0 | 0 |
| Licencias de software | Componentes de código abierto (Tabla 29) | 0 | 0 |
| Capacitación | 8 horas del equipo a Q 60/h | 480 | 0 |
| Mantenimiento y soporte | 4 h mensuales a Q 60/h | 2,880 | 2,880 |
| **Total con costo sombra** | | **42,720** | **3,840** |
| **Desembolso efectivo** | | **4,320** | **3,840** |

Tabla 31. Costos del proyecto. Fuente: Elaboración propia; las tarifas y horas son supuestos declarados.

### 5.7.2 Beneficios y supuestos

El beneficio principal identificado en el planteamiento del problema son las ventas que se pierden por falta de existencia en temporada alta y el capital que se inmoviliza por sobrepedido. Ninguno de los dos puede cuantificarse con datos de la empresa en esta fase. Se construye, en consecuencia, un modelo paramétrico con supuestos explícitos (Tabla 32) que la empresa podrá sustituir por sus cifras reales, tal como recomienda la guía metodológica y el PMBOK Guide para la documentación de estimaciones (Project Management Institute, 2021).

| Parámetro | Valor supuesto | Origen |
|---|---|---|
| Proporción de la demanda no atendida por quiebre de existencia | 14.5 % | Única cifra tomada de la validación técnica sobre datos simulados (Tabla 14); debe verificarse con registros reales |
| Fracción de esa demanda que el sistema permitiría recuperar | 15 % (pesimista), 30 % (base), 50 % (optimista) | Supuesto conservador: el pronóstico reduce, no elimina, los faltantes |
| Margen bruto sobre ventas | 35 % | Supuesto para comercio minorista de accesorios; sustituir por el dato de la empresa |
| Ventas anuales de la empresa | Q 600,000; Q 1,200,000; Q 2,400,000 | Tres niveles ilustrativos; el nivel real es desconocido |

Tabla 32. Supuestos del análisis económico. Fuente: Elaboración propia.

Con estos parámetros, el beneficio anual se calcula como: ventas anuales × 14.5 % × fracción recuperada × 35 %. No se cuantifica el beneficio por menor capital inmovilizado, con lo que la estimación es conservadora.

### 5.7.3 Retorno de la inversión y relación beneficio-costo

La Tabla 33 presenta el beneficio anual, el retorno de la inversión (ROI) y la relación beneficio-costo (B/C) para cada combinación de supuestos, en dos horizontes: el primer año considerando solo el desembolso efectivo, y tres años considerando el costo total incluido el costo sombra del desarrollo. Las fórmulas son las estándar de evaluación de proyectos de tecnología (Schwalbe, 2019): ROI = (beneficios − costos) / costos × 100, y B/C = beneficios / costos.

| Ventas anuales (Q) | Fracción recuperada | Beneficio anual (Q) | ROI año 1, desembolso Q 4,320 | ROI a 3 años, costo total Q 50,400 | B/C a 3 años |
|---|---|---|---|---|---|
| 600,000 | 15 % | 4,568 | 6 % | −73 % | 0.27 |
| 600,000 | 30 % | 9,135 | 111 % | −46 % | 0.54 |
| 600,000 | 50 % | 15,225 | 252 % | −9 % | 0.91 |
| 1,200,000 | 15 % | 9,135 | 111 % | −46 % | 0.54 |
| 1,200,000 | 30 % | 18,270 | 323 % | 9 % | 1.09 |
| 1,200,000 | 50 % | 30,450 | 605 % | 81 % | 1.81 |
| 2,400,000 | 15 % | 18,270 | 323 % | 9 % | 1.09 |
| 2,400,000 | 30 % | 36,540 | 746 % | 117 % | 2.17 |
| 2,400,000 | 50 % | 60,900 | 1,310 % | 263 % | 3.63 |

Tabla 33. Escenarios de retorno de la inversión según los supuestos de la Tabla 32. Fuente: Elaboración propia.

### 5.7.4 Interpretación y punto de equilibrio

La lectura de la Tabla 33 distingue dos situaciones. Considerando únicamente el desembolso efectivo —servidor, capacitación y mantenimiento—, el proyecto se recupera dentro del primer año en todos los escenarios salvo el más pesimista, y en el escenario base con ventas de Q 1,200,000 el periodo de recuperación es de aproximadamente tres meses (Q 4,320 / Q 18,270 × 12). Esta es la situación que enfrenta la empresa si adopta el sistema desarrollado en el marco del trabajo de graduación.

Considerando el costo total, es decir, valorando el desarrollo como si se hubiera contratado, el resultado depende de la escala del negocio. Con el escenario base de recuperación (30 %), el proyecto alcanza el punto de equilibrio a tres años cuando las ventas anuales superan aproximadamente Q 1,105,000, que es el nivel en que 3 × 0.0152 × ventas iguala Q 50,400. Por debajo de esa escala, el desarrollo a tarifa de mercado no se justificaría solo por las ventas recuperadas; por encima, la relación beneficio-costo crece con la escala y alcanza 2.17 con ventas de Q 2,400,000.

Tres precisiones son necesarias para no sobreinterpretar el análisis. Primero, el único parámetro con respaldo cuantitativo, la proporción de demanda no atendida, proviene de la simulación y debe medirse en la operación real antes de tomar cualquier decisión de inversión. Segundo, el beneficio por menor capital inmovilizado no se incluyó, por lo que los resultados son conservadores. Tercero, la conclusión que sí es robusta a los supuestos es que el costo recurrente del sistema —menos de Q 4,000 anuales— es una fracción pequeña de cualquier escenario de beneficio razonable, de modo que la decisión económica relevante para la empresa no es si operar el sistema, sino si el volumen de faltantes justifica el esfuerzo de registro que exige. Con esa salvedad, el proyecto se considera económicamente factible.

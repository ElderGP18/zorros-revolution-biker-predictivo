# Guión de presentación — Fase 2: Validación y MVP

**Para:** los cuatro presentadores del equipo
**Duración objetivo:** 12 minutos de exposición + demo, dejando margen para preguntas
**Sistema en vivo:** https://prediccionzrb.duckdns.org
**Presentación de apoyo:** https://claude.ai/artifact/NDQfAWUVHQwtmxT9yruRkA (12 diapositivas; la sección 3 indica cuál va con cada parte). Quien la abra necesita que el dueño la comparta desde el menú Share.

---

## 1. Antes de entrar — checklist de 30 minutos

Hacerlo **una persona**, media hora antes, desde la misma laptop que se va a proyectar:

- [ ] Abrir https://prediccionzrb.duckdns.org y **entrar como admin**. Si la contraseña no funciona, restablecerla desde el servidor: `ssh zorros`, `cd /var/www/zorros-prediccion`, `docker compose exec api python -m app.manage_users password admin@zorrosrevolution.com --generar`.
- [ ] Dejar la sesión abierta en una pestaña. Abrir una **segunda pestaña** con el dashboard ya cargado.
- [ ] Ir a **Predicciones** y confirmar que la gráfica y las tarjetas cargan (modelo entrenado).
- [ ] Tener a mano el nombre de **un producto con stock** para la venta en vivo (ver Productos → cualquiera con existencia > 5).
- [ ] Tener capturas de pantalla de las 5 pantallas guardadas en la laptop **por si se cae la red** (Plan B, sección 7).
- [ ] Abrir el deck en otra pestaña y probar que avanza.
- [ ] Silenciar notificaciones del sistema operativo.

**Dato a tener presente:** la simulación de ventas termina el 18 de septiembre. Si la demo es el 19 o después, "Ventas de hoy" mostrará Q 0.00 hasta que se registre la venta en vivo. **Eso es una oportunidad, no un problema**: el jurado ve el dashboard actualizarse en tiempo real.

---

## 2. Reparto

| Presentador | Bloque | Minutos | Diapositivas |
|---|---|---|---|
| **P1** | Problema y lo que la teoría exige | 2.5 | 1–4 |
| **P2** | Diseño de la solución e infraestructura | 2.5 | 5–7 |
| **P3** | Demostración en vivo del MVP | 4.5 | 8 (pantalla del sistema) |
| **P4** | Resultados, limitaciones y siguiente fase | 2.5 | 9–12 |

Regla para los cuatro: **cada afirmación técnica se apoya en algo que el jurado puede verificar** — una URL, un número de pruebas, un PR, una tabla. Nada de "el sistema es muy preciso"; sí "mejora 22 % sobre el naïve estacional en 5 ventanas de validación".

---

## 3. Guión por presentador

### P1 — Problema y lo que la teoría exige (2.5 min, diapositivas 1–4)

**Diapositiva 1 — Portada.** Nombre del proyecto, integrantes, "Fase 2: Validación y MVP".

**Diapositiva 2 — El problema.**
> "Zorros Revolution Biker vende accesorios para motociclistas que se importan de China con 60 días de envío. Decidir *cuánto pedir y cuándo* se hace hoy por experiencia. Un error hacia arriba inmoviliza capital; hacia abajo, se pierden ventas en temporada alta — diciembre, Bono 14, la Caravana del Zorro."

**Diapositiva 3 — Qué dice la tesis que el sistema debe hacer.** Esta es la diapositiva que enlaza teoría y solución; hay que decirla con calma:
> "El marco teórico no pide 'un modelo de IA'. Pide cuatro cosas concretas, y las cuatro se van a ver funcionando hoy:
> 1. **Compararlo contra líneas base** — la tesis dice literalmente que la IA *solo agrega valor si supera de forma consistente* a métodos simples (cap. 2.2.2).
> 2. **Validarlo con origen móvil**, no con un solo corte (cap. 2.5).
> 3. **Medir con MASE y WAPE**, y con sesgo (cap. 2.5).
> 4. **Publicar solo si supera la referencia en al menos 10 %**; si no, se queda la línea base (cap. 2.5.1).
> Y antes de todo eso, **perfilar las series**: proporción de ceros, intervalo entre demandas, variabilidad (cap. 2.2.3)."

**Diapositiva 4 — Alcance de esta fase.** MVP funcional, infraestructura, manual, evaluación honesta. Entrega el turno:
> "P2 les cuenta cómo está construido."

---

### P2 — Diseño de la solución e infraestructura (2.5 min, diapositivas 5–7)

**Diapositiva 5 — Arquitectura real.** Diagrama: navegador → Nginx → FastAPI (Gunicorn) → PostgreSQL, en contenedores Docker sobre un VPS. Motor de ML con scikit-learn y statsmodels.
> "Esto no es un mockup: es la arquitectura desplegada. Base de datos PostgreSQL —la que especifica la tesis—, API en FastAPI, contenedores Docker que cumplen el requisito no funcional de despliegue reproducible. Corre en un VPS con un solo núcleo y consume unos 350 MB, así que es viable económicamente para una pyme."

**Diapositiva 6 — Cómo se trabaja.** Flujo rama → PR → revisión → despliegue. Cifras: 9 PRs mezclados en la fase, **128 pruebas automatizadas** que corren antes de cada cambio.
> "Cada cambio entra por un pull request y pasa 128 pruebas. Las fórmulas de las métricas están verificadas contra valores calculados a mano, no contra el propio código — porque una fórmula comparada consigo misma pasa la prueba aunque esté mal."

**Diapositiva 7 — Módulos del MVP.** Los seis: Login con roles, Centro de control, Ventas, Productos e inventario, Pronóstico con IA, Usuarios y roles.
> "P3 lo va a mostrar en vivo."

---

### P3 — Demostración en vivo (4.5 min, pantalla del sistema)

Cambiar a la pestaña del sistema. Hablar mientras se hace clic; no leer.

**Paso 1 — Login (20 s).** Ya debe estar abierta la sesión. Señalar el nombre y el rol en la barra lateral.
> "Autenticación con JWT, contraseñas cifradas con bcrypt, dos roles: cajero y administrador. Estoy como administrador."

**Paso 2 — Centro de control (40 s).** Recorrer las tarjetas.
> "Ventas del día y del mes, ticket promedio, productos con stock crítico. Y aquí —señalar— la proyección del próximo mes que calcula el modelo, con la gráfica de ventas reales contra proyectadas."
Si "Ventas de hoy" está en cero: *"Está en cero porque aún no hemos vendido hoy. Vamos a corregir eso."*

**Paso 3 — Registrar una venta (60 s).** Ventas → **Nueva venta** → **Agregar producto** → elegir el producto preparado, cantidad 2 → **Registrar venta**. Volver al Centro de control.
> "La venta descontó stock, quedó registrada con cajero, canal y forma de pago, y el dashboard ya la refleja."
Señalar que "Ventas de hoy" cambió.

**Paso 4 — Productos e inventario (40 s).** Productos → filtro de stock bajo → abrir **Recibir stock** (no hace falta guardar).
> "Cada producto tiene su lead time desde China configurable. El sistema calcula el punto de reorden con ese tiempo y adelanta la alerta si un evento de alta demanda cae dentro de la ventana de envío."

**Paso 5 — Pronóstico con IA (90 s).** Predicciones. Cambiar el horizonte a **30 días** y luego **3 meses**.
> "La gráfica separa histórico de pronóstico. Abajo, señales por producto —qué sube y qué baja— y recomendaciones de reabastecimiento con cantidad sugerida."
Luego **Recalibrar modelo**. Tarda unos segundos.
> "Esto que acaba de pasar es lo que la tesis exige: el sistema entrenó **seis líneas base** —naïve, naïve estacional, media móvil, suavizamiento exponencial, Holt-Winters y ARIMA— y el modelo de IA, los evaluó a todos con **cinco ventanas de origen móvil**, y publicó el modelo **solo porque superó al naïve estacional en más del 10 %**. Si no lo hubiera superado, habría rechazado la publicación y conservado el anterior. Aquí está el resultado: MASE, WAPE y mejora sobre la línea base."
Leer las tres cifras de la tarjeta.

**Paso 6 — Usuarios y roles (30 s).** Usuarios. Mostrar la lista y el botón **Nuevo usuario**; no crear nada.
> "Gestión de cuentas desde la base de datos: alta, cambio de rol, activar o desactivar, restablecer contraseña. Con guardas: no se puede dejar el sistema sin administrador."

Entregar el turno:
> "P4 les cuenta qué dicen los números."

---

### P4 — Resultados, limitaciones y siguiente fase (2.5 min, diapositivas 9–12)

**Diapositiva 9 — Perfil del catálogo.** Tabla: 25 productos, **100 % series intermitentes**, ~77 % de días sin venta, ADI ≈ 5.
> "Antes de modelar, perfilamos las series como pide el cap. 2.2.3. El resultado: todo el catálogo es demanda intermitente. Eso determina la estrategia: un regresor diario por producto aprendería a predecir cero. Por eso el modelo actual trabaja sobre el agregado, y el paso siguiente es agregar semanalmente por producto."

**Diapositiva 10 — Ranking de candidatos.** La tabla completa:

| Candidato | MASE | WAPE % |
|---|---|---|
| gradient_boosting | **0.803** | 43.99 |
| suavizamiento_exponencial | 0.831 | 46.06 |
| arima | 0.841 | 46.57 |
| holt_winters | 0.851 | 46.55 |
| media_movil | 0.886 | 48.85 |
| naive_estacional | 1.034 | 56.95 |

> "Cinco ventanas de validación, horizonte de 30 días. El modelo de IA gana con **22 % de mejora** sobre el naïve estacional y le gana en 4 de las 5 ventanas. Pero fíjense en la distancia con el suavizamiento exponencial: 0.03 de MASE. La IA aporta, pero no es mágica."

**Diapositiva 11 — La honestidad del método.** La tabla antes/después:

| | Generador anterior | Simulador actual |
|---|---|---|
| Mejora sobre naïve estacional | 35 % | **22 %** |
| Distancia al método simple | 0.12 | **0.03** |

> "Este es, para nosotros, el hallazgo más importante de la fase. El primer generador de datos usaba las mismas funciones de calendario que el modelo recibe como variables: le estábamos regalando la respuesta, y marcaba 35 %. Lo reemplazamos por un simulador que no comparte nada con el modelo —hay una prueba automática que lo garantiza— y la mejora bajó a 22 %. **El 22 % es defendible; el 35 % no lo era.** Preferimos el número honesto."

**Diapositiva 12 — Limitaciones y siguiente fase.** Decirlas antes de que las pregunten:
> "Tres limitaciones claras. Una: **los datos son simulados** porque no tuvimos acceso al histórico de la empresa; el simulador reproduce intermitencia, quiebres de stock y el calendario guatemalteco, pero no es la empresa. Dos: **12 meses de historia** significan que cada evento anual aparece una sola vez, y el modelo subestima el Bono 14 porque lo vio por primera vez en la ventana de evaluación. Tres: el modelo pronostica **el total diario**, no unidades por producto.
> Siguiente fase: importador de datos reales, pronóstico por producto con agregación semanal, y validación con la empresa."

Cierre:
> "Todo lo que mostramos está en el repositorio, con su historial, y desplegado en la URL de la pantalla. Gracias."

---

## 4. Tabla teoría → solución (para la diapositiva 3 y para preguntas)

| La tesis exige | Sección | Dónde está en el MVP | Verificable en |
|---|---|---|---|
| Líneas base: naïve, naïve estacional, media móvil, suavizamiento, ARIMA | 2.2.2 | Seis candidatos evaluados en cada recalibración | `backend/app/ml/baselines.py` |
| Validación de origen móvil, varios cortes | 2.5 | 5 ventanas, reentrenamiento en cada una | `backend/app/ml/evaluation.py` |
| MASE (escalado in-sample), WAPE, MAE, RMSE, sMAPE, sesgo | 2.5 / Tabla 2 | Las seis métricas por ventana | `backend/app/ml/metrics.py` |
| Publicar solo con mejora ≥ 10 % y sin sesgo inaceptable | 2.5.1 | Criterio de publicación; si falla, conserva el modelo anterior | `evaluation.decidir_publicacion` |
| Perfilar ceros, intervalo entre demandas, variabilidad | 2.2.3 | Clasificación Syntetos-Boylan-Croston por producto | `GET /predictions/series-profile` |
| Estacionalidad de Guatemala como variables explícitas | 2.1.2 | Diciembre, Bono 14, Caravana como features | `backend/app/ml/calendar_features.py` |
| Versionado del modelo | 2.7 | Artefactos versionados por fecha, escritura atómica | `/var/lib/zorros/artifacts/` |
| Roles y autenticación | RF-01, RNF-03 | JWT, bcrypt, guardas de último administrador | `backend/app/routers/users_router.py` |
| Despliegue reproducible en contenedores | RNF-12 | Docker Compose + PostgreSQL | `docker-compose.yml` |
| Demanda censurada por inventario | 2.1 | El simulador pierde ventas sin stock (424 unidades en 12 meses) | `backend/app/simular_ventas.py` |

---

## 5. Cifras: cuáles sí y cuáles no

**Sí se pueden citar** (verificables en el repositorio o en producción):

- 6 módulos funcionales · 9 PRs mezclados · **128 pruebas automatizadas**
- 6 líneas base · 5 ventanas de origen móvil · horizonte de 30 días
- MASE **0.803** vs naïve estacional **1.034** → **22.35 % de mejora**, consistencia 4 de 5
- 25 productos, **100 % intermitentes**, ~77 % de días sin venta, ADI medio 5.2
- 12 meses simulados: 366 días, 1,607 tickets, 2,492 unidades, 424 perdidas por stock
- Producción: 1 núcleo, ~350 MB de RAM, HTTPS con renovación automática

**No citar:**

- **Nada del generador anterior** (el "35 %" o "MASE 0.699" solo como contraste de la diapositiva 11).
- **"Confianza del modelo: X %"** que aparece en el dashboard: es `100 − WAPE`, no es un nivel de confianza estadístico. Está documentado como defecto pendiente. Si lo preguntan, decirlo así.
- Cualquier número sobre la empresa real: no hay datos de la empresa.

---

## 6. Preguntas probables del jurado

**"¿Por qué datos simulados y no reales?"**
> No tuvimos acceso al histórico de la empresa en esta fase. En lugar de usar datos inventados al azar, construimos un simulador que reproduce las propiedades que la tesis identifica como críticas: intermitencia, quiebres de stock, calendario guatemalteco. Y nos aseguramos de que no comparta nada con el modelo, para que la evaluación no sea circular. El importador para datos reales es la primera tarea de la siguiente fase.

**"¿22 % es mucho o poco?"**
> La tesis fija el umbral en 10 %, así que lo supera con margen. Pero lo más honesto es decir que un suavizamiento exponencial de tres líneas queda a 0.03 de MASE. La IA aporta; la distancia con lo simple es pequeña. Con datos reales y más historia esperamos que crezca, pero no lo damos por hecho.

**"¿Por qué el sesgo es del 19 %?"**
> El modelo subestima. Con 12 meses de historia, el primer Bono 14 que ve cae en la ventana de evaluación, no en la de entrenamiento: no puede anticipar un pico que nunca vio. Con 24 meses vería cada evento una vez antes de evaluarse. Es una limitación de la ventana de datos, no del método.

**"¿Qué pasa si el modelo no supera la línea base?"**
> No se publica. El sistema conserva el modelo anterior y registra el intento con sus métricas y el motivo del rechazo. Lo probamos forzando un umbral imposible: rechazó, y el artefacto activo no cambió.

**"¿Por qué el total diario y no por producto?"**
> Porque perfilamos primero, como pide la tesis, y el 100 % del catálogo salió intermitente. Un regresor diario por producto aprende a predecir cero. La estrategia correcta es agregar semanalmente por producto, y es el siguiente paso del motor.

**"¿La 'confianza del modelo' del dashboard qué es?"**
> Es 100 menos el WAPE. No es un intervalo ni una probabilidad; está identificado como un defecto de presentación pendiente de corregir. Las métricas reales son MASE y WAPE.

**"¿Cómo garantizan que el simulador no hace trampa?"**
> Hay una prueba automática que lee el código fuente del simulador y falla si importa el módulo de features del modelo. Además, el simulador usa fechas concretas —la Caravana es un sábado específico, no medio febrero— mientras el modelo solo ve banderas de temporada.

---

## 7. Plan B — si falla la red o el sistema

1. **Sin internet:** mostrar las capturas guardadas en la laptop siguiendo el mismo orden de la sección 3. P3 narra igual.
2. **La página carga pero el login falla:** P2 restablece la contraseña por SSH desde el celular (comando en la sección 1) mientras P3 sigue con Productos y Predicciones, que no requieren re-login si la sesión sigue abierta en la otra pestaña.
3. **Recalibrar tarda más de 30 s o falla:** no insistir. Decir *"el resultado de la última recalibración es este"* y leer las tarjetas que ya están en pantalla.
4. **Todo falla:** el deck tiene en las diapositivas 9–11 las tablas de resultados. Se presenta con el deck y se ofrece la URL para que el jurado la abra después.

---

## 8. Lo que este guión no cubre

- **Capítulo 5 (factibilidad):** lo redacta el equipo del documento. Para la diapositiva 5 pueden usar: VPS de un núcleo compartido, ~350 MB, stack 100 % open source (FastAPI, PostgreSQL, scikit-learn, statsmodels), certificado gratuito.
- **Resultados del instrumento de investigación (cap. 4):** exceptuado en esta fase según la rúbrica.

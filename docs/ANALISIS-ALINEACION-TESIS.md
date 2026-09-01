# Análisis de alineación: código vs. Trabajo de Graduación

**Proyecto:** Sistema Predictivo basado en Inteligencia Artificial para la Gestión de Ventas de Zorros Revolution Biker
**Documento de referencia:** `docs/Trabajo de Graduacion.pdf` (35 páginas, Universidad Mariano Gálvez)
**Repositorio auditado:** `zorros-revolution-biker-predictivo` — commit `4c4b3d3`, rama `main`
**Fecha del análisis:** 31 de agosto de 2026
**Alcance:** 2,726 líneas (backend FastAPI, frontend HTML/CSS/JS, esquema SQL, archivos de despliegue)

---

## 1. Veredicto

**El sistema construido y el sistema documentado en la tesis no son el mismo sistema.**

La tesis describe un **sistema analítico de pronóstico** que ingiere históricos de ventas externos, los valida bajo un contrato de datos, construye series por producto–sucursal–día, compara modelos de IA contra líneas base con validación de origen móvil y publica pronósticos trazables con explicación e incertidumbre.

Lo construido es un **punto de venta (POS) con gestión de inventario** que genera sus propias ventas transaccionalmente, más un pronosticador agregado adosado: un único `GradientBoostingRegressor` sobre **una sola serie** (el total diario en quetzales de toda la empresa), evaluado con un hold-out simple y entrenado exclusivamente sobre datos sintéticos.

Esto no invalida el trabajo: hay una aplicación funcional, con autenticación por roles verificada en servidor, separación cabecera/detalle de venta correcta, control de fuga temporal bien resuelto en el pipeline de features, y un módulo de reabastecimiento con lead time de China que es genuinamente útil para el negocio. Pero **la documentación técnica del Capítulo IV no describe el artefacto**, y el motor de IA no cumple los compromisos metodológicos del Capítulo II que sostienen la validez académica del trabajo.

### Cuadro de mando

| Dimensión | Resultado |
|---|---|
| Requerimientos funcionales (RF-01…18) | **0 completos · 8 parciales · 10 ausentes** |
| Requerimientos no funcionales (RNF-01…12) | 2 parciales · 1 por omisión · 1 incumplido · 5 ausentes · 3 sin evidencia |
| Entidades del modelo de datos (Tabla 11) | 4 implementadas y usadas · 3 definidas pero muertas · **3 inexistentes** |
| Endpoints de la API (Tabla 12) | 5 con equivalente aproximado · **7 ausentes** · 0 con la ruta especificada |
| Componentes de arquitectura (Tabla 10) | 1 conforme · 4 divergentes · 4 ausentes |
| Compromisos del motor de IA (Cap. II) | **0 completos · 4 parciales · 7 ausentes** |
| Cobertura de features (Tabla 1) | **5 de ~18 elementos (28 %)** |
| Casos de uso (CU-01/02/03) | CU-01 ausente al 100 % · CU-02 parcial · CU-03 parcial |
| Cobertura de pruebas | **0 %** — no existe ninguna prueba automatizada |

### Los cinco problemas que hay que resolver antes de la defensa

1. **Circularidad de la evidencia.** El generador de datos sintéticos usa las mismas funciones de calendario que el modelo consume como features. Toda métrica reportada es circular.
2. **La dimensión sucursal no existe.** El objetivo general promete pronóstico "por sucursal y canal"; no hay tabla `stores` y `canal` es texto libre.
3. **Entrenar y publicar son el mismo acto.** No hay criterio de aceptación, ni versionado de artefactos, ni forma de revertir.
4. **No hay ingesta de datos.** Todo el Capítulo 3.4 y el caso de uso CU-01 dependen de un importador CSV/XLSX que no existe.
5. **La documentación técnica no corresponde al código.** React/Vue → JS vanilla; PostgreSQL → SQLite/MySQL; Celery+Redis → nada; OpenTelemetry → nada.

---

## 2. Metodología de esta auditoría

Se extrajo el texto íntegro del PDF (35 páginas) y se contrastó contra el código en cuatro frentes en paralelo: motor de ML, modelo de datos y API, frontend y wireframes, y seguridad/RNF/despliegue. **Cada afirmación de este informe fue verificada contra una línea de código concreta.** Los hallazgos de mayor impacto se re-verificaron de forma independiente antes de incluirse.

---

## 3. Requerimientos funcionales (Tabla 4 de la tesis)

| RF | Requerimiento | Prioridad | Estado | Evidencia |
|---|---|---|---|---|
| RF-01 | Autenticación con roles | Debe | **Parcial** | Login JWT `auth_router.py:11`; RBAC `deps.py:47-53`. **Roles equivocados**: `admin`/`cajero` (`models.py:10-12`) en vez de administrador/analista/consulta. Sin revocación de token |
| RF-02 | Catálogo (productos, categorías, sucursales, canales) | Debe | **Parcial** | Productos CRUD `products_router.py:30,41,58`. **Sucursales inexistentes**; categorías y canal son texto libre |
| RF-03 | Carga de ventas CSV/XLSX | Debe | **Ausente** | Cero coincidencias de `UploadFile`/`csv`/`xlsx` en todo el repo. `python-multipart` instalado sin uso |
| RF-04 | Validación de esquema, nulos, duplicados, claves | Debe | **Ausente** | Existe validación Pydantic de payloads, no de cargas |
| RF-05 | Trazabilidad de carga | Debe | **Ausente** | Sin tabla `data_loads`, sin `sales.source_load_id` |
| RF-06 | Perfilamiento (cobertura, ceros, atípicos, densidad) | Debe | **Ausente** | Ningún endpoint lo expone |
| RF-07 | Entrenamiento con parámetros versionados | Debe | **Parcial** | `forecasting.py:107` un solo algoritmo con hiperparámetros hardcodeados |
| RF-08 | Evaluación temporal multi-corte vs baseline | Debe | **Parcial** | `forecasting.py:99-101` **un solo hold-out**, no origen móvil |
| RF-09 | Publicación solo de versión aprobada, conservando la anterior | Debe | **Ausente** | `forecasting.py:121-123` sobrescribe el artefacto sin condición ni historial |
| RF-10 | Pronóstico 7/14/30 días por nivel autorizado | Debe | **Parcial** | Un único nivel: total diario de la empresa (`forecasting.py:40-58`). Falta el horizonte de 14 |
| RF-11 | Intervalos de incertidumbre | Debería | **Parcial (cosmético)** | `forecasting.py:255` ±15 % fijo, no derivado del modelo |
| RF-12 | Explicación (factores, limitaciones, versión) | Debería | **Ausente** | Sin SHAP; `schemas.py:145-150` no incluye versión ni fecha de corte |
| RF-13 | Alertas (demanda alta, baja rotación, datos desactualizados) | Debería | **Parcial** | `forecasting.py:267-313` cubre alta/baja demanda; falta la alerta de frescura de datos |
| RF-14 | Escenarios (ajustar promoción o precio) | Podría | **Ausente** | — |
| RF-15 | Exportación CSV/XLSX/PDF | Debe | **Ausente** | Sin dependencias, sin endpoint, sin botón |
| RF-16 | Monitoreo pronóstico vs. venta real | Debe | **Ausente** | Sin `actuals` y con `forecasts` nunca escrita, es estructuralmente imposible |
| RF-17 | Bitácora de cargas, entrenamiento, aprobación, fallos | Debe | **Ausente** | `AuditLog` aparece solo en su definición (`models.py:145-146`); nunca se escribe |
| RF-18 | Endpoints seguros para POS/e-commerce | Podría | **Parcial** | API REST con JWT, pero sin versionado, sin scopes, sin rate limiting, CORS `*` |

**Ocho de los diez requerimientos ausentes son de prioridad "Debe".**

### Casos de uso

- **CU-01 Importar histórico de ventas — ausente al 100 %.** Ninguno de los seis pasos del flujo principal existe.
- **CU-02 Entrenar y evaluar — parcial.** Hay ejecución, métricas y un baseline, pero sin alcance seleccionable, sin origen móvil, sin múltiples candidatos y sin la postcondición clave: *"modelo candidato disponible para aprobación"*.
- **CU-03 Consultar pronóstico — parcial.** Falta selección de nivel, explicación, exportación y advertencia por datos atrasados. Además está restringido a `admin` (`predictions_router.py:14`), lo que **excluye al actor que la propia tesis define** (gerencia, ventas, inventario) y omite la postcondición *"consulta registrada para auditoría"*.

---

## 4. Modelo de datos (Tabla 11)

| Entidad | Estado | Detalle |
|---|---|---|
| `users` | Implementada | `models.py:27-38`. Roles `admin`/`cajero` en vez de administrador/analista/consulta |
| `stores` | **Inexistente** | Cero coincidencias de `store`/`sucursal` en todo el repositorio. `canal` es un `String(40)` libre (`models.py:67`) sin catálogo ni FK |
| `products` | Implementada | `models.py:41-58`. Falta `marca`; `categoria` es texto libre. Añade campos de inventario no previstos |
| `sales` | Implementada con divergencia | `models.py:61-72`. Faltan `store_id` y `source_load_id`; en su lugar hay `cajero_id` y `metodo_pago` — es una venta de POS, no una venta importada |
| `sale_items` | **Implementada correctamente** | `models.py:75-85`. La separación cabecera/detalle que exige la tesis está bien resuelta. Falta `descuento` |
| `data_loads` | **Inexistente** | Bloquea RF-03/04/05/06 y CU-01 completo |
| `model_runs` | Parcial | `models.py:116-127`. Faltan `fecha_corte`, `horizonte`, `estado` y marca de publicación |
| `forecasts` | **Definida pero muerta** | `models.py:130-142`. Cero escrituras y cero lecturas: los pronósticos se recalculan al vuelo y nunca se persisten |
| `actuals` | **Inexistente** | Sin ella, RF-16 es imposible |
| `audit_log` | **Definida pero muerta** | `models.py:145-154`. Ninguna acción del sistema escribe bitácora |

**Entidades presentes fuera de la tesis:** `stock_movements` (`models.py:88-99`), `purchase_orders` (`models.py:102-113`).

---

## 5. API REST (Tabla 12)

**Ningún endpoint usa `/api/v1/`.** Cero coincidencias de `api/v1` en todo el repositorio; los routers se montan sin prefijo global (`main.py:32-38`), produciendo rutas planas.

| Ruta de la tesis | Estado | Ruta real |
|---|---|---|
| `POST /api/v1/auth/login` | Parcial | `POST /auth/login` (`auth_router.py:11`) |
| `GET /api/v1/catalog/products` | Parcial | `GET /products` (`products_router.py:12`) |
| `POST /api/v1/data-loads` | **Ausente** | — |
| `POST /api/v1/data-loads/{id}/confirm` | **Ausente** | — |
| `GET /api/v1/data-quality/summary` | **Ausente** | — |
| `POST /api/v1/model-runs` | Parcial | `POST /predictions/retrain` — **síncrono, entrena y publica en un solo paso** |
| `GET /api/v1/model-runs/{id}` | **Ausente** | — |
| `POST /api/v1/model-runs/{id}/publish` | **Ausente** | El incumplimiento más crítico |
| `GET /api/v1/forecasts` | Parcial | `GET /predictions/forecast` — `require_role("admin")`, más restrictivo que la tesis |
| `GET /api/v1/forecasts/metrics` | **Ausente** | Sin sesgo, sin métricas consultables |
| `GET /api/v1/alerts` | Parcial | `GET /predictions/signals` + `/recommendations` |
| `GET /api/v1/exports/forecasts` | **Ausente** | — |

No se usa el envelope `{data, error, meta}` ni `requestId` en ninguna respuesta.

---

## 6. Componentes de arquitectura (Tabla 10)

| Capa | Tesis | Realidad | Estado |
|---|---|---|---|
| Presentación | React o Vue | HTML/CSS/JS vanilla, servido por el propio FastAPI (`main.py:48-50`) | **Divergente** |
| Aplicación | FastAPI | FastAPI | **Conforme** |
| Datos | PostgreSQL | SQLite (dev) / MySQL (prod); `db/schema.sql` es MySQL puro | **Divergente** |
| Datos | Repositorio de artefactos versionados | joblib a **ruta fija**, sobrescrito en cada entrenamiento (`forecasting.py:28,123`) | **Parcial/roto** |
| Procesamiento | Servicio ETL con pandas | pandas solo para features internas; sin ingesta ni normalización | **Parcial** |
| IA | scikit-learn / XGBoost / SHAP | Solo `GradientBoostingRegressor`. **XGBoost y SHAP no están en `requirements.txt`** | **Parcial** |
| Tareas | Celery/RQ + Redis, entrenamiento asíncrono con 4 estados | Nada. El entrenamiento corre dentro del request HTTP | **Ausente** |
| Infraestructura | Nginx + TLS | Plantilla con solo `listen 80`; TLS como paso manual de certbot | **Parcial** |
| Observabilidad | OpenTelemetry / Prometheus | Solo `accesslog` de Gunicorn y `/api/health` | **Ausente** |

---

## 7. Motor de inteligencia artificial vs. Capítulo II

Esta es la sección de mayor riesgo académico: el Capítulo II es el que sostiene la validez metodológica del trabajo.

| Compromiso | Sección | Estado | Evidencia |
|---|---|---|---|
| Líneas base: naïve, naïve estacional, media móvil, suavizamiento exponencial, ARIMA, Prophet | 2.2.2 | **Ausente (1 de 6)** | Solo naïve estacional s=7 como referencia interna (`forecasting.py:111`). Cero coincidencias de `prophet`/`arima`/`holt`/`statsmodels` en el repo |
| El modelo de IA solo agrega valor si supera las referencias | 2.2.2 | **Parcial** | `forecasting.py:115-117` calcula `mejora_pct`, pero no se persiste ni condiciona nada |
| Validación temporal con origen móvil, múltiples cortes | 2.5 | **Ausente** | `forecasting.py:99-101` es un hold-out simple de un solo corte |
| MASE como métrica primaria | 2.5 | **Mal calculado** | `forecasting.py:79-85` escala por el MAE del naïve *out-of-sample*: es RelMAE, no el MASE de Hyndman & Koehler (2006) que la propia tesis cita |
| WAPE | 2.5 | **Implementado** | `forecasting.py:72-76`. Único punto plenamente conforme |
| MAE, RMSE, sMAPE, sesgo | 2.5 | **Ausentes** | RMSE, sMAPE y sesgo no existen en ninguna línea del repo |
| Publicar solo con mejora ≥ 10 % vs naïve estacional | 2.5.1 | **Ausente** | `forecasting.py:121-123` publica **sin un solo `if`** |
| Si ningún modelo supera la referencia, publicar el baseline | 2.5.1 | **Ausente** | Esa ruta no existe |
| Demanda intermitente: % de ceros, intervalo entre demandas, variabilidad | 2.2.3 | **Ausente** | `forecasting.py:56` *crea* ceros con `asfreq(fill_value=0.0)` sin medirlos nunca |
| Modelos globales, clustering y segmentación de series | 2.3.3 | **Ausente** | El pipeline agrega todo a **una sola serie escalar**; no hay `product_id` ni `categoria` en ninguna parte del ML |
| XGBoost / Random Forest como candidatos | 2.3.1 | **Parcial** | Un solo algoritmo fijo |
| Intervalos de incertidumbre | 2.6 | **Cosmético** | `forecasting.py:255` `margen = valor * 0.15`: constante mágica que no crece con el horizonte pese a que la predicción es recursiva |
| SHAP / explicabilidad | 2.6 | **Ausente** | `shap` no instalado; `feature_importances_` nunca se lee |
| Advertencia por poco historial o alta volatilidad | 2.6 | **Ausente** | Con 61 días entrena y publica sin advertir, sin haber visto un ciclo anual |
| Metadatos de la predicción (versión, fecha de corte, horizonte) | 2.6 | **Ausente** | `schemas.py:145-150` no los incluye |
| Control de fuga de información | 2.2, 2.3 | **Implementado** | `forecasting.py:66-69` usa `.shift()` correctamente; alineación train/serve verificada |
| Versionado del modelo | 2.7 | **Parcial** | Faltan features exactas, fecha de corte, hash del dataset y ruta del artefacto |
| Horizontes 7, 14 y 30 | 1.6.4 | **Desalineado** | **Falta 14**; la UI ofrece 7/30/90/180 (`predicciones.html:36-39`), y 90/180 están fuera del alcance declarado |

### Cobertura de features (Tabla 1): 5 de ~18 elementos

| Grupo | Presente | Ausente |
|---|---|---|
| Calendario | día de semana, mes (+ seno/coseno), día del mes | **semana del año, quincena, fin de mes, feriados oficiales** |
| Rezagos | t-1, t-7, t-14 | **t-28** — el código usa t-30, que no es múltiplo de 7 y rompe la alineación de día de semana |
| Ventanas | media móvil 7 y 30 | **mediana móvil, desviación móvil** — la volatilidad, que es el propósito declarado del grupo, no se captura |
| Comerciales | — | **precio, descuento, promoción, canal (0 de 4)** |
| Producto | — | **categoría, marca, talla, antigüedad (0 de 4)** |
| Inventario | — | **existencia, días sin stock (0 de 2)** — `StockMovement` tiene el histórico y ningún módulo de ML lo consume |

Los tres proxies de evento son groseros: `es_temporada_diciembre` marca el mes completo, `es_semana_bono14` del 1 al 15 de julio, y `es_caravana_del_zorro` **del 14 al 28 de febrero entero** (`calendar_features.py:20-31`).

---

## 8. Frontend vs. wireframes (sección 4.3)

| Elemento | Estado | Detalle |
|---|---|---|
| Navegación lateral: Resumen, Ventas, Pronósticos, **Inventario**, **Configuración** | **Parcial** | Solo 4 ítems (`dashboard.html:19-24`). **No existe Inventario** (aunque el backend expone `/inventory/*`) ni **Configuración** |
| Panel ejecutivo: ventas y pronóstico | Cumple | `dashboard.html:42-73` |
| Panel ejecutivo: **error del modelo** | **No cumple** | Muestra "Confianza del modelo: X %" (`dashboard.html:72`), que no es una métrica de error. MASE/WAPE no aparecen |
| Panel ejecutivo: alertas | Parcial | Solo reabastecimiento; para el cajero el panel se sustituye por "Disponible solo para administradores" |
| **Flujo completo de importación (Figura 5)** | **Ausente** | Ninguna de sus cuatro etapas tiene UI. Sin ella caen HU-02, HU-03 y HU-04 |
| Filtro por horizonte | Cumple | `predicciones.html:35-40` |
| Filtro por **sucursal** y **categoría** | **Ausente** | No existen ni el selector ni el concepto |
| Gráfico que diferencia histórico de pronóstico | **Cumple bien** | `predicciones.js:44-45` — distingue por color **y** por `borderDash`, no solo por color |
| **Panel de factores que contribuyen** | **No cumple** | Muestra qué producto sube o baja, nunca **por qué** |
| **Vista técnica (versión, fecha de corte, métrica, límites)** | **Ausente** | El backend devuelve `intervalo_inf`/`intervalo_sup` y **el cliente los descarta** (`predicciones.js:31-33`). Los KPI de modelo solo se llenan tras pulsar "Recalibrar"; al recargar vuelven a "Sin entrenar" |
| HU-05 comparación contra período anterior | No cumple | Solo existe por producto en señales |
| HU-07 tablero real vs pronóstico con **error y sesgo** | Parcial | La tendencia sí; error y sesgo no aparecen en ninguna vista |
| HU-08 comparar modelos antes de publicar | **Ausente** | `predicciones.js:116-133` publica directamente |
| HU-09 explicabilidad · HU-10 exportar · HU-11 restaurar versión · HU-12 alerta de deriva | **Ausentes** | — |
| HU-01 gestión de usuarios | **Ausente en frontend** | `users_router.py` completo sin interfaz |

---

## 9. Requerimientos no funcionales (Tabla 5)

| RNF | Requisito | Estado | Evidencia |
|---|---|---|---|
| RNF-01 Rendimiento | p95 < 3 s | **Sin evidencia** | Nunca se midió |
| RNF-02 Disponibilidad | 99 % mensual | Parcial | `Restart=always`; `/api/health` (`main.py:41`). Sin `/ready`, sin monitoreo de uptime |
| RNF-03 Seguridad | TLS, roles, hash | **Parcial** | Hash bcrypt correcto (`security.py:9`), RBAC en servidor (`deps.py:47-53`). **Pero**: `SECRET_KEY` con default publicado en el código (`config.py:15`); CORS `*` con `allow_credentials=True` (`main.py:23-29`); Nginx solo HTTP; sin HSTS/CSP; sin rate limiting en login; token de 12 h sin refresh |
| RNF-04 Privacidad | Excluir datos personales | Cumple por omisión | No se modelan clientes. Sin inventario de campos documentado |
| RNF-05 Usabilidad | 80 % de tareas completadas | **Sin evidencia** | No se aplicó el cuestionario del Cap. 3.3.2 |
| RNF-06 Accesibilidad | **WCAG 2.2 AA** | **Incumplido** | Ver sección 10 |
| RNF-07 Mantenibilidad | Pruebas, docs, análisis estático | **Ausente** | Cero pruebas, sin linter ni type checker configurado |
| RNF-08 Reproducibilidad | Cada pronóstico referencia datos y modelo | **Ausente** | Artefacto sobrescrito, `forecasts` vacía: hoy es imposible reconstruir qué predijo el sistema el mes pasado. Sin migraciones (`main.py:19` usa `create_all`) |
| RNF-09 Respaldo | Copias automáticas, restauración ensayada | **Ausente** | Sin procedimiento en `deploy/` |
| RNF-10 Escalabilidad | Prueba con 2× el volumen piloto | **Sin evidencia** | No se ejecutó |
| RNF-11 Observabilidad | Logs estructurados, métricas, correlación | **Ausente** | Solo accesslog a stdout |
| RNF-12 Portabilidad | **Despliegue en contenedores** | **Ausente** | No existe `Dockerfile` ni `docker-compose` |

### Higiene de dependencias
- **Faltan** `xgboost`, `shap`, `statsmodels`/`prophet` (exigidos por Cap. 2.3/2.5/2.6) y `openpyxl` (necesario para RF-03).
- `python-jose==3.3.0` arrastra CVE-2024-33663 (confusión de algoritmo) y CVE-2024-33664 (JWT bomb).
- No hay auditoría de dependencias en CI porque no hay CI.

---

## 10. Accesibilidad — RNF-06 incumplido

La tesis compromete **WCAG 2.2 nivel AA en las vistas principales**. Los cinco HTML no contienen **ni un solo atributo `aria-*`, `role=` o `scope=`**.

| Criterio WCAG | Hallazgo | Evidencia |
|---|---|---|
| 1.4.3 Contraste | `#e11d2e` sobre `#12151c` = **3.84:1** (requiere 4.5) en mensajes de error, texto de peligro y deltas negativos | `styles.css:89,120,177` |
| 1.4.11 Contraste no textual | Borde de `input`/`select` = **1.31:1** (requiere 3:1): el límite del campo no es perceptible | `styles.css:166-174` |
| 2.4.7 Foco visible | `outline: none` en campos; botones, enlaces y `.filtro-btn` sin ningún estilo `:focus` | `styles.css:175` |
| 4.1.3 Mensajes de estado | Errores y KPI se inyectan por JS **sin `role="alert"` ni `aria-live`**: el lector de pantalla nunca los anuncia | `auth.js:17-18`, `dashboard.js:6-20` |
| 1.3.1 Información y relaciones | `<th>` sin `scope="col"`; etiqueta y valor de los KPI son `<span>` hermanos sin relación programática | `productos.html:66`, `ventas.html:41` |
| 4.1.2 Nombre, función, valor | `<button id="btn-logout">⎋</button>` se anuncia como el glifo "⎋". Botones `✕` sin `aria-label`. Modales sin `role="dialog"` | `dashboard.html:30`, `productos.html:78,94` |
| 2.4.3 / 2.1.1 Foco y teclado | Al abrir un modal no se mueve el foco, no hay trampa de foco, no se restaura al cerrar y **no se cierra con Escape** | `productos.js:62,93`, `ventas.js:37` |
| 2.5.8 Tamaño del objetivo (nuevo en 2.2) | `.btn-icon` ≈ 16-19 px efectivos; requisito 24×24 | `styles.css:136` |
| 1.1.1 Contenido no textual | `<canvas>` de Chart.js sin alternativa textual ni tabla equivalente | `dashboard.html:81` |
| 3.1.2 Idioma de las partes | "Predictive Dashboard", "AI Predictive Engine" en inglés dentro de `<html lang="es">` | `dashboard.html:16,37` |
| 2.4.1 Evitar bloques | Sin enlace "saltar al contenido"; 15 líneas de navegación repetidas en cada página | `dashboard.html:11-32` |

**Aciertos:** `autocomplete="username"`/`current-password` presentes (3.3.8), y las series del gráfico se distinguen por color **y** trazo (1.4.1).

---

## 11. Defectos que hay que corregir

### Críticos

**C1 — Los tres modales están visibles permanentemente.**
`styles.css:186` declara `.modal-overlay { display: flex }` y **no existe ninguna regla `[hidden] { display: none !important }`** en la hoja. Al ser origen de autor, vence a la hoja del navegador: los modales de `productos.html:76`, `productos.html:92` y `ventas.html:52` se muestran al cargar la página, y `hidden = true` en el JS no cierra nada. En `productos.html` esto expone el formulario "Nuevo producto" —restringido a admin— a cualquier usuario. *(Verificado directamente.)*

**C2 — Circularidad total de la evidencia empírica.**
`seed_data.py:16` importa `calendar_features`, y las líneas 96-100 generan la demanda sintética con `es_temporada_diciembre`, `es_semana_bono14` y `es_caravana_del_zorro` — **las mismas tres funciones** que producen las features `is_diciembre`, `is_semana_bono14` e `is_caravana_zorro` en `FEATURE_COLUMNS` (`forecasting.py:33-37`). El modelo recupera por construcción la señal que el generador inyectó. **Ninguna métrica obtenida sobre estos datos constituye evidencia.** *(Verificado directamente.)*

**C3 — XSS con robo de sesión.**
Todas las listas y tablas se construyen con `innerHTML` interpolando datos del servidor sin escapar (`dashboard.js:71-77`, `predicciones.js:72-81,98-104`, `productos.js:36-45`, `ventas.js:88-97`). Combinado con el JWT en `localStorage` (`api.js:3-5`), un nombre de producto con `<img onerror>` permite exfiltrar la sesión.

**C4 — Sin gate de publicación.**
`forecasting.py:121-123` ejecuta `joblib.dump` incondicionalmente sobre una ruta fija. El modelo se publica **aunque sea peor que el naïve**, se pierde la versión anterior y no hay rollback. *(Verificado directamente.)*

### Altos

**A1 — El "MASE" no es MASE.** `forecasting.py:79-85` escala por el MAE del naïve en el mismo conjunto de prueba; el MASE de Hyndman & Koehler escala por el MAE in-sample. La métrica es RelMAE y no es comparable con la literatura. *(Verificado.)*

**A2 — Guardas que reportan "error cero".** `forecasting.py:74-75` devuelve WAPE = 0 % si la serie de test es nula, y `:82-83` devuelve MASE = 0 si el naïve es perfecto. Combinado con `confianza = 100 - wape` (`:212`), el gerente puede ver **"Confianza del modelo: 100 %"** por un caso degenerado.

**A3 — "Confianza del modelo" es una métrica inventada.** El complemento a 100 de un WAPE no es una probabilidad ni un nivel de confianza estadístico. Es exactamente el "valor puntual sin contexto interpretado como certeza" que la sección 2.6 advierte evitar.

**A4 — El sistema deja de anticipar un evento justo cuando ocurre.** `calendar_features.py:34-39`: el 15 de diciembre, `dias_hasta_diciembre` devuelve 351, no 0. Por tanto `reorder.py:55` **nunca aplica el refuerzo durante el propio evento**. Mismo defecto para Bono 14 y Caravana.

**A5 — La recomendación de reposición no usa el modelo de IA.** `reorder.py` **no importa `forecasting`**: `_demanda_diaria_promedio` es un promedio aritmético de 60 días, expuesto en un campo llamado `demanda_diaria_pronosticada`. El nombre afirma un pronóstico que no existe. Además divide por 60 fijo, así que un producto dado de alta hace 10 días queda 6× subestimado y **nunca generará una recomendación**. *(Verificado.)*

**A6 — DoS trivial.** `predictions_router.py:14` acepta `horizonte: int` sin validar. `?horizonte=500000` ejecuta un bucle O(n²) con `pd.concat` dentro, bloqueando el worker.

**A7 — El fallback heurístico es indistinguible del modelo en la UI.** `forecasting.py:163-176` aplica factores mágicos (1.35 / 1.25 / 1.2) cuando no hay artefacto, y la respuesta se devuelve como `pronostico` sin marcar el origen. **El usuario no puede saber si ve IA o una regla de tres.**

### Medios

- **M1** — Escritura no atómica del artefacto (`forecasting.py:123`): un `/retrain` concurrente con un `/forecast` puede cargar un pickle a medio escribir. Falta `os.replace`.
- **M2** — Entrenamiento síncrono dentro del request HTTP (`predictions_router.py:26`).
- **M3** — El modelo se recarga de disco en cada petición, dos veces por request en `/dashboard/summary`.
- **M4** — Zona horaria: `datetime.utcnow()` en todo el backend contra ventas generadas en hora local; Guatemala es UTC-6, los cortes de día están desfasados 6 horas.
- **M5** — Desajuste train/serve en el fallback de lags (`forecasting.py:186-188`): en entrenamiento `dropna()` garantiza que el modelo nunca vio `lag_30 == lag_1`; en inferencia con historial corto se le entrega justo esa distribución.
- **M6** — Hiperparámetros triplicados (`forecasting.py:107`, `:121`, `:131`): cambiar uno sin los otros produce un registro de trazabilidad que miente.
- **M7** — `dias_hasta_*` se calculan y nunca llegan al modelo: la proximidad a un evento, la señal más informativa del conjunto, no está en `FEATURE_COLUMNS`.
- **M8** — El rol se lee de `localStorage` (`api.js:7-9`), dato controlado por el usuario. **No hay escalada real** —el backend verifica con `require_role` en todos los endpoints sensibles— pero sí fuga de la interfaz y UX rota.

---

## 12. Plan priorizado

### P0 — Sin esto la tesis no tiene evidencia defendible

1. **Conseguir datos reales de la empresa** y ejecutar el procedimiento del Cap. 3.4. Mientras el único histórico sea `seed_data.py`, ninguna métrica del capítulo de resultados es defendible. Si no hay datos reales a tiempo, **declararlo como limitación explícita** y no presentar MASE/WAPE como validación.
2. **Módulo de líneas base** (`ml/baselines.py`): naïve, naïve estacional, media móvil, Holt-Winters y ARIMA, con la misma interfaz que el modelo de IA. Añadir `statsmodels` a `requirements.txt`.
3. **Validación de origen móvil**: sustituir el hold-out de `forecasting.py:99-101` por un bucle de ≥5 orígenes con reentrenamiento por corte y horizontes 7/14/30, reportando estabilidad entre ventanas.
4. **Suite de métricas correcta**: MASE con escalado in-sample, WAPE, MAE, RMSE, sMAPE y sesgo. Corregir A1 y A2.
5. **Gate de publicación**: condicionar `forecasting.py:121-123` a mejora ≥ 10 % y sesgo aceptable; implementar la rama que publica el baseline cuando ningún candidato gana.
6. **Corregir C1 y C3** (modales visibles y XSS): son defectos de seguridad y funcionamiento en producción, no deuda estética.

### P1 — Cumplimiento de los requerimientos "Debe" pendientes

7. **Importador CSV/XLSX** con `data_loads`, hash de archivo, validación por reglas, reporte de filas rechazadas y confirmación en dos pasos (RF-03/04/05, CU-01). Añadir `sales.source_load_id` y `openpyxl`.
8. **Entidad `stores`** y `sales.store_id`; migrar `canal` de texto libre a FK. Sin esto el objetivo general es inalcanzable.
9. **Persistir `forecasts`** (con nivel + clave) y crear `actuals`, para poder comparar lo pronosticado contra lo real (RF-16, RNF-08).
10. **Separar entrenamiento de publicación**: `model_runs.estado` y `fecha_corte`, `GET /model-runs/{id}`, `POST /model-runs/{id}/publish` y artefactos versionados por nombre con escritura atómica.
11. **Alinear roles** a administrador/analista/consulta y reabrir `GET /forecasts` al rol consulta, que hoy queda excluido de su propio caso de uso.
12. **Activar `audit_log`** (la tabla ya existe; falta el `write`) y **versionar la API bajo `/api/v1/`** con el envelope `{data, error, meta}`.
13. **Exportación** CSV/XLSX/PDF y **perfilamiento** `GET /data-quality/summary` (RF-15, RF-06).

### P2 — Calidad, explicabilidad y cierre de la Tabla 10

14. Bajar el pronóstico a nivel producto/categoría, modelar **unidades** además de ingreso, y perfilar intermitencia (% de ceros, ADI, CV²) por SKU.
15. Completar la Tabla 1: `t-28` en vez de `t-30`, semana/quincena/fin de mes, calendario de feriados de Guatemala, mediana y desviación móviles, y las dimensiones comerciales, de producto e inventario.
16. SHAP con agregación a factores de alto nivel; intervalos por cuantiles empíricos de residuos que se ensanchen con el horizonte; retirar "Confianza del modelo".
17. Cola asíncrona (RQ + Redis basta para esta escala), logging estructurado con correlación, `/ready`, y `Dockerfile` para cerrar RNF-11 y RNF-12.
18. Suite `pytest`: fórmulas de métricas contra valores calculados a mano, una prueba que confirme que ninguna feature de la fila *t* usa datos ≥ *t*, equivalencia train/serve de lags, y el gate del 10 %.
19. Corregir accesibilidad: `[hidden]`, `aria-live` en zonas dinámicas, `scope` en tablas, `aria-label` en botones de icono, foco visible, gestión de foco y Escape en modales, y subir el rojo de error a ≥ 4.5:1.

---

## 13. Decisiones que el equipo debe tomar (no son técnicas)

1. **Alcance del módulo de reabastecimiento.** La tesis lo declara **extensión futura** (Cap. 2.1.3: *"una futura extensión podría calcular sugerencias de reposición bajo reglas aprobadas por la empresa"*), pero el código ya lo implementa con constantes que nadie aprobó (`DIAS_SEGURIDAD_STOCK = 10`, `factor_evento = 1.4`). Hay dos salidas coherentes: incorporarlo formalmente a la tesis documentando la política de inventario y validándola con la empresa, o degradarlo a "señales de demanda exportables". Mantenerlo como está es la peor opción.

2. **Divergencias de la Tabla 10.** React/Vue → JS vanilla, PostgreSQL → SQLite/MySQL, Celery+Redis → nada, OpenTelemetry → nada. Hay que corregir el código o corregir la tesis; hoy la documentación técnica no describe el artefacto y cualquier revisor lo verá al primer contraste.

3. **Fase del trabajo.** La Introducción declara: *"El documento desarrolla únicamente los entregables de la fase de ideación, análisis y diseño."* Pero existe un sistema construido. Conviene decidir si el trabajo se presenta como diseño (y el código es un prototipo de validación) o como implementación (y entonces el Capítulo IV debe reescribirse para describir lo que realmente se construyó).

4. **Nivel de agregación.** El Cap. 3.1.1 fija producto–sucursal–día como unidad de análisis. El sistema opera sobre el total diario de la empresa. O se baja el motor a la unidad declarada, o se ajusta la unidad de análisis en la tesis con su justificación.

---

## 14. Trazabilidad de los objetivos específicos (Cap. 1.5.2)

| # | Objetivo | Estado |
|---|---|---|
| 1 | Levantar y documentar el proceso actual de registro y planificación | **Sin evidencia** — trabajo de campo pendiente (Cap. 3.3 sin instrumentos en el repositorio) |
| 2 | Proceso reproducible de integración, validación, limpieza y agregación con trazabilidad por carga | **No cumplido** — no existe ingesta ni `data_loads` |
| 3 | Comparar modelos de referencia e IA con validación de origen móvil | **No cumplido** — un solo candidato, un solo baseline, un solo corte |
| 4 | Arquitectura web modular para consultar pronósticos, métricas, intervalos, explicaciones y alertas | **Parcial** — faltan métricas expuestas, explicaciones e intervalos reales |
| 5 | Prototipo de baja fidelidad y backlog inicial | **Cumplido** en la tesis (Figuras 4-6, Tabla 6) |
| 6 | Criterios de aceptación para publicar un modelo solo si supera la línea base | **No cumplido** — entrenar y publicar son el mismo acto |

Los instrumentos del Capítulo 3.3 (guía de entrevista, cuestionario de usabilidad Likert, ficha de observación, diccionario de datos, ficha de perfilamiento) no tienen ningún artefacto en el repositorio. Es esperable si el trabajo de campo aún no se ejecuta, pero conviene dejarlo explícito porque los objetivos 1 y 2 dependen de ellos.

---

## 15. Lo que sí está bien

Vale la pena registrarlo, porque es defendible tal cual:

- **Control de fuga temporal correctamente resuelto** (`forecasting.py:66-69`): los rezagos usan `.shift(lag)` y las medias móviles `.shift(1).rolling(...)`, excluyendo el instante *t*. La alineación train/serve de lags y ventanas es consistente.
- **Separación cabecera/detalle de venta** (`models.py:61-85`) implementada exactamente como la exige la tesis, con cascade.
- **RBAC verificado en el servidor** en todos los endpoints sensibles (`deps.py:47-53` + `require_role` en predictions, users, products e inventory). El ocultamiento por rol en el cliente es cosmético, pero **no hay escalada de privilegios real**.
- **Hash de contraseñas con bcrypt** (`security.py:9`), conforme a RNF-03.
- **WAPE correctamente implementado** (`forecasting.py:72-76`).
- **El gráfico distingue histórico de pronóstico por color y por trazo** (`predicciones.js:44-45`), no solo por color — cumple WCAG 1.4.1 sin que nadie lo pidiera.
- **Portabilidad SQLite → MySQL sin tocar código**, solo `DATABASE_URL`, con documentación de despliegue real (`deploy/DEPLOY.md`).
- **El módulo de lead time de China** responde a una necesidad real del negocio que la tesis identifica pero no desarrolla. Es una contribución genuina; solo necesita respaldo documental y usar el modelo predictivo de verdad.

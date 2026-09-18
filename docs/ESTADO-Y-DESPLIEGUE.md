# Estado del proyecto y guía de despliegue

> **Para quién es esto:** el equipo de tesis y sus asistentes de IA. El objetivo es
> que puedan trabajar sin leerse todo el proyecto. Si vas a tocar código, lee al
> menos las secciones **Decisiones que no hay que deshacer** y **Trampas conocidas**.

**Última actualización:** 1 de septiembre de 2026
**Rama principal:** `main` (a partir del merge del PR #2)
**Producción:** https://prediccionzrb.duckdns.org — funcionando

---

## 1. Qué es este proyecto

Sistema predictivo de ventas para Zorros Revolution Biker (trabajo de graduación, UMG).
Backend **FastAPI**, frontend **HTML/CSS/JS sin framework**, base de datos
**PostgreSQL** en producción (SQLite en local), y un motor de ML con **scikit-learn**
que pronostica ventas y sugiere reabastecimiento considerando el lead time de China.

El documento de la tesis es `docs/Trabajo de Graduacion.pdf` (no versionado; cada
quien tiene su copia).

---

## 2. Estado actual de un vistazo

| Área | Estado |
|---|---|
| Aplicación en producción | Funcionando en https://prediccionzrb.duckdns.org con HTTPS |
| Contenerización (RNF-12) | Hecha: Docker Compose + PostgreSQL |
| Bugs críticos de UI y seguridad | Corregidos (PR #1) |
| Motor de IA vs. lo que promete la tesis | **Muy incompleto** — ver `docs/ANALISIS-ALINEACION-TESIS.md` |
| Datos reales de la empresa | **No hay.** Todo corre con datos sintéticos |
| Pruebas automatizadas | **Cero** |

**Lo más importante que hay que entender:** el sistema funciona, pero **el motor
predictivo todavía no cumple lo que la tesis documenta**. Hay un análisis completo
en [`ANALISIS-ALINEACION-TESIS.md`](ANALISIS-ALINEACION-TESIS.md) con el detalle
requisito por requisito. No lo repito aquí.

---

## 3. Qué se hizo (los dos PRs ya mezclados)

### PR #1 — `fix: cuatro defectos criticos` (`648163a`)

| Defecto | Dónde estaba | Qué pasaba |
|---|---|---|
| **Modales siempre visibles** | `frontend/css/styles.css` | `.modal-overlay { display: flex }` vencía al `[hidden]` del navegador. El formulario "Nuevo producto" (solo admin) quedaba a la vista de cualquier rol |
| **XSS con robo de sesión** | los 5 `frontend/js/*.js` | Se interpolaban datos del servidor en `innerHTML` sin escapar. Con el JWT en `localStorage`, un nombre de producto con `<img onerror>` robaba la sesión |
| **Evento no detectado durante el evento** | `backend/app/ml/calendar_features.py` | El 15 de diciembre, `dias_hasta_diciembre` devolvía 351 en vez de 0, así que el refuerzo de reabastecimiento **nunca se aplicaba en temporada alta** |
| **DoS por horizonte sin validar** | `backend/app/routers/predictions_router.py` | `?horizonte=500000` bloqueaba el worker |

Se agregó `escapeHtml()` en `frontend/js/api.js` — **úsenla siempre** que metan datos
del servidor en `innerHTML`.

### PR #2 — `feat: contenerizacion` (`f248693` + `cf272e7`)

- `Dockerfile` multi-etapa (`python:3.12-slim`), usuario no-root, healthcheck.
- `docker-compose.yml` con dos servicios: `api` + `db` (PostgreSQL 16).
- **Cambio de MySQL a PostgreSQL**, que es lo que la tesis especifica en su Tabla 10.
  Salió casi gratis porque SQLAlchemy abstrae el dialecto: solo se agregó `psycopg`.
- `deploy/nginx.prediccionzrb.conf.example` y `deploy/DEPLOY-DOCKER.md`.
- `backend/app/init_db.py`: crea el esquema **antes** de arrancar los workers (ver
  Trampa 1 más abajo).

---

## 4. Cómo correrlo en local

### Opción A — con Docker (recomendada: igual que producción)

```bash
cp .env.example .env
# Rellenar POSTGRES_PASSWORD y SECRET_KEY. Genera valores con:
#   openssl rand -hex 24
#   openssl rand -hex 32

docker compose up -d --build
docker compose exec api python -m app.seed_data   # datos de demostración
```

Abre http://localhost:8020 · Admin: `admin@zorrosrevolution.com`

La contraseña la **genera `seed_data` al azar y la imprime una sola vez**: anótala de la
salida del comando. Si la pierdes, `python -m app.manage_users password <correo> --generar`
la restablece.

Compose **se niega a levantar** si `SECRET_KEY` o `POSTGRES_PASSWORD` están vacíos.
Es a propósito, para que la clave por defecto del código no llegue a producción.

### Opción B — sin Docker (SQLite, más rápido para iterar en el backend)

```bash
cd backend
python -m venv venv
venv\Scripts\Activate.ps1        # Windows;  source venv/bin/activate en Linux/Mac
pip install -r requirements.txt
cp .env.example .env             # este es backend/.env.example, apunta a SQLite
python -m app.seed_data
uvicorn app.main:app --reload
```

Abre http://127.0.0.1:8000 · Documentación de la API en `/docs`.

> **Ojo con los dos `.env`:** el de la **raíz** es para Docker Compose (PostgreSQL);
> el de **`backend/`** es para correr sin Docker (SQLite). Son distintos y ninguno
> se sube a git.

Para entrenar el modelo por primera vez: **Predicciones → Recalibrar Modelo** (solo
admin). Sin eso el dashboard muestra la proyección vacía.

---

## 5. Cómo desplegar

Guía completa en [`../deploy/DEPLOY-DOCKER.md`](../deploy/DEPLOY-DOCKER.md). Resumen:

### Actualizar producción (el caso normal)

```bash
ssh zorros
cd /var/www/zorros-prediccion
git pull
docker compose up -d --build
curl -fsS http://127.0.0.1:8020/api/health
```

Eso es todo. Los datos y el modelo entrenado sobreviven porque viven en volúmenes.

### Flujo de trabajo del equipo

Nunca commitear directo a `main`. Siempre: **rama → PR → merge → pull en el servidor
→ `docker compose up -d --build`**. Un PR = un cambio lógico (no mezclar bugs con
features).

---

## 6. Cómo está montada la producción

```
Internet
   │
   ▼
Nginx del HOST  (puertos 80/443, sirve además otros 4 proyectos)
   │  sitio: /etc/nginx/sites-available/prediccionzrb.duckdns.org
   ▼
127.0.0.1:8020
   │
   ▼
┌─────────────────── docker compose ───────────────────┐
│  api  (FastAPI + Gunicorn, 2 workers, usuario zorros)│
│    └── volumen model_artifacts → el .joblib entrenado│
│  db   (PostgreSQL 16)                                │
│    └── volumen pgdata → la base de datos             │
└──────────────────────────────────────────────────────┘
```

| Dato | Valor |
|---|---|
| Acceso al servidor | `ssh zorros` |
| Ruta del proyecto | `/var/www/zorros-prediccion` |
| Puerto de la API | **8020** (el 8000 lo usa otro proyecto) |
| Dominio | https://prediccionzrb.duckdns.org (DuckDNS → 31.97.139.50) |
| Certificado | Let's Encrypt, renovación automática ya configurada |
| Consumo real | API ~355 MB · Postgres ~47 MB |

### El VPS es COMPARTIDO — esto es lo más importante de esta sección

En la misma máquina corren **cuatro proyectos ajenos en producción**: `clubiker`,
`descomplica2`, `kekitos-gym`, `zorrosrevolutionbikergt` y `sistema-preventivo-agricultura`.

**Reglas:**

1. En Nginx solo se **agregan** archivos propios. Nunca editar los de otros ni `nginx.conf`.
2. **`sudo nginx -t` siempre antes de `reload`.** Un error de sintaxis tumba también los otros dominios.
3. No usar el puerto 8000 (ocupado) ni declarar `default_server`.
4. No reiniciar Docker, Nginx ni MariaDB globalmente.
5. El servidor tiene **1 solo núcleo** y la memoria es compartida. No subir `GUNICORN_WORKERS` sin medir.

---

## 7. Decisiones que no hay que deshacer

Están así por una razón concreta. Si alguien "optimiza" alguna, rompe algo:

| Decisión | Dónde | Por qué |
|---|---|---|
| `GUNICORN_WORKERS=2` fijo | `backend/gunicorn_conf.py` | La fórmula clásica `cpu_count()*2+1` daba 3 workers. Cada uno carga pandas + scikit-learn (~250-350 MB) y el VPS tiene 1 núcleo con memoria compartida: riesgo de OOM sin ganar rendimiento |
| `timeout = 300` en Gunicorn | `backend/gunicorn_conf.py` | El reentrenamiento corre **dentro del request**. Con los 60 s originales el worker moría a media faena |
| `ARTIFACTS_DIR` en un volumen | `config.py` + `docker-compose.yml` | Si el `.joblib` vive dentro de la imagen, **cada `up --build` borra el modelo entrenado** y la app cae al fallback heurístico sin avisar en la interfaz |
| `init_db.py` antes de Gunicorn | `Dockerfile` (CMD) | Ver Trampa 1 |
| Nginx **fuera** del compose | `docker-compose.yml` | El host ya tiene uno sirviendo otros 4 dominios en 80/443. Meterlo al stack los tumba |
| Sin `default_server` en el sitio | `deploy/nginx.prediccionzrb.conf.example` | Capturaría el tráfico de los otros dominios |
| Secretos sin valor por defecto | `docker-compose.yml` | Para que la `SECRET_KEY` de ejemplo del código no llegue nunca a producción |

---

## 8. Trampas conocidas

### Trampa 1 — El esquema debe crearse en un solo proceso

`Base.metadata.create_all()` corre al importar `main.py`. Con varios workers, todos
intentan crear el esquema a la vez y sobre PostgreSQL uno muere:

```
UniqueViolation: duplicate key ... "pg_type_typname_nsp_index"
DETAIL:  Key (typname, typnamespace)=(rolusuario, 2200) already exists.
```

Solo pasa con **PostgreSQL + varios workers + base vacía** a la vez, o sea el primer
despliegue. Por eso el `CMD` del Dockerfile ejecuta `python -m app.init_db` antes de
Gunicorn. **No quitar ese paso.**

### Trampa 2 — No hay migraciones

El esquema se crea con `create_all()`, que **no modifica tablas existentes**. Si
cambian un modelo en `models.py`, la columna nueva no aparece sola en producción.
Hoy hay que hacerlo a mano; la solución de fondo es incorporar Alembic.

### Trampa 3 — Las cuentas creadas antes de septiembre siguen con la clave vieja

Desde ahora `seed_data` genera contraseñas aleatorias, pero **el seed no toca usuarios
que ya existen**. Cualquier instancia sembrada antes conserva la contraseña original que
estaba publicada en el repositorio. En esos casos hay que restablecerla:

```bash
docker compose exec api python -m app.manage_users password admin@zorrosrevolution.com --generar
```

Después, la gestión normal se hace desde **Usuarios** en la interfaz.

### Trampa 4 — El fallback heurístico es invisible

Si no hay modelo entrenado, `forecasting.py` devuelve predicciones calculadas con
factores fijos (1.35 / 1.25 / 1.2) y **la interfaz las muestra igual que las del
modelo**. Si ven números raros, verifiquen primero que el modelo esté entrenado.

### Trampa 5 — "Confianza del modelo" no es una métrica real

Es `100 - WAPE`, que no es una probabilidad ni un nivel de confianza estadístico.
Está documentado como defecto pendiente. No lo citen como resultado en la tesis.

---

## 9. Qué falta (resumen)

El detalle completo, con evidencia archivo:línea, está en
[`ANALISIS-ALINEACION-TESIS.md`](ANALISIS-ALINEACION-TESIS.md). Lo esencial:

**Bloqueante para la tesis**
1. **Datos reales de la empresa.** No hubo acceso al histórico, así que todo corre
   con ventas simuladas por `simular_ventas.py`. El simulador **no comparte ninguna
   función con las features del modelo** (hay una prueba que lo verifica), de modo que
   la evaluación ya no es circular — pero sigue siendo una simulación. Con datos
   simulados no circulares el modelo pasa el criterio con **22 % de mejora** sobre el
   naïve estacional (antes, con el generador circular, marcaba un 35 % engañoso).

   ```bash
   docker compose exec api python -m app.simular_ventas --meses 12 --confirmar
   ```

   Con 12 meses cada evento anual aparece **una sola vez**: el primer Bono 14 que el
   modelo ve cae en la ventana de evaluación, no en la de entrenamiento, y por eso
   subestima ese pico. Es una limitación real que hay que declarar en la tesis.
2. **El motor pronostica el total diario de la empresa en quetzales**, no unidades por
   producto. `sale_items` ya tiene los datos por SKU y el pipeline los descarta.
3. **No hay líneas base** (ARIMA, Prophet, suavizamiento) ni validación de origen móvil.
4. **Entrenar y publicar son el mismo acto**, sin criterio de aceptación ni rollback.
5. **No existe la entidad `stores`**, así que "pronóstico por sucursal" es imposible hoy.

**Deuda técnica**
- Cero pruebas automatizadas, cero CI.
- `audit_log` y `forecasts` están definidas en `models.py` y **nunca se escriben**.
- Sin importador CSV/XLSX (RF-03), que es por donde entrarán los datos de la empresa.
- Accesibilidad WCAG 2.2 AA incumplida (RNF-06).
- Sin respaldo automatizado (RNF-09).

---

## 10. Comandos de referencia

```bash
# --- Local ---
docker compose up -d --build                      # levantar
docker compose logs -f api                        # ver logs
docker compose exec api python -m app.seed_data   # sembrar datos
docker compose down                               # bajar (conserva datos)
docker compose down -v                            # bajar Y BORRAR datos y modelo

# --- Producción ---
ssh zorros
cd /var/www/zorros-prediccion
git pull && docker compose up -d --build          # desplegar
docker compose ps                                 # estado
docker compose logs api --since 10m               # logs recientes
curl -fsS http://127.0.0.1:8020/api/health        # salud

# Respaldo de la base (aún no automatizado)
docker compose exec -T db pg_dump -U zorros zorros | gzip > backup-$(date +%F).sql.gz

# --- Nginx (con cuidado: VPS compartido) ---
sudo nginx -t                                     # SIEMPRE antes de recargar
sudo systemctl reload nginx
```

---

## 11. Mapa de archivos

```
backend/app/
  main.py                 Arranque de FastAPI, CORS, monta el frontend estático
  config.py               Variables de entorno (settings)
  init_db.py              Crea el esquema una sola vez (ver Trampa 1)
  models.py               Tablas SQLAlchemy
  schemas.py              Modelos Pydantic (contratos de la API)
  security.py             Hash de contraseñas y JWT
  deps.py                 Sesión de BD y control de roles (require_role)
  seed_data.py            Usuarios demo + catálogo; delega las ventas al simulador
  simular_ventas.py       Simulador de ventas (calendario real, Poisson, quiebres de stock)
  routers/                Un archivo por área de la API
  ml/
    forecasting.py        Motor de pronóstico (entrena, predice, señales)
    calendar_features.py  Estacionalidad de Guatemala
    reorder.py            Recomendaciones de reabastecimiento

frontend/
  *.html                  Una página por módulo
  js/api.js               fetch + sesión + escapeHtml()  <- cargar siempre primero
  js/*.js                 Un archivo por página

Dockerfile · docker-compose.yml · .env.example      Contenerización
deploy/DEPLOY-DOCKER.md                             Guía de despliegue
docs/ANALISIS-ALINEACION-TESIS.md                   Auditoría vs. la tesis
```

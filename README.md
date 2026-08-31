# Zorros Revolution Biker — Sistema Predictivo de Ventas e Inventario

Aplicación web funcional (no solo mockup) basada en el prototipo Stitch y la tesis del equipo:
backend en **Python (FastAPI)**, frontend en **HTML/CSS/JavaScript** puro, base de datos vía
**SQLAlchemy** (SQLite en desarrollo, **MySQL en producción/Hostinger**), y un motor de
**Machine Learning (scikit-learn)** que:

1. **Predice ventas futuras** (7 / 30 / 90 / 180 días) considerando la estacionalidad propia de
   Guatemala: diciembre (aguinaldo), Bono 14 (julio) y la Caravana del Zorro (febrero).
2. **Recomienda cuándo y cuánto reabastecer** cada producto, tomando en cuenta que los
   accesorios se importan de China y por tanto tienen un tiempo de envío (lead time) que debe
   cubrirse con anticipación para evitar quedarse sin stock.

Incluye dos roles: **cajero** (registra ventas y recibe stock) y **administrador** (acceso total:
productos, predicciones, recalibrar modelo, usuarios).

## Estructura del proyecto

```
PRO_SE/
  backend/     API FastAPI, modelos de datos, lógica de ML
  frontend/    HTML/CSS/JS servidos por el propio backend
  db/          schema.sql (alternativa manual para crear las tablas en MySQL)
  deploy/      Archivos para desplegar en un VPS de Hostinger (Gunicorn + Nginx + systemd)
```

## Cómo correrlo en local (sin instalar MySQL)

Requiere **Python 3.11+** instalado (verifica con `python --version`; en Windows, si no está
instalado, descárgalo desde python.org o `winget install Python.Python.3.12`).

```bash
cd backend
python -m venv venv

# Windows (PowerShell):
venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate

pip install -r requirements.txt
copy .env.example .env      # Windows; en macOS/Linux: cp .env.example .env

python -m app.seed_data     # genera usuarios demo + catálogo + ~24 meses de ventas sintéticas
uvicorn app.main:app --reload
```

Abre `http://127.0.0.1:8000` en el navegador. Inicia sesión con:

- **Administrador**: `admin@zorrosrevolution.com` / `Admin123!`
- **Cajero**: `cajero@zorrosrevolution.com` / `Cajero123!`

La documentación interactiva de la API está en `http://127.0.0.1:8000/docs`.

Desde el módulo **Predicciones → Recalibrar Modelo** (solo admin) se entrena el modelo de
pronóstico por primera vez usando el histórico sembrado; después de eso el Dashboard mostrará
la proyección del próximo mes y el nivel de confianza real del modelo.

## Migrar a MySQL (Hostinger)

1. Crea una base de datos MySQL en hPanel (Hostinger) y anota host, usuario, contraseña y nombre
   de la base.
2. En `backend/.env`, cambia:
   ```
   DATABASE_URL=mysql+pymysql://usuario_mysql:password_mysql@localhost/nombre_basedatos
   ```
3. Vuelve a correr la app (`uvicorn app.main:app`): SQLAlchemy crea las tablas automáticamente en
   MySQL la primera vez. Si prefieres crearlas manualmente, importa `db/schema.sql` desde
   phpMyAdmin.
4. Corre `python -m app.seed_data` de nuevo si quieres los datos de demostración también en MySQL
   (o sáltalo si vas a cargar ventas reales).

No se necesita cambiar ningún archivo de código para pasar de SQLite a MySQL — solo la variable
`DATABASE_URL`.

## Desplegar en un VPS de Hostinger (producción)

Sigue la guía detallada en [`deploy/DEPLOY.md`](deploy/DEPLOY.md): clonar el repositorio, crear el
entorno virtual, configurar `.env` con las credenciales reales de MySQL, levantar el servicio con
Gunicorn + systemd, y exponerlo con Nginx + HTTPS (Let's Encrypt).

## Reglas de negocio implementadas

- **Roles**: `cajero` solo puede registrar ventas y recibir stock; `admin` tiene acceso completo
  (productos, predicciones, recalibrar modelo, usuarios).
- **Estacionalidad Guatemala**: el modelo de predicción y las recomendaciones de reabastecimiento
  incorporan diciembre, la primera quincena de julio (Bono 14) y la segunda quincena de febrero
  (Caravana del Zorro) como picos de demanda.
- **Reabastecimiento con lead time de China**: cada producto tiene un `lead_time_dias_china`
  configurable (60 días por defecto). El sistema calcula el punto de reorden como la demanda
  pronosticada durante ese periodo + margen de seguridad, y alerta con anticipación cuando un
  evento de alta demanda cae dentro de la ventana de envío.

## Próximos pasos sugeridos

- Reemplazar los datos sintéticos por un histórico de ventas real (vía un importador CSV, si se
  agrega más adelante) y volver a entrenar el modelo.
- Ajustar `lead_time_dias_china` por producto según los tiempos reales de cada proveedor.
- Revisar y ajustar las ventanas de "Caravana del Zorro" en
  `backend/app/ml/calendar_features.py` si la fecha real del evento cambia cada año.
- Cambiar las contraseñas de los usuarios de demostración antes de operar con datos reales.

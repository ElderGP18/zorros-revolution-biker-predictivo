# Despliegue en Hostinger (VPS)

Guía paso a paso para llevar el sistema (backend FastAPI + frontend estático + MySQL) a un VPS de Hostinger.

## 0. Requisitos previos

- Un VPS de Hostinger activo (Ubuntu 22.04 recomendado) con acceso SSH.
- Una base de datos MySQL creada desde hPanel (o `mysql` por consola), con usuario y contraseña dedicados.
- Un dominio o subdominio apuntando a la IP del VPS (registro A en el DNS).

## 1. Preparar el servidor

```bash
ssh root@TU_IP_VPS

apt update && apt upgrade -y
apt install -y python3-venv python3-pip nginx git

# Usuario dedicado para correr la app (no usar root)
adduser deploy
usermod -aG sudo deploy
su - deploy
```

## 2. Clonar el proyecto y crear el entorno virtual

```bash
git clone <URL_DE_TU_REPOSITORIO> PRO_SE
cd PRO_SE/backend

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configurar variables de entorno

```bash
cp .env.example .env
nano .env
```

Ajusta como mínimo:

```
DATABASE_URL=mysql+pymysql://usuario_mysql:password_mysql@localhost/nombre_basedatos
SECRET_KEY=<genera una cadena aleatoria larga, ej: openssl rand -hex 32>
CORS_ORIGINS=https://tudominio.com
```

## 4. Crear las tablas y sembrar datos de demostración

SQLAlchemy crea las tablas automáticamente al iniciar la app (`Base.metadata.create_all`), pero también puedes
crearlas manualmente importando `db/schema.sql` desde phpMyAdmin si lo prefieres.

Para poblar datos de demostración (usuarios y catálogo — recomendado para la primera puesta en marcha):

```bash
python -m app.seed_data
```

Esto imprime las credenciales del usuario `admin` y `cajero` de prueba. **Cámbialas o elimínalas antes de usar datos reales.**

## 5. Probar manualmente antes de exponerlo

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
# Verifica en otra terminal: curl http://127.0.0.1:8000/api/health
```

Si responde `{"status": "ok", ...}`, detén el proceso (Ctrl+C) y continúa.

## 6. Configurar Gunicorn como servicio systemd

```bash
exit  # vuelve a root o usa sudo
cp /home/deploy/PRO_SE/deploy/zorros-api.service /etc/systemd/system/zorros-api.service
```

Revisa que las rutas dentro de `zorros-api.service` coincidan con tu instalación real (usuario, `WorkingDirectory`, `venv`).

```bash
systemctl daemon-reload
systemctl enable zorros-api
systemctl start zorros-api
systemctl status zorros-api
```

## 7. Configurar Nginx como proxy reverso

```bash
cp /home/deploy/PRO_SE/deploy/nginx.zorros.conf.example /etc/nginx/sites-available/zorros
nano /etc/nginx/sites-available/zorros   # ajusta server_name a tu dominio real

ln -s /etc/nginx/sites-available/zorros /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

## 8. HTTPS con Let's Encrypt

```bash
apt install -y certbot python3-certbot-nginx
certbot --nginx -d tudominio.com -d www.tudominio.com
```

## 9. Verificación final

- Abre `https://tudominio.com` en el navegador → debe cargar la pantalla de login.
- Inicia sesión con el usuario admin sembrado y confirma que el Dashboard, Ventas, Productos y Predicciones cargan datos.
- Desde **Predicciones → Recalibrar Modelo**, entrena el modelo por primera vez con el histórico real una vez que
  hayan cargado datos de ventas verdaderos (o sigue usando los sintéticos mientras validan el prototipo).

## 10. Actualizaciones futuras

```bash
su - deploy
cd PRO_SE
git pull
cd backend
source venv/bin/activate
pip install -r requirements.txt   # solo si cambiaron dependencias
exit
sudo systemctl restart zorros-api
```

## Notas de seguridad

- Nunca subas el archivo `.env` real a git (ya está en `.gitignore`).
- Cambia `SECRET_KEY` por un valor aleatorio propio en producción.
- Restringe `CORS_ORIGINS` a tu dominio real (no dejes `*` en producción).
- Cambia las contraseñas de los usuarios de demostración (`admin@zorrosrevolution.com`, `cajero@zorrosrevolution.com`)
  o elimínalos antes de operar con datos reales.

# Despliegue con Docker Compose (recomendado)

Ruta de despliegue oficial del proyecto. Cumple el RNF-12 de la tesis
("despliegue reproducible en contenedores") y sigue el patrón que el VPS ya usa
para otros proyectos.

> La guía manual con `venv` + systemd sigue en [`DEPLOY.md`](DEPLOY.md) como
> alternativa, pero no es la vía recomendada.

## Contexto del servidor

El VPS **está compartido con otros proyectos en producción** (`clubiker`,
`descomplica2`, `kekitos-gym`, `zorrosrevolutionbikergt`, `sistema-preventivo-agricultura`).
De ahí tres decisiones:

- **Nginx no va en el stack.** El host ya tiene uno sirviendo esos dominios en los
  puertos 80/443. Este stack solo publica la API en `127.0.0.1:8020` y el Nginx
  del host hace de proxy.
- **El puerto 8000 está ocupado** por `sistema-preventivo-agricultura`. Usamos el **8020**.
- **1 núcleo y memoria ajustada.** `GUNICORN_WORKERS=2` y límites de memoria en
  `docker-compose.yml`. No subirlos sin medir.

**Regla:** en Nginx solo se **agregan** archivos propios. Nunca editar los de
otros proyectos ni `nginx.conf`.

## 1. Clonar

```bash
ssh zorros
mkdir -p /var/www/zorros-prediccion && cd /var/www/zorros-prediccion
git clone git@github.com:ElderGP18/zorros-revolution-biker-predictivo.git .
```

## 2. Configurar el entorno

```bash
cp .env.example .env
nano .env
```

Rellenar como mínimo:

```bash
POSTGRES_PASSWORD=$(openssl rand -hex 24)
SECRET_KEY=$(openssl rand -hex 32)
CORS_ORIGINS=https://prediccionzrb.duckdns.org
```

Compose **se niega a levantar** si `SECRET_KEY` o `POSTGRES_PASSWORD` están vacíos:
es deliberado, para que no llegue a producción la clave por defecto del código.

## 3. Levantar el stack

```bash
docker compose up -d --build
docker compose ps
curl -fsS http://127.0.0.1:8020/api/health
```

Debe responder `{"status":"ok",...}`. Las tablas se crean solas al arrancar
(`Base.metadata.create_all`).

Para poblar datos de demostración (opcional, solo en la primera puesta en marcha):

```bash
docker compose exec api python -m app.seed_data
```

**Cambiar o eliminar los usuarios demo antes de operar con datos reales.**

## 4. Publicar el dominio en el Nginx del host

```bash
sudo cp deploy/nginx.prediccionzrb.conf.example \
        /etc/nginx/sites-available/prediccionzrb.duckdns.org
sudo ln -s /etc/nginx/sites-available/prediccionzrb.duckdns.org /etc/nginx/sites-enabled/

sudo nginx -t          # OBLIGATORIO: hay otros sitios en producción
sudo systemctl reload nginx
```

`nginx -t` no es opcional. Un error de sintaxis en el reload tumba también a los
demás dominios del servidor.

## 5. HTTPS

```bash
sudo certbot --nginx -d prediccionzrb.duckdns.org
```

Certbot necesita que el reto HTTP-01 funcione en el puerto 80, así que el paso 4
debe estar verificado antes.

## 6. Actualizaciones

```bash
cd /var/www/zorros-prediccion
git pull
docker compose up -d --build
```

## Volúmenes: qué se persiste y qué no

| Volumen | Contiene | Si se pierde |
|---|---|---|
| `pgdata` | Base de datos PostgreSQL | Se pierden ventas, catálogo y usuarios |
| `model_artifacts` | `sales_model.joblib` | La app cae al fallback heurístico **sin avisar en la interfaz** |

El segundo es el que más fácil se pasa por alto: el modelo entrenado vive **fuera**
de la imagen (`ARTIFACTS_DIR=/var/lib/zorros/artifacts`) precisamente para que
`up --build` no lo borre.

Respaldo de la base (RNF-09, aún sin automatizar):

```bash
docker compose exec -T db pg_dump -U zorros zorros | gzip > backup-$(date +%F).sql.gz
```

## Limitaciones conocidas

- **El entrenamiento corre dentro del request HTTP.** Por eso el timeout de
  Gunicorn está en 300 s y el `proxy_read_timeout` de Nginx también. Con un
  histórico real y un solo núcleo puede quedarse corto: la solución de fondo es
  sacarlo a una tarea asíncrona.
- **Sin migraciones.** El esquema se crea con `create_all()`, que no aplica
  cambios sobre tablas ya existentes. Cualquier cambio de modelo requerirá una
  migración manual mientras no se incorpore Alembic.

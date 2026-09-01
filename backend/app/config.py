from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación, leída desde variables de entorno / .env.

    En desarrollo local DATABASE_URL apunta a SQLite (no requiere instalar MySQL).
    En producción (Hostinger) se cambia a una cadena mysql+pymysql://... sin tocar código.
    """

    APP_NAME: str = "Zorros Revolution Biker - Sistema Predictivo"

    DATABASE_URL: str = "sqlite:///./zorros.db"

    SECRET_KEY: str = "cambia-esta-clave-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 12

    # Carpeta donde se persisten los artefactos del modelo (.joblib). Debe apuntar a
    # un volumen fuera de la imagen: si queda dentro del contenedor, cada redespliegue
    # borra el modelo entrenado y la app cae al fallback heurístico sin avisar.
    # Vacío = usar la ruta por defecto junto al código (comportamiento en local).
    ARTIFACTS_DIR: str = ""

    # Días promedio de envío desde China usados como default cuando un producto
    # no tiene su propio lead_time_dias_china configurado.
    LEAD_TIME_DEFAULT_DIAS: int = 60
    DIAS_SEGURIDAD_STOCK: int = 10

    CORS_ORIGINS: str = "*"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()

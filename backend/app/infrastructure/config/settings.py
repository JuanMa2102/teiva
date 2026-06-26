import logging
import os
import secrets
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_jwt_secret_fallback() -> str:
    """Implementa resolución multinivel de secretos según las directrices de seguridad."""
    # 1. Intentar leer desde variable de entorno directamente (ya lo hace BaseSettings)
    env_secret = os.getenv("JWT_SECRET_KEY")
    if env_secret:
        return env_secret

    # 2. Intentar buscar en archivo de secretos local (útil para contenedores/Kubernetes)
    secret_path = "/run/secrets/jwt_secret"
    if os.path.exists(secret_path):
        try:
            with open(secret_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            pass

    # 3. Generación efímera segura con advertencia de escalabilidad horizontal
    logging.warning(
        "MANDATORY SECURITY WARNING: JWT_SECRET_KEY no está configurado en el entorno ni en archivos. "
        "Generando secreto efímero aleatorio. ¡Esta instancia no escalará horizontalmente de forma segura!"
    )
    return secrets.token_hex(32)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Entorno
    ENV: str = "development"
    
    # Configuración de base de datos / Supabase
    # TODO(security): Nunca harcodear URL ni llaves. Se obtendrán del entorno.
    SUPABASE_URL: str = "https://your-supabase-project.supabase.co"
    SUPABASE_KEY: str = "your-supabase-anon-key"
    
    # Configuración de Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Configuración de seguridad JWT
    JWT_SECRET_KEY: str = get_jwt_secret_fallback()
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # CORS (Separados por coma en el entorno)
    # Por defecto en desarrollo local permitimos localhost
    # TODO(security): En producción especificar exactamente los dominios cliente.
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://teiva.co"
    ]


# Instancia única de configuraciones
settings = Settings()

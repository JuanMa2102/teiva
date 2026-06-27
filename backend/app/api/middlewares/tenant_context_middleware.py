"""
Middleware con validación JWT y extracción de tenant_id y user_id para usar en toda la aplicación
"""
from contextvars import ContextVar
from typing import Optional
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt

# Declaración de variables de contexto globales y seguras para hilos asíncronos
tenant_id_var: ContextVar[Optional[str]] = ContextVar('tenant_id', default=None)
user_id_var: ContextVar[Optional[str]] = ContextVar('user_id', default=None)

class TenantContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware que intercepta las peticiones entrantes,
    extrae de forma segura el tenant_id y user_id del JWT de Supabase
    y gestiona el ciclo de vida del contexto.
    """
    async def dispatch(self, request: Request, call_next):
        # 1. Bypass para rutas públicas y documentación
        # Añadimos "/" al inicio de docs y openapi.json para un match exacto
        if request.url.path in ["/docs", "/redoc", "/openapi.json", "/api/v1/auth/onboarding"]:
            return await call_next(request)

        # 2. Extracción y Validación del Header de Autorización
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return JSONResponse(
                status_code=401, 
                content={"detail": "Authorization header is missing or malformed"}
            )

        token = auth.split(" ")[1]

        try:
            # Decodificación del JWT (Fase inicial sin verificación de firma, ideal antes de configurar secrets)
            payload = jwt.decode(token, options={"verify_signature": False})
            
            # Supabase guarda el UUID del usuario en la llave 'sub'
            user_id = payload.get("sub")
            
            # Las variables personalizadas inyectadas suelen vivir en app_metadata en Supabase
            app_metadata = payload.get("app_metadata", {})
            tenant_id = app_metadata.get("tenant_id") or payload.get("tenant_id")

            if not tenant_id or not user_id:
                return JSONResponse(
                    status_code=401, 
                    content={"detail": "Missing tenant_id or user_id inside JWT claims"}
                )

            # 3. Establecer Contexto Asíncrono
            # Almacenamos los tokens generados por el .set() para poder limpiarlos después
            tenant_token = tenant_id_var.set(tenant_id)
            user_token = user_id_var.set(user_id)

            # 4. Continuar con la ejecución de la petición hacia los endpoints
            response = await call_next(request)
            return response

        except jwt.DecodeError:
            return JSONResponse(
                status_code=401, 
                content={"detail": "Invalid or corrupted token encryption"}
            )
        finally:
            # 5. Limpieza Absoluta del Contexto (Evita fugas de memoria entre peticiones concurrentes)
            tenant_id_var.reset(tenant_token)
            user_id_var.reset(user_token)
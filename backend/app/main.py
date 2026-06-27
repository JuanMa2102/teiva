"""
Entry Point para la Ejecución del Backend.
Configura la aplicación FastAPI, establece la conexión inicial con la base de datos
y registra todas las rutas de la API.
"""

from fastapi import FastAPI
from app.api.middlewares.tenant_context_middleware import TenantContextMiddleware
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.crm import router as crm_router

app = FastAPI(
    title="Teiva API",
    description="CRM Inteligente para Agentes de Seguros - Backend API",
    version="1.0.0"
)

app.add_middleware(TenantContextMiddleware)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(crm_router, prefix="/api/v1")

@app.get("/")
async def root():
    """
    Endpoint raíz para verificar el estado de la API
    """
    return {
        "status": "healthy",
        "project": "Teiva API"
    }

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.v1.api_router import api_router
from app.domain.exceptions import DomainException, EntityNotFoundException
from app.infrastructure.config import settings

# Inicialización de la aplicación FastAPI con metadatos descriptivos
app = FastAPI(
    title="Teiva API",
    description="CRM Inteligente para Agentes de Seguros - Backend API",
    version="1.0.0"
)

# Configuración de CORS
# TODO(security): En producción, asegurarse de no permitir orígenes comodín (*).
# settings.BACKEND_CORS_ORIGINS maneja una lista explícita de dominios confiables.
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
    )


# --- MANEJADORES DE EXCEPCIONES GLOBALES (SEGURIDAD) ---

@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    """
    Controla excepciones de la capa de negocio.
    Retorna un mensaje limpio sin trazas internas del sistema.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message}
    )


@app.exception_handler(EntityNotFoundException)
async def entity_not_found_handler(request: Request, exc: EntityNotFoundException):
    """Manejador especializado para recursos no encontrados."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message}
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    TODO(security): Manejador global contra fugas de información.
    Captura cualquier error inesperado y retorna un error genérico (Internal Server Error)
    al cliente para evitar exponer bases de datos, código o trazas internas.
    El error original debe ser guardado en logs protegidos en el backend.
    """
    # En desarrollo podríamos querer imprimir la traza para depuración rápida.
    if settings.ENV == "development":
        import traceback
        traceback.print_exc()
        
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Ha ocurrido un error interno del servidor. Por favor, intente más tarde."}
    )


# --- REGISTRO DE ENRUTADORES ---

app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["Salud"], status_code=status.HTTP_200_OK)
async def health_check():
    """Endpoint simple para validaciones de salud y monitoreo del servicio."""
    return {
        "status": "healthy",
        "env": settings.ENV,
        "version": app.version
    }


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Bienvenido a Teiva API",
        "docs": "/docs"
    }

from fastapi import APIRouter
from app.api.v1.endpoints import auth, clients

api_router = APIRouter()

# Registro de enrutadores secundarios con sus respectivos prefijos y tags de documentación
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(clients.router, prefix="/clients", tags=["Clientes"])

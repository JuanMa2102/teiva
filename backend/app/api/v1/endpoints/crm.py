"""
Endpoint de crm clients
"""
from fastapi import APIRouter, Depends, HTTPException, status
from supabase._async.client import AsyncClient

from app.application.use_cases.crm.create_client_use_case import CreateClientUseCase, CreateClientRequest
from app.infrastructure.adapters.database.supabase_client_repository import SupabaseClientRepository

router = APIRouter(prefix="/crm/clients", tags=["Clientes"])

# Dependencia para obtener el cliente de Supabase (compartida en la arquitectura)
async def get_supabase_client() -> AsyncClient:
    """
    Obtiene la instancia del cliente asíncrono de Supabase.
    """
    pass

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_client(
    request: CreateClientRequest,
    supabase_client: AsyncClient = Depends(get_supabase_client)
):
    """
    Ruta para crear un nuevo cliente o prospecto dentro de la organización actual.
    """
    client_repo = SupabaseClientRepository(supabase_client)
    create_client_use_case = CreateClientUseCase(client_repo)
    
    try:
        result = await create_client_use_case.execute(request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el cliente: {str(e)}"
        ) from e

@router.get("/", status_code=status.HTTP_200_OK)
async def list_clients(
    supabase_client: AsyncClient = Depends(get_supabase_client)
):
    """
    Ruta para listar todos los clientes pertenecientes al Tenant autenticado.
    El aislamiento de datos ocurre automáticamente gracias al ContextVar del middleware.
    """
    client_repo = SupabaseClientRepository(supabase_client)
    
    try:
        # Al ser una consulta directa de lectura que respeta el Scope del Tenant,
        # podemos llamar al repositorio sin pasar por un caso de uso intermedio si no hay lógica de negocio extra.
        clients = await client_repo.list()
        return {
            "success": True,
            "count": len(clients),
            "clients": clients
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la lista de clientes: {str(e)}"
        ) from e
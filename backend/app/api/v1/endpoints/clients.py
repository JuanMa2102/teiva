from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.middlewares.tenant_middleware import get_current_tenant_id
from app.application.ports.inputs.client_use_cases import CreateClientCommand
from app.application.use_cases.client.client_use_cases import ClientUseCases
from app.domain.exceptions import EntityNotFoundException
from app.domain.models.client import Client

# Para fines demostrativos y de pruebas locales, definiremos una implementación
# en memoria si no hay una conexión real de base de datos activa.
from app.application.ports.outputs.client_repository import ClientRepositoryPort


class InMemoryClientRepository(ClientRepositoryPort):
    def __init__(self):
        self._clients = {}

    async def save(self, client: Client) -> Client:
        self._clients[client.id] = client
        return client

    async def find_by_id(self, tenant_id: str, client_id: str) -> Client:
        client = self._clients.get(client_id)
        if client and client.tenant_id == tenant_id:
            return client
        return None

    async def find_all_by_tenant(self, tenant_id: str) -> List[Client]:
        return [c for c in self._clients.values() if c.tenant_id == tenant_id]


# Instancia singleton del repositorio en memoria para fines demostrativos
_in_memory_repo = InMemoryClientRepository()


def get_client_use_cases() -> ClientUseCases:
    # TODO(security): En producción, resolver mediante inyección del SupabaseClientRepository real
    return ClientUseCases(client_repository=_in_memory_repo)


router = APIRouter()


@router.post("/", response_model=Client, status_code=status.HTTP_201_CREATED)
async def create_client(
    command: CreateClientCommand,
    tenant_id: str = Depends(get_current_tenant_id),
    use_cases: ClientUseCases = Depends(get_client_use_cases)
):
    """
    Crea un nuevo cliente asociado al inquilino (tenant) extraído del token JWT.
    """
    return await use_cases.create_client(tenant_id, command)


@router.get("/{client_id}", response_model=Client, status_code=status.HTTP_200_OK)
async def get_client(
    client_id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    use_cases: ClientUseCases = Depends(get_client_use_cases)
):
    """
    Obtiene los detalles de un cliente específico, garantizando que pertenece al tenant autenticado.
    """
    try:
        return await use_cases.get_client_by_id(tenant_id, client_id)
    except EntityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/", response_model=List[Client], status_code=status.HTTP_200_OK)
async def list_clients(
    tenant_id: str = Depends(get_current_tenant_id),
    use_cases: ClientUseCases = Depends(get_client_use_cases)
):
    """
    Obtiene todos los clientes pertenecientes al tenant del token autenticado.
    """
    return await use_cases.list_clients(tenant_id)

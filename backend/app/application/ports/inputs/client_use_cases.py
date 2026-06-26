from typing import List, Optional, Protocol
from app.domain.models.client import Client
from pydantic import BaseModel, EmailStr


class CreateClientCommand(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class ClientUseCasesPort(Protocol):
    async def create_client(self, tenant_id: str, command: CreateClientCommand) -> Client:
        """Crea un nuevo cliente dentro del tenant especificado."""
        ...

    async def get_client_by_id(self, tenant_id: str, client_id: str) -> Optional[Client]:
        """Obtiene un cliente por su ID y tenant_id (garantizando aislamiento)."""
        ...

    async def list_clients(self, tenant_id: str) -> List[Client]:
        """Obtiene todos los clientes pertenecientes a un tenant."""
        ...

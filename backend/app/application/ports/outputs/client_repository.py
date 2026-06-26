from typing import List, Optional, Protocol
from app.domain.models.client import Client


class ClientRepositoryPort(Protocol):
    async def save(self, client: Client) -> Client:
        """Guarda un cliente en el almacenamiento persistente."""
        ...

    async def find_by_id(self, tenant_id: str, client_id: str) -> Optional[Client]:
        """Busca un cliente por su ID y valida pertenencia al tenant."""
        ...

    async def find_all_by_tenant(self, tenant_id: str) -> List[Client]:
        """Obtiene la lista de todos los clientes de un tenant específico."""
        ...

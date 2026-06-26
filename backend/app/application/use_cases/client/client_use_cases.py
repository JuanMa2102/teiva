import uuid
from datetime import datetime
from typing import List, Optional
from app.application.ports.inputs.client_use_cases import ClientUseCasesPort, CreateClientCommand
from app.application.ports.outputs.client_repository import ClientRepositoryPort
from app.domain.exceptions import EntityNotFoundException
from app.domain.models.client import Client


class ClientUseCases(ClientUseCasesPort):
    def __init__(self, client_repository: ClientRepositoryPort):
        self._client_repository = client_repository

    async def create_client(self, tenant_id: str, command: CreateClientCommand) -> Client:
        client = Client(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            first_name=command.first_name,
            last_name=command.last_name,
            email=command.email,
            phone=command.phone,
            created_at=datetime.utcnow()
        )
        return await self._client_repository.save(client)

    async def get_client_by_id(self, tenant_id: str, client_id: str) -> Optional[Client]:
        client = await self._client_repository.find_by_id(tenant_id, client_id)
        if not client:
            raise EntityNotFoundException("Cliente", client_id)
        return client

    async def list_clients(self, tenant_id: str) -> List[Client]:
        return await self._client_repository.find_all_by_tenant(tenant_id)

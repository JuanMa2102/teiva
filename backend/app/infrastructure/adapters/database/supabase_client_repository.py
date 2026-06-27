"""
Implementation of ClientRepositoryPort using Supabase AsyncClient
"""
from supabase._async.client import AsyncClient
from app.application.ports.outputs.client_repository_port import ClientRepositoryPort
from app.domain.models.client import Client
from app.api.middlewares.tenant_context_middleware import tenant_id_var

class SupabaseClientRepository(ClientRepositoryPort):
    """
    Implementación asíncrona del contrato ClientRepositoryPort para Supabase
    """

    def __init__(self, supabase_client: AsyncClient):
        self.client = supabase_client

    async def save(self, client: Client) -> Client:
        data = client.model_dump()

        data["created_at"] = data["created_at"].isoformat()
        if data.get("updated_at"):
            data["updated_at"] = data["updated_at"].isoformat()

        response = await self.client.table("clients").upsert(data).execute()

        if not response.data:
            raise ConnectionError("Error al guardar o actualizar el cliente en Supabase")

        return Client(**response.data[0])

    async def find_by_id(self, client_id: str) -> Client | None:
        # Consulta asíncrona utilizando await
        response = (
            await self.client.table("clients")
            .select("*")
            .eq("id", client_id)
            .execute()
        )

        if not response.data:
            return None

        client_data = response.data[0]
        return Client(**client_data)

    async def list(self) -> list[Client]:
        tenant_id = tenant_id_var.get()
        response = (
            await self.client.table("clients")
            .select("*")
            .eq("tenant_id", tenant_id)
            .execute()
        )

        if not response.data:
            return []

        return [Client(**client_data) for client_data in response.data]

    async def delete(self, client_id: str) -> None:
        response = (
            await self.client.table("clients")
            .delete()
            .eq("id", client_id)
            .execute()
        )

        if not response.data:
            raise ConnectionError("Error al eliminar el cliente en Supabase")

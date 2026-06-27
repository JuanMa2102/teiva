"""
Implementation of TenantRepositoryPort using Supabase AsyncClient
"""
from supabase._async.client import AsyncClient
from app.application.ports.outputs.tenant_repository_port import TenantRepositoryPort
from app.domain.models.tenant import Tenant

class SupabaseTenantRepository(TenantRepositoryPort):
    """
    Implementación asíncrona del contrato TenantRepositoryPort para Supabase
    """

    def __init__(self, supabase_client: AsyncClient):
        self.client = supabase_client

    async def save(self, tenant: Tenant) -> Tenant:
        # Serializamos el modelo de dominio a diccionario nativo de Python
        data = tenant.model_dump()

        # Pydantic v2 maneja bien datetime a ISO strings, pero nos aseguramos por Supabase
        data["created_at"] = data["created_at"].isoformat()
        if data.get("updated_at"):
            data["updated_at"] = data["updated_at"].isoformat()

        # Usamos .upsert para permitir creación y actualización con el await asíncrono
        response = await self.client.table("tenants").upsert(data).execute()

        if not response.data:
            raise ConnectionError("Error al guardar o actualizar el tenant en Supabase")

        return Tenant(**response.data[0])

    async def find_by_id(self, tenant_id: str) -> Tenant | None:
        # Consulta asíncrona utilizando await
        response = (
            await self.client.table("tenants")
            .select("*")
            .eq("id", tenant_id)
            .execute()
        )

        if not response.data:
            return None

        tenant_data = response.data[0]
        return Tenant(**tenant_data)

    async def find_by_name(self, name: str) -> Tenant | None:
        pass

    async def list(self) -> list[Tenant]:
        pass

    async def delete(self, tenant_id: str) -> None:
        pass

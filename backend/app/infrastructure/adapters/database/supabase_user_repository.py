"""
Implementation of UserRepositoryPort using Supabase AsyncClient
"""
from supabase._async.client import AsyncClient
from app.application.ports.outputs.user_repository_port import UserRepositoryPort
from app.domain.models.user import User

class SupabaseUserRepository(UserRepositoryPort):
    """
    Implementación asíncrona del contrato UserRepositoryPort para Supabase
    """

    def __init__(self, supabase_client: AsyncClient):
        self.client = supabase_client

    async def save(self, user: User) -> User:
        data = user.model_dump()

        data["created_at"] = data["created_at"].isoformat()
        if data.get("updated_at"):
            data["updated_at"] = data["updated_at"].isoformat()

        response = await self.client.table("users").upsert(data).execute()

        if not response.data:
            raise ConnectionError("Error al guardar o actualizar el user en Supabase")

        return User(**response.data[0])

    async def find_by_id(self, user_id: str) -> User | None:
        # Consulta asíncrona utilizando await
        response = (
            await self.client.table("users")
            .select("*")
            .eq("id", user_id)
            .execute()
        )

        if not response.data:
            return None

        user_data = response.data[0]
        return User(**user_data)

    async def find_by_email(self, email: str) -> User | None:
        pass

    async def list(self, tenant_id: str) -> list[User]:
        pass

    async def delete(self, user_id: str) -> None:
        pass

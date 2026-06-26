from typing import List, Optional
from app.application.ports.outputs.client_repository import ClientRepositoryPort
from app.domain.models.client import Client
# Nota: La base de datos de Supabase en producción debe tener habilitado RLS (Row Level Security)
# para asegurar el aislamiento estricto por tenant_id mediante políticas.
from supabase import Client as SupabaseClient


class SupabaseClientRepository(ClientRepositoryPort):
    def __init__(self, supabase_client: SupabaseClient):
        self.client = supabase_client

    async def save(self, client: Client) -> Client:
        # Usamos la interfaz de Supabase para guardar el registro.
        # Al usar el SDK oficial de Supabase, las consultas se parametrizan automáticamente por debajo,
        # lo que previene ataques de inyección SQL (SQL Injection).
        data = client.model_dump()
        # Convertir objetos datetime a strings ISO para JSON
        data["created_at"] = data["created_at"].isoformat()
        if data.get("updated_at"):
            data["updated_at"] = data["updated_at"].isoformat()

        # TODO(security): Asegurar que el rol de base de datos tenga privilegios limitados.
        response = self.client.table("clients").upsert(data).execute()
        
        # En Supabase v2, `response.data` contiene los registros insertados/actualizados
        if not response.data:
            raise RuntimeError("Error al guardar el cliente en Supabase")
            
        return client

    async def find_by_id(self, tenant_id: str, client_id: str) -> Optional[Client]:
        # Para garantizar el aislamiento de tenants (Multi-tenancy), siempre filtramos por tenant_id.
        # Esto previene problemas de Broken Object Level Authorization (BOLA).
        response = (
            self.client.table("clients")
            .select("*")
            .eq("id", client_id)
            .eq("tenant_id", tenant_id)
            .execute()
        )
        
        if not response.data:
            return None
            
        row = response.data[0]
        return Client(
            id=row["id"],
            tenant_id=row["tenant_id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            email=row.get("email"),
            phone=row.get("phone"),
            created_at=row["created_at"]
        )

    async def find_all_by_tenant(self, tenant_id: str) -> List[Client]:
        response = (
            self.client.table("clients")
            .select("*")
            .eq("tenant_id", tenant_id)
            .execute()
        )
        
        clients = []
        for row in response.data:
            clients.append(
                Client(
                    id=row["id"],
                    tenant_id=row["tenant_id"],
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    email=row.get("email"),
                    phone=row.get("phone"),
                    created_at=row["created_at"]
                )
            )
        return clients

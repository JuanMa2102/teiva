"""
Caso de uso para insertar nuevos clientes.
"""
import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.application.ports.outputs.client_repository_port import ClientRepositoryPort
from app.domain.models.client import Client
from app.domain.enums import ClientStatus, PersonType
from app.api.middlewares.tenant_context_middleware import tenant_id_var

class CreateClientRequest(BaseModel):
    """
    Modelo para la request de creación de cliente.
    Usa los Enums de dominio para validar la entrada desde la capa API.
    """
    first_name: str
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    person_type: PersonType = PersonType.FISICA
    status: ClientStatus = ClientStatus.PROSPECTO


class CreateClientUseCase:
    """
    Caso de uso encargado de registrar un nuevo cliente o prospecto.
    """
    def __init__(self, client_repo: ClientRepositoryPort):
        self.client_repo = client_repo

    async def execute(self, request: CreateClientRequest):
        """
        Ejecuta de forma orquestada la creación del cliente enlazado al Tenant actual.
        """
        tenant_id = tenant_id_var.get()

        if not tenant_id:
            raise ValueError(
                "No se encontró un contexto de Tenant activo para realizar esta operación."
            )

        client_id = str(uuid.uuid4())

        try:
            # Instanciamos la entidad de dominio con tipado consistente
            client = Client(
                id=client_id,
                tenant_id=tenant_id,
                first_name=request.first_name,
                last_name=request.last_name,
                email=request.email,
                phone=request.phone,
                person_type=request.person_type,
                status=request.status
            )

            # Persistencia mediante puerto de salida
            await self.client_repo.save(client)

            return {
                "success": True,
                "client": client,
                "message": "Cliente creado exitosamente"
            }
        except Exception as e:
            # Espacio para inyección de logging en infraestructura más adelante
            raise e

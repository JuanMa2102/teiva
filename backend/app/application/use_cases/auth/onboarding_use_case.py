"""
Caso de uso para onboarding
"""
import uuid
from typing import Dict, Any
from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel

from app.application.ports.outputs.tenant_repository_port import TenantRepositoryPort
from app.application.ports.outputs.user_repository_port import UserRepositoryPort
from app.domain.models.tenant import Tenant
from app.domain.models.user import User
from app.domain.enums import TenantPlan, TenantStatus, UserRole

class OnboardingRequest(BaseModel):
    """
    Modelo para la request de onboarding.
    Permite recibir atributos en camelCase desde Next.js y usarlos como snake_case en Python.
    """
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )

    user_id: uuid.UUID
    email: EmailStr
    first_name: str
    last_name: str
    organization_name: str


class OnboardingUseCase:
    """
    Caso de Uso encargado de registrar y asociar una nueva organización (Tenant)
    con su usuario administrador principal.
    """
    def __init__(self, tenant_repo: TenantRepositoryPort, user_repo: UserRepositoryPort):
        self.tenant_repo = tenant_repo
        self.user_repo = user_repo

    async def execute(self, request: OnboardingRequest) -> Dict[str, Any]:
        """
        Ejecuta de forma orquestada la creación del Tenant operativo y el Perfil de Usuario.
        """
        tenant_id = str(uuid.uuid4())
        # Acoplamos el ID operativo al ID de autenticación que nos provee Supabase
        user_id = str(request.user_id) 

        try:
            # 1. Instanciar Entidad de Dominio: Tenant
            tenant = Tenant(
                id=tenant_id,
                name=request.organization_name,
                status=TenantStatus.ACTIVE,
                plan=TenantPlan.TRIAL
            )

            # 2. Instanciar Entidad de Dominio: User (El creador por defecto es Admin de la Agencia)
            user = User(
                id=user_id,
                email=request.email,
                role=UserRole.ADMIN_AGENCIA,
                tenant_id=tenant_id,
                first_name=request.first_name,
                last_name=request.last_name
            )

            # 3. Persistir de forma asíncrona mediante los Puertos de Salida
            await self.tenant_repo.save(tenant)
            await self.user_repo.save(user)

            return {
                "tenant_id": tenant_id,
                "user_id": user_id,
                "success": True,
                "message": "Onboarding completado correctamente"
            }

        except Exception as e:
            # Aquí en el futuro inyectaremos logs específicos antes de re-lanzar
            raise e
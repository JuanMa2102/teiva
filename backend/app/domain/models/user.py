"""
    Modelo de Entidad de Dominio: User
"""
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from ..enums import UserRole

class User(BaseModel):
    """
    Representa un usuario en el sistema.

    Contiene la información del perfil, rol y estado de un usuario,
    asociado a un tenant específico para soporte multi-tenant.
    """
    model_config = ConfigDict(frozen=True)

    id: str = Field(description="Identificador único del usuario (UUID de Supabase)")
    email: EmailStr = Field(description="Correo electrónico del usuario")
    role: UserRole = Field(
        default=UserRole.AGENTE,
        description="Rol dentro del sistema (ej. admin, agent)"
    )
    tenant_id: str = Field(description="Referencia al tenant (multi-tenancy)")
    first_name: Optional[str] = Field(default=None, description="Primer nombre")
    last_name: Optional[str] = Field(default=None, description="Apellido")
    is_active: bool = Field(default=True, description="Indica si el usuario está activo")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

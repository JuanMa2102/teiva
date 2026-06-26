from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class User(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str = Field(description="Identificador único del usuario (UUID de Supabase)")
    email: EmailStr = Field(description="Correo electrónico del usuario")
    role: str = Field(default="agent", description="Rol dentro del sistema (ej. admin, agent)")
    tenant_id: str = Field(description="Referencia al tenant (multi-tenancy)")
    first_name: Optional[str] = Field(default=None, description="Primer nombre")
    last_name: Optional[str] = Field(default=None, description="Apellido")
    is_active: bool = Field(default=True, description="Indica si el usuario está activo")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

"""
Módulo del modelo de dominio para Tenant.

Define la entidad Tenant que representa a las organizaciones
registradas en el sistema SaaS.
"""
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from ..enums import TenantPlan, TenantStatus

class Tenant(BaseModel):
    """
    Modelo de Entidad de Dominio: Tenant (Inquilino)
    
    Representa la organización cliente del SaaS.
    Inmutable (frozen=True) para reflejar que una vez creado, el tenant
    solo evoluciona mediante eventos o comandos de actualización específicos
    (ej: upgrade_plan).
    """
    model_config = ConfigDict(frozen=True)

    id: str = Field(description="Identificador único del tenant (UUID)")
    name: str = Field(description="Nombre comercial o razón social de la organización")
    status: TenantStatus = Field(
        default=TenantStatus.ACTIVE,
        description="Estado de la cuenta del tenant"
    )
    plan: TenantPlan = Field(default=TenantPlan.TRIAL, description="Plan contratado por el tenant")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

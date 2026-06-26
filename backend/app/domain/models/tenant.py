from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class Tenant(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str = Field(description="Identificador único del tenant (UUID)")
    name: str = Field(description="Nombre comercial o razón social de la organización")
    status: str = Field(default="active", description="Estado de la cuenta del tenant")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

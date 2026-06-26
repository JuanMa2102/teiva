from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Client(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str = Field(description="Identificador único del cliente (UUID)")
    tenant_id: str = Field(description="Referencia al tenant al que pertenece el cliente")
    first_name: str = Field(description="Nombre o nombres del cliente")
    last_name: str = Field(description="Apellidos del cliente")
    email: Optional[EmailStr] = Field(default=None, description="Correo electrónico de contacto")
    phone: Optional[str] = Field(default=None, description="Número de teléfono de contacto")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

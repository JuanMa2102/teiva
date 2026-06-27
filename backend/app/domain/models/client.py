"""
Módulo del modelo de dominio para Client.

Define la entidad Cliente que representa a las personas físicas o morales
registradas por una organización (Tenant).
"""
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.domain.enums import ClientStatus, PersonType

class Client(BaseModel):
    """
    Entidad de dominio inmutable que representa a un Cliente/Prospecto.
    """
    model_config = ConfigDict(frozen=True)

    id: str = Field(description="Identificador único del cliente (UUID)")
    tenant_id: str = Field(description="Referencia al tenant al que pertenece el cliente")
    first_name: str = Field(description="Nombre(s) del cliente o Razón Social si es Persona Moral")
    last_name: Optional[str] = Field(
        default=None,
        description="Apellidos del cliente (Opcional para Personas Morales)"
    )
    email: Optional[EmailStr] = Field(default=None, description="Correo electrónico de contacto")
    phone: Optional[str] = Field(default=None, description="Número de teléfono de contacto")
    person_type: PersonType = Field(
        default=PersonType.FISICA,
        description="Tipo de persona: Física o Moral"
    )
    status: ClientStatus = Field(
        default=ClientStatus.PROSPECTO,
        description="Estatus del cliente en el embudo"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Fecha de creación en UTC")
    updated_at: Optional[datetime] = Field(
        default=None,
        description="Fecha de última actualización en UTC"
    )

from typing import Protocol
from pydantic import BaseModel, EmailStr


class LoginCommand(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    tenant_id: str


class AuthUseCasesPort(Protocol):
    async def login(self, command: LoginCommand) -> LoginResponse:
        """Autentica a un usuario y genera un token JWT."""
        ...

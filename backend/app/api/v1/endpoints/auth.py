from fastapi import APIRouter, HTTPException, status
from app.application.ports.inputs.auth_use_cases import LoginCommand, LoginResponse
from app.application.use_cases.auth.login import LoginUseCase
from app.domain.exceptions import InvalidCredentialsException

router = APIRouter()


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(command: LoginCommand):
    """
    Ruta para autenticar a un agente o administrador de seguros.
    Retorna un token de sesión de prueba.
    """
    use_case = LoginUseCase()
    try:
        return await use_case.login(command)
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

import uuid
from app.application.ports.inputs.auth_use_cases import AuthUseCasesPort, LoginCommand, LoginResponse
from app.domain.exceptions import InvalidCredentialsException


class LoginUseCase(AuthUseCasesPort):
    def __init__(self):
        # En una implementación real, aquí inyectaríamos el puerto del proveedor de identidad (ej. SupabaseAuthPort)
        pass

    async def login(self, command: LoginCommand) -> LoginResponse:
        # Validación de prueba simplificada (stub/mock)
        # TODO(security): Integrar con autenticación real de Supabase / Firebase Auth.
        if command.email == "demo@teiva.co" and command.password == "Password123":
            # Retorna un JWT de prueba / mock tokens
            return LoginResponse(
                access_token="mock-jwt-token-for-testing",
                user_id=str(uuid.uuid4()),
                tenant_id="tenant-demo-123"
            )
        else:
            raise InvalidCredentialsException("Correo o contraseña incorrectos")

class DomainException(Exception):
    """Excepción base para todos los errores de la capa de dominio."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EntityNotFoundException(DomainException):
    """Se lanza cuando un recurso/entidad no es encontrado."""
    def __init__(self, entity_name: str, entity_id: str):
        super().__init__(f"No se encontró {entity_name} con ID: {entity_id}")


class TenantAccessDeniedException(DomainException):
    """Se lanza cuando se intenta acceder a un recurso de otro tenant."""
    def __init__(self, message: str = "Acceso denegado: Violación de aislamiento de inquilino (Tenant)"):
        super().__init__(message)


class InvalidCredentialsException(DomainException):
    """Se lanza cuando las credenciales no son válidas o el token ha expirado."""
    def __init__(self, message: str = "Credenciales inválidas o token expirado"):
        super().__init__(message)


class ValidationException(DomainException):
    """Se lanza cuando hay una violación de reglas de negocio en la entrada."""
    def __init__(self, message: str):
        super().__init__(message)

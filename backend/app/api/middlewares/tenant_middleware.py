from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from app.infrastructure.config import settings

# Esquema de autenticación Bearer Token para OpenAPI / Swagger
security_scheme = HTTPBearer(auto_error=True)


async def get_current_tenant_id(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
) -> str:
    """
    Dependency para extraer y validar de forma segura el tenant_id a partir de un JWT.
    Cumple con las pautas de seguridad de rechazo del algoritmo 'none' y verificación estricta.
    """
    token = credentials.credentials
    
    try:
        # Decodificación y validación estricta del JWT.
        # - Se fuerza el algoritmo configurado (nunca derivado del header del token).
        # - La librería jose valida de manera nativa la expiración ('exp') por defecto.
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        tenant_id: str = payload.get("tenant_id")
        if not tenant_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: falta tenant_id en los claims",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        return tenant_id

    except JWTError as e:
        # Evitamos filtrar detalles de la traza original por seguridad, retornando un error genérico de credenciales.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas o token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

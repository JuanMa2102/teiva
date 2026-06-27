"""
Endpoint de authenticacion
"""
from fastapi import APIRouter, Depends, HTTPException, status
from supabase._async.client import AsyncClient

from app.application.use_cases.auth.onboarding_use_case import OnboardingUseCase, OnboardingRequest
from app.infrastructure.adapters.database.supabase_tenant_repository import SupabaseTenantRepository
from app.infrastructure.adapters.database.supabase_user_repository import SupabaseUserRepository


router = APIRouter( prefix='/auth', tags=['Authentication'] )

# Necesitaremos una función auxiliar para obtener el cliente de
# Supabase (por ahora simúlalo o inyéctalo si ya tienes un archivo de config)
async def get_supabase_client() -> AsyncClient:
    """
    Obtiene el cliente de Supabase.
    """
    # Aquí irá tu inicialización real de Supabase más adelante
    # Por ahora puedes retornar None o un cliente ficticio para armar la firma

@router.post("/onboarding", status_code=status.HTTP_201_CREATED)
async def onboarding(
    request: OnboardingRequest,
    supabase_client: AsyncClient = Depends( get_supabase_client )
):
    """
    Ruta para autenticar a un agente o administrador de seguros.
    Retorna un token de sesión de prueba.
    """
    # 1. Instanciar los adaptadores de infraestructura pasándole el cliente
    user_repo = SupabaseUserRepository( supabase_client=supabase_client )
    tenant_repo = SupabaseTenantRepository( supabase_client=supabase_client )

    # 2. Instanciar el Caso de Uso con los repositorios
    use_case = OnboardingUseCase( tenant_repo=tenant_repo, user_repo=user_repo )

    # 3. Ejecutar el Caso de Uso y retornar el resultado
    try:
        return await use_case.execute(request)
    except Exception as e:
        # En producción, loguear 'e' antes de relanzar
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        ) from e

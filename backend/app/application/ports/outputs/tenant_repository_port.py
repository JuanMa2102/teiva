"""
    Puerto de salida para el repositorio de tenants
"""

from abc import ABC, abstractmethod
from app.domain.models.tenant import Tenant

class TenantRepositoryPort(ABC):
    """
    Puerto de salida para el repositorio de tenants
    """

    @abstractmethod
    async def save(self, tenant: Tenant) -> Tenant:
        """
        Guarda un tenant
        Args:
            tenant: Tenant a guardar
        Returns:
            Tenant guardado
        """

    @abstractmethod
    async def find_by_id(self, tenant_id: str) -> Tenant | None:
        """
        Busca un tenant por id
        Args:
            tenant_id: Id del tenant
        Returns:
            Tenant encontrado
        """

    @abstractmethod
    async def find_by_name(self, name: str) -> Tenant | None:
        """
        Busca un tenant por nombre
        Args:
            name: Nombre del tenant
        Returns:
            Tenant encontrado
        """

    @abstractmethod
    async def list(self) -> list[Tenant]:
        """
        Lista los tenants
        Returns:
            Lista de tenants
        """

    @abstractmethod
    async def delete(self, tenant_id: str) -> None:
        """
        Elimina un tenant
        Args:
            tenant_id: Id del tenant
        """

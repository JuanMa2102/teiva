"""
Interface para el repositorio de clientes.

Contiene los métodos que deben ser implementados por el adaptador de infraestructura
para la gestión de clientes/prospectos.
"""

from abc import ABC, abstractmethod
from app.domain.models.client import Client

class ClientRepositoryPort(ABC):
    """
    Puerto de salida para el repositorio de clientes.
    """

    @abstractmethod
    async def save(self, client: Client) -> Client:
        """
        Guarda o actualiza un cliente.
        Args:
            client: Cliente a guardar.
        Returns:
            Cliente guardado.
        """

    @abstractmethod
    async def find_by_id(self, client_id: str) -> Client | None:
        """
        Busca un cliente por id.
        Args:
            client_id: Id del cliente.
        Returns:
            Cliente encontrado o None.
        """

    @abstractmethod
    async def list(self) -> list[Client]:
        """
        Lista los clientes del tenant actual (obtenido implícitamente del contexto).
        Returns:
            Lista de clientes.
        """

    @abstractmethod
    async def delete(self, client_id: str) -> None:
        """
        Elimina un cliente.
        Args:
            client_id: Id del cliente.
        """

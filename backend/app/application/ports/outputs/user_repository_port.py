"""
    Interface para el repositorio de usuarios

    Contiene los metodos que deben ser implementados por el repositorio
    de usuarios
"""

from abc import ABC, abstractmethod
from app.domain.models.user import User

class UserRepositoryPort(ABC):
    """
        Puerto de salida para el repositorio de usuarios
    """
    @abstractmethod
    async def save(self, user: User) -> User:
        """
            Guarda un usuario
            Args:
                user: Usuario a guardar
            Returns:
                Usuario guardado
        """

    @abstractmethod
    async def find_by_id(self, user_id: str) -> User | None:
        """
            Busca un usuario por id
            Args:
                id: Id del usuario
            Returns:
                Usuario encontrado
        """

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None:
        """
            Busca un usuario por email
            Args:
                email: Email del usuario
            Returns:
                Usuario encontrado
        """

    @abstractmethod
    async def list(self, tenant_id: str) -> list[User]:
        """
            Lista los usuarios de un tenant
            Args:
                tenant_id: Id del tenant
            Returns:
                Lista de usuarios
        """


    @abstractmethod
    async def delete(self, user_id: str) -> None:
        """
            Elimina un usuario
            Args:
                id: Id del usuario
        """

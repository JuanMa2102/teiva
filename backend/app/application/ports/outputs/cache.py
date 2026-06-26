from typing import Optional, Protocol


class CachePort(Protocol):
    async def get(self, key: str) -> Optional[str]:
        """Obtiene un valor almacenado en caché."""
        ...

    async def set(self, key: str, value: str, expire_seconds: Optional[int] = None) -> None:
        """Establece un valor en la caché con un tiempo de expiración opcional."""
        ...

    async def delete(self, key: str) -> None:
        """Elimina una clave de la caché."""
        ...

    async def is_rate_limited(self, key: str, limit: int, window_seconds: int) -> bool:
        """Determina si una acción excede la cuota permitida (Rate Limiting)."""
        ...

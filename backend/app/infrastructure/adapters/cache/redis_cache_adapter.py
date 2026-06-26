from typing import Optional
from app.application.ports.outputs.cache import CachePort
from redis.asyncio import Redis


class RedisCacheAdapter(CachePort):
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    async def get(self, key: str) -> Optional[str]:
        val = await self.redis.get(key)
        return val.decode("utf-8") if val else None

    async def set(self, key: str, value: str, expire_seconds: Optional[int] = None) -> None:
        await self.redis.set(key, value, ex=expire_seconds)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)

    async def is_rate_limited(self, key: str, limit: int, window_seconds: int) -> bool:
        """Implementación de un limitador de tasa mediante Ventana Deslizante / Fija en Redis."""
        # Se usa una clave estructurada por IP / Token e ID de endpoint.
        # Incrementa la cuenta de peticiones.
        pipe = self.redis.pipeline()
        await pipe.incr(key)
        await pipe.expire(key, window_seconds)
        results = await pipe.execute()
        
        current_requests = results[0]
        if current_requests > limit:
            return True
        return False

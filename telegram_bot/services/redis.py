from infrastructure.redis import RedisClient

_redis_client: RedisClient | None = None

async def get_redis() -> RedisClient:
	global _redis_client
	if _redis_client is None:
		_redis_client = RedisClient()
		await _redis_client.get_client()
	return _redis_client

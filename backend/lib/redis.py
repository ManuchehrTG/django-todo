from infrastructure.redis import RedisClient

_backend_redis: RedisClient | None = None

async def get_redis() -> RedisClient:
	global _backend_redis
	if _backend_redis is None:
		_backend_redis = RedisClient()
		await _backend_redis.get_client()
	return _backend_redis

async def close_redis():
	global _backend_redis
	if _backend_redis:
		await _backend_redis.close()
		_backend_redis = None
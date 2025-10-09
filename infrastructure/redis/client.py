from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool
from redis.exceptions import RedisError, ConnectionError

from configs import redis_config
from infrastructure.logger import get_logger

app_logger = get_logger("redis")

class RedisClient:
	def __init__(self, max_connections: int = redis_config.MAX_CONNECTIONS):
		self.max_connections = max_connections

		self._client: Redis | None = None
		self._pool: ConnectionPool | None = None

	async def get_client(self) -> Redis:
		if self._client is None or not await self._check_connection():
			await self._connect()
		return self._client

	async def _connect(self):
		try:
			self._pool = ConnectionPool.from_url(str(redis_config.DSN))
			self._client = Redis(connection_pool=self._pool)

			await self._client.ping()
			app_logger.info("⚡️ Redis connected")

		except (ConnectionError, RedisError) as e:
			app_logger.error(f"Redis connection failed: {e}", exc_info=True)
			raise

	async def _check_connection(self) -> bool:
		try:
			await self._client.ping()
			return True
		except (ConnectionError, RedisError):
			app_logger.warning("Redis connection lost, reconnecting...")
			await self.close()
		return False

	async def close(self):
		if self._client:
			await self._client.aclose()
			self._client = None
			app_logger.info("⚡️ Redis disconnected")

		if self._pool:
			await self._pool.disconnect()
			self._pool = None

	def __getattr__(self, name):
		async def wrapper(*args, **kwargs):
			await self.get_client()
			method = getattr(self._client, name)
			return await method(*args, **kwargs)
		return wrapper

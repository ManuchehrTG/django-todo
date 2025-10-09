from pydantic import BaseModel, RedisDsn

class RedisConfig(BaseModel):
	DSN: RedisDsn
	MAX_CONNECTIONS: int

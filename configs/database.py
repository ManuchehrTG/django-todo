from pydantic import BaseModel, PostgresDsn

class DatabaseConfig(BaseModel):
	NAME: str
	USER: str
	PASSWORD: str
	HOST: str
	PORT: int
	DSN: PostgresDsn

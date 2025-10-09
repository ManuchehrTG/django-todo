from pydantic import BaseModel, Field
from typing import List

class DjangoConfig(BaseModel):
	SECRET_KEY: str

	ALLOWED_HOSTS: List[str] = Field(default_factory=list)
	CSRF_TRUSTED_ORIGINS: List[str] = Field(default_factory=list)

	LANGUAGE_CODE: str

	PORT: int
	PORT_MAPPING: str
	DOMAIN: str

	@property
	def URL(self) -> str:
		return f"https://{self.DOMAIN}"

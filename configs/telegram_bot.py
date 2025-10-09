from pydantic import BaseModel, Field
from typing import Dict, List

class TelegramBotConfig(BaseModel):
	TOKEN: str
	ADMIN_IDS: List[int] = Field(default_factory=list)
	SUPPORT_USERNAME: str

	PORT: int
	PORT_MAPPING: str
	DOMAIN: str

	BACKEND_DOMAIN: str = Field(default="")
	BACKEND_ACCESS_TOKEN: str = Field(default="")

	def setup_django_config(self, django_config: 'DjangoConfig') -> 'TelegramBotConfig':
		self.BACKEND_DOMAIN = django_config.DOMAIN

	@property
	def URL(self) -> str:
		return f"https://{self.DOMAIN}"

	@property
	def BACKEND_API_URL(self) -> str:
		return f"https://{self.BACKEND_DOMAIN}/api"

	@property
	def DEFAULT_HTTP_HEADERS(self) -> Dict:
		try:
			headers = {"Authorization": f"Token {self.BACKEND_ACCESS_TOKEN}"}
		except Exception as e:
			headers = {}

		return headers

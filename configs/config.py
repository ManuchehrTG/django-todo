from pydantic_settings import BaseSettings

from .app import AppConfig
from .django import DjangoConfig
from .telegram_bot import TelegramBotConfig
from .database import DatabaseConfig
from .redis import RedisConfig
from .logger import LoggerConfig

class Config(BaseSettings):
	APP: AppConfig = AppConfig()
	DJANGO: DjangoConfig
	TELEGRAM_BOT: TelegramBotConfig
	DATABASE: DatabaseConfig
	REDIS: RedisConfig
	LOGGER: LoggerConfig

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.TELEGRAM_BOT.setup_django_config(self.DJANGO)

	class Config:
		env_file = ".env"
		env_file_encoding = "utf-8"
		extra = "ignore"
		env_nested_delimiter = "__"

config = Config()

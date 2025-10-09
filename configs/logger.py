from pathlib import Path
from pydantic import BaseModel

class LoggerConfig(BaseModel):
	# Уровни логирования
	LEVEL: str
	FORMAT: str

	# Файлы логов
	DIR: Path
	ENABLE_FILE_LOGGING: bool
	ENABLE_CONSOLE_LOGGING: bool

	# Ротация логов
	MAX_LOG_SIZE: int
	BACKUP_COUNT: int

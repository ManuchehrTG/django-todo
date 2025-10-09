from datetime import datetime
from httpx import HTTPStatusError
from typing import List

from configs import telegram_bot_config
from infrastructure.logger import LoggerMixin
from schemes.database import User
from services.http import get_http_client

class UserRepository(LoggerMixin):
	API_URL = f"{telegram_bot_config.BACKEND_API_URL}/users"
	logger = LoggerMixin()

	@classmethod
	async def create_or_update_user(cls, user_id: int, first_name: str, username: str | None, language_code: str, is_admin: bool):
		cls.logger.info("POST User")
		async_http_client = get_http_client(mode="async")
		user_data = {
			"first_name": first_name,
			"username": username,
			"language_code": language_code,
			"is_admin": is_admin
		}

		try:
			response = await async_http_client.apatch(url=f"{cls.API_URL}/{user_id}/", json=user_data, response_type="response")
			if response.status_code == 404:
				user_data["id"] = user_id
				response = await async_http_client.apost(url=f"{cls.API_URL}/", json=user_data, response_type="response")

			response.raise_for_status()
			record = response.json()

		except HTTPStatusError as e:
			cls.logger.warning(
				f"Ошибка обновления/записи пользователя: {user_id} | "
				f"StatusCode: {e.response.status_code}, Response: {e.response.text}"
			)
			record = await async_http_client.aget(url=f"{cls.API_URL}/{user_id}/", response_type="json")

		return User(**record)

	@classmethod
	async def get_user(cls, user_id: int):
		cls.logger.info("GET User")
		async_http_client = get_http_client(mode="async")
		record = await async_http_client.aget(url=f"{cls.API_URL}/{user_id}/", response_type="json")
		return User(**record)

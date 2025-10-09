from datetime import datetime
from httpx import HTTPStatusError
from typing import List

from configs import telegram_bot_config
from services.http import get_http_client
from schemes.database import Category

class CategoryRepository:
	API_URL = f"{telegram_bot_config.BACKEND_API_URL}/categories"

	@classmethod
	async def get_categories(cls, user_id: int) -> List[Category]:
		async_http_client = get_http_client(mode="async")
		params = {"user_id": user_id}
		records = await async_http_client.aget(url=f"{cls.API_URL}/", response_type="json", params=params)
		return [Category(**record) for record in records]

	@classmethod
	async def get_category(cls, category_id: str, user_id: int) -> Category:
		async_http_client = get_http_client(mode="async")
		params = {"user_id": user_id}
		record = await async_http_client.aget(url=f"{cls.API_URL}/{category_id}/", response_type="json", params=params)
		return Category(**record)

	@classmethod
	async def create(cls, name: str, user_id: int) -> Category:
		async_http_client = get_http_client(mode="async")
		data = {"name": name, "user_id": user_id}
		record = await async_http_client.apost(url=f"{cls.API_URL}/", response_type="json", json=data)
		return Category(**record)

from datetime import datetime
from httpx import HTTPStatusError
from typing import List

from configs import telegram_bot_config
from services.http import get_http_client
from schemes.database import Task

class TaskRepository:
	API_URL = f"{telegram_bot_config.BACKEND_API_URL}/tasks"

	@classmethod
	async def get_tasks(cls, user_id: int, category_id: str | None = None) -> List[Task]:
		async_http_client = get_http_client(mode="async")
		params = {"user_id": user_id}

		if category_id:
			params["category_id"] = category_id

		records = await async_http_client.aget(url=f"{cls.API_URL}/", response_type="json", params=params)
		return [Task(**record) for record in records]

	@classmethod
	async def get_task(cls, task_id: str, user_id: int) -> Task:
		async_http_client = get_http_client(mode="async")
		params = {"user_id": user_id}
		record = await async_http_client.aget(url=f"{cls.API_URL}/{task_id}/", response_type="json", params=params)
		return Task(**record)

	@classmethod
	async def create(cls, title: str, category_id: str, user_id: int, due_date: datetime, description: str | None = None) -> Task:
		async_http_client = get_http_client(mode="async")
		data = {"title": title, "category_id": category_id, "user_id": user_id, "due_date": due_date, "description": description}
		record = await async_http_client.apost(url=f"{cls.API_URL}/", response_type="json", json=data)
		return Task(**record)

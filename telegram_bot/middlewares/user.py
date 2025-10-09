from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject, Update
from typing import Any, Awaitable, Callable, Dict

from configs import app_config, telegram_bot_config
from repositories.user import UserRepository
from schemes.database import User

class UserMiddleware(BaseMiddleware):
	def __init__(self, create_user_enable: bool = False) -> None:
		super().__init__()
		self.create_user_enable = create_user_enable

	async def __call__(
		self,
		handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
		event: TelegramObject,
		data: Dict[str, Any]
	) -> Any:
		user_id = event.from_user.id
		first_name = event.from_user.first_name
		username = event.from_user.username
		language_code = app_config.DEFAULT_LANGUAGE # Если бот будет многоязычным, нужно добавить функционал для определения языка

		if self.create_user_enable:
			user = await UserRepository.create_or_update_user(
				user_id=user_id,
				first_name=first_name,
				username=username,
				language_code=language_code,
				is_admin=user_id in tuple(telegram_bot_config.ADMIN_IDS)
			)

			if user.is_block:
				return

			data["user"] = user
		else:
			data["user"] = User(
				**user_data,
				id=user_id
			)

		return await handler(event, data)

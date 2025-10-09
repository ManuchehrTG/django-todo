from aiogram import Dispatcher

from infrastructure.logger import get_logger

from .user import UserMiddleware
from .album import AlbumMiddleware
from .throttling import ThrottlingMiddleware

logger = get_logger("middlewares")

def register_middlewares(dp: Dispatcher):
	dp.message.middleware(AlbumMiddleware())
	dp.message.middleware(UserMiddleware(create_user_enable=True))
	dp.message.middleware(ThrottlingMiddleware())

	dp.callback_query.middleware(UserMiddleware(create_user_enable=True))
	dp.callback_query.middleware(ThrottlingMiddleware())

	logger.info("Middlewares is connected ✅")

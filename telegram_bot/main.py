import asyncio
import os
import uvicorn

from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Update
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from configs import app_config, telegram_bot_config
from dialogs.categories import dialog as categories_dialog 
from dialogs.tasks import dialog as tasks_dialog 
from infrastructure.logger import logger
from middlewares import register_middlewares
from services.http import get_http_client
from services.redis import get_redis

async def create_app() -> FastAPI:
	async_http_client = get_http_client(mode="async", headers=telegram_bot_config.DEFAULT_HTTP_HEADERS)
	redis = await get_redis()

	bot = Bot(token=telegram_bot_config.TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
	key_builder = DefaultKeyBuilder(with_destiny=True)
	storage = RedisStorage(redis, key_builder=key_builder)
	dp = Dispatcher(storage=storage)

	register_middlewares(dp=dp)

	from handlers import router

	dp.include_router(router)

	dp.include_router(categories_dialog)
	dp.include_router(tasks_dialog)
	setup_dialogs(dp)

	logger.info("🟢 The bot is running!")

	@asynccontextmanager
	async def lifespan(app: FastAPI):
		try:
			await bot.set_webhook(url=f"{telegram_bot_config.URL}/webhook")

			yield
		except Exception as e:
			logger.error(f"⚠️ Startup failed: {e}", exc_info=True)
			raise
		finally:
			logger.info("🔴 Shutting down...")
			try:
				await bot.delete_webhook()
				await dp.storage.close()
				await bot.session.close()
				await async_http_client.close_async()
				await redis.close()
				logger.info("🤖 Aiogram bot session closed")
			except Exception as e:
				logger.error(f"Error during shutdown: {e}", exc_info=True)

	app = FastAPI(
		title=app_config.PROJECT_NAME,
		version="1.0.0",
		lifespan=lifespan,
		docs_url="/api/docs" if app_config.DEBUG else None
	)

	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"]
	)

	@app.post("/webhook")
	async def bot_webook(update: dict):
		"""Обработка обновлений через вебхук."""
		try:
			telegram_update = Update(**update)
			await dp.feed_update(bot=bot, update=telegram_update)
		except Exception as e:
			logger.exception(f"Error processing update: {e}")
		finally:
			return {"status": "ok"}

	@app.get("/health")
	async def health_check():
		return {"message": "ok", "status": "healthy"}

	return app

async def main() -> None:
	try:
		app = await create_app()

		config = uvicorn.Config(app=app, host=app_config.HOST, port=telegram_bot_config.PORT, log_level="info")
		server = uvicorn.Server(config)
		logger.info(f">>> Starting server at {app_config.HOST}:{telegram_bot_config.PORT}")

		await server.serve()
	except KeyboardInterrupt:
		logger.info("🔴 Server stopped gracefully")


if __name__ == "__main__":
	asyncio.run(main())

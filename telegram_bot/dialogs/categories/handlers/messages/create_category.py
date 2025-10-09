from aiogram_dialog import DialogManager, StartMode
from aiogram.types import Message

from dialogs.categories.states import StateCategories
from repositories.category import CategoryRepository
from schemes.database import Category
from utils.i18n import i18n

async def on_category_create(message: Message, widget, manager: DialogManager, title: str):
	user = manager.middleware_data["user"]
	category = await CategoryRepository.create(name=title, user_id=user.id)

	text_json = i18n.translate(namespace="categories.create_category", lang=user.language_code)

	if isinstance(category, Category):
		await message.answer(text=text_json["message"].format(title=title))
		await manager.start(StateCategories.categories, mode=StartMode.RESET_STACK, data={"user": user.model_dump_json()})
	else:
		await message.answer(text=text_json["errors"]["create_error"]["message"])

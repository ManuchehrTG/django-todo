from aiogram_dialog import DialogManager, StartMode
from aiogram.types import Message
from datetime import datetime
import pytz

from configs import app_config
from dialogs.tasks.states import StateTasks
from repositories.task import TaskRepository
from schemes.database import Task
from utils.i18n import i18n

async def on_task_create(message: Message, widget, manager: DialogManager):
	title = manager.dialog_data.get("title")
	description = manager.dialog_data.get("description")
	due_date = manager.dialog_data.get("due_date")
	category_id = manager.dialog_data.get("category_id")
	user = manager.middleware_data.get("user")

	text_json = i18n.translate(namespace="categories.create_category", lang=user.language_code)

	if not category_id:
		return await message.answer(text=text_json["errors"]["category_id_not_found"]["message"])

	task = await TaskRepository.create(title=title, category_id=category_id, user_id=user.id, due_date=due_date, description=description)

	if isinstance(task, Task):
		await message.answer(text=text_json["message"].format(title=title))
		await manager.start(StateTasks.tasks, mode=StartMode.RESET_STACK, data={"user": user.model_dump_json(), "category_id": category_id})
	else:
		await message.answer(text=text_json["errors"]["create_error"]["message"])

async def on_title_input(message: Message, widget, manager: DialogManager, *args, **kwargs):
	manager.dialog_data["title"] = message.text
	await manager.next()

async def on_description_input(message: Message, widget, manager: DialogManager, *args, **kwargs):
	manager.dialog_data["description"] = message.text
	await manager.next()

async def on_due_date_input(message: Message, widget, manager: DialogManager, *args, **kwargs):
	text = message.text.strip()
	try:
		tz = pytz.timezone(app_config.TIME_ZONE)
		due_date = datetime.strptime(text, "%Y-%m-%d %H:%M") # "2025-10-07 15:30"
		due_date = tz.localize(due_date)

		manager.dialog_data["due_date"] = due_date.isoformat()
		await on_task_create(message, widget, manager)

	except ValueError:
		text = i18n.translate(namespace="categories.create_category", key="errors.due_date_invalid.message", lang=user.language_code)
		await message.answer(text=text)

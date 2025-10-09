from aiogram_dialog import DialogManager, StartMode
from aiogram.types import CallbackQuery

from dialogs.categories.states import StateCategories
from repositories.task import TaskRepository
from utils.i18n import i18n

async def on_task_selected(call: CallbackQuery, widget, manager: DialogManager, item_id: str):
	user = manager.middleware_data["user"]
	task = await TaskRepository.get_task(task_id=item_id, user_id=user.id)
	text = i18n.translate(namespace="tasks.task", key="message", lang=user.language_code).format(
		title=task.title,
		description=task.description or "—",
		category_name=task.category.name,
		created_at=task.created_at.replace(tzinfo=None, microsecond=0),
		due_date=task.due_date.replace(tzinfo=None, microsecond=0)
	)

	await call.message.answer(text=text)

async def back_to_categories(callback: CallbackQuery, widget, manager: DialogManager):
	user = manager.middleware_data["user"]
	await manager.start(StateCategories.categories, mode=StartMode.RESET_STACK, data={"user": user.model_dump_json()})

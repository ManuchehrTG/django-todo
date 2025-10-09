from aiogram_dialog import DialogManager, StartMode
from aiogram.types import CallbackQuery

from dialogs.tasks.states import StateTasks

async def on_category_selected(call: CallbackQuery, widget, manager: DialogManager, item_id: str):
	user = manager.middleware_data["user"]
	await manager.start(StateTasks.tasks, mode=StartMode.RESET_STACK, data={"category_id": item_id, "user": user.model_dump_json()})

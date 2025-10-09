from aiogram_dialog import DialogManager
from aiogram.types import CallbackQuery

async def on_description_skip(callback: CallbackQuery, widget, manager: DialogManager):
	manager.dialog_data["description"] = None
	await manager.next()

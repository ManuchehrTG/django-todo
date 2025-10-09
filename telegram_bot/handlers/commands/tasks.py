from aiogram import Bot, F, Router
from aiogram_dialog import DialogManager, StartMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from dialogs.categories.states import StateCategories
from schemes.database import User

router = Router()

@router.message(F.text == "Мои задачи 📑", F.chat.type == "private")
@router.message(Command("tasks"), F.chat.type == "private")
async def message_tasks(message: Message, dialog_manager: DialogManager, state: FSMContext, bot: Bot, user: User):
	await dialog_manager.start(StateCategories.categories, mode=StartMode.RESET_STACK, data={"user": user.model_dump_json()})

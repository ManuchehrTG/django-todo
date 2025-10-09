from aiogram import Bot, F, Router
from aiogram_dialog import DialogManager
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from repositories.category import CategoryRepository
from repositories.task import TaskRepository
from schemes.database import User
from utils.i18n import i18n

router = Router()

@router.message(F.text == "Статистика моих задач 📊", F.chat.type == "private")
@router.message(Command("stats"), F.chat.type == "private")
async def command_start_private(message: Message, dialog_manager: DialogManager, state: FSMContext, bot: Bot, user: User):
	await state.clear()
	await dialog_manager.reset_stack()

	categories = await CategoryRepository.get_categories(user_id=user.id)
	tasks = await TaskRepository.get_tasks(user_id=user.id)

	stats = {
		"count_categories": len(categories),
		"count_tasks": len(tasks),
		"count_completed_tasks": 0,
		"count_failed_tasks": 0
	}

	for task in tasks:
		if task.completed:
			stats["count_completed_tasks"] += 1
		else:
			stats["count_failed_tasks"] += 1

	text = i18n.translate(namespace="commands.stats", key="message", lang=user.language_code).format(**stats)

	await message.answer(text=text)

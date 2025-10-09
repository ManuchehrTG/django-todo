from aiogram import Bot, F, Router
from aiogram_dialog import DialogManager
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.main_menu import MainMenuReplyKeyboard
from schemes.database import User
from utils.i18n import i18n

router = Router()

@router.message(Command("start"), F.chat.type == "private")
async def command_start_private(message: Message, dialog_manager: DialogManager, state: FSMContext, bot: Bot, user: User):
	await state.clear()
	await dialog_manager.reset_stack()

	await message.answer(
		text=i18n.translate(namespace="commands.start", key="message", lang=user.language_code),
		reply_markup=MainMenuReplyKeyboard.main_menu()
	)

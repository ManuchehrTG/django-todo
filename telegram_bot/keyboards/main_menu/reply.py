from aiogram.utils.keyboard import ReplyKeyboardBuilder

class MainMenuReplyKeyboard:
	@staticmethod
	def main_menu():
		builder = ReplyKeyboardBuilder()
		builder.button(text="Мои задачи 📑")
		builder.button(text="Статистика моих задач 📊")
		builder.adjust(1)
		return builder.as_markup(resize_keyboard=True)

from aiogram.filters.callback_data import CallbackData

class BaseCallbackData(CallbackData, prefix="base"):
	"""
	role - Роль пользователя (например: user/admin/moder)
	action - Действие (например: menu, back, open, close)
	"""
	role: str
	action: str

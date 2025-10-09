from aiogram.fsm.state import StatesGroup, State

class StateCategories(StatesGroup):
	categories = State()
	create_category = State()

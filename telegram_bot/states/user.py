from aiogram.fsm.state import StatesGroup, State

class StateTest(StatesGroup):
	categories = State()
	tasks = State()

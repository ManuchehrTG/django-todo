from aiogram.fsm.state import StatesGroup, State

class StateTasks(StatesGroup):
	tasks = State()
	create_task_title = State()
	create_task_description = State()
	create_task_due_date = State()

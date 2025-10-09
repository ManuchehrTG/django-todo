from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, SwitchTo, Button, Row, Back
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput

from dialogs.categories.states import StateCategories

from .getters import get_tasks_data
from .handlers.callbacks.tasks import on_task_selected, back_to_categories
from .handlers.callbacks.create_task import on_description_skip
from .handlers.messages.create_task import on_title_input, on_description_input, on_due_date_input
from .states import StateTasks

tasks_window = Window(
	Format("{text}"),
	ScrollingGroup(
		Select(
			Format("{item.title}"),
			id="tasks_select",
			item_id_getter=lambda x: x.id,
			items="tasks",
			on_click=on_task_selected,
		),
		id="tasks_scroll",
		width=1,
		height=5,
	),
	SwitchTo(Const("➕ Добавить задачу"), id="create_task_btn", state=StateTasks.create_task_title),
	Button(Const("← Назад"), id="back_to_categories", on_click=back_to_categories),
	# Back(Const("← Назад")),
	getter=get_tasks_data,
	state=StateTasks.tasks,
)

create_task_title_window = Window(
	Const("<b>Введите название задачи:</b>"),
	TextInput(id="task_title", on_success=on_title_input),
	SwitchTo(Const("← Назад"), id="back_to_tasks", state=StateTasks.tasks),
	state=StateTasks.create_task_title,
)

create_task_description_window = Window(
	Const("<b>Введите описание задачи (или нажмите 'Пропустить'):</b>"),
	TextInput(id="task_description", on_success=on_description_input),
	Button(Const("Пропустить ➡️"), id="skip_description", on_click=on_description_skip),
	Back(Const("← Назад")),
	state=StateTasks.create_task_description,
)

create_task_due_date_window = Window(
	Const("<b>Введите дедлайн (в формате YYYY-MM-DD HH:MM):</b>"),
	TextInput(id="task_due_date", on_success=on_due_date_input),
	Back(Const("← Назад")),
	state=StateTasks.create_task_due_date,
)

dialog = Dialog(
	tasks_window,
	create_task_title_window, create_task_description_window, create_task_due_date_window
)

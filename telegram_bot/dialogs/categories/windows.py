from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, SwitchTo, Button, Row, Back
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput

from utils.i18n import i18n

from .getters import get_categories_data
from .handlers.callbacks.categories import on_category_selected
from .handlers.messages.create_category import on_category_create
from .states import StateCategories

categories_window = Window(
	Format("{text}"),
	ScrollingGroup(
		Select(
			Format("{item.name}"),
			id="categories_select",
			item_id_getter=lambda x: x.id,
			items="categories",
			on_click=on_category_selected,
		),
		id="categories_scroll",
		width=1,
		height=5,
	),
	SwitchTo(Const("➕ Добавить категорию"), id="create_category_btn", state=StateCategories.create_category),
	getter=get_categories_data,
	state=StateCategories.categories,
)

create_category_window = Window(
	Const("<b>Введите название категории:</b>"),
	TextInput(id="category_title", on_success=on_category_create),
	SwitchTo(Const("← Назад"), id="back_to_categories", state=StateCategories.categories),
	state=StateCategories.create_category,
)

dialog = Dialog(categories_window, create_category_window)

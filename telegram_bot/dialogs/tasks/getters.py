import json

from repositories.task import TaskRepository
from schemes.database import User
from utils.i18n import i18n

async def get_tasks_data(dialog_manager, **kwargs):
	user = User(**json.loads(dialog_manager.start_data["user"]))
	category_id = (
		dialog_manager.start_data.get("category_id") or
		dialog_manager.dialog_data.get("category_id")
	)
	dialog_manager.dialog_data["category_id"] = category_id

	tasks = await TaskRepository.get_tasks(category_id=category_id, user_id=user.id)
	text = i18n.translate(namespace="tasks.tasks", lang=user.language_code)
	data = {
		"tasks": tasks,
		"tasks_count": len(tasks)
	}

	if tasks:
		data["text"] = text["tasks_found"]["message"]
	else:
		data["text"] = text["tasks_not_found"]["message"]

	return data
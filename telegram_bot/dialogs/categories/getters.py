import json

from repositories.category import CategoryRepository
from schemes.database import User
from utils.i18n import i18n

async def get_categories_data(dialog_manager, **kwargs):
	user = User(**json.loads(dialog_manager.start_data["user"]))

	categories = await CategoryRepository.get_categories(user_id=user.id)
	text = i18n.translate(namespace="categories.categories", lang=user.language_code)
	data = {
		"categories": categories,
		"categories_count": len(categories)
	}

	if categories:
		data["text"] = text["categories_found"]["message"]
	else:
		data["text"] = text["categories_not_found"]["message"]

	return data

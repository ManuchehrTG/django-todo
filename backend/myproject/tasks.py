from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail

from configs import telegram_bot_config
from backend.lib.http import get_http_client

from .models import Task

@shared_task
def send_task_notification(user_id: int, task_title: str, task_category_name: str, task_completed: bool):
	print(f"📩 Sending notification for user {user_id}: {task_title}")

	task_status = "Выполнено ✅" if task_completed else "Просрочено ❌"

	url = f"https://api.telegram.org/bot{telegram_bot_config.TOKEN}"
	params = {
		"chat_id": user_id,
		"text": (
			"<b>🔔 Напоминание!</b>\n\n"
			f"<b>Задача:</b> {task_title}\n"
			f"<b>Категория:</b> {task_category_name}\n"
			f"<b>Статус:</b> {task_status}"
		),
		"parse_mode": "HTML"
	}
	sync_http_client = get_http_client(mode="sync")
	response = sync_http_client.post(url=f"{url}/sendMessage", data=params)

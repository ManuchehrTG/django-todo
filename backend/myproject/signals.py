from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Task
from .tasks import send_task_notification

@receiver(post_save, sender=Task)
def task_post_save(sender, instance, created, **kwargs):
	# Данный сигнал необходим как аналог preform_create, который срабатывает из Админки, API, Shell 
	if not created:
		return

	# Проверка на погрешность, если DUE_DATE уже наступило, то обрабатываем задачу сразу
	if instance.due_date <= timezone.now():
		send_task_notification.delay(instance.user.id, instance.title, instance.category.name, instance.completed)
	else:
		send_task_notification.apply_async(
			args=(instance.user.id, instance.title, instance.category.name, instance.completed),
			eta=instance.due_date
		)

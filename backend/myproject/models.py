import secrets
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

def generate_random_id():
	"""Генерирует случайный ID для моделей"""
	return secrets.token_urlsafe(12)

class TelegramUser(models.Model):
	id = models.BigIntegerField(primary_key=True)
	username = models.CharField(max_length=32, blank=True, null=True)
	first_name = models.CharField(max_length=64, blank=True, null=True)
	language_code = models.CharField(max_length=2, blank=True, null=True)
	is_admin = models.BooleanField(default=False)
	is_block = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.id} ({self.username})"

class Category(models.Model):
	id = models.CharField(primary_key=True, max_length=16, unique=True, default=generate_random_id)
	name = models.CharField(max_length=100)
	user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
	created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	created_at = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.name

class Task(models.Model):
	id = models.CharField(primary_key=True, max_length=16, unique=True, default=generate_random_id)
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True, null=True)
	user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	due_date = models.DateTimeField()
	completed = models.BooleanField(default=False)
	created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

from rest_framework import serializers

from .models import TelegramUser, Task, Category

class TelegramUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = TelegramUser
		fields = '__all__'
		read_only_fields = ['created_at', 'updated_at']

class CategorySerializer(serializers.ModelSerializer):
	user = TelegramUserSerializer(read_only=True)

	class Meta:
		model = Category
		fields = '__all__'
		read_only_fields = ['created_at']

class TaskSerializer(serializers.ModelSerializer):
	category = CategorySerializer(read_only=True)
	user = TelegramUserSerializer(read_only=True)

	class Meta:
		model = Task
		fields = '__all__'
		read_only_fields = ['created_at', 'updated_at']

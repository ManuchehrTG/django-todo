from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import TelegramUser, Task, Category
from .serializers import TelegramUserSerializer, TaskSerializer, CategorySerializer

class TelegramUserViewSet(viewsets.ModelViewSet):
	serializer_class = TelegramUserSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return TelegramUser.objects.all()

	def retrieve(self, request, pk=None):
		try:
			user = TelegramUser.objects.get(pk=pk)
			serializer = TelegramUserSerializer(user)
			return Response(serializer.data)
		except TelegramUser.DoesNotExist:
			return Response(status=404)

	def create(self, request):
		serializer = TelegramUserSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=201)

	def partial_update(self, request, pk=None):
		try:
			user = TelegramUser.objects.get(pk=pk)
		except TelegramUser.DoesNotExist:
			return Response(status=404)

		if user.is_block:
			return Response({"detail": "User is blocked"}, status=403)

		serializer = TelegramUserSerializer(user, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)

class TaskViewSet(viewsets.ModelViewSet):
	serializer_class = TaskSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		user_id = self.request.query_params.get("user_id")
		category_id = self.request.query_params.get("category_id") #опционально, иногда может быть None

		if not user_id:
			return Task.objects.none()

		queryset = Task.objects.filter(user_id=user_id)

		if category_id:
			queryset = queryset.filter(category_id=category_id)

		return queryset.order_by("-created_at")

	def perform_create(self, serializer):
		user_id = self.request.data.get("user_id")
		category_id = self.request.data.get("category_id")

		user = TelegramUser.objects.get(pk=user_id)
		category = Category.objects.get(pk=category_id)

		serializer.save(user=user, category=category)

	# @action(detail=False, methods=['get'])
	# def overdue(self, request):
	# 	overdue_tasks = self.get_queryset().filter(
	# 		due_date__lt=timezone.now(),
	# 		completed=False
	# 	)
	# 	serializer = self.get_serializer(overdue_tasks, many=True)
	# 	return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
	serializer_class = CategorySerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		user_id = self.request.query_params.get("user_id")
		if not user_id:
			return Category.objects.none()
		return Category.objects.filter(user=user_id)

	def perform_create(self, serializer):
		user_id = self.request.data.get("user_id")
		user = TelegramUser.objects.get(pk=user_id)
		serializer.save(user=user)

from django.contrib import admin

from .models import TelegramUser, Category, Task

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
	list_display = ('id', 'first_name', 'username', 'is_admin', 'is_block')
	list_filter = ('id', 'first_name', 'username', 'is_admin', 'is_block', 'created_at', 'updated_at')
	search_fields = ('id', 'first_name', 'username')
	list_editable = ('is_admin', 'is_block')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'user', 'created_at')
	list_filter = ('user', 'created_at')
	search_fields = ('name', 'user__username')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	list_display = ('title', 'user', 'category', 'completed', 'created_at')
	list_filter = ('completed', 'category', 'user')
	search_fields = ('title', 'description')
	list_editable = ('completed',)

	actions = ['mark_completed', 'mark_incomplete']

	def mark_completed(self, request, queryset):
		updated = queryset.update(completed=True)
		self.message_user(request, f'{updated} задач отмечено как выполненные')
	mark_completed.short_description = 'Отметить как выполненные'

	def mark_incomplete(self, request, queryset):
		updated = queryset.update(completed=False)
		self.message_user(request, f'{updated} задач отмечено как не выполненные')
	mark_incomplete.short_description = 'Отметить как не выполненные'

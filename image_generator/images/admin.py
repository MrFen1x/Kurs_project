# Регистрация модели ImageConfig в админ-панели
from django.contrib import admin
from .models import ImageConfig, User

@admin.register(ImageConfig)
class ImageConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'color', 'amplitude', 'scale', 'created_at')  # Отображаемые поля
    list_filter = ('user', 'created_at')  # Фильтры
    search_fields = ('user__username', 'color')  # Поиск по имени пользователя и цвету
    readonly_fields = ('created_at',) # Поле только для чтения
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'is_superuser', 'last_login')  # Отображаемые поля

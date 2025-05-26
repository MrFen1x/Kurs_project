from django.urls import path
from . import views

urlpatterns = [
    # Маршрут для генерации изображения
    path('generate/', views.generate_image_view, name='generate_image'),
    # Маршрут для личной галереи
    path('gallery/my/', views.my_gallery, name='my_gallery'),
    # Маршрут для публичной галереи
    path('gallery/public/', views.public_gallery, name='public_gallery'),
    # Маршрут для галереи конкретного пользователя
    path('gallery/user/<str:username>/', views.user_gallery, name='user_gallery'),
    # Маршрут для удаления конфигурации
    path('config/<int:pk>/delete/', views.delete_config, name='delete_config'),
    # Маршрут для генерации изображения из конфигурации
    path('config/<int:pk>/image/', views.generate_image_from_config, name='generate_image_from_config'),
    # Маршрут для редактирования конфигурации
    path('config/<int:pk>/edit/', views.edit_config, name='edit_config'),
    # Маршрут для просмотра изображения
    path('config/<int:pk>/', views.image_detail, name='image_detail'),
    # Маршрут для регистрации
    path('register/', views.register, name='register'),
]
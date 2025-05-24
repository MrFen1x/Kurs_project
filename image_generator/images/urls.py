from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_image_view, name='generate_image'),
    path('gallery/my/', views.my_gallery, name='my_gallery'),
    path('gallery/public/', views.public_gallery, name='public_gallery'),
    path('config/<int:pk>/delete/', views.delete_config, name='delete_config'),
    path('config/<int:pk>/image/', views.generate_image_from_config, name='generate_image_from_config'),
    path('config/<int:pk>/edit/', views.edit_config, name='edit_config'),
    path('config/<int:pk>/', views.image_detail, name='image_detail'),  # New route for image detail
    path('register/', views.register, name='register'),
]
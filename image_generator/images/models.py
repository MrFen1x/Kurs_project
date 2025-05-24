from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    # Указываем уникальные related_name для избежания конфликта
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='images_user_groups',  # Уникальное имя для обратного аксессора
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='images_user_permissions',  # Уникальное имя для обратного аксессора
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

class ImageConfig(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='image_configs')
    color = models.CharField(max_length=7, default='#0000FF')  # HEX-код цвета, по умолчанию синий
    amplitude = models.FloatField(
        validators=[MinValueValidator(0.1), MaxValueValidator(10.0)], default=1.0
    )  # Амплитуда косинуса
    scale = models.FloatField(
        validators=[MinValueValidator(0.1), MaxValueValidator(10.0)], default=1.0
    )  # Масштаб графика
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Config by {self.user.username} ({self.created_at})"
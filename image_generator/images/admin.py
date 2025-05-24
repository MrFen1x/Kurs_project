from django.contrib import admin
from .models import ImageConfig

@admin.register(ImageConfig)
class ImageConfigAdmin(admin.ModelAdmin):
    list_display = ('user', 'color', 'amplitude', 'scale', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__username', 'color')
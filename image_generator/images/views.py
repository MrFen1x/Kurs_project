from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
import cv2
import numpy as np
import io
import base64
from images.models import ImageConfig
from images.forms import CustomUserCreationForm
from django.contrib.auth import get_user_model

# Получение модели пользователя
User = get_user_model()

# Кастомный декоратор для проверки прав владельца или админа
def owner_or_admin_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        config_id = kwargs.get('pk')
        config = get_object_or_404(ImageConfig, pk=config_id)
        if config.user == request.user or request.user.is_staff:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Вы не имеете прав доступа.")
    return wrapper

# Генерация изображения на основе параметров (только для авторизованных)
@login_required
def generate_image_view(request):
    image_base64 = None
    if request.method == 'POST':
        color = request.POST.get('color', '#0000FF')
        amplitude = float(request.POST.get('amplitude', 1.0))
        scale = float(request.POST.get('scale', 1.0))

        # Image parameters
        width, height = int(600 * scale), int(400 * scale)
        image = np.ones((height, width, 3), dtype=np.uint8) * 255  # White background

        # Convert HEX color to RGB
        color = color.lstrip('#')
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)

        # Generate cosine function points
        x = np.linspace(0, 2 * np.pi, width)
        y = amplitude * 100 * np.cos(x)  # Scale amplitude for visibility
        y = (height / 2 - y).astype(int)  # Center on Y-axis

        # Draw cosine line
        for i in range(width - 1):
            cv2.line(
                image,
                (i, y[i]),
                (i + 1, y[i + 1]),
                (b, g, r),  # OpenCV uses BGR
                thickness=2
            )

        # Draw axes
        cv2.line(image, (0, height // 2), (width, height // 2), (0, 0, 0), 1)  # X-axis
        cv2.line(image, (width // 2, 0), (width // 2, height), (0, 0, 0), 1)  # Y-axis

        # Save to buffer and convert to base64
        _, buffer = cv2.imencode('.png', image)
        image_base64 = base64.b64encode(buffer).decode('utf-8')

        # Save parameters
        ImageConfig.objects.create(
            user=request.user,
            color=color,
            amplitude=amplitude,
            scale=scale
        )

    return render(request, 'generate_image.html', {'image_base64': image_base64})

# Генерация изображения из сохранённой конфигурации (для ссылок в галерее)
def generate_image_from_config(request, pk):
    config = get_object_or_404(ImageConfig, pk=pk)
    width, height = int(600 * config.scale), int(400 * config.scale)
    image = np.ones((height, width, 3), dtype=np.uint8) * 255  # White background

    # Convert HEX color to RGB
    color = config.color.lstrip('#')
    r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)

    # Generate cosine function points
    x = np.linspace(0, 2 * np.pi, width)
    y = config.amplitude * 100 * np.cos(x)  # Scale amplitude for visibility
    y = (height / 2 - y).astype(int)  # Center on Y-axis

    # Draw cosine line
    for i in range(width - 1):
        cv2.line(
            image,
            (i, y[i]),
            (i + 1, y[i + 1]),
            (b, g, r),  # OpenCV uses BGR
            thickness=2
        )

    # Draw axes
    cv2.line(image, (0, height // 2), (width, height // 2), (0, 0, 0), 1)  # X-axis
    cv2.line(image, (width // 2, 0), (width // 2, height), (0, 0, 0), 1)  # Y-axis

    # Save to buffer
    _, buffer = cv2.imencode('.png', image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    return image_base64

# Отображение отдельного изображения
def image_detail(request, pk):
    config = get_object_or_404(ImageConfig, pk=pk)
    image_base64 = generate_image_from_config(request, pk)
    return render(request, 'image_detail.html', {'config': config, 'image_base64': image_base64})

# Личная галерея пользователя
@login_required
def my_gallery(request):
    configs = ImageConfig.objects.filter(user=request.user)
    return render(request, 'gallery.html', {'configs': configs})

# Публичная галерея (отображение уникальных авторов)
def public_gallery(request):
    # Получение уникальных пользователей, создавших конфигурации
    authors = User.objects.filter(image_configs__isnull=False).distinct()
    return render(request, 'gallery.html', {'authors': authors})

# Галерея конкретного пользователя
def user_gallery(request, username):
    user = get_object_or_404(User, username=username)
    configs = ImageConfig.objects.filter(user=user)
    return render(request, 'gallery.html', {'configs': configs, 'gallery_user': user})

# Удаление конфигурации (ограничено владельцем или админом)
@owner_or_admin_required
def delete_config(request, pk):
    config = get_object_or_404(ImageConfig, pk=pk)
    config.delete()
    return redirect('my_gallery')

# Редактирование конфигурации (только для админов)
@staff_member_required
def edit_config(request, pk):
    config = get_object_or_404(ImageConfig, pk=pk)
    if request.method == 'POST':
        config.color = request.POST.get('color', config.color)
        config.amplitude = float(request.POST.get('amplitude', config.amplitude))
        config.scale = float(request.POST.get('scale', config.scale))
        config.save()
        return redirect('public_gallery')
    return render(request, 'edit_config.html', {'config': config})

# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
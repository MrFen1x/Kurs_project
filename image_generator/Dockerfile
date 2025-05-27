# Установка базового образа Python
FROM python:3.13-slim

# Установка рабочей директории
WORKDIR /app

# Обновление pip до последней версии
RUN pip install --upgrade pip

# Копирование зависимостей
COPY requirements.txt .

# Установка системных зависимостей и Python-пакетов
RUN apt-get update && apt-get install -y \
    libopencv-dev \
    python3-opencv \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Установка переменной окружения для Django
ENV PYTHONUNBUFFERED=1

# Запуск Django-сервера
CMD ["python", "manage.py", "runserver", "localhost:8000"]
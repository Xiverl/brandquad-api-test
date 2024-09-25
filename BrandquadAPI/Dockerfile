# Используем официальный образ Python
FROM python:3.10

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект в контейнер
COPY . .

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Запускаем команду при старте контейнера
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "BrandquadAPI.wsgi"]

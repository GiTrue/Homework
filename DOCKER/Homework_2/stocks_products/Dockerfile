# Используем компактный Python на Alpine Linux
FROM python:3.9-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apk add --no-cache gcc musl-dev libffi-dev sqlite

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Автоматически применяем миграции
RUN python manage.py migrate --noinput

# Открываем порт
EXPOSE 8000

# Точка входа и запуск сервера
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
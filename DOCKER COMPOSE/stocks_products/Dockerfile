FROM python:3.10-slim

WORKDIR /app

# Устанавливаем зависимости для postgres
RUN apt-get update && apt-get install -y libpq-dev gcc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Собираем статику (нужно для Nginx)
RUN python manage.py collectstatic --noinput

EXPOSE 8000
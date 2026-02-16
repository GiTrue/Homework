FROM python:3.9-alpine

# Устанавливаем зависимости для работы с Postgres в Alpine
RUN apk add --no-cache gcc musl-dev libffi-dev postgresql-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Экспертный подход: разделяем команду запуска
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
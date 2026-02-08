# 1. Базовый образ с Python
FROM python:3.10-slim

# 2. Установка рабочей директории внутри контейнера
WORKDIR /app

# 3. Копирование файла зависимостей
# (Убедись, что файл requirements.txt лежит в этой же папке)
COPY requirements.txt .

# 4. Установка библиотек
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копирование всего остального кода проекта в контейнер
COPY . .

# 6. Установка переменных окружения
# Используем твой секретный ключ из памяти
ENV SECRET_KEY=En43_Qw89:UtyDgML12
ENV DEBUG=True
ENV ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# 7. Открываем порт, на котором работает Django
EXPOSE 8000

# 8. Команда для запуска: 
# сначала применяем миграции (создаем базу sqlite), затем запускаем сервер
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
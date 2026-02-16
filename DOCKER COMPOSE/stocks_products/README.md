# Склады и товары (Docker edition)

# Домашнее задание: Docker Compose (Склады и товары)

Этот проект демонстрирует развертывание Django-приложения в связке с базой данных PostgreSQL и прокси-сервером Nginx с помощью Docker Compose.

## Архитектура проекта
Конфигурация состоит из 3-х контейнеров:
1. **db**: База данных PostgreSQL (образ `postgres:13`).
2. **backend**: Django-приложение, запущенное через WSGI-сервер `Gunicorn`.
3. **nginx**: Веб-сервер, который отдает статику и перенаправляет запросы к Django.

---

## Как запустить проект

1. Соберите и запустите проект одной командой:
   ```bash
   docker-compose up --build -d
2. Если миграции не применились автоматически, выполните:
   docker-compose exec backend python manage.py migrate
   
2. Что происходит автоматически при запуске:
Docker создает внутреннюю сеть для общения контейнеров.

Запускается PostgreSQL и проходит проверку готовности (healthcheck).

Выполняются миграции Django и сбор статических файлов (collectstatic).

Запускаются процессы Gunicorn и Nginx.

3. Проверка:
Приложение доступно по адресу: http://localhost (порт 80).


## Важные команды
Остановить все контейнеры:
docker-compose down

Просмотр логов приложения:
docker-compose logs -f backend

Создать суперпользователя:
docker-compose exec backend python manage.py createsuperuser
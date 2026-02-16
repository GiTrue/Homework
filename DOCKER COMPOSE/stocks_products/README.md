# Склады и товары (Docker edition)

# Домашнее задание: Docker Compose

Этот проект демонстрирует развертывание Django-приложения в связке с базой данных PostgreSQL и прокси-сервером Nginx с помощью Docker Compose.

## Архитектура проекта
Конфигурация состоит из 3-х контейнеров:
1. **db**: База данных PostgreSQL (образ `postgres:13`).
2. **backend**: Django-приложение, запущенное через WSGI-сервер `Gunicorn`.
3. **nginx**: Веб-сервер, который отдает статику и перенаправляет запросы к Django.

---

## Как запустить проект

Все действия выполняются одной командой из корневой директории проекта:

1. **Сборка и запуск:**
   ```bash
   docker-compose up --build
   
2. Что произойдет автоматически:

Docker создаст сеть для контейнеров.

Запустится PostgreSQL и дождется готовности (healthcheck).

Выполнятся миграции Django (python manage.py migrate).

Сберется статика (collectstatic).

Запустится Gunicorn и Nginx.

3. Проверка:
Откройте браузер по адресу: http://localhost (порт 80, стандартный).


## Важные команды
Остановить проект:
docker-compose down

Просмотр логов приложения:
docker-compose logs -f backend

Создать суперпользователя:
docker-compose exec backend python manage.py createsuperuser
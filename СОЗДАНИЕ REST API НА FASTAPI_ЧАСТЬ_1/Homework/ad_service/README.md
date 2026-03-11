# Advertisement Service (FastAPI)

Сервис объявлений купли/продажи.

## Как запустить

1. Клонируйте репозиторий.
2. Создайте файл `.env` на основе `.env.example`:
   ```bash
   cp .env.example .env
   
3. Запустите проект через Docker Compose:
   ```bash
   docker-compose up --build
   
## Использование

API будет доступно по адресу: http://localhost:8080

Интерактивная документация (Swagger): http://localhost:8080/docs

## Эндпоинты

POST /advertisement — Создание объявления

GET /advertisement/{id} — Получение по ID

PATCH /advertisement/{id} — Обновление

DELETE /advertisement/{id} — Удаление

GET /advertisement?title=текст&author=имя — Поиск
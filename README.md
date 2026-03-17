# Dictionary Words Service

Приложение на FastAPI для управления словами (создание, получение, обновление, удаление) с асинхронной работой с базой данных.

## Содержание
- Требования
- Конфигурация
- Запуск в Docker
- Локальный запуск
- Запуск тестов
- Запуск тестов через Docker
- API — основные эндпоинпты
- Примеры запросов (из OpenAPI)
- Структура проекта
- Контакты

## Требования
- Python 3.12+
- MongoDB (или контейнер с БД через Docker). Версия MongoDB, используемая в docker-compose: `mongodb/mongodb-community-server:8.0-ubuntu2204`.
- Рекомендуется использовать виртуальное окружение

Зависимости перечислены в `requirements.txt`.

## Конфигурация
Проект читает переменные окружения из файлов в папке `conf` (например, `.env.dev`, `.env.test`, `.env.db`, `.env.testdb`).

Пример `.env.dev` (для разработки / Docker):

```dotenv
DB_PREFIX=mongodb
DB_NAME=dictionary-words-db
DB_HOST=app_db  # при запуске через docker-compose — имя сервиса (app_db)
DB_USER=pyuser
DB_PASSWORD=float123
DB_PORT=27017
```

Пример `.env.test` (для тестов, локально):

```dotenv
DB_PREFIX=mongodb
DB_NAME=dictionary-words-db-test
DB_HOST=localhost
DB_USER=pyuser
DB_PASSWORD=float123
DB_PORT=27017
```

Файлы для конфигурации контейнера БД (пример):

`conf/.env.db`:

```dotenv
MONGODB_INITDB_ROOT_USERNAME=pydev
MONGODB_INITDB_ROOT_PASSWORD=strongpassword123
MONGODB_INITDB_DATABASE=words-db
OUTER_PORT=27018
```

`conf/.env.testdb` (для тестовой БД в docker-compose):

```dotenv
MONGO_INITDB_ROOT_USERNAME=pydev
MONGO_INITDB_ROOT_PASSWORD=float123
MONGO_INITDB_DATABASE=words-db
```

Убедитесь, что указанные базы созданы и доступны перед запуском (или используйте docker-compose, который поднимает БД).

## Запуск в Docker
1. Создайте/обновите `conf/.env.dev` с нужными переменными окружения (см. выше).
2. Из корня проекта выполните:

```bash
./run_app.sh
# или
docker-compose down && docker-compose up --build app
```

При запуске в Docker в `.env.dev` должен быть `DB_HOST=app_db` (имя сервиса из `docker-compose.yml`).

## Локальный запуск
1. Создайте виртуальное окружение:

```bash
python -m venv env
source env/bin/activate    # Linux/macOS
# .\env\Scripts\activate # Windows
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Создайте/настройте `conf/.env.dev` (DB_HOST=localhost для локального запуска) и запустите приложение:

```bash
python -m uvicorn app.main:app --reload
```

Или используйте предлагаемые скрипты в `sh/`.

## Запуск тестов (локально)
1. Создайте `conf/.env.test` с настройками тестовой БД (см. выше).
2. Активируйте виртуальное окружение и выполните:

```bash
pytest -v test
```

Тесты находятся в директории `test` и включают unit и end-to-end тесты.

## Запуск тестов через Docker
Этот репозиторий содержит сервисы `test_app` и `test_db` в `docker-compose.yml`.

1. Убедитесь, что `conf/.env.test` и `conf/.env.testdb` заполнены (для контейнера тестовой БД). Пример `conf/.env.testdb` есть выше.
2. Из корня проекта выполните:

```bash
# Собрать образ и поднять тестовые контейнеры (включая MongoDB тестовую БД)
docker-compose up --build test_db test_app
```

3. Контейнер `test_app` запустит скрипт `sh/run_test.sh`, который запускает тесты и сохраняет отчёты в папке `reports` (см. `docker/test.Dockerfile`).

После завершения можно забрать отчёты из `reports/` на хостовой машине (в docker-compose volume смонтирована папка `./reports`).

## API — основные эндпоинпты
Базовый префикс маршрутов слов: `/users/{user_id}/words`

- POST `/users/{user_id}/words/` — создать слово
  - Код ответа: 201
  - Тело запроса: JSON (пример в схемах `app/schemas/requests.py`)

- GET `/users/{user_id}/words/` — получить список слов пользователя
  - Код ответа: 200

- GET `/users/{user_id}/words/{word_id}/` — получить слово по id
  - Код ответа: 200

- PUT `/users/{user_id}/words/{word_id}/` — обновить слово
  - Код ответа: 200

- DELETE `/users/{user_id}/words/{word_id}/` — удалить слово
  - Код ответа: 200

Подробнее о форматах запросов/ответов смотрите в `app/schemas/requests.py` и `app/schemas/responses.py`.

## Примеры запросов (из OpenAPI)
Ниже приведены примерные запросы и ожидаемые ответы для каждого эндпоинта, сформированные по вашей OpenAPI-спецификации и схемам.

1) Создание слова — POST /users/{user_id}/words/

Пример запроса (cURL):

```bash
curl -X POST http://localhost:8000/users/1/words/ \
  -H 'Content-Type: application/json' \
  -d '{
    "text": "apple",
    "collections": [{"id": "fruits", "name": "Fruits"}],
    "translations": ["яблоко"]
  }'
```

Тело запроса (JSON):

```json
{
  "text": "apple",
  "collections": [
    {"id": "fruits", "name": "Fruits"}
  ],
  "translations": ["яблоко"]
}
```

Пример успешного ответа (201 Created, `WordResponseEntity`):

```json
{
  "id": "644d2f0a-1a2b-4c5d-9e6f-1234567890ab",
  "text": "apple",
  "collections": [
    {"id": "fruits", "name": "Fruits"}
  ],
  "user_id": 1,
  "translations": ["яблоко"],
  "created_at": "2026-03-17T12:34:56.789Z",
  "updated_at": "2026-03-17T12:34:56.789Z"
}
```

2) Получение списка слов — GET /users/{user_id}/words/

Пример запроса (cURL):

```bash
curl http://localhost:8000/users/1/words/
```

Пример успешного ответа (200 OK):

```json
[
  {
    "id": "644d2f0a-1a2b-4c5d-9e6f-1234567890ab",
    "text": "apple",
    "collections": [{"id": "fruits", "name": "Fruits"}],
    "user_id": 1,
    "translations": ["яблоко"],
    "created_at": "2026-03-17T12:34:56.789Z",
    "updated_at": "2026-03-17T12:34:56.789Z"
  },
  {
    "id": "8f3c2e1b-2b3a-4d5c-9a7b-0987654321cd",
    "text": "book",
    "collections": [{"id": "objects", "name": "Objects"}],
    "user_id": 1,
    "translations": ["книга"],
    "created_at": "2026-03-16T10:20:30.400Z",
    "updated_at": "2026-03-16T10:20:30.400Z"
  }
]
```

3) Получение слова по id — GET /users/{user_id}/words/{word_id}/

Пример запроса (cURL):

```bash
curl http://localhost:8000/users/1/words/644d2f0a-1a2b-4c5d-9e6f-1234567890ab/
```

Пример успешного ответа (200 OK):

```json
{
  "id": "644d2f0a-1a2b-4c5d-9e6f-1234567890ab",
  "text": "apple",
  "collections": [{"id": "fruits", "name": "Fruits"}],
  "user_id": 1,
  "translations": ["яблоко"],
  "created_at": "2026-03-17T12:34:56.789Z",
  "updated_at": "2026-03-17T12:34:56.789Z"
}
```

4) Обновление слова — PUT /users/{user_id}/words/{word_id}/

Пример запроса (cURL):

```bash
curl -X PUT http://localhost:8000/users/1/words/644d2f0a-1a2b-4c5d-9e6f-1234567890ab/ \
  -H 'Content-Type: application/json' \
  -d '{
    "translations": ["яблоко", "эппл"],
    "collections": [{"id": "fruits", "name": "Fruits"}]
  }'
```

Тело запроса (JSON) — `UpdateWordRequest` (поля могут быть null):

```json
{
  "translations": ["яблоко", "эппл"],
  "collections": [{"id": "fruits", "name": "Fruits"}]
}
```

Пример успешного ответа (200 OK): обновлённый `WordResponseEntity`:

```json
{
  "id": "644d2f0a-1a2b-4c5d-9e6f-1234567890ab",
  "text": "apple",
  "collections": [{"id": "fruits", "name": "Fruits"}],
  "user_id": 1,
  "translations": ["яблоко", "эппл"],
  "created_at": "2026-03-17T12:34:56.789Z",
  "updated_at": "2026-03-17T15:00:00.000Z"
}
```

5) Удаление слова — DELETE /users/{user_id}/words/{word_id}/

Пример запроса (cURL):

```bash
curl -X DELETE http://localhost:8000/users/1/words/644d2f0a-1a2b-4c5d-9e6f-1234567890ab/
```

Пример успешного ответа (200 OK):

```json
{
  "id": "644d2f0a-1a2b-4c5d-9e6f-1234567890ab",
  "text": "apple",
  "collections": [{"id": "fruits", "name": "Fruits"}],
  "user_id": 1,
  "translations": ["яблоко"],
  "created_at": "2026-03-17T12:34:56.789Z",
  "updated_at": "2026-03-17T12:34:56.789Z"
}
```

## Структура проекта (кратко)
- app/ — исходники приложения (routers, services, models, db и т.д.)
- conf/ — конфигурационные файлы и шаблоны окружения
- test/ — тесты (unit и end-to-end)
- docker/ — Dockerfile'ы
- sh/ — утилиты запуска


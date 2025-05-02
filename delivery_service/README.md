# Сервис международной доставки

Backend‑приложение на FastAPI для учёта посылок и расчёта стоимости доставки. Реализует регистрацию посылок, периодический расчёт стоимости (Celery), логирование в MongoDB и простой аналитический API.

---

## Быстрый старт (Docker)

```bash
# 1. Клонируем репозиторий
$ git clone https://github.com/your-org/delivery_service.git
$ cd delivery_service

# 2. Заполняем переменные окружения
$ cp .env.docker.example .env.docker    # отредактируйте при необходимости

# 3. Собираем и поднимаем стек
$ docker compose up -d --build

# 4. Проверяем состояние
$ docker compose ps --status=running

# 5. Swagger → http://localhost:8000/docs
```

| Сервис          | Образ           | Порт | Назначение                          |
|-----------------|-----------------|------|-------------------------------------|
| **app**         | `delivery-service` | 8000 | FastAPI + Celery‑задачи              |
| **celery_worker**| тот же образ    | —    | фоновый расчёт стоимости            |
| **celery_beat** | тот же образ    | —    | планировщик задач (каждые 5 минут)  |
| **postgres**    | `postgres:16`   | 5433 | База данных + health‑check          |
| **redis**       | `redis:7`       | 6379 | Брокер Celery / кэш                |
| **mongo**       | `mongo:6`       | 27017| Хранение логов аналитики            |

> `docker compose logs -f app` — смотреть вывод приложения.

---

## Переменные окружения

| Переменная               | Значение по умолчанию (docker) | Описание                              |
|--------------------------|--------------------------------|---------------------------------------|
| `SESSION_SECRET`         | —                              | Секрет для подписи cookie сессии      |
| `POSTGRES_*`             | см. `.env.docker.example`      | Подключение к Postgres                |
| `REDIS_URL`              | `redis://redis:6379`           | Брокер / кэш Redis                    |
| `MONGO_URL`              | `mongodb://mongo:27017`        | MongoDB для логов                     |
| `CELERY_BROKER_URL`      | `${REDIS_URL}`                 | Celery broker                         |
| `CELERY_RESULT_BACKEND`  | `${REDIS_URL}`                 | Celery backend                        |

*Локально* приложение читает **`.env`**, а в контейнерах используется **`.env.docker`** через `env_file:`.

---

## Локальная разработка (Poetry)

```bash
# Устанавливаем зависимости
$ poetry install
$ poetry shell

# Поднимаем Postgres / Redis / Mongo докером
$ docker compose up -d postgres redis mongo

# Миграции и начальные данные
$ alembic upgrade head
$ python -m src.db.init_data

# Запуск сервера
$ uvicorn src.main:app --reload
```

---

## Тесты и линт

```bash
$ pre-commit run --all-files   # Ruff автоправка + линт
$ pytest -q                    # запуск тестов
```

Конфигурация Ruff хранится в `pyproject.toml`. Git‑хуки ставятся один раз командой `pre-commit install`.

---

## CI

GitHub Actions (`.github/workflows/ci.yml`) запускается при каждом push / PR:

1. Поднимает Postgres, Redis и Mongo.
2. Устанавливает зависимости Poetry.
3. Прогоняет миграции и сиды.
4. Запускает Ruff и pytest.

---

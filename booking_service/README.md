# Booking Service

Booking Service — это бэкенд-приложение для управления системой бронирования отелей.  
Проект построен на **Django**, **Django REST Framework**, использует **PostgreSQL** и **Poetry** для управления зависимостями. Всё запускается в **Docker**, включая поддержку локальной разработки и CI.

## Стек
- Python 3.12
- Django
- DRF (Django Rest Framework)
- PostgreSQL (через Docker Compose)
- Poetry
- Pytest
- Docker

### 1. Клонируем репозиторий

git clone https://github.com/4xperience/DevProjects.git
cd booking_service

### 2. Создаем файл .env в корне проекта

DEBUG=False
SECRET_KEY=
DATABASE_URL=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
ALLOWED_HOSTS=

### 3. Собираем и запускаем

docker-compose up --build

### 4. Миграции и суперпользователь

docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

### 5. Тесты внутри контейнера

docker-compose exec web pytest

### 6. Команды

# Активация виртуального окружения
source .venv/bin/activate

# Установка зависимостей
poetry install

# Запуск сервера разработки
poetry run python src/manage.py runserver

# Тесты
poetry run pytest



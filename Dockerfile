# 1.
FROM python:3.12-slim

# 2.
RUN apt-get update && apt-get install -y libpq-dev gcc 

# 3.
RUN pip install poetry

# 4.
WORKDIR /app

# 5.
COPY ./booking_service/pyproject.toml ./booking_service/poetry.lock ./booking_service/README.md ./

# 6.
COPY booking_service/src ./src

# 7.
RUN poetry config virtualenvs.create false \ 
    && poetry install --no-interaction --no-ansi

# 8.
ENV PYTHONPATH=/app/src

# 9.
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]

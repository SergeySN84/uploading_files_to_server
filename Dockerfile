FROM python:3.12-slim

ARG SECRET_KEY
ENV SECRET_KEY=${SECRET_KEY}

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only=main --no-root --no-interaction --no-ansi

COPY . .

# Передаём SECRET_KEY напрямую (без .env)
RUN SECRET_KEY=${SECRET_KEY} python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "api.wsgi:application", "--bind", "0.0.0.0:8000"]
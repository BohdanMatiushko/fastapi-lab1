# Базовий образ Python 3.12 (мінімальний slim-варіант)
FROM python:3.12-slim

# Налаштування середовища
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Робоча директорія
WORKDIR /app

# Встановлення Poetry
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

# Копіюємо тільки файли залежностей (для кешування шарів)
COPY pyproject.toml poetry.lock* /app/

# Встановлення залежностей
RUN poetry install --no-root

# Копіюємо весь проект
COPY . /app

# Копіюємо entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Відкриваємо порт
EXPOSE 8000

# Старт через entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
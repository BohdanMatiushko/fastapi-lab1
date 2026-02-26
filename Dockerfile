# Базовий образ Python 3.12 (мінімальний slim-варіант)
FROM python:3.12-slim

# Налаштування середовища:
# - не створювати .pyc файли
# - вивід логів без буферизації
# - версія Poetry
# - вимкнути інтерактивність
# - встановлювати залежності без створення venv
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Робоча директорія всередині контейнера
WORKDIR /app

# Встановлення Poetry
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

# Копіюємо тільки файли залежностей (для кешування шарів Docker)
COPY pyproject.toml poetry.lock* /app/

# Встановлення залежностей проекту
# --no-root означає, що сам проект як пакет не встановлюється
RUN poetry install --no-root

# Копіюємо весь проект у контейнер
COPY . /app

# Відкриваємо порт 8000
EXPOSE 8000

# Запуск FastAPI через uvicorn
# --reload потрібен для dev (автоперезавантаження при зміні коду)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
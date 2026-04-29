"""
Кореневий main.py — перенаправляє на основний додаток.
Запуск: uvicorn main:app або uvicorn app.main:app
"""
from app.main import app  # noqa: F401
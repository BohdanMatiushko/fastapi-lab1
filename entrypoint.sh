#!/bin/sh
set -e

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

# 1) Міграції
alembic upgrade head

# 2) Запуск
if [ "${RELOAD:-0}" = "1" ]; then
  exec uvicorn app.main:app --host "$HOST" --port "$PORT" --reload
else
  exec uvicorn app.main:app --host "$HOST" --port "$PORT"
fi
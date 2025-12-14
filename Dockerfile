# Stage 1: Builder
FROM python:3.11-slim-bookworm as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Final
FROM python:3.11-slim-bookworm

WORKDIR /app

# Создаем непривилегированного пользователя (Security Best Practice)
RUN addgroup --system bot && adduser --system --group bot

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*

# Копируем код проекта
COPY src/ ./src/
# Если есть alembic.ini и папка миграций
COPY alembic.ini .
COPY migrations/ ./migrations/

# Меняем владельца файлов
RUN chown -R bot:bot /app

USER bot

# Запуск. 
# Предполагается, что точка входа src/main.py.
# Используем модуль (-m) для корректного импорта пакетов.
CMD ["python", "-m", "src.main"]

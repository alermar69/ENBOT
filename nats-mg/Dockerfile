FROM python:3.13-slim AS builder

# Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Установка uv в стандартное место
COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev
COPY . .

# ---------- Stage 2: Runtime ----------
FROM python:3.13-slim AS runtime

# Копируем uv из builder
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv

WORKDIR /app
COPY --from=builder /app /app
# Устанавливаем переменные окружения
ENV PATH="/app/.venv/bin:$PATH"
CMD ["uv", "run", "migration.py"]
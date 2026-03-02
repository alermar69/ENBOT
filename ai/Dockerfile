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
CMD ["uv", "run", "main.py"]


#
#FROM python:3.13.7-bookworm AS builder
#ENV VIRTUAL_ENV=/opt/venv
#ENV CODE_PATH=/code
#RUN python3 -m venv $VIRTUAL_ENV
#WORKDIR $CODE_PATH
#COPY uv.lock pyproject.toml ${CODE_PATH}/
#RUN $VIRTUAL_ENV/bin/pip install uv && $VIRTUAL_ENV/bin/uv sync --locked --no-install-project --no-dev
#
#FROM python:3.13.7-slim-bookworm
#ARG VCS_SHA
#ARG BUILD_AT
#ENV VIRTUAL_ENV=/opt/venv
#ENV CODE_PATH=/code
#ENV PATH="$VIRTUAL_ENV/bin:$PATH"
#COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
#COPY . ${CODE_PATH}/ai
#WORKDIR $CODE_PATH/ai
#RUN echo "{\"vcs_hash\": \"${VCS_SHA}\", \"build_at\": \"${BUILD_AT}\" }" > version.yaml
#CMD ["uv", "run", "migration.py"]
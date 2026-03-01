FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app
COPY uv.lock pyproject.toml ./

RUN uv sync --locked --no-install-project --no-dev

COPY .. .

CMD ["uv", "run", "migration.py"]
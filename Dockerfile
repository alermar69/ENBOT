FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app
COPY uv.lock pyproject.toml ./

RUN #uv install --no-interaction --no-cache --no-root

## Enable bytecode compilation
#ENV UV_COMPILE_BYTECODE=1
#
## Copy from the cache instead of linking since it's a mounted volume
#ENV UV_LINK_MODE=copy
#
## Print Python and uv version for debugging
#RUN python --version && which python && uv --version
#
## Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY .. .
#
## Place executables in the environment at the front of the path
#ENV PATH="/app/.venv/bin:$PATH"
#
## Reset the entrypoint, don't invoke `uv`
#ENTRYPOINT []

# Run the python script using `uv run`
CMD ["uv", "run", "app.py"]

#CMD ["poetry", "run", "python", "app.py"]

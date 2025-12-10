# Этап 1: сборка с uv
FROM ghcr.io/astral-sh/uv:0.9.16-python3.14-bookworm 

# Настройки для оптимизации
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app
COPY pyproject.toml uv.lock ./
# Устанавливаем зависимости (кэшируется)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# В продакшине 
# PYTHONUNBUFFERED=1 → логи в реальном времени (критично для мониторинга).
# PYTHONDONTWRITEBYTECODE=1 → меньше размера образа и чистое окружение.
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# COPY . .
RUN uv --version
CMD ["uv", "run", "app/main.py"]

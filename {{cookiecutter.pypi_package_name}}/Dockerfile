# 1. Base stage: Install uv and dependencies
FROM python:3.12-slim AS base
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1
COPY pyproject.toml uv.lock ./

# 2. Development/Test stage: Includes pytest and dev tools
FROM base AS test
RUN uv sync --frozen --dev
COPY . .
# Default command for this stage
CMD ["sh", "-c", "for v in 3.10 3.11 3.12 3.13 3.14; do uv run --python $v pytest; done"]

# 3. Production stage: Minimal and secure
FROM base AS run
# Only sync production dependencies (no dev tools)
RUN uv sync --frozen --no-dev
COPY . .
# Use the app's entry point
CMD ["uv", "run", "python", "-m", "my_app"]

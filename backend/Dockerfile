FROM python:3.14 AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /backend

COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --frozen --no-dev


FROM python:3.14 AS final

WORKDIR /backend

COPY --from=builder /backend /backend
COPY . .

ENV PATH="/backend/.venv/bin:$PATH"

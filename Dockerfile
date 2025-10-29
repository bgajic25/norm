FROM python:3.10-buster AS builder

WORKDIR /app

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY ./app ./app



FROM python:3.10-slim-buster AS final

WORKDIR /app

RUN groupadd -r appuser && useradd -r -g appuser appuser

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PYTHONUNBUFFERED=1

COPY --from=builder /app/.venv ./.venv

COPY --from=builder /app/app ./app

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

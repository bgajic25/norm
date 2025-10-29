# Text Normalization Microservice

[![Language](https://img.shields.io/badge/Language-Python%203.10-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)
[![Code Style](https://img.shields.io/badge/Code%20Style-Ruff-black.svg)](https://github.com/astral-sh/ruff)

A high-performance microservice for text normalization with a pluggable, multi-language architecture. This service is designed to convert semi-structured text containing numbers, dates, and currencies into a clean, spoken-word format.

The initial implementation provides a comprehensive normalizer for the **Serbian (sr)** language.

## Key Features

-   **Multi-Language by Design**: The architecture is built on a Strategy pattern, allowing new languages to be added as self-contained modules without modifying the core service.
-   **Extensible Rule Engine**: Each language's normalization logic is implemented using a Chain of Responsibility pattern, making it easy to add, remove, or reorder normalization rules.
-   **Clean & Modern Stack**: Built with FastAPI, Pydantic, and Poetry for a modern, type-safe, and dependency-managed Python environment.
-   **Production-Ready**: Comes with a multi-stage `Dockerfile` for building small, secure, and efficient container images.
-   **Self-Documenting API**: Leverages FastAPI's automatic generation of OpenAPI and ReDoc documentation.

## Architecture Overview

The service is built on three key design patterns:

1.  **Strategy Pattern**: The top-level pattern. Each language (e.g., Serbian) is a concrete `NormalizerStrategy`. The API layer doesn't know the details of any language; it simply asks for the correct strategy.
2.  **Factory Pattern**: A `NormalizerFactory` is responsible for discovering and instantiating the correct language `Strategy` based on a language code (e.g., `"sr"`).
3.  **Chain of Responsibility Pattern**: Within each strategy, a series of `NormalizationHandler` objects are linked together. Each handler is responsible for one specific rule (e.g., `DateHandler`, `CurrencyHandler`). Text is passed through the chain, and each handler applies its transformation in a predefined order.

## API Documentation

Once the service is running, the interactive API documentation is available at:

-   **Swagger UI**: [`http://localhost:8000/docs`](http://localhost:8000/docs)
-   **ReDoc**: [`http://localhost:8000/redoc`](http://localhost:8000/redoc)

### Endpoint: `POST /api/v1/{lang}/normalize`

Normalizes a given string of text for the specified language.

**Path Parameters:**
-   `lang` (string, required): The two-letter language code (ISO 639-1) for the normalization rules to apply. Example: `sr`.

**Request Body:**
```json
{
  "text": "Tekst za normalizaciju, napisan 25.12.2023. godine, košta €1.234,56."
}
```

**Example cURL Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/sr/normalize' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Sastanak je 25.12.2023. godine. Cena je 1.500 RSD."
}' | jq
```

**Example Success Response (200 OK):**
```json
{
  "normalized_text": "Sastanak je dvadeset petog decembra dve hiljade dvadeset treće godine. Cena je hiljadu petsto dinara."
}
```

**Example Error Response (404 Not Found):**
If a language is not supported (e.g., `en`), the API will return:
```json
{
  "detail": "Language 'en' is not supported."
}
```

---

## Getting Started (Local Development)

### Prerequisites

-   Python 3.10+
-   [Poetry](https://python-poetry.org/docs/#installation) for dependency management.
-   [Docker](https://www.docker.com/get-started) (for containerized workflow).

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd text-normalizer
    ```

2.  **Install dependencies using Poetry:**
    This command will create a virtual environment (`.venv`) and install all necessary packages from `pyproject.toml`.
    ```bash
    poetry install
    ```

### Running the Service

-   **Run the FastAPI server with hot-reload:**
    ```bash
    poetry run uvicorn app.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

### Running Tests

-   **Execute the test suite with Pytest:**
    ```bash
    poetry run pytest
    ```

---

## Containerization (Docker)

This service is designed to be run as a container.

### Building the Image

Build a production-ready Docker image using the provided multi-stage `Dockerfile`.

```bash
docker build -t text-normalizer:0.1.0 .
```

### Running the Container

-   **Run in Production Mode:**
    This runs the container in detached mode from the lean, production-ready image.
    ```bash
    docker run -d --name text-normalizer-api -p 8000:8000 text-normalizer:0.1.0
    ```

-   **Run in Development Mode (with Hot-Reload):**
    This command mounts your local `app` directory into the container, allowing `uvicorn` to automatically reload on code changes.
    ```bash
    docker run -d --name text-normalizer-dev \
      -p 8000:8000 \
      -v "$(pwd)/app:/app/app" \
      text-normalizer:0.1.0 \
      uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

-   **To view logs:** `docker logs -f text-normalizer-api`
-   **To stop the container:** `docker stop text-normalizer-api`

---

## How to Add a New Language

The architecture makes it simple to add support for a new language (e.g., English - `en`).

1.  **Create the Module Directory:**
    Create a new directory inside `app/normalizers/` for the new language.
    ```
    app/normalizers/en/
    ├── __init__.py
    ├── data/
    │   └── currencies.json  # (example data file)
    ├── rules/
    │   ├── __init__.py
    │   ├── date_handler.py
    │   └── ... (other handlers)
    └── strategy.py
    ```

2.  **Add Data Files:**
    Place any language-specific data (e.g., month names, currency info) as JSON files in the `data/` directory.

3.  **Implement Rule Handlers:**
    In the `rules/` directory, create classes inheriting from `NormalizationHandler` for each normalization rule (e.g., `EnglishDateHandler`).

4.  **Create the Language Strategy:**
    In `app/normalizers/en/strategy.py`, create the main strategy class that builds the chain of responsibility from your handlers.
    ```python
    # app/normalizers/en/strategy.py
    from app.normalizers.base import NormalizerStrategy, NormalizationHandler
    from .rules.date_handler import EnglishDateHandler
    # ... import other handlers

    class EnglishNormalizerStrategy(NormalizerStrategy):
        def __init__(self):
            self._chain_head = self._build_chain()

        def _build_chain(self) -> NormalizationHandler:
            # Instantiate and link your English handlers here
            date_handler = EnglishDateHandler()
            # ...
            # date_handler.set_next(...)
            return date_handler

        def normalize(self, text: str) -> str:
            return self._chain_head.handle(text)
    ```

5.  **Register the New Strategy:**
    Finally, open `app/main.py` and register your new strategy with the factory inside the `lifespan` function.
    ```python
    # app/main.py
    # ...
    from app.normalizers.sr.strategy import SerbianNormalizerStrategy
    from app.normalizers.en.strategy import EnglishNormalizerStrategy # <-- ADD THIS

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("Registering normalizer strategies...")
        normalizer_factory.register("sr", SerbianNormalizerStrategy)
        normalizer_factory.register("en", EnglishNormalizerStrategy) # <-- AND ADD THIS
        print("Registration complete.")
        yield
    # ...
    ```

## Code Quality

This project uses `Ruff` for linting/formatting and `Mypy` for static type checking.

-   **Run Ruff:** `poetry run ruff check .`
-   **Run Mypy:** `poetry run mypy .`
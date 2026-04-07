# FastAPI AI Base

A high-performance FastAPI template featuring SQLAlchemy 2.0 (via SQLModel), Pydantic V2, and `uv` for lightning-fast dependency management.

## 🚀 Quick Start

### Prerequisites
- [Python 3.14+](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv)
- [Docker](https://www.docker.com/get-started) & [Docker Compose](https://docs.docker.com/compose/install/)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fastapi_ai_base
   ```

2. **Setup environment**
   Install dependencies and create a virtual environment using `uv`:
   ```bash
   uv sync --all-groups
   ```

3. **Database Setup**
   The project is configured to use PostgreSQL. For local development, you can start only the database container:
   ```bash
   docker compose up db -d
   ```

4. **Run Migrations**
   ```bash
   uv run alembic upgrade head
   ```

5. **Run the Application**
   ```bash
   uv run uvicorn app.main:app --reload
   ```
   The API will be available at [http://localhost:8000](http://localhost:8000) and documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 🛠 Development Commands

### Linting & Formatting
We use `ruff` for both linting and formatting:
```bash
# Check for linting issues
uv run ruff check .

# Fix linting issues
uv run ruff check . --fix

# Format code
uv run ruff format .
```

### Type Checking
```bash
uv run mypy .
```

### Database Migrations
We use `alembic` for database migrations:
```bash
# Create a new migration
uv run alembic revision --autogenerate -m "description of changes"

# Upgrade to the latest version
uv run alembic upgrade head

# Downgrade one version
uv run alembic downgrade -1
```

---

## 🧪 Testing

The project uses `pytest` for testing, with `pytest-asyncio` for async support.

```bash
# Run all tests
uv run pytest

# Run tests with coverage report
uv run pytest --cov=app --cov-report=term-missing
```

---

## 🐳 Deployment

### Docker Compose (Full Stack)
To run the entire stack (Postgres + FastAPI app) in production-like mode:
```bash
docker compose up --build
```

### Docker Manual Build
```bash
docker build -t fastapi-ai-base .
docker run -p 8000:8000 fastapi-ai-base
```

### CI/CD
The project includes a GitHub Actions workflow (`.github/workflows/ci-cd.yml`) that:
1. Runs linting (`ruff`), type checking (`mypy`), and tests (`pytest`) on every push to `master` and pull requests.
2. Builds and pushes a Docker image to GitHub Container Registry (GHCR) when a push to `master` is successful.
3. Automated dependency updates via GitHub Dependabot, with auto-merge for passing PRs.
4. Provides a manual workflow for Trivy vulnerability scanning on the Docker image.

---

## 📁 Project Structure

```text
.
├── app/                # Application source code
│   ├── api/            # API routes and dependencies
│   ├── core/           # Configuration, logging, security
│   ├── crud/           # CRUD operations
│   ├── models/         # SQLAlchemy/SQLModel models
│   ├── schemas/        # Pydantic schemas
│   └── main.py         # FastAPI application entry point
├── migrations/         # Alembic database migrations
├── tests/              # Pytest test suite
├── Dockerfile          # Production Dockerfile
├── docker-compose.yml  # Docker Compose configuration
├── pyproject.toml      # Project dependencies and tool configuration
└── start.sh           # Entrypoint script for Docker
```

## 🔐 Configuration
Settings are managed via `pydantic-settings` in `app/core/config.py`. You can override any setting using environment variables or by creating a `.env` file in the project root.

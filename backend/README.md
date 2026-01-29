# ABB Simulation Platform - Backend

FastAPI + PyBullet backend for robot trajectory simulation.

## Setup

```bash
poetry install --with dev
```

## Running

```bash
poetry run uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

## Development

- `poetry add <package>` - Add dependency
- `poetry add --group dev <package>` - Add dev dependency
- `poetry run pytest` - Run tests
- `poetry run ruff check .` - Lint code

# ABB Simulation Platform - Backend

FastAPI + PyBullet backend for robot trajectory simulation.

## Setup

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

## Development

- `pip install <package>` - Add dependency (then add to requirements.txt manually)
- `pip install <package>` - Add dev dependency (then add to requirements.txt manually)
- `pytest` - Run tests
- `ruff check .` - Lint code

# Development Setup Guide

Quick start guide assuming pip and pnpm are not installed.

## Prerequisites

### 1. Install Node.js (includes npm)
Download and install from https://nodejs.org/ (LTS version recommended)

Verify installation:
```bash
node --version
npm --version
```

### 2. Install pnpm
```bash
npm install -g pnpm
```

Verify:
```bash
pnpm --version
```

### 3. Install Python 3.11+
Download from https://www.python.org/

Verify:
```bash
python --version
# or
python3 --version
```

---

## Clone & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/sait-aris/simulation-platform.git
cd simulation-platform
```

### 2. Frontend Setup
```bash
cd frontend
pnpm install
```

Start dev server:
```bash
pnpm dev
```
App runs at `http://localhost:5173`

### 3. Backend Setup
```bash
cd backend
pip install -r requirements.txt
# or if using pip3:
pip3 install -r requirements.txt
```

Start FastAPI server:
```bash
uvicorn app.main:app --reload
```
API available at `http://localhost:8000`
Swagger docs at `http://localhost:8000/docs`

---

## Verify Installation

### Frontend
- Open `http://localhost:5173` in browser
- Should see the app loading without errors

### Backend
- Open `http://localhost:8000/docs` in browser
- Should see Swagger UI with available endpoints

---

## Common Issues

| Issue | Solution |
|-------|----------|
| `pnpm not found` | Run `npm install -g pnpm` again |
| `python not found` | Use `python3` instead, or reinstall Python |
| Port 5173 already in use | Kill process or use `pnpm dev -- --port 5174` |
| Port 8000 already in use | Use `uvicorn app.main:app --reload --port 8001` |

---

## Next Steps

- Read `/docs/team/task-assignments.md` for your tasks
- Check `/docs/PROJECT_SPECIFICATION.md` for feature details
- See `/docs/roadmap/11-week-plan.md` for timeline

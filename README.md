# ABB Online Simulation Platform

**A web-based robot trajectory simulator for ABB industrial robots**

Enabling real-time visualization of RAPID programs with physics-based inverse kinematics and collision detection.

---

## Project Overview

This platform allows users to:
- Upload RAPID code or create trajectories interactively
- Visualize robot motion in real-time 3D (Babylon.js WebGL)
- Simulate physics-accurate kinematics (PyBullet IK solver)
- Detect collisions with user-defined obstacles
- Validate programs before physical deployment
- Export validated trajectories for ABB robot controllers

**Supported Robots:** ABB IRB 4600, IRB 2600, IRB 6700

**Partnership:** SAIT Research Applications × ARIS Robotics

---

## Technical Architecture

**Frontend:**
- **Next.js 16 + React + TypeScript** - UI framework and type safety
- **Babylon.js** - WebGL/WebGPU 3D rendering engine
- **Tailwind CSS 4** - Utility-first styling

**Backend:**
- **FastAPI** - Modern Python web framework
- **PyBullet** - Physics simulation and inverse kinematics
- **Lark Parser** - Grammar-based RAPID language parser

**Workflow:**
1. User uploads RAPID code via web interface
2. Backend parses RAPID → AST → trajectory points
3. PyBullet computes inverse kinematics for joint angles
4. Collision detection against obstacles (mesh-to-mesh)
5. Backend returns trajectory data (JSON)
6. Frontend animates robot in Babylon.js 3D scene

See [docs/02-ARCHITECTURE.md](docs/02-ARCHITECTURE.md) for details.

---

## Quick Start

### Prerequisites

- **Node.js** 20+
- **Python** 3.11+
- **Git**

### Package Managers

- **Frontend:** pnpm (faster, efficient)
- **Backend:** pip (Python standard package manager)

### Installation

**Automated Setup (All Platforms):**

Linux/macOS:
```bash
git clone <repo-url>
cd SAIT-ARIS-AdditiveManufacturing
bash scripts/setup.sh
```

Windows (PowerShell):
```powershell
git clone <repo-url>
cd SAIT-ARIS-AdditiveManufacturing
powershell -ExecutionPolicy Bypass -File scripts/setup.ps1
```

Windows (Command Prompt):
```cmd
git clone <repo-url>
cd SAIT-ARIS-AdditiveManufacturing
scripts\setup.bat
```

**Manual Setup:**
```bash
# Backend (requires Python 3.11+)
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend (requires Node.js + pnpm)
cd frontend
pnpm install
```

### Development

**Option 1: Start Script (Recommended)**

```bash
./start.sh
# Auto-installs dependencies on first run, starts both services
```

**Option 2: Manual (Two Terminals)**

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
pnpm dev
```

**Option 3: Docker**

```bash
docker-compose up
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs (Swagger UI)

---

## Project Structure

```
frontend/        - Next.js + React + Babylon.js visualization layer
backend/         - FastAPI + PyBullet simulation engine
models/          - 3D robot models (GLB) + obstacle STLs
  robots/        - ABB IRB 4600/2600/6700 models + metadata
  obstacles/     - User-uploaded STL/OBJ obstacles
docs/            - Numbered docs (spec, architecture, API, roadmap, sprints)
  contract/      - OpenAPI contract (openapi.json)
  diagrams/      - SVG sequence diagrams
scripts/         - Development utilities (setup, conversion tools)
.github/         - CI/CD workflows
```

---

## Development Strategy: MVP-First Approach

**Commitment:** Focus on **Student View MVP** (Weeks 1-8) with high polish and reliability.
**Stretch Goals:** Engineer View and Production Readiness as Phase 2 (Weeks 9-11) if time permits.

See **[Project Specification](docs/01-PROJECT-SPECIFICATION.md)** for complete scope and success criteria.

### 11-Week Staged Roadmap

| Phase | Duration | Focus | MVP Status |
|-------|----------|-------|-----------|
| **1: Visualization** | Weeks 1-3 | Babylon.js/TS setup, Robot rigging, STL Uploader | **Foundation** |
| **2: The Brain** | Weeks 4-6 | RAPID parser, PyBullet kinematics, Batch execution | **Critical** |
| **3: Student MVP** | Weeks 7-8 | Playback engine, Collision detection, UI polish | **GOAL: MVP LAUNCH** |
| **4: Expansion** | Weeks 9-10 | Line-linked logs, Multi-robot support, Advanced overlays | *As Time Permits* |
| **5: Finalization** | Week 11 | Docs, testing, deployment, final presentation | **Critical** |

**Key Milestones:**
- ✅ Week 3: Robot rigging + STL uploader working
- ✅ Week 6: End-to-end RAPID → trajectory pipeline
- 🎯 Week 8: MVP Demo-ready (Student View complete)
- ⭐ Week 11: Production delivery + documentation

---

## Documentation

### 📍 **[Documentation Hub](docs/README.md)** ⭐

**New to the project?** The Documentation Hub is your single entry point for all project documentation.

---

### Core Documents

#### Project Overview
- **[Project Specification](docs/01-PROJECT-SPECIFICATION.md)** - Complete MVP requirements (FR-1 to FR-12)
- **[CLAUDE.md](CLAUDE.md)** - Development commands and project instructions

#### Architecture & Design
- **[System Architecture](docs/02-ARCHITECTURE.md)** - Full pipeline workflow and component design
- **[API Specification](docs/03-API-SPECIFICATION.md)** - REST endpoints and schemas
- **[OpenAPI Contract](docs/contract/openapi.json)** - Source of truth for frontend/backend boundary

#### Planning & Roadmap
- **[Roadmap](docs/04-ROADMAP.md)** - 11-week plan with phase overview
- **[Team Assignments](docs/05-TEAM-ASSIGNMENTS.md)** - Roles and phase-by-phase breakdown
- **[Testing Strategy](docs/06-TESTING-STRATEGY.md)** - Test pyramid and coverage targets

#### Sprint Plans
- **[Sprint Plan W5–W8](docs/08-SPRINT-PLAN-W5-W8.md)** - Weeks 5-8 detailed plan
- **[Sprint Plan W7–W11](docs/09-SPRINT-PLAN-W7-W11.md)** - Weeks 7-11 detailed plan

---

## Team

**SAIT Research Applications - ARIS Robotics Partnership**

See [docs/05-TEAM-ASSIGNMENTS.md](docs/05-TEAM-ASSIGNMENTS.md) for current team structure and roles.

**Previous Work:** This project builds on experience from the SAIT-ARIS Additive Manufacturing project. See `archive-20260129-3dp-project/` for historical 3D printing robot work (local archive, not tracked in git).

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CLAUDE.md](CLAUDE.md) for development workflow and coding guidelines.

---

## License

[Specify License - MIT, Apache 2.0, etc.]

---

## Acknowledgments

Built on robotics simulation research and ABB RAPID expertise developed through the SAIT-ARIS partnership. Special thanks to Craig, Ryan, and Majid from ARIS Robotics for continued collaboration and guidance.
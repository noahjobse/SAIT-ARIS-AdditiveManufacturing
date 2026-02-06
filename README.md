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
- **React + TypeScript** - UI framework and type safety
- **Babylon.js** - WebGL/WebGPU 3D rendering engine
- **Vite** - Fast build tool and dev server

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

See [docs/architecture/system-design.md](docs/architecture/system-design.md) for details.

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

**Option 1: Manual (Two Terminals)**

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
pnpm dev
```

**Option 2: Docker**

```bash
docker-compose up
```

**Access:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/docs (Swagger UI)

---

## Project Structure

```
frontend/        - React + Babylon.js visualization layer
backend/         - FastAPI + PyBullet simulation engine
models/          - 3D robot models (GLB) + obstacle STLs
  robots/        - ABB IRB 4600/2600/6700 models + metadata
  obstacles/     - User-uploaded STL/OBJ obstacles
docs/            - Architecture, API specs, research notes
  architecture/  - System design, API specification
  guides/        - Development setup, deployment
  roadmap/       - 11-week development plan
  team/          - Team structure and roles
scripts/         - Development utilities (setup, conversion tools)
.github/         - CI/CD workflows
```

---

## Development Strategy: MVP-First Approach

**Commitment:** Focus on **Student View MVP** (Weeks 1-8) with high polish and reliability.
**Stretch Goals:** Engineer View and Production Readiness as Phase 2 (Weeks 9-11) if time permits.

See **[PROJECT_SPECIFICATION.md](docs/PROJECT_SPECIFICATION.md)** for complete scope and success criteria.

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

### 📍 **[START HERE - Documentation Hub](docs/START_HERE.md)** ⭐

**New to the project?** The Documentation Hub is your single entry point for all project documentation, organized by role and task.

**Quick links from the hub:**
- **By Role:** Frontend dev, Backend dev, QA/PM guides
- **Sprint Plans:** Week-by-week detailed task breakdowns
- **Architecture:** System design and API specs
- **Getting Help:** Slack channels, daily standups, troubleshooting

---

### Core Documents

#### Project Overview
- **[Project Specification](docs/PROJECT_SPECIFICATION.md)** - Complete MVP requirements (FR-1 to FR-7)
- **[CLAUDE.md](CLAUDE.md)** - Development commands and project instructions

#### Architecture & Design
- **[System Architecture](docs/architecture/system-design.md)** - Full pipeline workflow and component design
- **[API Specification](docs/architecture/api-specification.md)** - REST endpoints and schemas

#### Planning & Roadmap
- **[11-Week Roadmap](docs/roadmap/11-week-plan.md)** - High-level phase overview
- **[Implementation Timeline](docs/roadmap/implementation-timeline.md)** - Person-by-person breakdown
- **[Task Assignments](docs/team/task-assignments.md)** - Current task assignments

#### Sprint Plans (Detailed 2-Week Plans)
- **[Week 1-2 Sprint Plan](docs/roadmap/week-1-2-sprint-plan.md)** - Foundation (3D scene, robot loading)
- **[Week 3-4 Sprint Plan](docs/roadmap/week-3-4-sprint-plan.md)** - Parser & kinematics
- **[Week 5-6 Sprint Plan](docs/roadmap/week-5-6-sprint-plan.md)** - Simulation pipeline
- **[Week 7-8 Sprint Plan](docs/roadmap/week-7-8-sprint-plan.md)** - MVP launch ⭐
- **[Week 9-10 Sprint Plan](docs/roadmap/week-9-10-sprint-plan.md)** - Stretch goals
- **[Week 11 Finalization](docs/roadmap/week-11-finalization.md)** - Handoff & presentation

---

## Team

**SAIT Research Applications - ARIS Robotics Partnership**

See [docs/team/README.md](docs/team/README.md) for current team structure and roles.

**Previous Work:** This project builds on experience from the SAIT-ARIS Additive Manufacturing project. See `archive-20260129-3dp-project/` for historical 3D printing robot work (local archive, not tracked in git).

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [docs/guides/contributing.md](docs/guides/contributing.md) for detailed guidelines.

---

## License

[Specify License - MIT, Apache 2.0, etc.]

---

## Acknowledgments

Built on robotics simulation research and ABB RAPID expertise developed through the SAIT-ARIS partnership. Special thanks to Craig, Ryan, and Majid from ARIS Robotics for continued collaboration and guidance.
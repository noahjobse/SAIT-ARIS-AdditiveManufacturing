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
- **Custom RAPID Parser** - Lexer/parser for ABB robot language

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
- **Backend:** poetry (modern Python package manager with lock files)

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
# Backend (requires Poetry)
cd backend
poetry install --with dev

# Frontend (requires Node.js + pnpm)
cd frontend
pnpm install
```

### Development

**Option 1: Manual (Two Terminals)**

```bash
# Terminal 1: Backend
cd backend
poetry run uvicorn app.main:app --reload

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

## Development Roadmap

**11-Week Plan** (see [docs/roadmap/11-week-plan.md](docs/roadmap/11-week-plan.md)):

**Phase 1 (Weeks 1-3): Foundation**
- [x] Repository setup and scaffolding
- [ ] RAPID parser (lexer, AST for MoveJ/MoveL/MoveC)
- [ ] Forward kinematics for IRB 4600
- [ ] Basic Babylon.js scene and robot visualization

**Phase 2 (Weeks 4-6): Kinematics & Trajectory**
- [ ] PyBullet inverse kinematics integration
- [ ] Trajectory interpolation and smooth motion
- [ ] Real-time 3D visualization with playback controls

**Phase 3 (Weeks 7-9): Collision & Interactivity**
- [ ] Obstacle import (STL/OBJ) and positioning
- [ ] Mesh-to-mesh collision detection during simulation
- [ ] Interactive trajectory editor and path adjustments

**Phase 4 (Weeks 10-11): Multi-Robot & Deployment**
- [ ] Support for IRB 2600 and IRB 6700 models
- [ ] RAPID export for validated programs
- [ ] Cloud deployment and performance optimization

---

## Documentation

- **[System Architecture](docs/architecture/system-design.md)** - Component design and data flow
- **[API Specification](docs/architecture/api-specification.md)** - REST endpoint documentation
- **[Development Setup](docs/guides/development-setup.md)** - Detailed installation guide
- **[RAPID Language Reference](docs/research/rapid-language-spec.md)** - ABB RAPID syntax and semantics
- **[11-Week Roadmap](docs/roadmap/11-week-plan.md)** - Detailed development schedule
- **[ARIS Partnership](docs/aris-partnership.md)** - Stakeholder collaboration details

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
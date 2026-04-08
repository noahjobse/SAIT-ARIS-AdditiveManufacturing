# ArmStudio — Architecture & Design Decisions

**Project:** ArmStudio — ABB Online Simulation Platform
**Version:** 2.0
**Date:** 2026-02-12

---

## System Overview

```
Frontend (React + Babylon.js)
  - 3D Viewport (Babylon.js scene)
  - RAPID Editor (textarea, Monaco upgrade Phase 4)
  - Control Panel (upload, playback, status)
  - Timeline Scrubber
         |
         | REST API (JSON over HTTP) /api/*
         v
Backend (FastAPI)
  - RAPID Parser (Lark grammar -> AST)
  - Trajectory Generator (AST -> waypoints)
  - IK Solver (PyBullet)
  - Collision Detector (PyBullet meshes)
  - File Manager (GLB/STL uploads)
         |
         v
Data Layer (File-based, no database)
  - /models/robots/*.glb (robot meshes)
  - /models/robots/*.json (DH parameters)
  - /models/robots/*.urdf (PyBullet models)
  - /models/obstacles/ (user STL uploads)
  - /uploads/ (RAPID files, temp storage)
```

## Data Flow: End-to-End Simulation

![End-to-End Simulation Flow](./diagrams/end-to-end-flow.svg)

**Flow Overview:**
1. **Upload Phase** - User uploads RAPID file, backend parses into AST
2. **Simulation Phase** - Frontend sends AST + obstacles, backend computes trajectory
3. **Trajectory Generation** - PyBullet solves IK for each movement, interpolates waypoints
4. **Collision Detection** - Each waypoint checked for collisions
5. **Visualization Phase** - Frontend animates robot at 60 FPS, highlights collisions

## Frontend Architecture

The frontend uses the **Next.js App Router** (Next.js 16). Global state is lifted into `src/app/page.tsx` and passed down via props.

```
src/app/layout.tsx              (RootLayout — font loading, global metadata)
src/app/page.tsx                (Home — lifts global state: robot, trajectory, playback)
src/app/globals.css
src/components/Header.tsx       (robot selector, upload buttons)
src/components/MainLayout.tsx   (split pane 70/30)
src/components/SidePanel.tsx    (30% right panel container)
src/components/SidePanelTabs.tsx (tab switcher: RAPID / Jog)
src/components/RapidPanel.tsx   (RAPID code textarea + run button)
src/components/JointJogPanel.tsx (manual joint angle controls)
src/components/BottomPanel.tsx  (resizable, horizontal split)
src/components/PlaybackControls.tsx (play/pause/stop/speed/step)
src/components/StatusPanel.tsx  (errors, warnings, collision alerts)
src/components/babylon/Viewport3D.tsx        (Babylon.js canvas, 70%)
src/components/babylon/createRobotScene.ts   (starfield, grid, robot loading)
src/components/ui/PrimaryButton.tsx
src/components/ui/SidePanelHeader.tsx
src/types.ts                    (centralized shared types)
```

**State Management:** React `useState` + `useContext` only (no Redux for MVP). Three global states: `currentRobot`, `trajectory`, `playbackState`.

**Legacy directories (do not use for new work):**
- `demo-frontend/` — frozen Vite app kept for e2e reference; not actively developed
- `_reference/` — old Vite components pending deletion after team review

**Babylon.js:** Single scene, ArcRotateCamera, HemisphericLight, ground plane + grid. One robot mesh (skeleton-animated), multiple obstacle meshes. No shadows/post-processing for MVP.

## Backend Module Structure

```
backend/app/
+-- main.py              # FastAPI app, CORS, startup/shutdown
+-- config.py            # Settings (paths, PyBullet config)
+-- routers/
|   +-- robots.py        # GET /api/robots, GET /api/robots/{id}/model
|   +-- upload.py        # POST /api/upload/rapid, POST /api/upload/obstacle
|   +-- kinematics.py    # POST /api/kinematics/fk, POST /api/kinematics/ik  ✅
|   +-- simulate.py      # POST /api/simulate
+-- parser/
|   +-- grammar.lark     # RAPID grammar definition
|   +-- transformer.py   # Lark Transformer -> AST nodes
|   +-- parser.py        # Parse RAPID string -> AST
|   +-- ast_nodes.py     # AST node dataclasses
+-- kinematics/          # ✅ IMPLEMENTED
|   +-- __init__.py      # Module exports
|   +-- exceptions.py    # KinematicsError, IKSolutionNotFoundError, etc.
|   +-- robot_loader.py  # PyBullet URDF loading + joint discovery
|   +-- solver.py        # FK/IK solver (PyBullet wrapper)
|   +-- trajectory.py    # AST -> interpolated waypoints (TODO)
+-- collision/
|   +-- detector.py      # PyBullet collision checking
|   +-- mesh_loader.py   # Load STL/OBJ into PyBullet
+-- schemas/
|   +-- kinematics.py    # FK/IK request/response models  ✅
|   +-- requests.py      # Pydantic request models
|   +-- responses.py     # Pydantic response models
+-- utils/
    +-- file_handler.py  # Temp file management
    +-- validation.py    # Input validation helpers
```

## Multi-Robot Architecture

The kinematics and collision detection system is **robot-agnostic**. Once the controller is built, all 3 robots work via configuration files:

- `models/robots/{id}/robot.urdf` - PyBullet kinematics model
- `models/robots/{id}/visual.glb` - Babylon.js 3D model
- `models/robots/{id}/config.json` - DH parameters, joint limits, metadata

Noah creates 3 sets of configuration files; the single controller consumes them all.

## Technology Stack (Full)

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Frontend** | React | 19.2.4 | UI components |
| | TypeScript | 5.9.3 | Type safety |
| | Next.js | 16 | App Router, dev server + bundler |
| | Babylon.js | 8.46.2 | WebGL 3D visualization |
| | openapi-fetch | — | Type-safe API requests |
| | Tailwind CSS | 4.1.18 | Utility-first CSS |
| | Unit tests | TBD | — |
| | ESLint | 9.39.2 | Code quality |
| **Backend** | FastAPI | 0.128.0 | Web framework |
| | Uvicorn | 0.40.0 | ASGI server |
| | PyBullet | 3.2.6 | IK + collision |
| | NumPy | 2.4.1 | Numerical computation |
| | SciPy | 1.17.0 | Optimization |
| | Lark | 1.3.1 | RAPID grammar parsing |
| | Pydantic | 2.12.5 | Request/response schemas |
| | pytest | 9.0.2 | Unit + integration tests |
| | ruff | 0.14.14 | Python linter |

## Performance Targets

**Backend:** `/api/simulate` < 5s for 50-200 movement instructions. Optimizations: PyBullet headless, IK warm start, adaptive step size, broad-phase collision culling.

**Frontend:** 60 FPS. Optimizations: one robot at a time, low-poly collision meshes, no shadows, limit obstacles (warn >10).

## Security

- RAPID files: max 1MB, `.mod` extension, validate headers
- STL files: max 10MB, `.stl` extension, validate headers
- Pydantic schemas enforce type safety
- CORS: allow all origins (dev), restrict to frontend domain (prod)
- Rate limiting deferred to Phase 4

## Deployment

- **Development:** Docker Compose (backend :8000, frontend :3000, Next.js dev server proxies `/api/*`)
- **Production:** FastAPI on Uvicorn+Gunicorn, static frontend via Nginx/Vercel, Docker on cloud VM

---

## Backend Migration Strategy

**Decision (March 2026):** Python/FastAPI serves as the MVP backend. A C# (.NET) backend
will replace it post-semester for industry compatibility.

**Why C#:**
- ABB provides a C# API for robot controller integration (RobotStudio, IRC5/OmniCore)
- Industrial PLCs and automation controllers primarily support C#
- Aligns the platform with industrial deployment requirements

**Contract Boundary:**

```
Frontend (React + Babylon.js)  ← unchanged
         |
         | OpenAPI contract (docs/contract/openapi.json)
         |
Backend v1 (Python/FastAPI)  →  Backend v2 (C#/.NET)
```

**Contract Details:**
- Source of truth: `docs/contract/openapi.json` (committed, versioned)
- Live reference: FastAPI serves `/openapi.json` showing current implementation
- Model: Core contract (all endpoints required) + extensions (C# may add ABB-specific endpoints)
- Migration: Full swap — complete C# backend built and tested against contract before replacing Python

**Cross-Branch Implementation:**
- Parser (`jason` branch): Lark grammar → AST transformer → Python objects
- Kinematics (`noah` branch): PyBullet FK/IK solver, collision detection
- Frontend (`dylane`/`frontend` branches): React components, Babylon.js 3D scene

---

**Last Updated:** 2026-03-03

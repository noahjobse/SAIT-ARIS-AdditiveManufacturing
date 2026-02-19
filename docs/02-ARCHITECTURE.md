# Architecture & Design Decisions

**Project:** ABB Online Simulation Platform
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

```
1. User uploads RAPID file via frontend
2. POST /api/upload/rapid -> Lark parses RAPID -> AST -> Returns AST JSON + errors
3. User clicks "Simulate"
4. POST /api/simulate {robot_id, ast, obstacles[]}
   -> Load robot URDF into PyBullet
   -> Load obstacle STL meshes into PyBullet
   -> For each AST node (MoveL, MoveJ, MoveC):
      -> Compute target TCP pose
      -> Run IK solver -> joint angles
      -> Interpolate intermediate waypoints
      -> Check collision at each waypoint
   -> Return {trajectory: [{joints[], tcp_pose, timestamp, collisions[]}]}
5. Frontend receives trajectory JSON
   -> Animates Babylon.js robot through waypoints at 60 FPS
   -> Highlights collisions in red when detected
```

## Frontend Architecture

```
App
+-- Header
|   +-- Robot selector dropdown (IRB 4600 / 2600 / 6700)
|   +-- Upload RAPID button
|   +-- Upload Obstacle button
+-- MainLayout (split pane - 70/30)
|   +-- Viewport3D (Babylon.js canvas - 70%)
|   |   +-- Loads robot GLB from /api/robots/{id}/model
|   |   +-- Renders obstacle STL meshes
|   |   +-- Animates through trajectory waypoints
|   |   +-- Highlights collisions (red overlay)
|   +-- SidePanel (30%)
|       +-- RapidEditor (code textarea)
|       +-- SimulationControls (play/pause/stop/speed/step)
|       +-- StatusPanel (errors, warnings, collision alerts)
+-- TimelineScrubber (bottom bar)
    +-- Seek slider (0 to trajectory.length)
    +-- Current timestamp display
```

**State Management:** React `useState` + `useContext` only (no Redux for MVP). Three global states: `currentRobot`, `trajectory`, `playbackState`.

**Babylon.js:** Single scene, ArcRotateCamera, HemisphericLight, ground plane + grid. One robot mesh (skeleton-animated), multiple obstacle meshes. No shadows/post-processing for MVP.

## Backend Module Structure

```
backend/app/
+-- main.py              # FastAPI app, CORS, startup/shutdown
+-- config.py            # Settings (paths, PyBullet config)
+-- routers/
|   +-- robots.py        # GET /api/robots, GET /api/robots/{id}/model
|   +-- upload.py        # POST /api/upload/rapid, POST /api/upload/obstacle
|   +-- simulate.py      # POST /api/simulate
+-- parser/
|   +-- grammar.lark     # RAPID grammar definition
|   +-- transformer.py   # Lark Transformer -> AST nodes
|   +-- parser.py        # Parse RAPID string -> AST
|   +-- ast_nodes.py     # AST node dataclasses
+-- kinematics/
|   +-- solver.py        # PyBullet IK/FK solver wrapper
|   +-- trajectory.py    # AST -> interpolated waypoints
|   +-- robot_config.py  # Load DH params + URDF
+-- collision/
|   +-- detector.py      # PyBullet collision checking
|   +-- mesh_loader.py   # Load STL/OBJ into PyBullet
+-- schemas/
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
| | Vite | 7.3.1 | Dev server + bundler |
| | Babylon.js | 8.46.2 | WebGL 3D visualization |
| | axios | 1.13.4 | API requests |
| | Tailwind CSS | 4.1.18 | Utility-first CSS |
| | Vitest | 4.0.17 | Unit tests |
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

- **Development:** Docker Compose (backend :8000, frontend :5173, Vite proxy `/api/*`)
- **Production:** FastAPI on Uvicorn+Gunicorn, static frontend via Nginx/Vercel, Docker on cloud VM

---

**Last Updated:** 2026-02-12

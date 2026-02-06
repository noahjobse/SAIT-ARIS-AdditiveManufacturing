# System Architecture Design

**Project:** ABB Online Simulation Platform
**Version:** 1.0
**Date:** 2026-02-05
**Status:** Approved for Implementation

## Executive Summary

Three-tier web application enabling real-time visualization of RAPID programs with physics-based inverse kinematics and collision detection. Primary constraint: **lightweight client** - all heavy computation (IK solving, collision detection, trajectory interpolation) runs server-side.

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│  Frontend (React + Babylon.js)              │
│  - 3D Viewport (Babylon.js scene)           │
│  - RAPID Editor (CodeMirror/Monaco)         │
│  - Control Panel (upload, playback, status) │
│  - Timeline Scrubber                        │
└──────────────┬──────────────────────────────┘
               │ REST API (JSON over HTTP)
               │ /api/*
┌──────────────▼──────────────────────────────┐
│  Backend (FastAPI)                           │
│  - RAPID Parser (Lark grammar → AST)        │
│  - Trajectory Generator (AST → waypoints)   │
│  - IK Solver (PyBullet)                     │
│  - Collision Detector (PyBullet meshes)     │
│  - File Manager (GLB/STL uploads)           │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│  Data Layer (File-based, no database)       │
│  - /models/robots/*.glb (robot meshes)      │
│  - /models/robots/*.json (DH parameters)    │
│  - /models/robots/*.urdf (PyBullet models)  │
│  - /models/obstacles/ (user STL uploads)    │
│  - /uploads/ (RAPID files, temp storage)    │
└─────────────────────────────────────────────┘
```

## Design Decisions

### 1. No Database (File-Based Storage)

**Rationale:** MVP has no user accounts, no persistence requirements beyond session scope. Robot models and DH parameters are static configuration files.

**Implementation:**
- Robot configs: JSON files in `/models/robots/`
- User uploads: Session-scoped temporary files in `/uploads/`
- No SQLite, no PostgreSQL, no Redis

**Trade-offs:**
- ✅ Simpler deployment (no DB setup)
- ✅ Easier development (no migrations)
- ❌ No multi-user support (deferred to post-MVP)
- ❌ Sessions don't persist across server restarts (acceptable for MVP)

### 2. Synchronous Request/Response (No WebSockets)

**Rationale:** Frontend requests a full trajectory, receives it as JSON, then animates locally. No need for real-time streaming.

**Implementation:**
- All endpoints return complete responses
- Long-running simulations block until complete (acceptable for MVP - typically <5s)
- Frontend shows loading spinner during computation

**Trade-offs:**
- ✅ Simpler implementation
- ✅ Easier debugging
- ✅ Works with standard HTTP infrastructure
- ❌ No progress updates during simulation (deferred to Phase 4)

### 3. Lightweight Client Architecture

**Constraint:** Client-side performance is critical for smooth 3D rendering.

**Implementation:**
- **All heavy computation on backend:**
  - IK solving (PyBullet runs server-side only)
  - Collision detection (mesh-to-mesh checks server-side)
  - Trajectory interpolation (waypoint generation server-side)
- **Frontend receives pre-computed waypoints:**
  - JSON array of `[{joints[], tcp_pose, timestamp, collisions[]}]`
  - Typical payload: 100-500 waypoints = 50-200KB JSON
  - Frontend iterates through array to animate
- **Babylon.js kept minimal:**
  - Single scene, single camera
  - One robot mesh at a time
  - No shadows, no post-processing for MVP
  - No client-side physics

**Trade-offs:**
- ✅ Smooth client-side animation (60 FPS target)
- ✅ Works on low-end hardware
- ✅ No WebGL/WASM dependencies for physics
- ❌ Server must handle all computation (requires sufficient backend resources)

### 4. RAPID Parser: Lark Grammar (Not Hand-Written)

**Rationale:** RAPID is a well-defined language. Grammar files are easier to review and modify than hand-written recursive descent parser.

**Implementation:**
- `grammar.lark` defines RAPID syntax
- Lark parser auto-generates parse tree
- Custom Transformer converts to AST dataclasses
- Focus development on AST-to-trajectory logic instead of parser plumbing

**Trade-offs:**
- ✅ Faster to implement (2 weeks instead of 4-6)
- ✅ Grammar file is readable documentation
- ✅ Easy to extend with new instructions
- ❌ Adds Lark dependency (acceptable - pure Python, lightweight)

### 5. Dual Model Formats: GLB + URDF

**Challenge:** Babylon.js requires GLB, PyBullet requires URDF.

**Implementation:**
- **GLB (Graphics Library Binary):** For frontend 3D rendering
  - Obtained from ABB (official models available)
  - Stored in `/models/robots/{model_id}/visual.glb`
- **URDF (Unified Robot Description Format):** For backend physics
  - Created manually from DH parameters
  - Stored in `/models/robots/{model_id}/robot.urdf`
  - Simplified collision meshes (convex hulls, not full visual detail)

**Workflow:**
- Frontend loads GLB from `/api/robots/{id}/model` (serves binary stream)
- Backend loads URDF into PyBullet for IK/collision
- Both formats represent same robot kinematics

## Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Frontend Framework** | React | 19.2.4 | UI components |
| **Frontend Language** | TypeScript | 5.9.3 | Type safety |
| **Frontend Build** | Vite | 7.3.1 | Dev server + bundler |
| **3D Rendering** | Babylon.js | 8.46.2 | WebGL 3D visualization |
| **HTTP Client** | axios | 1.13.4 | API requests |
| **Styling** | Tailwind CSS | 4.1.18 | Utility-first CSS |
| **Testing (Frontend)** | Vitest | 4.0.17 | Unit tests |
| **Linting (Frontend)** | ESLint | 9.39.2 | Code quality |
| **Backend Framework** | FastAPI | 0.128.0 | Web framework |
| **ASGI Server** | Uvicorn | 0.40.0 | Production server |
| **Physics/IK** | PyBullet | 3.2.6 | Inverse kinematics + collision |
| **Math** | NumPy | 2.4.1 | Numerical computation |
| **Math** | SciPy | 1.17.0 | Optimization |
| **Parser** | Lark | *TBD* | RAPID grammar parsing |
| **Data Validation** | Pydantic | 2.12.5 | Request/response schemas |
| **Testing (Backend)** | pytest | 9.0.2 | Unit + integration tests |
| **Linting (Backend)** | ruff | 0.14.14 | Fast Python linter |

## System Components

### Frontend Architecture

```
App
├── Header
│   ├── Robot selector dropdown (IRB 4600 / 2600 / 6700)
│   ├── Upload RAPID button
│   └── Upload Obstacle button
├── MainLayout (split pane - 70/30)
│   ├── Viewport3D (Babylon.js canvas - 70% width)
│   │   ├── Loads robot GLB from /api/robots/{id}/model
│   │   ├── Renders obstacle STL meshes
│   │   ├── Animates through trajectory waypoints
│   │   └── Highlights collisions (red overlay on mesh)
│   └── SidePanel (30% width)
│       ├── RapidEditor (code textarea with syntax highlighting)
│       ├── SimulationControls (play/pause/stop/speed/step)
│       └── StatusPanel (errors, warnings, collision alerts)
└── TimelineScrubber (bottom bar)
    ├── Seek slider (0 to trajectory.length)
    └── Current timestamp display
```

**State Management:**
- React `useState` + `useContext` only
- No Redux/Zustand for MVP (adds complexity)
- Three pieces of global state:
  1. `currentRobot` - selected robot ID + loaded GLB mesh
  2. `trajectory` - array of waypoints from `/api/simulate`
  3. `playbackState` - current frame index, playing/paused, speed multiplier

**Babylon.js Scene Setup:**
- Single scene instance (reused for all animations)
- ArcRotateCamera (orbital camera around robot)
- HemisphericLight (ambient lighting)
- Ground plane + grid helper
- One robot mesh (skeleton-animated via joint angles)
- Multiple obstacle meshes (static, user-uploaded STLs)

**Code Editor:**
- MVP: Simple `<textarea>` with monospace font
- Phase 4 (if time): Upgrade to Monaco Editor or CodeMirror
- Keeps initial bundle size small (<500KB)

### Backend Module Structure

```
backend/app/
├── main.py              # FastAPI app, CORS middleware, startup/shutdown
├── config.py            # Settings (paths, PyBullet config, defaults)
├── routers/
│   ├── robots.py        # GET /api/robots, GET /api/robots/{id}/model
│   ├── upload.py        # POST /api/upload/rapid, POST /api/upload/obstacle
│   └── simulate.py      # POST /api/simulate
├── parser/
│   ├── grammar.lark     # RAPID grammar definition (Lark syntax)
│   ├── transformer.py   # Lark Transformer → AST nodes
│   ├── parser.py        # Parse RAPID string → AST
│   └── ast_nodes.py     # AST node dataclasses (MoveL, MoveJ, RobTarget, etc.)
├── kinematics/
│   ├── solver.py        # PyBullet IK/FK solver wrapper
│   ├── trajectory.py    # AST → interpolated waypoints
│   └── robot_config.py  # Load DH params + URDF from /models/robots/
├── collision/
│   ├── detector.py      # PyBullet collision checking (mesh-to-mesh)
│   └── mesh_loader.py   # Load STL/OBJ into PyBullet collision world
├── schemas/
│   ├── requests.py      # Pydantic request models (UploadRapidRequest, etc.)
│   └── responses.py     # Pydantic response models (TrajectoryResponse, etc.)
└── utils/
    ├── file_handler.py  # Temp file management
    └── validation.py    # Input validation helpers
```

### Data Flow: End-to-End Simulation

```
1. User uploads RAPID file via frontend
   ↓
2. POST /api/upload/rapid
   → Lark parses RAPID string → AST
   → Returns AST JSON + errors/warnings to frontend
   ↓
3. User clicks "Simulate"
   ↓
4. POST /api/simulate {robot_id, ast, obstacles[]}
   → Load robot URDF into PyBullet headless server
   → Load obstacle STL meshes into PyBullet world
   → For each AST node (MoveL, MoveJ, MoveC):
      → Compute target TCP pose
      → Run IK solver → joint angles
      → Interpolate intermediate waypoints (based on speed/zone data)
      → Check collision at each waypoint
   → Return {trajectory: [{joints[], tcp_pose, timestamp, collisions[]}]}
   ↓
5. Frontend receives trajectory JSON
   → Loads trajectory into playback state
   → Animates Babylon.js robot through waypoints at 60 FPS
   → Highlights collisions in red when detected
```

## API Specification

See [`api-specification.md`](./api-specification.md) for detailed endpoint documentation.

**Summary:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Status check |
| `/api/robots` | GET | List available robots |
| `/api/robots/{id}/model` | GET | Serve GLB file (binary stream) |
| `/api/upload/rapid` | POST | Upload & parse RAPID → AST |
| `/api/upload/obstacle` | POST | Upload obstacle STL + transform |
| `/api/simulate` | POST | Run full simulation → trajectory |

## Performance Considerations

### Backend

**Target:** `/api/simulate` completes in <5 seconds for typical RAPID programs (50-200 movement instructions)

**Optimizations:**
- PyBullet headless mode (no GUI overhead)
- IK solver warm start (use previous joint config as seed)
- Trajectory interpolation: adaptive step size (fewer points on straight lines)
- Collision detection: broad phase culling (AABB checks before mesh-to-mesh)

**Bottlenecks to monitor:**
- IK convergence time (PyBullet can be slow for complex poses)
- Mesh-to-mesh collision (high poly STLs will be slow)
- Trajectory interpolation (too many waypoints = large JSON payload)

### Frontend

**Target:** 60 FPS animation in Babylon.js viewport

**Optimizations:**
- Load only one robot model at a time
- Use low-poly collision meshes for obstacles (not high-res STLs)
- Disable shadows, post-processing for MVP
- Limit obstacle count (warn if >10 obstacles uploaded)

**Bottlenecks to monitor:**
- Babylon.js rendering (large scenes will drop FPS)
- JSON parsing (large trajectories >1MB may cause jank)
- React re-renders (memoize components, avoid unnecessary state updates)

## Security Considerations

**File Upload Validation:**
- RAPID files: Max 1MB size, `.mod` extension required
- STL files: Max 10MB size, `.stl` extension required
- Validate file headers (magic bytes) to prevent arbitrary file execution

**Input Sanitization:**
- RAPID parser must handle malformed input gracefully (no crashes)
- Pydantic schemas enforce type safety on all API requests
- FastAPI dependency injection prevents SQL injection (no DB = no SQL)

**CORS Policy:**
- Development: Allow all origins (`*`)
- Production: Restrict to deployed frontend domain

**Rate Limiting:**
- Deferred to Phase 4 (not critical for student MVP)

## Testing Strategy

See [`../team/task-assignments.md`](../team/task-assignments.md) for detailed test responsibilities.

**Test Pyramid:**
1. **Unit Tests (70%)**
   - Parser: Valid RAPID → expected AST
   - FK/IK: Known joint configs → expected TCP poses
   - Collision: Known mesh overlaps → detected
2. **Integration Tests (20%)**
   - Upload → Parse → Simulate → Trajectory
   - End-to-end API workflows
3. **Manual/UAT (10%)**
   - Real RAPID programs from RobotStudio
   - Visual validation of animations

**Coverage Target:** 80% line coverage for backend, 60% for frontend

## Deployment Architecture

**Development:**
- Docker Compose: 2 services (backend, frontend)
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- Vite proxy: `/api/*` → `http://localhost:8000`

**Production (Post-MVP):**
- Backend: FastAPI on Uvicorn + Gunicorn (multi-worker)
- Frontend: Static build served via Nginx or Vercel
- Deployment: Docker on cloud VM (AWS EC2, DigitalOcean, etc.)

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| PyBullet IK inaccurate | Medium | High | Validate against RobotStudio ground truth, Week 4 |
| RAPID parser incomplete | Low | High | Phased grammar (movement-only MVP, control flow Phase 4) |
| Babylon.js performance | Medium | Medium | Profile early (Week 2), simplify scene if needed |
| Timeline overrun | High | High | MVP gate at Week 8, defer stretch goals |

## Future Enhancements (Post-Week 11)

1. **Multi-user support:** Add authentication, save sessions to DB
2. **WebSocket streaming:** Real-time simulation progress updates
3. **Advanced RAPID features:** Procedures, modules, error handling
4. **Optimization:** Genetic algorithms for trajectory smoothing
5. **Visualization:** Tool path preview, reach envelope display
6. **Export:** Download trajectory as CSV, JSON, or RobotStudio compatible format

## References

- [RAPID Language Reference](https://library.e.abb.com/public/688894b98123f87bc1257cc50044e809/Technical%20reference%20manual_RAPID_3HAC16581-1_revJ_en.pdf)
- [PyBullet Quickstart Guide](https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA)
- [Babylon.js Documentation](https://doc.babylonjs.com/)
- [ABB RobotStudio](https://new.abb.com/products/robotics/robotstudio)

---

**Approved by:** Noah (PM/QA Lead), 2026-02-05
**Next Review:** End of Week 2 (Architecture validation checkpoint)

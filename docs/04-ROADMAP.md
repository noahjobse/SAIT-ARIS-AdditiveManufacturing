# Roadmap & Sprint Plans

**Project:** ABB Online Simulation Platform
**Version:** 2.0
**Date:** 2026-02-12

---

## Phase Overview

| Phase | Weeks | Goal | MVP Impact |
|-------|-------|------|-----------|
| **1: Visualization** | 1-3 | 3D scene, robot models, obstacles, gizmo | Foundation |
| **2: Logic Engine** | 4-6 | RAPID parser, IK/FK, trajectory, `/api/simulate` | Critical |
| **3: Student MVP** | 7-8 | Playback, collision, polish, UAT, sign-off | **MVP LAUNCH** |
| **4: Expansion** | 9-10 | Control flow (IF/FOR/WHILE), multi-robot validation | Stretch |
| **5: Finalization** | 11 | Docs, deployment, demo, presentation | Handoff |

## Sprint: Weeks 1-2 (Foundation)

**Goal:** 3D scene working, robot loads and moves, API structure, upload flow
**Key Milestone:** Robot visible and joints controllable in browser

**Deliverables:**
- Babylon.js 3D scene with IRB 4600 robot loaded and orbitable
- 6 joint angle sliders that move the robot in real-time
- Frontend layout (Header, Viewport, Sidebar) styled with Tailwind
- Robot selector dropdown (UI only)
- File upload UI (drag & drop for RAPID + STL)
- Backend: `/api/robots`, `/api/robots/{id}/model`, upload endpoints
- GLB file serving, upload endpoints accepting files
- Test infrastructure (pytest + vitest in CI), sample RAPID files

**Blocking Dependencies:**
- Day 1 (Noah): GLB file in repo -> blocks Dylane's robot loading
- Day 1-2 (Jason): FastAPI router setup -> blocks Umaya's upload wiring

## Sprint: Weeks 3-4 (Parse & Solve)

**Goal:** RAPID parser complete, FK/IK working, obstacles in scene
**Key Milestone:** Upload RAPID -> get parsed AST, kinematics validated

**Deliverables:**
- Obstacle STL loading + transform gizmo (position + rotation)
- StatusPanel displays parsing errors with line numbers
- Lark grammar for MoveL/MoveJ/MoveC, AST transformer, parser wired to upload endpoint
- PyBullet headless, FK solver, IK solver (all 3 robot URDFs)
- Parser test suite (20+ cases), FK/IK validation tests

**Progress:**
- [x] **Noah:** IRB 4600 URDF created (ROS Industrial parameters) — `models/robots/irb4600/irb4600.urdf`
- [x] **Noah:** PyBullet headless robot loader — `app/kinematics/robot_loader.py`
- [x] **Noah:** FK solver (joint angles → TCP pose) — `app/kinematics/solver.py`
- [x] **Noah:** IK solver (target pose → joint angles) — `app/kinematics/solver.py`
- [x] **Noah:** FK/IK REST endpoints — `POST /api/kinematics/fk`, `POST /api/kinematics/ik`
- [x] **Noah:** 21 kinematics tests passing (unit + integration)
- [x] **Noah:** IRB 2600 + IRB 6700 URDFs — `models/robots/irb2600/`, `models/robots/irb6700/`
- [x] **Noah:** Collision detector + obstacle mesh loader — `app/collision/detector.py`
- [ ] **Jason:** Lark grammar skeleton
- [ ] **Jason:** AST transformer

**Blocking Dependencies:**
- ~~Week 3 Day 2-3 (Noah): PyBullet + IRB 4600 URDF -> blocks Week 4 IK solver~~ ✅ DONE
- ~~Week 6 Day 1 (Noah): Obstacle mesh in PyBullet -> blocks collision testing~~ ✅ DONE
- Week 3 Day 1 (Jason): `grammar.lark` skeleton -> blocks Week 4 AST implementation

## Sprint: Weeks 5-6 (Simulation Pipeline)

**Current Week: Week 5 (2026-03-03)**

**Goal:** End-to-end `/api/simulate`, trajectory generation, collision detection
**Key Milestone:** Upload RAPID -> see trajectory waypoints returned with collision data

**Deliverables:**
- `/api/simulate` endpoint complete (RAPID -> trajectory JSON)
- Trajectory generator: MoveL (linear), MoveJ (joint-space), MoveC (circular arc)
- Obstacle CRUD endpoints: `POST/GET/DELETE /api/obstacles` ← **added to scope**
- Collision detector (mesh-to-mesh via PyBullet), obstacle mesh loading ✅
- Frontend animation through trajectory waypoints, basic playback (play/pause/stop)
- Collision highlighting on robot mesh
- Performance < 5s for 100-waypoint trajectory
- Integration tests (upload -> parse -> simulate -> animate)

**Progress:**
- [x] **Noah:** Collision detection module with STL/OBJ obstacle loading
- [x] **Noah:** PyBullet mesh collision detection working
- [x] **Noah:** Collision tests passing (13 tests)
- [x] **Jason:** RAPID parser (Lark grammar + AST transformer) — merged to main PR #4
- [x] **Noah:** CI fixed (ruff lint, ESLint v9 flat config, Node 20/22 matrix) — March 3
- [x] **Noah:** Docker Compose dev environment working — March 3
- [x] **Noah:** OpenAPI contract committed `docs/contract/openapi.json` — March 3
- [ ] **Noah:** `/api/parse` endpoint wiring parser — **IN PROGRESS (Week 5)**
- [ ] **Noah:** `TrajectoryGenerator` (MoveL/MoveJ/MoveC, time-based speed data) — **IN PROGRESS**
- [ ] **Noah:** `/api/simulate` endpoint (parse → trajectory → collision → JSON) — **IN PROGRESS**
- [ ] **Noah:** Obstacle CRUD (`POST/GET/DELETE /api/obstacles`, in-memory) — **IN PROGRESS**
- [ ] **Umaya:** RapidPanel → `/api/simulate` wiring — **IN PROGRESS**

**Note:** Dylane is unavailable Week 5. Returns Week 6 for obstacle UI and transform gizmo.

**Blocking Dependencies:**
- Week 5 (Noah): `/api/simulate` format finalized → blocks Umaya frontend wiring
- Week 5 (Noah): Obstacle CRUD endpoints → blocks collision testing + Umaya obstacle UI
- Week 6 (Dylane returns): obstacle STL in scene → blocks obstacle-based collision demos

## Sprint: Weeks 7-8 (MVP Launch)

**Goal:** Timeline scrubber, playback controls, error states, MVP sign-off
**Key Milestone:** STUDENT MVP COMPLETE

![Playback Controls Flow](./diagrams/playback-controls.svg)

**Deliverables:**
- Timeline scrubber (seek to any waypoint), step-through (next/prev)
- Speed controls (0.25x, 0.5x, 1x, 2x)
- Error states with friendly messages, loading indicators
- IK caching (LRU, 1000 entries), edge case handling
- Input validation hardening, timeout handling (2s IK, 5s collision)
- Full regression testing, UAT with 10+ real RAPID programs
- Multi-browser testing (Chrome, Firefox, Edge)
- MVP sign-off demo with stakeholders

### MVP Sign-Off Acceptance Criteria

- **FR-1:** Select IRB 4600/2600/6700, each loads correctly
- **FR-2:** Upload STL obstacles, appear in scene, 5+ supported
- **FR-3:** Gizmo allows position/rotation, changes persist
- **FR-4:** Parser handles MoveL/MoveJ/MoveC, errors are helpful
- **FR-5:** Trajectory calculated server-side in <5s
- **FR-6:** Timeline scrubber, play/pause/stop, speed controls, step-through
- **FR-7:** Collision visual warning (red), collision details in StatusPanel
- UI intuitive for non-programmers
- No crashes during 30+ min sessions
- Works on Chrome, Firefox, Edge

## Sprint: Weeks 9-10 (Stretch Goals)

**Goal:** IF/ELSE/FOR/WHILE control flow, all 3 robots fully validated

**Deliverables:**
- Extend Lark grammar: IF/ELSE, boolean expressions, FOR, WHILE, PROC/ENDPROC
- AST interpreter for control flow execution
- Multi-robot selector with thumbnails and robot info panel
- Control flow visualization and variable inspector (optional)
- Execution timeout (10K iterations max)
- Multi-robot test matrix (3 robots x 5 programs = 15 tests)

**Note:** IF/ELSE + multi-robot is core. FOR/WHILE are stretch within stretch.

## Sprint: Week 11 (Handoff)

**Goal:** Documentation, testing, final delivery

**Deliverables:**
- User guide with screenshots and step-by-step tutorials
- Developer guide (extending parser, adding robots)
- API docs auto-generated from OpenAPI
- Architecture documentation
- Deployment config (Docker Compose), tested on cloud VM
- Demo video (3-5 min), final presentation (15-20 min + Q&A)
- Final test pass, handoff package

---

## Post-Semester: C# Backend Migration (Summer 2026)

**Goal:** Full swap of Python/FastAPI backend to C#/.NET while preserving the OpenAPI contract.

**Prerequisites:**
- MVP complete and stable on Python/FastAPI
- OpenAPI contract frozen at `docs/contract/openapi.json`
- All contract endpoints implemented and tested in Python

**Key Tasks:**
- C#/.NET project scaffold (ASP.NET Web API)
- Port RAPID parser (Lark grammar → C# parser, e.g., ANTLR or Pidgin)
- Port kinematics engine (PyBullet → BulletSharp or custom IK solver)
- Port collision detection
- Implement all contract endpoints
- Integration testing: validate every endpoint against committed OpenAPI schema
- Frontend smoke test: verify React app works identically with new backend

**Contract:** `docs/contract/openapi.json` — C# backend must pass all contract endpoints.
Extensions (ABB controller API, RobotStudio integration) can be added beyond core contract.

---

## Recent Completions (2026-02-12)

### Kinematics Module (Weeks 3-4) ✅
- **All 3 robot URDFs**: IRB 4600, IRB 2600, IRB 6700 with DH parameters
- **PyBullet integration**: Robot loader with URDF parsing
- **FK/IK solvers**: Forward and inverse kinematics implementation
- **API endpoints**: `/api/kinematics/fk` and `/api/kinematics/ik`
- **Test coverage**: 21 unit + integration tests passing

### Collision Detection (Week 6) ✅
- **STL/OBJ obstacle loading**: Dynamic mesh import via PyBullet
- **Mesh-to-mesh collision**: Robot-to-obstacle collision detection
- **API ready**: Collision detector module integrated
- **Test coverage**: 13 collision detection tests passing

### Total Test Coverage
- **Backend**: 34 tests passing across kinematics + collision modules
- **API integration**: Full endpoint coverage with Pydantic validation
- **Documentation**: Architecture, API spec, setup guide updated

---

**Last Updated:** 2026-03-03

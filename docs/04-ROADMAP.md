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

**Blocking Dependencies:**
- Week 3 Day 1 (Jason): `grammar.lark` skeleton -> blocks Week 4 AST implementation
- Week 3 Day 2-3 (Noah): PyBullet + IRB 4600 URDF -> blocks Week 4 IK solver

## Sprint: Weeks 5-6 (Simulation Pipeline)

**Goal:** End-to-end `/api/simulate`, trajectory generation, collision detection
**Key Milestone:** Upload RAPID -> see trajectory waypoints returned with collision data

**Deliverables:**
- `/api/simulate` endpoint complete (RAPID -> trajectory JSON)
- Trajectory generator: MoveL (linear), MoveJ (joint-space), MoveC (circular arc)
- Collision detector (mesh-to-mesh via PyBullet), obstacle mesh loading
- Frontend animation through trajectory waypoints, basic playback (play/pause/stop)
- Collision highlighting on robot mesh
- Performance < 5s for 100-waypoint trajectory
- Integration tests (upload -> parse -> simulate -> animate)

**Blocking Dependencies:**
- Week 5 Day 1 (Jason): SimulateRequest/Response schemas -> blocks Dylane frontend integration
- Week 6 Day 1 (Noah): Obstacle mesh in PyBullet -> blocks collision testing

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

**Last Updated:** 2026-02-12

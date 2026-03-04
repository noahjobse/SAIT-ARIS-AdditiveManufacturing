# Team Assignments

**Project:** ABB Online Simulation Platform
**Version:** 2.0
**Date:** 2026-02-12

---

## Team Structure

| Person | Primary Role | Key Focus |
|--------|-------------|-----------|
| **Dylane** | Frontend - Babylon.js | 3D scene, robot loading, animation, gizmo, timeline scrubber, collision highlighting |
| **Umaya** | Frontend - React UI | Layout, upload UI, playback controls, status panel, responsive design, accessibility |
| **Jason** | Backend Lead | FastAPI routes, RAPID parser (Lark), trajectory generator, `/api/simulate`, IK caching |
| **Noah** | Backend (IK/Collision) + PM + QA | PyBullet FK/IK, collision detection, URDFs, upload endpoints, testing, docs, sprint planning |

## Phase-by-Phase Breakdown

### Phase 1 (Weeks 1-3): Visualization Foundation

| Person | Deliverables |
|--------|-------------|
| **Dylane** | Babylon.js scene (camera, lighting, ground), IRB 4600 GLB loading, skeleton joint animation, 6 joint sliders, obstacle STL loading, transform gizmo |
| **Umaya** | App layout (Header, MainLayout, SidePanel), robot selector, file upload (drag-drop), RAPID editor textarea, StatusPanel, obstacle list sidebar |
| **Jason** | FastAPI router structure, `GET /api/robots`, `GET /api/robots/{id}/model`, CORS middleware, begin Lark research |
| **Noah (BE)** | IRB 4600 GLB in repo, `POST /api/upload/rapid`, `POST /api/upload/obstacle`, Pydantic schemas, file validation |
| **Noah (QA)** | Vitest + pytest setup, CI pipelines, sample RAPID programs, integration test skeleton |

### Phase 2 (Weeks 4-6): Logic Engine & Kinematics

> **Week 5 Status Update (2026-03-03):** Assignments revised to reflect actual sprint ownership.
> Dylane is unavailable Week 5 — returns Week 6 for obstacle UI and gizmo.

| Person | Deliverables |
|--------|-------------|
| **Dylane** | *(Week 5: unavailable)* Week 6+: obstacle STL loading in Babylon.js, transform gizmo, animation controller, collision highlighting (red material) |
| **Umaya** | RapidPanel → `POST /api/simulate` wiring, `PlaybackControls` with real trajectory data (frontend-driven), collision visualization, basic timeline scrubber |
| **Jason** | ✅ Lark grammar + AST transformer (complete, merged PR #4), parser test coverage review, additional edge case tests, parser module documentation |
| **Noah (BE)** | ✅ FK/IK solvers (complete), ✅ Collision detector (complete) — **Week 5:** `/api/parse` wiring, `TrajectoryGenerator` (MoveL/MoveJ/MoveC, time-based speed data), IK LRU cache (1000 entries), `/api/simulate` endpoint, obstacle CRUD (`POST/GET/DELETE /api/obstacles`) |
| **Noah (QA)** | FK/IK + collision tests ✅, trajectory generator unit tests, `/api/simulate` integration tests, performance benchmark (100-waypoint < 5s) |

### Phase 3 (Weeks 7-8): Student MVP

| Person | Deliverables |
|--------|-------------|
| **Dylane** | TimelineScrubber, step-through, keyboard shortcuts, rendering optimization |
| **Umaya** | SpeedControl, LoadingIndicator, ErrorMessage, responsive layout, ARIA labels |
| **Jason** | IK caching (LRU), edge case handling, Swagger docs, performance tuning |
| **Noah (BE)** | Input validation hardening, timeout handling, security review |
| **Noah (QA)** | Full regression, UAT (10+ RAPID programs), multi-browser testing, MVP sign-off demo |

### Phase 4 (Weeks 9-10): Expansion (Stretch)

| Person | Deliverables |
|--------|-------------|
| **Dylane** | Multi-robot selector with thumbnails, robot info panel |
| **Umaya** | ControlFlowVisualizer (optional), VariableInspector (optional), Monaco Editor |
| **Jason** | Extend grammar (IF/ELSE/FOR/WHILE/PROC), boolean expressions, AST interpreter |
| **Noah (BE)** | Verify all 3 robot URDFs, robot config loader, execution timeout |
| **Noah (QA)** | Control flow test suite, multi-robot test matrix (3x5=15 tests) |

### Phase 5 (Week 11): Finalization

| Person | Deliverables |
|--------|-------------|
| **Dylane** | Final UI polish, demo mode, demo video (3-5 min) |
| **Umaya** | User guide with screenshots |
| **Jason** | API docs auto-gen, deployment config, cloud VM test |
| **Noah (BE)** | Architecture docs, deployment scripts, developer guide |
| **Noah (QA)** | Final test pass, presentation slides, handoff package |

## Critical Integration Dependencies

| When | What | Blocks |
|------|------|--------|
| Week 1 Day 1 | Noah: GLB in repo | Dylane: robot loading |
| Week 1 Day 1-2 | Jason: FastAPI routes | Umaya: upload wiring |
| Week 3 Day 1 | Jason: `grammar.lark` | Week 4: AST implementation |
| Week 3 Day 2-3 | Noah: PyBullet + URDF | Week 4: IK solver |
| ~~Week 5 Day 1~~ ✅ | ~~Jason: Simulate schemas~~ | ~~Dylane: frontend animation~~ |
| **Week 5 (NOW)** | **Noah: `/api/simulate` endpoint** | **Umaya: frontend wiring** |
| **Week 5 (NOW)** | **Noah: Obstacle CRUD endpoints** | **Umaya: obstacle UI, collision testing** |
| Week 6 | Dylane returns: obstacle STL in scene | Collision demo, transform gizmo |
| Week 8 | Collision integration | Backend data -> frontend rendering |

## Definition of Done

A task is DONE when:
- Code committed to repo
- Code reviewed by at least one team member
- Tests written and passing (if applicable)
- No linting errors (ruff / eslint)
- Verified in browser/API (manual smoke test)

## Communication

- **Slack:** `#abb-sim-dev` (general), `#abb-sim-frontend`, `#abb-sim-backend`, `#abb-sim-qa`
- **Daily Standup:** 9:00 AM (15 min)
- **Sprint Reviews:** End of each 2-week sprint (30 min); Week 8 MVP sign-off (1 hour)

---

**Last Updated:** 2026-03-03

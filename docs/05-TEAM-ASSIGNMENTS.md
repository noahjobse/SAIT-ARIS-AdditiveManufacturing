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

| Person | Deliverables |
|--------|-------------|
| **Dylane** | Animation controller (play/pause/stop), collision highlighting (red material) |
| **Umaya** | Parse error display, PlaybackControls, SimulationControls, speed slider, progress bar, collision alerts |
| **Jason** | Lark grammar (MoveL/MoveJ/MoveC), AST nodes, transformer, `/api/upload/rapid` parser, trajectory generator, `/api/simulate` endpoint |
| **Noah (BE)** | PyBullet headless, IRB 4600 URDF, FK solver, IK solver, IRB 2600/6700 URDFs, collision detector, obstacle mesh loader |
| **Noah (QA)** | 20+ parser tests, FK/IK validation, collision tests, integration tests, performance benchmarks |

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
| Week 5 Day 1 | Jason: Simulate schemas | Dylane: frontend animation |
| Week 6 | `/api/simulate` format finalized | Both frontend and backend |
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

**Last Updated:** 2026-02-12

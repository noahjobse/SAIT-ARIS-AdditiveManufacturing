# Team Assignments

**Project:** ABB Online Simulation Platform
**Version:** 2.0
**Date:** 2026-02-12

---

## Team Structure (Updated Week 7)

| Person | Primary Role | Key Focus (Weeks 7-11) |
|--------|-------------|------------------------|
| **Noah** | Backend + PM + Deploy | Supabase setup, Stripe, production deploy (Vercel/Render), CI/CD, integration tests |
| **Jason** | Frontend + Migration + Docker | Next.js component port, CodeMirror editor, Docker setup, landing page, e2e demo, handoff docs |
| **Umaya** | Frontend + Auth UX | Component port (Week 7), execution UX, joint jog polish, collision/obstacle UI, handoff docs |
| **Dylane** | Frontend + Deliverables | Playback improvements, drag-to-resize, dashboard, capstone poster (returns Week 8) |

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

## Weeks 7-11 Assignments

> See `09-SPRINT-PLAN-W7-W11.md` for the full weekly breakdown with task IDs.

### Noah — Backend + PM + Deploy
- Supabase project setup, DB schema, auth integration
- Stripe PoC (single subscription, paywall gate)
- Save/load persistence (programs, simulations, obstacles)
- Simulate integration tests
- Production deploy: Vercel (frontend) + Render (backend)
- CI/CD pipeline

### Jason — Frontend + Migration + Docker (heavy load)
- Port all React components into Next.js App Router (M1-M2, M6)
- CodeMirror editor upgrade (F1-F6)
- Docker: production Dockerfile, new docker-compose, demo migration (M8-M12)
- Marketing landing page
- ARIS handoff docs (Week 10)

### Umaya — Frontend + Polish (lighter load)
- Port PlaybackControls, JointJogPanel, StatusPanel into Next.js (M3-M5)
- Execution UX improvements (F7-F11)
- Joint jog fixes (F18-F21)
- Collision highlighting, obstacle UI, loading states (F24-F27)
- Save obstacle setups per user
- ARIS handoff docs (Week 10)

### Dylane — Frontend + Deliverables (returns Week 8)
- Playback improvements (F12-F17) + tool tip trace (F28)
- Drag-to-resize panels, log filtering (F22-F23)
- User dashboard (U1)
- Capstone poster (D5)

---

**Last Updated:** 2026-03-17

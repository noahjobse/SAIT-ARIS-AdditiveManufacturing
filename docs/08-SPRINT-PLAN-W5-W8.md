# Sprint Plan: Weeks 5–8

**Project:** ABB Online Simulation Platform
**Created:** 2026-03-03
**Sprint Owner:** Noah (PM)

---

## Current State (Week 5 Start)

### What's Done

| Component | Owner | Status |
|-----------|-------|--------|
| IRB 4600/2600/6700 URDFs | Noah | ✅ Complete |
| PyBullet FK/IK solver | Noah | ✅ Complete — 21 tests passing |
| Collision detector + obstacle mesh loader | Noah | ✅ Complete — 13 tests passing |
| RAPID Lark grammar + AST transformer | Jason | ✅ Complete — merged to main (PR #4) |
| Parser AST nodes (Declaration, MoveL/J/C) | Jason | ✅ Complete |
| Parser test suite | Jason | ✅ Passing (PR #4) |
| CI pipelines (backend lint/test, frontend lint/build) | Noah | ✅ Fixed March 3 |
| Docker Compose dev environment | Noah | ✅ Working |
| OpenAPI contract | Noah | ✅ Committed `docs/contract/openapi.json` |
| Frontend 3D scene (Babylon.js, robot loading) | Dylane | ✅ Exists |
| Frontend React layout (SidePanel, RapidPanel stubs) | Umaya | ✅ Exists |

### What's Missing (Pipeline Gap)

The parser and kinematics exist independently but are **not connected**. There is no:
- `/api/simulate` endpoint
- Trajectory generator (parser AST → joint waypoints via IK)
- `/api/parse` standalone endpoint
- Obstacle CRUD endpoints (register/list/delete)
- Frontend wired to any real API (playback uses stub data)

**The entire simulate pipeline is the critical gap for MVP.**

---

## Critical Path

```
Jason's parser AST (done)
         ↓
  Noah wires parser into /api/parse        ← Week 5
         ↓
  Noah builds TrajectoryGenerator          ← Week 5
  (MoveL/MoveJ/MoveC + speed data)
         ↓
  Noah builds /api/simulate endpoint       ← Week 5-6
         ↓
  Umaya wires RapidPanel → /api/simulate   ← Week 5-6
         ↓
  Umaya builds PlaybackControls            ← Week 6
  (real waypoints + timestamps)
         ↓
  Obstacle CRUD → collision testing        ← Week 7
         ↓
  MVP polish + UAT                         ← Week 8
```

---

## Technical Decisions (March 3, 2026)

### Trajectory: Time-Based Using RAPID Speed Data

RAPID speed zones map directly to mm/s:
- `v100` = 100 mm/s
- `v500` = 500 mm/s
- `v1000` = 1000 mm/s

Waypoint count = `ceil(distance / (speed * dt))` where `dt` is a fixed timestep (e.g. 20ms).
Each waypoint carries a `timestamp` (seconds from start) used by the frontend playback engine.

**Rationale:** Mirrors real robot controller timing. Allows frontend to use `setTimeout`/`requestAnimationFrame` for accurate speed-scaled playback without needing a backend clock.

### MoveC: In MVP Scope

Circular arc interpolation (3-point) is required for MVP. ABB robots use MoveC for arc welds and pick paths — omitting it would invalidate most real programs.

### Playback: Frontend-Driven, Precomputed

Backend returns the full trajectory array with timestamps. Frontend owns playback:
- Receive array once from `/api/simulate`
- Use timestamps to drive `requestAnimationFrame` loop
- Speed control = scale timestamp intervals client-side (no round-trips)
- Scrubber = seek to waypoint index by timestamp

**Rationale:** Avoids streaming complexity, lets frontend control UX without backend state.

### IK Cache: LRU (1000 Entries)

Many trajectory waypoints use nearly identical target poses (small deltas between steps).
Add `functools.lru_cache` or a manual LRU on `KinematicsSolver.ik()`. Cache key = rounded (position, orientation) tuple.

**Rationale:** Can reduce IK call count 10–50× for smooth trajectories with small steps.

### Obstacle CRUD: In-Memory Registry

Obstacles stored in a dict keyed by UUID for Week 5-7. No database needed for MVP.
Endpoints: `POST /api/obstacles`, `GET /api/obstacles`, `DELETE /api/obstacles/{id}`.

---

## Week-by-Week Targets

### Week 5 (Current) — Backend Pipeline

| Owner | Task | Deliverable |
|-------|------|-------------|
| **Noah** | Wire Jason's parser into `/api/parse` | `POST /api/parse` returns AST JSON |
| **Noah** | Build `TrajectoryGenerator` class | MoveL + MoveJ working, IK per waypoint |
| **Noah** | Add MoveC to `TrajectoryGenerator` | Circular arc 3-point interpolation |
| **Noah** | Add IK LRU cache | `lru_cache` on solver, benchmark speedup |
| **Noah** | Build `/api/simulate` endpoint | Full pipeline: parse → trajectory → JSON |
| **Noah** | Obstacle CRUD endpoints | POST/GET/DELETE `/api/obstacles` |
| **Umaya** | Begin RapidPanel → `/api/simulate` wiring | Calls endpoint, displays raw response |
| **Jason** | Parser test coverage review | Ensure edge cases covered |
| **Dylane** | — | Unavailable Week 5 |

### Week 6 — Frontend Integration

| Owner | Task | Deliverable |
|-------|------|-------------|
| **Noah** | Integration tests for `/api/simulate` | Upload → simulate → assert trajectory valid |
| **Noah** | Performance benchmark | 100-waypoint trajectory < 5s |
| **Umaya** | `PlaybackControls` with real trajectory data | Play/pause/stop, speed control working |
| **Umaya** | Collision highlighting wired to response | Red material on collision frames |
| **Umaya** | Playback scrubber (basic) | Seek to waypoint by index |
| **Dylane** | Returns — obstacle UI + transform gizmo | Obstacle STL upload in scene |
| **Jason** | TBD — parser docs, additional tests | — |

### Week 7 — Polish + Obstacle System

| Owner | Task | Deliverable |
|-------|------|-------------|
| **Noah** | Timeout handling (2s IK, 5s simulate) | 408/504 responses on timeout |
| **Noah** | Input validation hardening | Reject malformed RAPID, bad robot IDs |
| **Umaya** | Obstacle list UI, add/remove obstacles | Users can manage obstacle set |
| **Umaya** | Error states, loading indicators | Friendly messages on all failure paths |
| **Dylane** | TimelineScrubber (step through) | Step-forward/back keyboard shortcuts |
| **Jason** | Swagger docs, API documentation | `/docs` fully describes all endpoints |

### Week 8 — MVP Launch

| Owner | Task | Deliverable |
|-------|------|-------------|
| **All** | UAT with 10+ real RAPID programs | Validated against acceptance criteria |
| **All** | Multi-browser testing (Chrome/Firefox/Edge) | No regressions |
| **Noah** | Final regression suite | All tests green |
| **Noah** | MVP sign-off demo | Stakeholder presentation |

---

## Unblocking Dependencies

| Dependency | Blocks | Owner | When |
|-----------|--------|-------|------|
| `/api/parse` wired | Umaya: display parse errors | Noah | Week 5 Day 1-2 |
| `TrajectoryGenerator` + `/api/simulate` | Umaya: frontend wiring | Noah | Week 5 |
| Frontend reads real trajectory | PlaybackControls, scrubber | Umaya | Week 6 |
| Dylane returns | Obstacle UI, gizmo, timeline scrubber | — | Week 6 |
| Obstacle CRUD endpoints | Collision testing, Umaya obstacle UI | Noah | Week 5 |

---

## Task Assignments (Phase 2 Reality)

### Noah — Backend + PM + QA

- `/api/parse`: wire Jason's parser to endpoint
- `app/trajectory/generator.py`: `TrajectoryGenerator` with MoveL/MoveJ/MoveC
- IK LRU cache on `KinematicsSolver`
- `/api/simulate`: orchestrate parse → trajectory → collision → JSON
- Obstacle CRUD: `POST/GET/DELETE /api/obstacles`, in-memory registry
- Integration tests for `/api/simulate`
- Timeout + validation hardening (Week 7)
- Regression suite + MVP demo (Week 8)

### Umaya — Frontend Integration

- Wire `RapidPanel` → `POST /api/simulate`
- Replace stub playback data with real trajectory response
- `PlaybackControls`: play/pause/stop, speed control (frontend-driven)
- Collision highlighting using response data
- Basic timeline scrubber (Week 6)
- Obstacle list UI (Week 6-7, after Dylane returns for gizmo)
- Error states + loading indicators (Week 7)

### Jason — Parser + Docs

- Review parser test coverage — add missing edge cases
- Documentation for parser module
- `/api/simulate` Swagger docs (Week 7)
- TBD based on Week 5 progress

### Dylane — Frontend 3D (Returns Week 6)

- Unavailable Week 5
- Week 6: obstacle STL loading into Babylon.js scene, transform gizmo
- Week 7: `TimelineScrubber`, step-through, keyboard shortcuts
- Week 8: rendering optimization, demo mode, demo video

---

**Last Updated:** 2026-03-03

# Meeting Notes

**Project:** ArmStudio

---

## 2026-03-03 — Week 5 Sprint Planning (Session 2)

**Attendees:** Noah (PM)
**Purpose:** Sprint planning, task assignments, and technical decisions for Weeks 5-8

---

### Sprint Assignments (Weeks 5-8)

Revised task ownership for the simulate pipeline sprint:

| Person | Week 5-6 Focus |
|--------|---------------|
| **Noah** | `/api/parse`, `TrajectoryGenerator`, `/api/simulate`, obstacle CRUD, IK cache |
| **Umaya** | RapidPanel → `/api/simulate` wiring, `PlaybackControls`, collision visualization |
| **Jason** | Parser test coverage, docs, TBD |
| **Dylane** | Unavailable Week 5 — returns Week 6 for obstacle UI + transform gizmo |

Full breakdown in `docs/08-SPRINT-PLAN-W5-W8.md`.

---

### Trajectory Technical Decisions

**Approach:** Time-based trajectory using RAPID speed data
- `v100` = 100 mm/s, `v500` = 500 mm/s, `v1000` = 1000 mm/s
- Waypoint spacing: `ceil(distance / (speed * dt))` where `dt = 20ms`
- Each waypoint carries a `timestamp` (seconds from start)

**MoveC:** In MVP scope — required for arc weld and pick paths in real programs.

**Playback:** Frontend-driven with precomputed waypoints
- Backend returns full trajectory array once
- Frontend uses timestamps in `requestAnimationFrame` loop
- Speed control = scale timestamp intervals client-side
- No streaming, no backend state between frames

---

### Infrastructure (Completed March 3)

- All 4 personal branches (noah, jason, dylane, umaya) synced to main
- CI optimized: split lint/test jobs, single Python 3.12, concurrency cancel on push
- Frontend CI: updated to Node 20/22 matrix (Vite 7 requirement)
- ESLint: migrated to v9 flat config format
- Backend linting: all ruff violations resolved

---

### Action Items

- [x] **Noah:** Build `/api/parse`, `TrajectoryGenerator`, `/api/simulate`, obstacle CRUD (Week 5)
- [ ] **Umaya:** Wire `RapidPanel` → `/api/simulate`, build `PlaybackControls` (Week 5-6)
- [ ] **Jason:** Parser test coverage review, edge case additions
- [ ] **Dylane:** Return Week 6 — obstacle UI + gizmo + `TimelineScrubber`

---

## 2026-03-03 — SAIT ARIS Strategy Meeting

**Attendees:** Noah, Jason (ARIS team)
**Purpose:** Project ownership, deployment direction, and backend architecture for post-semester

---

### Decision: C# Backend Migration

**Decision:** The Python/FastAPI backend will be fully replaced by a C#/.NET backend after the semester ends (Summer 2026).

**Rationale:**
- ABB provides a C# API for direct robot controller integration (RobotStudio, IRC5/OmniCore controllers)
- Industrial PLCs and automation controllers primarily support C# and .NET
- Aligns the platform with real industrial deployment requirements beyond the classroom MVP
- ARIS team member has C# background — reduces ramp-up cost for handoff

**Timeline:** Post-semester, Summer 2026. Python/FastAPI carries the project through MVP delivery.

**Scope:** Full swap — complete C# backend built and tested against the OpenAPI contract before replacing Python. No incremental migration. Frontend (React + Babylon.js) is unchanged.

---

### Decision: Contract-First Architecture

**Decision:** Define the full API contract now as an OpenAPI 3.1 document. Both the Python MVP and the future C# backend are built against this contract. The contract is the source of truth for all backend-frontend communication.

**Contract artifact:**
- Committed file: `docs/contract/openapi.json` — versioned with the codebase, authoritative
- Live reference: FastAPI also serves `/openapi.json` — reflects what's currently implemented (may lag behind the committed contract during development)

**Contract model:** Core contract + extensions
- All endpoints in `docs/contract/openapi.json` are required — C# must implement them all
- C# backend may add ABB-specific extensions (RobotStudio integration, live controller API) beyond the core contract
- Frontend depends only on core contract endpoints

**Migration approach:** Full swap, not incremental
- Python MVP remains the running backend until C# is complete
- C# backend validated against the committed contract before switchover
- No hybrid period with both backends running simultaneously

---

### Cross-Branch Implementation Notes

Work is distributed across git branches:

| Branch | Work | Key Files |
|--------|------|-----------|
| `jason` | RAPID parser | `grammar.lark`, `transformer.py`, `ast_nodes.py`, `parser.py` |
| `noah` | Kinematics + collision | `app/kinematics/solver.py`, `app/collision/detector.py` |
| `dylane` / `frontend` | Frontend UI | React components, Babylon.js scene, Tailwind layout |

Integration of parser (jason) into the noah backend is a pending action item before MVP.

---

### Action Items

- [x] **All:** Freeze `docs/contract/openapi.json` before C# development begins — committed to repo
- [x] **Jason:** Integrate RAPID parser from `jason` branch into `noah` backend upload endpoint — merged via PR #4
- [x] **Noah:** Complete trajectory generator (`app/kinematics/trajectory.py`) to unblock `/api/simulate`
- [ ] **Team:** MVP sign-off by Week 8 per roadmap

---

**Last Updated:** 2026-03-03

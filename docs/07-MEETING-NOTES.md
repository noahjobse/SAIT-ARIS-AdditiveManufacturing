# Meeting Notes

**Project:** ABB Online Simulation Platform

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

- [ ] **All:** Freeze `docs/contract/openapi.json` before C# development begins
- [ ] **Jason:** Integrate RAPID parser from `jason` branch into `noah` backend upload endpoint
- [ ] **Noah:** Complete trajectory generator (`app/kinematics/trajectory.py`) to unblock `/api/simulate`
- [ ] **Team:** MVP sign-off by Week 8 per roadmap

---

**Last Updated:** 2026-03-03

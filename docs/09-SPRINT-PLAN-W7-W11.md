# Sprint Plan: Weeks 7–11 (Final Push)

**Project:** ArmStudio — ABB Online Simulation Platform
**Date:** 2026-03-17
**Deadline:** Week 11 (end of April)

---

## Production Stack

| Layer | Service | Purpose |
|-------|---------|---------|
| Frontend | **Vercel** | Next.js app (Babylon.js viewport, code editor, dashboard) |
| Backend | **Render** | FastAPI + PyBullet container (parse, simulate, collision) |
| Auth + DB | **Supabase** | Student accounts, saved programs, simulation history, obstacles |
| Payments | **Stripe** | Single subscription tier |

---

## Completed (as of Week 7 start)

### Backend ✅
- B1: Collision detection wired into `/api/simulate` pipeline
- B3: IK LRU cache (1000 entries, 0.1mm rounding)
- B4: 10s simulate timeout with partial result return
- B5: Obstacle CRUD — in-memory registry, list/delete endpoints
- B7: Tool TCP offset support in trajectory generator
- B8: CIRAMM marker demo RAPID program

### Migration ✅
- Next.js 16 scaffold with Babylon.js verified (GLB loading + joint control)
- Vite components moved to `_reference/` for porting
- Lint and build passing

---

## Remaining Tasks

### Backend
| # | Task |
|---|------|
| B6 | `/api/simulate` integration tests |

### Next.js Migration
| # | Task |
|---|------|
| M1 | Port MainLayout, Header, SidePanel, SidePanelTabs |
| M2 | Port RapidPanel — wire to real API |
| M3 | Port PlaybackControls with trajectory interpolation |
| M4 | Port JointJogPanel (with per-robot joint limits) |
| M5 | Port StatusPanel, BottomPanel, log system |
| M6 | Configure Next.js API proxy to FastAPI |
| M7 | Delete `_reference/` files once port complete |

### Docker
| # | Task |
|---|------|
| M8 | Production Next.js Dockerfile (multi-stage build) |
| M9 | New `docker-compose.yml` — 2 services, networking, health checks |

### Frontend — Code Editor
| # | Task |
|---|------|
| F1-F6 | CodeMirror, new file, save/download, load example, file name header, validation |

### Frontend — Execution UX
| # | Task |
|---|------|
| F7-F11 | Inline error banner, progress indicator, actionable messages, success indicator, clear no-trajectory |

### Frontend — Playback
| # | Task |
|---|------|
| F12-F17 | Stop/reset, loop, default 1.0x, end state, live readout, waypoint markers |
| F28 | Tool tip visualization — TCP path trace |

### Frontend — Joint Jog
| # | Task |
|---|------|
| F18-F21 | Decimal rounding, playback/jog indicator, conflict behavior, timer fix |

### Frontend — Layout & Visualization
| # | Task |
|---|------|
| F22-F23 | Drag-to-resize panels, log filtering |
| F24-F27 | Collision highlighting, obstacle UI + gizmo, loading spinners |

### Auth + Persistence (Supabase)
| # | Task |
|---|------|
| S1 | Set up Supabase project (auth + Postgres) |
| S2 | Auth — sign up/in, protected routes, session management |
| S3 | DB schema — users, programs, simulations, obstacles |
| S4 | Save/load RAPID programs per user |
| S5 | Save simulation history + results per user |
| S6 | Save obstacle setups per user |

### Payments (Stripe)
| # | Task |
|---|------|
| P1 | Stripe PoC — single subscription tier, checkout, webhook |
| P2 | Paywall gate — restrict simulate to subscribers |

### Landing Page
| # | Task |
|---|------|
| L1 | Marketing landing page — hero, features, pricing, CTA |

### User Dashboard
| # | Task |
|---|------|
| U1 | Dashboard — saved programs, simulation history, obstacle setups |

### Deploy
| # | Task |
|---|------|
| D1 | Vercel deploy (Next.js frontend) |
| D2 | Render deploy (FastAPI + PyBullet container) |
| D3 | CI/CD pipeline for both services |

### Deliverables
| # | Task |
|---|------|
| D4 | ARIS handoff docs (architecture, setup, API reference) |
| D5 | Capstone poster |

---

## Week-by-Week Schedule

### Week 7 (March 17) — Merge + Migration + Supabase Setup
*3 people: Noah, Jason, Umaya (Dylane unavailable)*

| Owner | Tasks |
|-------|-------|
| **Noah** | B6: Simulate integration tests. S1: Set up Supabase project. S3: DB schema. |
| **Jason** | M1: Port layout components. M2: Port RapidPanel. M6: API proxy config. |
| **Umaya** | M3: Port PlaybackControls. M4: Port JointJogPanel. M5: Port StatusPanel + BottomPanel. |

**Note:** Jason's layout shell (M1) should land first — Umaya's component ports depend on it.

### Week 8 — Auth + Editor + Playback
*4 people*

| Owner | Tasks |
|-------|-------|
| **Noah** | S2: Supabase auth integration. P1: Stripe PoC. |
| **Jason** | F1-F6: CodeMirror editor upgrade. M7: Delete `_reference/`. |
| **Umaya** | F7-F11: Execution UX. F18-F21: Joint jog fixes. |
| **Dylane** | F12-F17: Playback improvements. F28: Tool tip visualization. |

### Week 9 — Persistence + Docker + Landing Page
*4 people*

| Owner | Tasks |
|-------|-------|
| **Noah** | P2: Paywall gate. S4: Save/load programs. S5: Save simulation history. |
| **Jason** | M8: Next.js Dockerfile. M9: New docker-compose. L1: Landing page. |
| **Umaya** | F24-F27: Collision highlighting, obstacle UI, gizmo, spinners. S6: Save obstacle setups. |
| **Dylane** | F22-F23: Drag-to-resize, log filtering. U1: User dashboard. |

### Week 10 — Deploy + Docs + Cleanup
*4 people*

| Owner | Tasks |
|-------|-------|
| **Noah** | D1: Vercel deploy. D2: Render deploy. D3: CI/CD pipeline. |
| **Jason** | L1: Landing page. |
| **Umaya** | D4: ARIS handoff docs. |
| **Dylane** | D5: Capstone poster. |

### Week 11 — UAT + Polish
*All 4 people*

| Task |
|------|
| UAT with 5-10 real RAPID programs, multi-browser |
| Bug fixes from UAT |
| Regression suite + production smoke test |
| Docs finalized |
| Poster finalized + printed |
| UI polish pass |

---

## Dependencies & Coordination

| Dependency | Blocks | When |
|-----------|--------|------|
| Jason's layout shell (M1) | Umaya's component ports (M3-M5) | Week 7 Day 1-2 |
| Supabase schema (S3) | Auth (S2), persistence (S4-S6) | Week 7 → Week 8-9 |
| Migration complete (M1-M6) | All frontend features (F*) | Week 7 end |
| Supabase save APIs (S4-S6) | Dashboard (U1) | Week 9 |

## Risks

1. **Migration bottleneck** — Jason + Umaya porting ~10 components in one week
2. **Supabase learning curve** — First time setting up auth + persistence
3. **Backend hosting** — PyBullet container on Render needs testing (memory, cold starts)
4. **Dylane availability** — If Week 8 slips, playback + dashboard compress
5. **Stripe integration** — Webhook testing in dev can be tricky

---

**Last Updated:** 2026-03-17

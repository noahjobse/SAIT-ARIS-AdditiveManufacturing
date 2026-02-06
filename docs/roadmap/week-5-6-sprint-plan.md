# Week 5-6 Sprint Plan

**Sprint Duration:** Weeks 5-6 (14 days)
**Sprint Goal:** End-to-end `/api/simulate`, trajectory generation, collision detection
**Key Milestone:** Upload RAPID → see trajectory waypoints returned with collision data

---

## Sprint Overview

By the end of Week 6, we should have:

✅ `/api/simulate` endpoint complete (RAPID → trajectory JSON)
✅ Trajectory generator interpolates waypoints between move commands
✅ Collision detection works (robot vs obstacles, mesh-to-mesh)
✅ Frontend animates robot through trajectory waypoints
✅ Basic playback controls (play, pause, stop)
✅ Collision highlighting on robot mesh (visual warning)
✅ Obstacle meshes loaded into PyBullet collision world
✅ Performance <5 seconds for 100-waypoint trajectory
✅ Integration test (upload → parse → simulate → animate)

---

## Weekly Goals

### Week 5 Overview

**Frontend - Dylane:**
- Wire `/api/simulate` endpoint to Babylon.js animation system
- Implement basic playback controls (play, pause, stop buttons)
- Animate robot through trajectory waypoints with smooth interpolation

**Frontend - Umaya:**
- Create PlaybackControls component with styled buttons
- Add loading spinner during simulation request
- Begin collision highlighting research (how to recolor mesh)

**Backend - Jason:**
- Implement trajectory generator (AST → waypoints)
- Define SimulateRequest/Response Pydantic schemas
- Begin `/api/simulate` endpoint implementation
- Handle interpolation between MoveL/MoveJ/MoveC commands

**Backend - Noah:**
- Implement collision detector using PyBullet
- Load obstacle meshes into PyBullet collision world
- Test mesh-to-mesh collision detection
- Optimize collision checks for performance

**PM/QA - Noah:**
- Write integration test (upload → parse → simulate)
- Set up performance benchmarks (<5s for 100 waypoints)
- Create test cases for collision detection

### Week 6 Overview

**Frontend - Dylane:**
- Implement collision highlighting (change robot material when collision detected)
- Improve animation smoothness (interpolation between waypoints)
- Add current waypoint indicator in UI

**Frontend - Umaya:**
- Wire collision data from backend to visual highlighting
- Add simulation progress bar
- Display collision warnings in StatusPanel
- Style playback controls

**Backend - Jason:**
- Complete `/api/simulate` endpoint with error handling
- Add edge case handling (empty RAPID, unreachable targets)
- Optimize trajectory interpolation (adaptive step size)
- Return collision data in response

**Backend - Noah:**
- Optimize collision detection (disable self-collision)
- Load all uploaded obstacles into collision world
- Add mesh simplification for large STL files (optional)
- Implement collision response (which link, which obstacle)

**PM/QA - Noah:**
- Run performance benchmarks on various program sizes
- Test edge cases (collision at start, no collision, multiple collisions)
- Write end-to-end test (full pipeline)
- Prepare sprint review demo

---

## Critical Daily Tasks

### Blocking Dependencies

**Week 5 Day 1 (Jason):** Define SimulateRequest/Response Pydantic schemas
- **Blocks:** Dylane Day 3-4 frontend integration
- **Why:** Frontend needs contract (request/response structure) to wire `/api/simulate`
- **Deliverable:** Schema file committed with docstrings, example JSON documented

**Week 6 Day 1 (Noah Backend):** Load first obstacle mesh into PyBullet
- **Blocks:** Collision testing Week 6 Day 2-3
- **Why:** Collision detection requires obstacle geometry in physics world
- **Deliverable:** Obstacle STL loaded, collision world initialized

### Cross-Team Integration Points

**Week 5 Day 3-4 (Dylane):** Wire frontend to `/api/simulate`
- **Integration:** Requires Jason's schema and partial endpoint implementation
- **Verification:** Call `/api/simulate` with sample RAPID → receive trajectory JSON
- **Fallback:** If endpoint not ready, Dylane uses mock trajectory data temporarily

**Week 6 Day 4-5 (All Team):** Full end-to-end test
- **Integration:** RAPID upload → parse → simulate → animate → collision visible
- **Verification:** Upload program with obstacle in path → see red robot highlight
- **Demo:** Show full workflow in sprint review

---

## Weekly Task Breakdown

### Frontend - Dylane

**Week 5:**
- [ ] Create `AnimationController.ts` in `src/babylon/`
- [ ] Implement `playTrajectory(waypoints: Waypoint[])` function
- [ ] Animate robot through waypoints using skeleton bones
- [ ] Add smooth interpolation between waypoints (linear or cubic)
- [ ] Create `api.simulate(rapidCode: string)` function in `src/services/api.ts`
- [ ] Wire simulate API call to animation playback
- [ ] Add loading state during simulation request
- [ ] Test animation with mock trajectory data (10-20 waypoints)

**Week 6:**
- [ ] Create `CollisionHighlighter.ts` utility
- [ ] Implement `highlightCollision(linkIndex: number)` function
- [ ] Change robot material to red when collision detected
- [ ] Add `unhighlightCollision()` to restore original color
- [ ] Wire collision data from simulate response to highlighter
- [ ] Add current waypoint index display (optional)
- [ ] Test collision highlighting with multiple collision points
- [ ] Optimize animation performance (target 60 FPS)

**Deliverable:** Robot animates smoothly through trajectory, collision highlighting works, playback controls functional

---

### Frontend - Umaya

**Week 5:**
- [ ] Create `PlaybackControls.tsx` component in `src/components/controls/`
- [ ] Add play, pause, stop buttons with icons
- [ ] Wire buttons to AnimationController (start, pause, stop functions)
- [ ] Style buttons with Tailwind CSS (professional look)
- [ ] Add loading spinner component (`LoadingSpinner.tsx`)
- [ ] Display spinner during `/api/simulate` request
- [ ] Research Babylon.js material system for collision highlighting

**Week 6:**
- [ ] Create `ProgressBar.tsx` component for simulation progress
- [ ] Show progress: current waypoint / total waypoints
- [ ] Wire ProgressBar to AnimationController state
- [ ] Update StatusPanel to show collision warnings
- [ ] Display collision details (which link, which obstacle, timestamp)
- [ ] Add "Simulation Complete" message when trajectory finishes
- [ ] Test UI responsiveness during long simulations
- [ ] Polish playback controls styling (hover states, disabled states)

**Deliverable:** Playback controls styled and functional, collision warnings in StatusPanel, progress bar shows simulation state

---

### Backend - Jason

**Week 5:**
- [ ] Create `backend/app/schemas/simulate.py`
- [ ] Define `SimulateRequest` schema (rapid_code, robot_id, obstacles)
- [ ] Define `Waypoint` schema (timestamp, joint_angles, tcp_position, collision)
- [ ] Define `SimulateResponse` schema (waypoints, duration, errors)
- [ ] Create `backend/app/trajectory/generator.py`
- [ ] Implement `generate_trajectory(ast: List[ASTNode])` function
- [ ] Interpolate waypoints for MoveL (linear interpolation)
- [ ] Interpolate waypoints for MoveJ (joint space interpolation)
- [ ] Add basic interpolation for MoveC (circular, simplified)

**Week 6:**
- [ ] Create `/api/simulate` endpoint in `routers/simulate.py`
- [ ] Wire endpoint to parser and trajectory generator
- [ ] Call collision detector for each waypoint (Noah's function)
- [ ] Add error handling for unreachable targets
- [ ] Add error handling for empty RAPID programs
- [ ] Implement adaptive step size (coarse for long moves, fine for short)
- [ ] Optimize trajectory generation (<5s for 100 waypoints)
- [ ] Write docstrings and add logging

**Deliverable:** `/api/simulate` endpoint complete, trajectory generation working, collision data included in response

---

### Backend - Noah

**Week 5:**
- [ ] Create `backend/app/collision/detector.py`
- [ ] Initialize PyBullet collision world (separate from kinematics world)
- [ ] Implement `load_obstacle_mesh(obstacle_id: string, stl_path: string)`
- [ ] Load obstacle STL into PyBullet using `p.createCollisionShape`
- [ ] Implement `check_collision(robot_id: string, joint_angles: List[float])`
- [ ] Test collision detection with robot at home position vs obstacle
- [ ] Verify mesh-to-mesh collision works (not just bounding boxes)
- [ ] Document collision detection limitations (mesh resolution)

**Week 6:**
- [ ] Implement `get_collision_details()` to return link index and obstacle ID
- [ ] Disable self-collision checks (robot links don't collide with each other)
- [ ] Load multiple obstacles into collision world
- [ ] Add mesh simplification for large STL files (use PyBullet mesh decimation)
- [ ] Optimize collision checks (only check nearby obstacles, not all)
- [ ] Add timeout for collision detection (max 100ms per check)
- [ ] Test collision detection with 5+ obstacles in scene
- [ ] Write unit tests for collision detector

**Deliverable:** Collision detector working, obstacles loaded, collision details returned (link + obstacle)

---

### PM/QA - Noah

**Week 5:**
- [ ] Create `backend/tests/test_simulate_integration.py`
- [ ] Write test: upload RAPID → parse → simulate → verify trajectory returned
- [ ] Write test: simulate with empty RAPID → verify error response
- [ ] Write test: simulate with unreachable target → verify error or warning
- [ ] Create `backend/tests/test_collision.py`
- [ ] Write test: robot at home, obstacle far → no collision
- [ ] Write test: robot at position, obstacle intersecting → collision detected
- [ ] Set up performance benchmark script (measure simulation time)

**Week 6:**
- [ ] Run performance benchmarks: 50, 100, 200 waypoint trajectories
- [ ] Document performance results in `docs/performance-benchmarks.md`
- [ ] Write test: simulate with multiple collisions → verify all detected
- [ ] Write test: trajectory with no collisions → verify clean response
- [ ] Test edge case: collision on first waypoint
- [ ] Test edge case: collision on last waypoint
- [ ] Create end-to-end test script (automate full workflow)
- [ ] Prepare demo script and test data for sprint review

**Deliverable:** Integration tests pass, performance benchmarks documented, collision tests comprehensive

---

## Risk Management

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Trajectory interpolation too slow (>5s per simulation) | Medium | High | Implement adaptive step size (coarse interpolation for MVP); optimize in Week 7 if needed |
| Collision detection false positives (robot "self-collides") | Medium | Medium | Disable self-collision checks; only check robot vs obstacles, not robot vs robot links |
| Animation jittery due to large JSON payloads | Low | Medium | Limit waypoint count (max 500); compress trajectory data (omit redundant fields) |
| PyBullet mesh loading fails for some STL files | Low | High | Add STL validation on upload; provide error message with file requirements |
| IK fails for some trajectory waypoints | High | High | Catch IK failures, mark waypoint as "unreachable", continue simulation with warning |
| Collision detection too slow for real-time playback | Medium | Medium | Pre-compute collisions during `/api/simulate`, not during playback; cache results |

---

## Testing Requirements

**Week 5:**
- [ ] Test trajectory generator with simple MoveL program (Jason + Noah)
- [ ] Test trajectory interpolation produces smooth path (Jason)
- [ ] Test collision detector with known collision scenario (Noah)
- [ ] Test obstacle mesh loads into PyBullet (Noah)
- [ ] Test `/api/simulate` returns valid trajectory JSON (Jason + Noah)
- [ ] Test frontend calls `/api/simulate` successfully (Dylane)
- [ ] Test playback controls start/stop animation (Umaya)

**Week 6:**
- [ ] Test collision highlighting changes robot color (Dylane + Umaya)
- [ ] Test multiple obstacles in collision world (Noah)
- [ ] Test `/api/simulate` with edge cases (empty, unreachable, etc.) (Noah)
- [ ] Test performance: 100 waypoints in <5s (Noah)
- [ ] Test end-to-end: upload → simulate → animate → collision visible (All)
- [ ] Test progress bar updates during playback (Umaya)
- [ ] Test collision warnings appear in StatusPanel (Umaya)

---

## Demo-Ready Acceptance Criteria

By end of this sprint, team can demo:

### Week 5 Demo Criteria:
- [ ] Upload RAPID program → click Simulate → receive trajectory JSON
- [ ] Robot animates through waypoints (basic playback, may be choppy)
- [ ] Play, pause, stop buttons control animation
- [ ] Loading spinner shows during simulation request
- [ ] Collision detection works in backend (tested via API, not visible yet)

### Week 6 Demo Criteria (Full Sprint):
- [ ] **Upload RAPID program → click Simulate → robot animates through full trajectory**
- [ ] **Place obstacle in robot path → collision warning visible (red highlight on robot)**
- [ ] **Simulation completes in <5 seconds for typical program (50-200 moves)**
- [ ] Progress bar shows current waypoint / total waypoints
- [ ] Collision warnings appear in StatusPanel with details
- [ ] Play/pause/stop controls work smoothly
- [ ] Animation runs at 60 FPS (no jitter or lag)

---

## Definition of Done

A task is **DONE** when:

✅ Code written and committed to repo
✅ Code reviewed by at least one other team member (informal or PR)
✅ Tests written and passing (if applicable)
✅ No linting errors (ruff for backend, eslint for frontend)
✅ Documented in code comments (complex logic explained)
✅ Verified in browser/API (manual smoke test)

---

## Team Assignments

| Person | Focus Area | Key Deliverable |
|--------|-----------|-----------------|
| **Dylane** | Animation + collision highlighting | Robot animates, collision visible |
| **Umaya** | Playback controls + progress UI | Controls styled, collision warnings shown |
| **Jason** | Trajectory generator + `/api/simulate` | Endpoint complete, waypoints generated |
| **Noah (Backend)** | Collision detector + mesh loading | Collision detection working |
| **Noah (QA/PM)** | Integration tests + performance | Tests pass, benchmarks documented |

---

## Communication

**Slack Channels:**
- `#abb-sim-dev` - General development discussion
- `#abb-sim-frontend` - Frontend-specific questions (Dylane, Umaya)
- `#abb-sim-backend` - Backend-specific questions (Jason, Noah)
- `#abb-sim-qa` - Testing and QA updates (Noah)

**Daily Standup:** 9:00 AM (15 minutes, async updates on weekends)

**Sprint Review:** End of Week 6 (30-minute demo, retrospective)

---

## Success Metrics

By end of Week 6, we should achieve:

- [ ] **Frontend:** Robot animates through trajectory, collision highlighted
- [ ] **Frontend:** Playback controls and progress bar functional
- [ ] **Backend:** `/api/simulate` endpoint complete
- [ ] **Backend:** Collision detection working for robot + obstacles
- [ ] **QA:** Integration tests pass, performance <5s
- [ ] **QA:** End-to-end workflow tested

**Sprint Goal Achievement:** 🟢 Green if all 6 items complete, 🟡 Yellow if 4-5 complete, 🔴 Red if <4 complete

---

## Next Sprint Planning

**Week 7-8 Preview (MVP Launch):**
- Dylane: Timeline scrubber, step-through controls
- Umaya: Error states, loading indicators, responsive layout fixes
- Jason: IK caching, edge case handling
- Noah (Backend): Input validation, timeout handling
- Noah (QA): Full regression testing, UAT with real RAPID programs, MVP sign-off

**Week 7-8 Goal:** Timeline scrubber, playback controls polished, MVP student demo ready

---

**Document Owner:** Noah (PM/QA Lead)
**Created:** 2026-02-05
**Last Updated:** 2026-02-05
**Next Update:** End of Week 6 (Sprint Review)

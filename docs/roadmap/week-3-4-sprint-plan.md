# Week 3-4 Sprint Plan

**Sprint Duration:** Weeks 3-4 (14 days)
**Sprint Goal:** RAPID parser complete, FK/IK working, obstacles in scene
**Key Milestone:** Upload RAPID → get parsed AST, kinematics validated

---

## Sprint Overview

By the end of Week 4, we should have:

✅ Obstacle STL files load into 3D scene
✅ 3D transform gizmo allows manual positioning of obstacles
✅ RAPID parser handles MoveL, MoveJ, and MoveC commands
✅ AST structure represents parsed RAPID code
✅ PyBullet physics engine integrated (headless mode)
✅ Forward kinematics (FK) solver returns TCP position from joint angles
✅ Inverse kinematics (IK) solver returns joint angles for target TCP position
✅ URDF files created for all 3 robots (IRB 4600, 2600, 6700)
✅ StatusPanel displays parsing errors and warnings
✅ Parser test suite validates grammar against sample programs

---

## Weekly Goals

### Week 3 Overview

**Frontend - Dylane:**
- Load obstacle STL files from backend API
- Display multiple obstacles in 3D scene
- Begin transform gizmo implementation (position control)

**Frontend - Umaya:**
- Create StatusPanel component to display errors/warnings
- Build obstacle list sidebar showing uploaded obstacles
- Wire StatusPanel to consume backend error responses

**Backend - Jason:**
- Create Lark grammar skeleton for MoveL/MoveJ/MoveC
- Define AST node classes (MoveL, MoveJ, MoveC, RobTarget, JointTarget)
- Begin parser implementation with basic move commands

**Backend - Noah:**
- Set up PyBullet in headless mode
- Load first URDF file for IRB 4600
- Implement forward kinematics (FK) solver
- Validate FK against known configurations

**PM/QA - Noah:**
- Create parser test suite foundation
- Write tests for simple MoveL commands
- Set up FK validation tests with known positions

### Week 4 Overview

**Frontend - Dylane:**
- Complete transform gizmo (add rotation controls)
- Wire gizmo updates to backend obstacle position API
- Test gizmo with multiple obstacles

**Frontend - Umaya:**
- Display parsing errors from `/api/upload/rapid` in StatusPanel
- Add obstacle metadata to sidebar (position, rotation)
- Improve RAPID editor with syntax highlighting (optional stretch)

**Backend - Jason:**
- Complete Lark grammar for all move command variants
- Implement AST transformer to convert parse tree to AST nodes
- Add error handling for malformed RAPID syntax
- Wire parser to `/api/upload/rapid` endpoint

**Backend - Noah:**
- Implement inverse kinematics (IK) solver using PyBullet
- Create URDF files for IRB 2600 and IRB 6700
- Validate IK convergence for reachable targets
- Document IK solver limitations (unreachable zones)

**PM/QA - Noah:**
- Write comprehensive parser tests (valid/invalid syntax)
- Create FK/IK validation test suite
- Test all 3 robot URDFs with known configurations
- Prepare end-of-sprint demo

---

## Critical Daily Tasks

### Blocking Dependencies

**Week 3 Day 1 (Jason):** Create `grammar.lark` skeleton
- **Blocks:** Week 4 parser implementation
- **Why:** Grammar defines parser structure; must be in place before AST transformation
- **Deliverable:** Basic grammar file with MoveL rule, committed to repo

**Week 3 Day 2-3 (Noah Backend):** PyBullet setup + first URDF loaded
- **Blocks:** Week 4 IK solver implementation
- **Why:** IK solver requires PyBullet physics engine and robot model
- **Deliverable:** PyBullet headless running, IRB 4600 URDF loads successfully

### Cross-Team Integration Points

**Week 4 Day 3-4 (Umaya):** StatusPanel consumes `/api/upload/rapid` errors
- **Integration:** Requires Jason's parser returning error responses
- **Verification:** Upload malformed RAPID → see error message in StatusPanel
- **Fallback:** If parser delayed, StatusPanel shows mock errors temporarily

**Week 4 Day 5 (All Team):** End-of-sprint demo preparation
- **Integration:** Full pipeline test (RAPID upload → parse → AST display)
- **Verification:** Upload `simple_movel.mod` → see AST, no errors, FK testable
- **Demo:** Show obstacle in scene with gizmo, show parsed RAPID in UI

---

## Weekly Task Breakdown

### Frontend - Dylane

**Week 3:**
- [ ] Create `ObstacleLoader.ts` utility in `src/babylon/`
- [ ] Implement `loadObstacle(obstacleId: string)` function
- [ ] Load obstacle STL from `/api/obstacles/{id}/mesh` using SceneLoader
- [ ] Support multiple obstacles in scene (track in array)
- [ ] Add basic click detection on obstacles for selection
- [ ] Research Babylon.js GizmoManager and TransformNode
- [ ] Begin gizmo implementation (position gizmo only)

**Week 4:**
- [ ] Complete `TransformGizmo.ts` utility
- [ ] Implement rotation gizmo (BoundingBoxGizmo or RotationGizmo)
- [ ] Wire gizmo position/rotation changes to state
- [ ] Call `PUT /api/obstacles/{id}/transform` when gizmo released
- [ ] Add visual feedback when obstacle selected (highlight/outline)
- [ ] Test gizmo with 2-3 obstacles simultaneously
- [ ] Verify gizmo snaps to selected obstacle

**Deliverable:** Obstacle STLs load in scene, transform gizmo allows positioning and rotation, changes persist to backend

---

### Frontend - Umaya

**Week 3:**
- [ ] Create `StatusPanel.tsx` component in `src/components/panels/`
- [ ] Design panel layout (collapsible, bottom or side of viewport)
- [ ] Add sections for Errors, Warnings, Info messages
- [ ] Style with Tailwind CSS (red for errors, yellow for warnings)
- [ ] Create `ObstacleList.tsx` component for sidebar
- [ ] Display uploaded obstacles with name and thumbnail (optional)
- [ ] Wire ObstacleList to global state (track uploaded obstacles)

**Week 4:**
- [ ] Wire StatusPanel to consume errors from `api.uploadRapid()` response
- [ ] Display parsing errors with line numbers (if available in response)
- [ ] Add clear button to dismiss messages
- [ ] Update ObstacleList to show position/rotation metadata
- [ ] Add delete button for obstacles (calls `DELETE /api/obstacles/{id}`)
- [ ] Optional: Integrate Monaco Editor for syntax highlighting in RapidEditor
- [ ] Test error display with malformed RAPID files

**Deliverable:** StatusPanel shows parsing errors, ObstacleList displays obstacles with metadata, UI responsive

---

### Backend - Jason

**Week 3:**
- [ ] Create `backend/app/parser/grammar.lark`
- [ ] Define grammar rules for `movel` instruction (basic version)
- [ ] Define grammar rules for `robtarget` (position + quaternion + config)
- [ ] Define grammar rules for `speed` and `zone` (v1000, z10, etc.)
- [ ] Create `backend/app/parser/ast_nodes.py`
- [ ] Define AST classes: `MoveL`, `MoveJ`, `MoveC`, `RobTarget`, `JointTarget`
- [ ] Test grammar with Lark standalone (parse simple MoveL string)

**Week 4:**
- [ ] Extend grammar for `movej` and `movec` instructions
- [ ] Add support for joint targets (array of 6 floats)
- [ ] Create `backend/app/parser/transformer.py`
- [ ] Implement Lark Transformer to convert parse tree to AST nodes
- [ ] Handle parsing errors gracefully (catch LarkError, return friendly message)
- [ ] Update `/api/upload/rapid` to use parser (return AST in response)
- [ ] Add line number tracking for error messages
- [ ] Write docstrings for all parser functions

**Deliverable:** RAPID parser complete for MoveL/MoveJ/MoveC, AST returned from upload endpoint, errors have line numbers

---

### Backend - Noah

**Week 3:**
- [ ] Install PyBullet: `pip install pybullet` (verify version 3.2.6)
- [ ] Create `backend/app/kinematics/pybullet_ik.py`
- [ ] Initialize PyBullet in headless mode (DIRECT connection)
- [ ] Create `backend/models/robots/irb4600/robot.urdf`
- [ ] Define URDF structure (links, joints, DH parameters)
- [ ] Load URDF into PyBullet: `p.loadURDF("robot.urdf")`
- [ ] Implement `forward_kinematics(joint_angles: List[float])` function
- [ ] Test FK with known configuration (compare to datasheet)

**Week 4:**
- [ ] Implement `inverse_kinematics(target_position: List[float], target_orientation: List[float])` function
- [ ] Use `p.calculateInverseKinematics()` with proper constraints
- [ ] Add joint limit enforcement in IK solver
- [ ] Test IK convergence for 10+ reachable targets
- [ ] Create URDF files for IRB 2600 and IRB 6700
- [ ] Verify all 3 URDFs load into PyBullet successfully
- [ ] Document unreachable zones (IK fails to converge)
- [ ] Add timeout handling for IK solver (max 1 second per solve)

**Deliverable:** FK/IK solvers working, all 3 robot URDFs validated, IK limitations documented

---

### PM/QA - Noah

**Week 3:**
- [ ] Create `backend/tests/test_parser.py`
- [ ] Write test for parsing simple MoveL command
- [ ] Write test for parsing command with invalid syntax (expect error)
- [ ] Write test for parsing empty RAPID file (expect error)
- [ ] Create `backend/tests/test_kinematics.py`
- [ ] Write FK test: joint angles [0,0,0,0,0,0] → verify TCP position
- [ ] Write FK test: joint angles from datasheet → verify against datasheet TCP
- [ ] Run tests: `pytest tests/test_parser.py tests/test_kinematics.py`

**Week 4:**
- [ ] Extend parser tests for MoveJ and MoveC commands
- [ ] Write parser test for control flow (should fail gracefully, not supported yet)
- [ ] Write IK test: target within reach → verify joint angles returned
- [ ] Write IK test: target out of reach → verify error or warning
- [ ] Test all 3 robot URDFs with FK (same joint angles, different TCP positions)
- [ ] Create test matrix: 3 robots × 5 configurations
- [ ] Document test coverage in `docs/testing-strategy.md` (update)
- [ ] Prepare demo script for sprint review

**Deliverable:** Parser test suite passes, FK/IK validation tests pass for all 3 robots, demo prepared

---

## Risk Management

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Lark grammar too complex for MoveL/MoveJ/MoveC | Medium | High | Start with MoveL only, add MoveJ/MoveC incrementally; simplify target syntax if needed |
| PyBullet IK doesn't converge for some poses | High | Medium | Document limitations, add "unreachable" warnings in UI; use FK-only mode as fallback |
| URDF files have incorrect joint axes | Medium | High | Validate against ABB datasheets early (Week 3); test FK with known configs before IK |
| Transform gizmo UX issues (hard to control) | Low | Medium | Test with users, iterate on sensitivity; provide reset button |
| Parsing errors not user-friendly | Medium | Low | Add line number tracking, provide example of correct syntax in error messages |
| ObstacleLoader performance issues with large STL | Low | Medium | Limit STL file size to <10MB, simplify mesh if needed (decimate in Blender) |

---

## Testing Requirements

**Week 3:**
- [ ] Test Lark grammar parses simple MoveL command (Jason + Noah)
- [ ] Test URDF loads into PyBullet without errors (Noah)
- [ ] Test FK with joint angles [0,0,0,0,0,0] returns expected TCP (Noah)
- [ ] Test obstacle STL loads in Babylon.js scene (Dylane)
- [ ] Test StatusPanel renders without errors (Umaya)

**Week 4:**
- [ ] Test parser handles all move commands (MoveL, MoveJ, MoveC) (Noah)
- [ ] Test parser returns friendly errors for malformed RAPID (Noah)
- [ ] Test IK solver converges for 10+ reachable targets (Noah)
- [ ] Test IK solver fails gracefully for unreachable targets (Noah)
- [ ] Test transform gizmo updates obstacle position (Dylane)
- [ ] Test StatusPanel displays parsing errors from backend (Umaya)
- [ ] Test all 3 robot URDFs with known configurations (Noah)

---

## Demo-Ready Acceptance Criteria

By end of this sprint, team can demo:

### Week 3 Demo Criteria:
- [ ] Upload obstacle STL → see it appear in 3D scene
- [ ] Basic transform gizmo allows moving obstacle (position only)
- [ ] StatusPanel component visible in UI (empty or with mock messages)
- [ ] Upload simple RAPID → backend attempts to parse (may fail, WIP)
- [ ] Run FK solver with joint angles → verify TCP position logged

### Week 4 Demo Criteria (Full Sprint):
- [ ] **Upload simple_movel.mod → see parsed AST with no errors**
- [ ] **Enter 6 joint angles → FK returns correct TCP position (validated against datasheet)**
- [ ] **Place obstacle STL in scene with gizmo, save position**
- [ ] Transform gizmo allows both position and rotation of obstacles
- [ ] Upload malformed RAPID → see error message in StatusPanel
- [ ] IK solver tested (bonus: show in demo if time permits)
- [ ] All 3 robot models load into PyBullet (backend only, not visible in UI yet)

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
| **Dylane** | Obstacle loading + transform gizmo | Obstacles load, gizmo allows positioning/rotation |
| **Umaya** | StatusPanel + obstacle list | Errors displayed, obstacles listed in sidebar |
| **Jason** | RAPID parser | MoveL/MoveJ/MoveC parsed, AST structure defined |
| **Noah (Backend)** | PyBullet FK/IK solver | FK/IK working for all 3 robots |
| **Noah (QA/PM)** | Parser + kinematics tests | Test suite validates parser and FK/IK |

---

## Communication

**Slack Channels:**
- `#abb-sim-dev` - General development discussion
- `#abb-sim-frontend` - Frontend-specific questions (Dylane, Umaya)
- `#abb-sim-backend` - Backend-specific questions (Jason, Noah)
- `#abb-sim-qa` - Testing and QA updates (Noah)

**Daily Standup:** 9:00 AM (15 minutes, async updates on weekends)

**Sprint Review:** End of Week 4 (30-minute demo, retrospective)

---

## Success Metrics

By end of Week 4, we should achieve:

- [ ] **Frontend:** Obstacles load with transform gizmo working
- [ ] **Frontend:** StatusPanel displays parsing errors
- [ ] **Backend:** RAPID parser handles MoveL/MoveJ/MoveC
- [ ] **Backend:** FK/IK solvers working for all 3 robots
- [ ] **QA:** Parser tests and FK/IK tests passing
- [ ] **QA:** All 3 robot URDFs validated

**Sprint Goal Achievement:** 🟢 Green if all 6 items complete, 🟡 Yellow if 4-5 complete, 🔴 Red if <4 complete

---

## Next Sprint Planning

**Week 5-6 Preview:**
- Dylane: Wire `/api/simulate` to Babylon.js animation, basic playback
- Umaya: Collision highlighting on robot mesh, playback controls UI
- Jason: Trajectory generator (AST → interpolated waypoints)
- Noah (Backend): Collision detector (mesh-to-mesh via PyBullet)
- Noah (QA): Integration tests, performance benchmarks

**Week 5-6 Goal:** End-to-end `/api/simulate`, trajectory generation, collision detection

---

**Document Owner:** Noah (PM/QA Lead)
**Created:** 2026-02-05
**Last Updated:** 2026-02-05
**Next Update:** End of Week 4 (Sprint Review)

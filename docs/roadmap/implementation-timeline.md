# Implementation Timeline

**Project:** ABB Online Simulation Platform
**Team:** 4 members (Dylane, Umaya, Jason, Noah)
**Duration:** 11 weeks
**MVP Target:** Week 8
**Date:** 2026-02-05

## High-Level Phases

| Weeks | Phase | Frontend (Dylane + Umaya) | Backend - Jason | Backend - Noah | PM/QA (Noah) |
|-------|-------|--------------------------|-----------------|----------------|--------------|
| **1-2** | Foundation | Babylon.js scene, robot GLB loading, joint sliders, app layout shell, upload UI, robot selector | Router structure, `/api/robots`, `/api/robots/{id}/model`, GLB serving | `/api/upload/rapid` + `/api/upload/obstacle` endpoints, file handling, Pydantic schemas | Test infra (pytest + vitest), CI green, add GLB files to repo, sample RAPID files |
| **3-4** | Parse & Solve | Obstacle STL loading + transform gizmo, StatusPanel, RAPID editor panel, obstacle list sidebar | Lark grammar + parser (MoveL/MoveJ/MoveC/targets), AST node definitions | FK/IK solver with PyBullet headless, URDF creation for all 3 robots, robot config loader | Parser test suite, FK/IK validation tests, sample RAPID programs |
| **5-6** | Simulation Pipeline | Wire `/api/simulate` to Babylon.js animation, basic playback (play/pause/stop), collision highlighting | Trajectory generator (AST → interpolated waypoints), `/api/simulate` endpoint | Collision detector (mesh-to-mesh via PyBullet), mesh loader for obstacles | Integration tests, performance benchmarks, collision test cases |
| **7-8** | MVP Polish | Timeline scrubber, speed controls, step-through, error states, loading indicators, bug fixes | IK caching, batch optimization, edge case handling, bug fixes | Error responses, input validation hardening, bug fixes | Full regression, UAT with real RAPID programs, MVP sign-off |
| **9-10** | Control Flow + Multi-Robot | Multi-robot selector for all 3 models, UI improvements | Extend Lark grammar (IF/ELSE/FOR/WHILE/procedures), AST interpreter | Multi-robot configs, control flow execution engine | Control flow tests, multi-robot test matrix |
| **11** | Handoff | UI final polish, demo mode | API docs auto-gen, deployment config | Architecture docs, deployment scripts | User guide, final test pass, demo prep |

---

## Week-by-Week Breakdown

### Week 1-2: Foundation

**Goal:** 3D scene working, robot loads and moves, API structure, upload flow

**Key Milestone:** Robot visible and joints controllable in browser

#### Frontend - Dylane

**Week 1:**
- [ ] Initialize Babylon.js scene (canvas, ArcRotateCamera, HemisphericLight)
- [ ] Add ground plane + grid helper
- [ ] Load IRB 4600 GLB from `/api/robots/irb4600/model`
- [ ] Render robot mesh in viewport (static, no animation yet)
- [ ] Ensure camera orbits around robot with mouse controls

**Week 2:**
- [ ] Implement skeleton-based joint animation on loaded GLB
- [ ] Build 6 joint angle sliders (range: -180° to +180°)
- [ ] Wire sliders to robot skeleton joints
- [ ] Add axis labels (J1-J6) and current angle display
- [ ] Test joint limits (verify no gimbal lock or visual glitches)

**Deliverable:** Robot visible and orbitable, joints move smoothly via sliders

---

#### Frontend - Umaya

**Week 1:**
- [ ] Build App layout shell (Header, MainLayout with split pane, SidePanel)
- [ ] Implement responsive layout (70% viewport, 30% sidebar)
- [ ] Create robot selector dropdown (placeholder options: IRB 4600, 2600, 6700)
- [ ] Wire dropdown to state management (`currentRobot` context)
- [ ] Apply Tailwind CSS styling (dark theme, professional look)

**Week 2:**
- [ ] Build file upload component (drag & drop + click to browse)
- [ ] Support two upload types: RAPID (`.mod`) and STL (`.stl`)
- [ ] Add upload buttons in Header ("Upload RAPID", "Upload Obstacle")
- [ ] Build RapidEditor panel (textarea with monospace font)
- [ ] Wire upload component to call `/api/upload/rapid` and `/api/upload/obstacle`
- [ ] Display uploaded RAPID code in editor panel

**Deliverable:** Files uploadable through UI, layout responsive and styled

---

#### Backend - Jason

**Week 1:**
- [ ] Set up FastAPI router structure (`routers/robots.py`, `routers/upload.py`, `routers/simulate.py`)
- [ ] Implement `GET /api/robots` endpoint (return hardcoded list of 3 robots)
- [ ] Implement `GET /api/robots/{id}/model` endpoint (serve GLB binary from `/models/robots/`)
- [ ] Create robot config JSON for IRB 4600 (DH parameters, joint limits, reach)
- [ ] Add CORS middleware to `main.py`
- [ ] Test endpoints via Swagger UI (`/docs`)

**Week 2:**
- [ ] Research Lark parser library (read docs, run examples)
- [ ] Draft initial RAPID grammar (`grammar.lark`) for MoveL only (simplified)
- [ ] Implement `POST /api/upload/rapid` endpoint skeleton (accepts file, returns placeholder AST)
- [ ] Add file validation (check `.mod` extension, max 1MB size)
- [ ] Return errors for malformed files
- [ ] Test with sample RAPID file

**Deliverable:** Robot list and GLB serving working, upload endpoints accepting files

---

#### Backend - Noah

**Week 1:**
- [ ] Copy IRB 4600 GLB file from local path to `/models/robots/irb4600/visual.glb`
- [ ] Add GLB files to git repo (commit with message "Add IRB 4600 GLB model")
- [ ] Set up pytest configuration (verify `pyproject.toml` is correct)
- [ ] Write test for `GET /api/health` endpoint
- [ ] Write test for `GET /api/robots` endpoint
- [ ] Set up GitHub Actions CI to run on push (verify backend-ci.yml works)

**Week 2:**
- [ ] Implement `POST /api/upload/rapid` endpoint (file handler logic)
- [ ] Implement `POST /api/upload/obstacle` endpoint (STL file handler logic)
- [ ] Create Pydantic schemas for upload requests (`schemas/requests.py`)
- [ ] Create Pydantic schemas for upload responses (`schemas/responses.py`)
- [ ] Write tests for file upload (valid file, invalid extension, file too large)
- [ ] Create 3 sample RAPID programs for testing (simple MoveL, MoveJ, MoveC examples)

**Deliverable:** Upload endpoints functional, test coverage for uploads, sample RAPID files ready

---

#### PM/QA - Noah

**Week 1:**
- [ ] Set up Vitest configuration for frontend (`vitest.config.ts`)
- [ ] Write one basic frontend test (render `<App />` component)
- [ ] Verify CI pipelines run successfully (backend + frontend)
- [ ] Create `.github/ISSUE_TEMPLATE.md` for bug reports
- [ ] Schedule Week 2 standup (check team progress)

**Week 2:**
- [ ] Write integration test: Upload RAPID file → receive response
- [ ] Document testing strategy in `docs/testing-strategy.md` (test pyramid, coverage targets)
- [ ] Create test data directory (`tests/fixtures/rapid/`) with sample RAPID programs
- [ ] Review code from Dylane, Umaya, Jason (PR reviews or informal)
- [ ] Update task assignments doc with Week 3-4 detailed breakdown

**Deliverable:** Test infrastructure running in CI, sample test data available

---

### Week 3-4: Parse & Solve

**Goal:** RAPID parser complete, FK/IK working, obstacles in scene

**Key Milestone:** Upload RAPID → get parsed AST, kinematics validated

#### Frontend - Dylane

**Week 3:**
- [ ] Implement STL mesh loading into Babylon.js scene
- [ ] Add obstacle list in sidebar (show uploaded obstacle names)
- [ ] Implement transform gizmo (PositionGizmo, RotationGizmo from Babylon.js)
- [ ] Wire gizmo to selected obstacle (click obstacle → activate gizmo)
- [ ] Save obstacle transform to state when gizmo changes

**Week 4:**
- [ ] Add obstacle delete button (remove from scene + state)
- [ ] Implement obstacle visibility toggle (show/hide checkbox per obstacle)
- [ ] Add obstacle bounds visualization (wireframe bounding box)
- [ ] Test with multiple obstacles (5+ STLs in scene)
- [ ] Performance optimization if needed (LOD, instancing)

**Deliverable:** Obstacles placeable in 3D, gizmo working smoothly

---

#### Frontend - Umaya

**Week 3:**
- [ ] Build StatusPanel component (show parse errors/warnings)
- [ ] Wire StatusPanel to parse response from `/api/upload/rapid`
- [ ] Display errors with line numbers and messages
- [ ] Add "Parsed Successfully" indicator (green checkmark)
- [ ] Style error messages (red for errors, yellow for warnings)

**Week 4:**
- [ ] Build obstacle list sidebar (table or card layout)
- [ ] Show obstacle metadata (filename, position, rotation, vertex count)
- [ ] Add delete button per obstacle
- [ ] Wire obstacle upload to backend (`POST /api/upload/obstacle`)
- [ ] Display obstacle bounds from backend response

**Deliverable:** Error feedback visible in UI, obstacle management working

---

#### Backend - Jason

**Week 3:**
- [ ] Complete Lark grammar for MoveL, MoveJ, MoveC instructions
- [ ] Add grammar rules for RobTarget, JointTarget definitions
- [ ] Add grammar rules for SpeedData, ZoneData
- [ ] Implement Lark Transformer to convert parse tree → AST dataclasses
- [ ] Define AST node dataclasses in `ast_nodes.py` (MoveL, MoveJ, MoveC, RobTarget, etc.)

**Week 4:**
- [ ] Integrate Lark parser into `/api/upload/rapid` endpoint
- [ ] Return parsed AST as JSON in response
- [ ] Catch Lark parsing errors and return friendly error messages
- [ ] Add line number tracking for errors
- [ ] Test parser with 10+ sample RAPID programs (valid and invalid)

**Deliverable:** RAPID files parse to AST, errors reported with line numbers

---

#### Backend - Noah

**Week 3:**
- [ ] Set up PyBullet headless environment (no GUI)
- [ ] Create URDF file for IRB 4600 (based on DH parameters)
- [ ] Load URDF into PyBullet and verify joint structure
- [ ] Implement FK solver (`kinematics/solver.py`) - joint angles → TCP pose
- [ ] Test FK with known joint configurations (compare to datasheet values)

**Week 4:**
- [ ] Implement IK solver using PyBullet's `calculateInverseKinematics`
- [ ] Add IK solver warm start (use previous joint config as seed)
- [ ] Create URDF files for IRB 2600 and IRB 6700
- [ ] Implement robot config loader (`kinematics/robot_config.py`) - load DH params from JSON
- [ ] Test IK with known TCP poses (verify joint solutions are valid)

**Deliverable:** FK/IK working in tests, URDFs created for all 3 robots

---

#### PM/QA - Noah

**Week 3:**
- [ ] Write parser test suite (20+ test cases: valid RAPID, syntax errors, edge cases)
- [ ] Test parser with real ABB RAPID programs (from RobotStudio examples)
- [ ] Write FK test cases (5+ known joint configs → expected TCP poses)
- [ ] Document test results in `tests/README.md`

**Week 4:**
- [ ] Write IK test cases (5+ known TCP poses → verify joint solutions)
- [ ] Test IK solver accuracy (compare PyBullet vs. ABB RobotStudio ground truth)
- [ ] Create obstacle test STLs (simple cube, cylinder, complex mesh)
- [ ] Test obstacle upload flow (upload → position → delete)
- [ ] Update roadmap with progress (mark Week 1-4 tasks complete)

**Deliverable:** Parser validated, FK/IK accuracy verified, test STLs available

---

### Week 5-6: Simulation Pipeline

**Goal:** End-to-end `/api/simulate`, trajectory generation, collision detection

**Key Milestone:** Upload RAPID → see trajectory waypoints returned

#### Frontend - Dylane

**Week 5:**
- [ ] Implement playback state management (current frame index, playing/paused)
- [ ] Wire `/api/simulate` response to playback state
- [ ] Implement animation loop (iterate through trajectory waypoints at 60 FPS)
- [ ] Update robot joint angles from trajectory `waypoint.joints`
- [ ] Add play/pause/stop buttons in SimulationControls panel

**Week 6:**
- [ ] Implement collision highlighting (red overlay on robot links when collision detected)
- [ ] Add collision indicator in UI (red warning icon when `waypoint.collisions.length > 0`)
- [ ] Test playback with 100+ waypoint trajectory
- [ ] Optimize rendering performance (ensure 60 FPS maintained)
- [ ] Add loading spinner during `/api/simulate` request

**Deliverable:** Trajectory animates smoothly, collisions highlighted

---

#### Frontend - Umaya

**Week 5:**
- [ ] Build SimulationControls component (play/pause/stop buttons)
- [ ] Add speed control slider (0.25x, 0.5x, 1x, 2x, 4x)
- [ ] Wire speed control to animation loop (adjust frame delay)
- [ ] Add "Simulate" button (triggers `/api/simulate` POST request)
- [ ] Display simulation status ("Simulating...", "Ready", "Error")

**Week 6:**
- [ ] Add step-through controls (prev frame, next frame buttons)
- [ ] Display current waypoint info (frame index, timestamp, joint angles)
- [ ] Build collision alert panel (list all collisions with details)
- [ ] Style collision alerts (expandable list, contact point coordinates)
- [ ] Test UI with simulations that have 10+ collisions

**Deliverable:** Playback controls working, simulation status visible

---

#### Backend - Jason

**Week 5:**
- [ ] Implement trajectory generator (`kinematics/trajectory.py`)
- [ ] Convert AST MoveL → linear interpolation of TCP waypoints
- [ ] Convert AST MoveJ → joint-space interpolation
- [ ] Convert AST MoveC → circular arc interpolation (via point)
- [ ] Respect SpeedData (interpolate based on v_tcp speed)
- [ ] Respect ZoneData (skip fine points when finep=false)

**Week 6:**
- [ ] Implement `POST /api/simulate` endpoint
- [ ] Load robot URDF into PyBullet for each request
- [ ] For each waypoint, run IK to get joint angles
- [ ] Call collision detector for each waypoint
- [ ] Return trajectory JSON with all waypoints + collision data
- [ ] Add error handling (IK failures, out-of-reach targets)

**Deliverable:** `/api/simulate` returns complete trajectory with collisions

---

#### Backend - Noah

**Week 5:**
- [ ] Implement collision detector (`collision/detector.py`)
- [ ] Load obstacle STL meshes into PyBullet collision world
- [ ] Implement mesh-to-mesh collision checking (PyBullet contact points)
- [ ] Return collision data (obstacle_id, link, penetration_depth, contact_point)
- [ ] Test collision detection with known overlapping meshes

**Week 6:**
- [ ] Implement mesh loader (`collision/mesh_loader.py`)
- [ ] Support STL and OBJ file formats
- [ ] Apply obstacle transforms (position, rotation) in PyBullet
- [ ] Optimize collision detection (broad phase culling with AABBs)
- [ ] Test collision accuracy (compare with known collision scenarios)

**Deliverable:** Collision detection working, mesh loading robust

---

#### PM/QA - Noah

**Week 5:**
- [ ] Write integration test: Upload RAPID → Parse → Simulate → Trajectory
- [ ] Test end-to-end workflow with 5+ sample RAPID programs
- [ ] Write performance benchmarks (measure `/api/simulate` response time)
- [ ] Target: <5s for 100-waypoint trajectory

**Week 6:**
- [ ] Write collision test cases (known overlaps → verify detection)
- [ ] Test with 0 obstacles, 1 obstacle, 5+ obstacles
- [ ] Test trajectory interpolation accuracy (verify waypoint spacing)
- [ ] Run regression tests (ensure Weeks 1-4 functionality still works)
- [ ] Document integration test results

**Deliverable:** Integration tests passing, performance benchmarks documented

---

### Week 7-8: MVP Polish

**Goal:** Timeline scrubber, speed controls, error states, bug fixes

**Key Milestone:** **Student MVP: upload RAPID → watch robot move with collision feedback**

#### Frontend - Dylane

**Week 7:**
- [ ] Build TimelineScrubber component (bottom bar with seek slider)
- [ ] Wire scrubber to playback state (seek to any frame)
- [ ] Display current timestamp and total duration
- [ ] Add keyframe markers on timeline (show each AST instruction)
- [ ] Test scrubber responsiveness (smooth seeking)

**Week 8:**
- [ ] Fix rendering bugs (gimbal lock, mesh flickering, camera jitter)
- [ ] Optimize Babylon.js scene (reduce draw calls, optimize materials)
- [ ] Add loading indicators (robot loading, simulation in progress)
- [ ] Test on low-end hardware (ensure 30+ FPS on integrated GPU)
- [ ] Final visual polish (lighting, grid styling, colors)

**Deliverable:** Timeline scrubber working, rendering polished and optimized

---

#### Frontend - Umaya

**Week 7:**
- [ ] Add error state UI (show friendly messages for IK failures, parse errors)
- [ ] Build responsive layout for smaller screens (collapse sidebar on mobile)
- [ ] Add tooltips and help text (explain controls, robot selector)
- [ ] Implement keyboard shortcuts (spacebar = play/pause, arrow keys = step)
- [ ] Test accessibility (keyboard navigation, screen reader support)

**Week 8:**
- [ ] Fix UI bugs (button states, form validation, edge cases)
- [ ] Add "Clear All" button (reset scene, clear obstacles, clear RAPID)
- [ ] Build demo mode (auto-load sample RAPID program on first visit)
- [ ] Final UI polish (consistent spacing, colors, typography)
- [ ] User acceptance testing with team members

**Deliverable:** UI responsive, error states clear, demo mode working

---

#### Backend - Jason

**Week 7:**
- [ ] Implement IK caching (reuse solutions for similar poses)
- [ ] Batch process trajectory waypoints (optimize PyBullet queries)
- [ ] Handle edge cases (IK failures, out-of-reach targets, singularities)
- [ ] Add input validation (reject empty AST, invalid robot_id)
- [ ] Improve error messages (user-friendly, actionable)

**Week 8:**
- [ ] Fix backend bugs (parser crashes, IK solver failures)
- [ ] Add logging (track simulation requests, errors, performance)
- [ ] Test with 20+ real RAPID programs from RobotStudio
- [ ] Optimize trajectory interpolation (reduce waypoint count without losing accuracy)
- [ ] Final code cleanup (remove debug prints, refactor complex functions)

**Deliverable:** Backend stable, optimized, handles edge cases gracefully

---

#### Backend - Noah

**Week 7:**
- [ ] Harden error responses (consistent error format, helpful messages)
- [ ] Add input validation for obstacle uploads (check STL format, vertex limits)
- [ ] Test collision detection edge cases (zero collisions, 100+ collisions)
- [ ] Optimize mesh loading (cache obstacle meshes, reduce memory usage)
- [ ] Add request timeout handling (kill long-running simulations after 30s)

**Week 8:**
- [ ] Fix backend bugs (collision false positives, mesh loading failures)
- [ ] Test multi-obstacle scenarios (10+ obstacles in scene)
- [ ] Write deployment documentation (`docs/guides/deployment.md`)
- [ ] Test Docker Compose setup (verify both services start correctly)
- [ ] Final code review (check for security issues, code quality)

**Deliverable:** Backend robust, deployment ready, bug-free

---

#### PM/QA - Noah

**Week 7:**
- [ ] Full regression testing (test all features from Weeks 1-6)
- [ ] Write UAT test plan (user scenarios, acceptance criteria)
- [ ] Test with real ABB RAPID programs (10+ programs from RobotStudio)
- [ ] Document known issues and bugs (create GitHub issues)
- [ ] Schedule MVP demo (invite stakeholders: Prof. Omar, ARIS team)

**Week 8:**
- [ ] Run MVP sign-off checklist (verify all FR-1 through FR-7 requirements met)
- [ ] Test on multiple browsers (Chrome, Firefox, Safari, Edge)
- [ ] Test on multiple OS (Windows, macOS, Linux)
- [ ] Create user guide (`docs/guides/user-guide.md`)
- [ ] Prepare MVP demo presentation (slides, talking points)
- [ ] **MVP SIGN-OFF** - Document completion of Week 8 milestone

**Deliverable:** MVP validated, user guide written, demo prepared

---

### Week 9-10: Control Flow + Multi-Robot

**Goal:** RAPID with control flow executes correctly, all 3 robots supported

**Key Milestone:** IF/ELSE/FOR/WHILE working, robot selector switches between 3 models

#### Frontend - Dylane + Umaya

**Week 9:**
- [ ] Update robot selector to load all 3 GLB models dynamically
- [ ] Test robot switching (IRB 4600 → IRB 2600 → IRB 6700)
- [ ] Add robot info panel (show specs: reach, payload, DOF)
- [ ] Improve RAPID editor (add syntax highlighting with Monaco Editor)

**Week 10:**
- [ ] Add control flow visualization (highlight current instruction during execution)
- [ ] Build variable inspector panel (show RAPID variable values during simulation)
- [ ] Add loop iteration counter (show FOR loop index, WHILE loop count)
- [ ] Final UI improvements (better error messages, help tooltips)

**Deliverable:** All 3 robots working, improved editor, control flow visible

---

#### Backend - Jason

**Week 9:**
- [ ] Extend Lark grammar to include IF/ELSE statements
- [ ] Extend Lark grammar to include FOR loops
- [ ] Extend Lark grammar to include WHILE loops
- [ ] Extend Lark grammar to include procedure definitions and calls
- [ ] Update AST nodes for control flow (IfNode, ForNode, WhileNode, ProcedureNode)

**Week 10:**
- [ ] Implement AST interpreter (execute control flow instructions)
- [ ] Handle variable assignments and references
- [ ] Handle procedure calls (stack frames, return values)
- [ ] Test with RAPID programs using loops and conditionals
- [ ] Optimize interpreter performance

**Deliverable:** Control flow fully implemented, RAPID programs with loops execute correctly

---

#### Backend - Noah

**Week 9:**
- [ ] Add DH parameters and configs for IRB 2600
- [ ] Add DH parameters and configs for IRB 6700
- [ ] Test FK/IK for all 3 robots
- [ ] Verify URDF files work correctly for all 3 robots

**Week 10:**
- [ ] Implement control flow execution engine (integrate interpreter with trajectory generator)
- [ ] Test multi-robot simulations (same RAPID on different robots)
- [ ] Verify all 3 robots handle same RAPID program correctly
- [ ] Document multi-robot support in API spec

**Deliverable:** All 3 robots configured, control flow execution working

---

#### PM/QA - Noah

**Week 9:**
- [ ] Write control flow test suite (IF/ELSE, FOR, WHILE, procedures)
- [ ] Test with 10+ RAPID programs using control flow
- [ ] Create multi-robot test matrix (3 robots × 5 RAPID programs = 15 tests)

**Week 10:**
- [ ] Update all documentation with control flow examples
- [ ] Test all 3 robots with collision scenarios
- [ ] Write advanced user guide (control flow syntax, multi-robot usage)
- [ ] Final regression testing (all features working together)

**Deliverable:** Control flow validated, multi-robot tested, docs updated

---

### Week 11: Handoff

**Goal:** Project deliverable complete, ready for demo and handoff

**Key Milestone:** Final demo, user guide, deployment docs

#### Frontend - Dylane + Umaya

- [ ] Final UI polish (fix any remaining visual bugs)
- [ ] Build demo mode (guided walkthrough for new users)
- [ ] Add "About" page (project info, team credits, license)
- [ ] Record demo video (3-5 minutes showing all features)

**Deliverable:** UI finalized, demo video recorded

---

#### Backend - Jason

- [ ] Auto-generate API docs (use FastAPI's built-in OpenAPI schema)
- [ ] Write deployment configuration (Dockerfile, docker-compose production)
- [ ] Add production CORS settings
- [ ] Final code cleanup and documentation

**Deliverable:** API docs auto-generated, deployment ready

---

#### Backend - Noah

- [ ] Write architecture documentation (system design, component diagrams)
- [ ] Write deployment scripts (setup.sh for production)
- [ ] Test deployment on cloud VM (AWS, DigitalOcean, or Heroku)
- [ ] Document production environment setup

**Deliverable:** Architecture docs complete, deployment tested

---

#### PM/QA - Noah

- [ ] Write user guide (step-by-step tutorials, screenshots)
- [ ] Write developer guide (how to extend, add new robots, modify parser)
- [ ] Final test pass (regression, smoke tests, exploratory testing)
- [ ] Prepare final demo presentation (for Prof. Omar and ARIS team)
- [ ] Create handoff package (docs, code, videos, test results)

**Deliverable:** All documentation complete, final demo delivered

---

## Success Criteria

### MVP (Week 8) - Must Have:

- ✅ Upload RAPID program with MoveL/MoveJ/MoveC instructions
- ✅ Select IRB 4600 robot (one robot functional)
- ✅ Click "Simulate" → receive trajectory waypoints
- ✅ Watch robot animate through trajectory in 3D
- ✅ Upload obstacle STL → position with gizmo
- ✅ See collision warnings when robot hits obstacle
- ✅ Timeline scrubber to seek through trajectory
- ✅ Play/pause/stop controls

### Final (Week 11) - Should Have:

- ✅ All 3 robots supported (IRB 4600, 2600, 6700)
- ✅ RAPID control flow working (IF/ELSE, FOR, WHILE)
- ✅ Procedure calls functional
- ✅ Improved editor with syntax highlighting
- ✅ User guide and developer guide
- ✅ Deployment documentation

---

## Risk Management

| Risk | Mitigation |
|------|-----------|
| PyBullet IK inaccuracy | Validate against RobotStudio early (Week 4) |
| RAPID parser complexity | Phase grammar (movement-only MVP, control flow Phase 4) |
| Timeline overrun | MVP gate at Week 8, defer stretch goals if needed |
| Team member unavailable | Cross-train on critical components (Jason/Noah both know backend) |
| Performance issues | Profile early (Week 2 frontend, Week 5 backend), optimize as needed |

---

## Next Steps

1. **Noah:** Schedule Week 1 kickoff meeting with team
2. **All:** Review this timeline and ask questions
3. **Noah:** Create Week 1-2 tickets in GitHub Issues (detailed task breakdown)
4. **Dylane:** Start Babylon.js scene initialization
5. **Umaya:** Start building app layout
6. **Jason:** Start FastAPI router setup
7. **Noah:** Add GLB files to repo, set up test infrastructure

---

**Last Updated:** 2026-02-05
**Approved by:** Noah (PM/QA Lead)
**Next Review:** End of Week 2

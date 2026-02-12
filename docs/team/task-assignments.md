# Task Assignments - 11-Week MVP Development

**Project:** ABB Online Simulation Platform
**Version:** 2.0 (Revised 2026-02-11)
**Team Size:** 4 developers
**Timeline:** 11 weeks, MVP target Week 8

> **📍 [START HERE - Documentation Hub](../START_HERE.md)** - Main entry point for all project documentation
>
> **Detailed Sprint Plans (2-Week Cycles):**
> - **[Week 1-2 Sprint Plan](../roadmap/week-1-2-sprint-plan.md)** - Foundation (3D scene, robot loading, upload)
> - **[Week 3-4 Sprint Plan](../roadmap/week-3-4-sprint-plan.md)** - Parser & kinematics (RAPID parser, FK/IK, gizmo)
> - **[Week 5-6 Sprint Plan](../roadmap/week-5-6-sprint-plan.md)** - Simulation pipeline (trajectory, collision)
> - **[Week 7-8 Sprint Plan](../roadmap/week-7-8-sprint-plan.md)** - MVP launch ⭐ (timeline scrubber, UAT, sign-off)
> - **[Week 9-10 Sprint Plan](../roadmap/week-9-10-sprint-plan.md)** - Stretch goals (control flow, multi-robot)
> - **[Week 11 Finalization](../roadmap/week-11-finalization.md)** - Handoff (docs, deployment, presentation)
>
> **Architecture & Testing:**
> - [System Design](../architecture/system-design.md) - Architecture decisions
> - [API Specification](../architecture/api-specification.md) - 10 endpoints with error codes
> - [Testing Strategy](../testing-strategy.md) - Test pyramid, coverage targets, CI/CD

---

## Team Structure

| Person | Primary Role | Secondary Responsibilities | Workload |
|--------|-------------|---------------------------|----------|
| **Dylane** | Frontend - Babylon.js Specialist | 3D rendering, animations, visual effects | ~32 tasks over 8 weeks |
| **Umaya** | Frontend - React UI Specialist | Components, layouts, controls, styling | ~30 tasks over 8 weeks |
| **Jason** | Backend Lead | FastAPI, RAPID parser, trajectory generation | ~32 tasks over 8 weeks |
| **Noah** | Backend (IK/Collision) + PM + QA Lead | PyBullet, collision detection, testing, docs | ~40 tasks over 8 weeks ⚠️ |

**⚠️ Risk:** Noah has significant workload across backend development, project management, QA, and documentation. This is acknowledged and monitored.

---

## Responsibility Matrix

### Frontend (Dylane - Babylon.js)

**Core Responsibilities:**
- 3D scene initialization (camera, lighting, ground plane)
- Robot GLB loading and skeletal animation
- Obstacle STL/OBJ rendering
- Transform gizmo (position, rotation controls)
- Trajectory animation and playback engine
- Collision highlighting (red material on collision)
- Timeline scrubber UI integration with 3D scene
- Rendering optimization (60 FPS target)

**Key Deliverables:**
- Week 1-2: 3D scene with camera controls, robot GLB loading
- Week 3-4: Obstacle rendering, transform gizmo
- Week 5-6: Trajectory animation, playback controls
- Week 7-8: Timeline scrubber, collision visualization

---

### Frontend (Umaya - React UI)

**Core Responsibilities:**
- React component hierarchy and layout
- File upload UI (drag-drop, validation)
- Robot selector dropdown
- RAPID editor (textarea → Monaco upgrade in Phase 4)
- StatusPanel (errors, warnings, collision alerts)
- Obstacle list sidebar
- SimulationControls (simulate button, progress indicator)
- PlaybackControls (play/pause/stop/speed)
- TimelineScrubber component
- Responsive design and accessibility

**Key Deliverables:**
- Week 1-2: Upload UI, robot selector, layout shell
- Week 3-4: StatusPanel, obstacle list, error display
- Week 5-6: SimulationControls, loading indicators
- Week 7-8: PlaybackControls, TimelineScrubber, ARIA labels

---

### Backend (Jason - Lead)

**Core Responsibilities:**
- FastAPI router structure and middleware
- RAPID parser (Lark grammar → AST)
  - Grammar definition in `grammar.lark`
  - AST node dataclasses (MoveL, MoveJ, MoveC, RobTarget, JointTarget, SpeedData, ZoneData)
  - Transformer (parse tree → AST)
- Trajectory generator
  - MoveL → linear interpolation
  - MoveJ → joint-space interpolation
  - MoveC → circular arc interpolation
  - SpeedData and ZoneData handling
- `/api/simulate` endpoint orchestration
- IK caching (LRU, 1000 entries)
- Control flow interpreter (IF/ELSE, FOR, WHILE) - Phase 4
- API documentation (Swagger/OpenAPI)

**Key Deliverables:**
- Week 1-2: FastAPI structure, health/robots/model endpoints
- Week 3-4: Lark grammar complete, AST nodes, `/api/upload/rapid` parser
- Week 5-6: Trajectory generator, `/api/simulate` endpoint
- Week 7-8: IK caching, edge case handling, Swagger docs polish

---

### Backend (Noah - IK/Collision + PM/QA)

**Backend Responsibilities:**
- PyBullet headless setup
- URDF creation for all 3 robots (IRB 4600, 2600, 6700)
- DH parameter research and validation
- Forward kinematics (FK) solver
- Inverse kinematics (IK) solver (PyBullet wrapper)
- Collision detector (mesh-to-mesh)
- Obstacle mesh loading (STL/OBJ into PyBullet)
- GLB/URDF file management
- Upload endpoints (`/api/upload/rapid`, `/api/upload/obstacle`)
- Obstacle CRUD endpoints (`GET /api/obstacles`, `PUT /transform`, `DELETE`)
- Pydantic request/response schemas
- Input validation and error handling
- Security review (file upload validation)

**PM/QA Responsibilities:**
- Sprint planning (task breakdown, dependency tracking)
- Daily standup scheduling and facilitation
- Test infrastructure (pytest, vitest, CI pipelines)
- Parser test suite (20+ RAPID programs)
- FK/IK validation (against RobotStudio ground truth)
- Collision detection tests
- Integration testing (end-to-end workflows)
- Performance benchmarking (<5s for 100 waypoints)
- UAT coordination (10+ real RAPID programs)
- Regression testing (full suite before MVP)
- Sample RAPID programs creation
- Demo script and presentation slides
- All documentation (user guide, developer guide, architecture docs, deployment guide)

**Key Deliverables:**
- Week 1-2: PyBullet setup, pytest/vitest frameworks, upload endpoints
- Week 3-4: IRB 4600 URDF, FK solver, IK solver, validation tests
- Week 5-6: IRB 2600/6700 URDFs, collision detector, integration tests
- Week 7-8: UAT, regression suite, SOP, demo prep
- Week 11: Full documentation package, deployment guide, presentation

---

## Multi-Robot Architecture

**Important:** The kinematics and collision detection system is **robot-agnostic**. Once the controller is built, all 3 robots work via configuration files.

### How Multi-Robot Support Works

**Single IK/Collision Controller:**
- PyBullet solver works for any URDF
- Collision detector works with any mesh
- Trajectory generator is independent of robot model

**Robot-Specific Configuration Files:**
- `models/robots/irb4600/robot.urdf` - PyBullet kinematics model
- `models/robots/irb4600/visual.glb` - Babylon.js 3D model
- `models/robots/irb4600/config.json` - DH parameters, joint limits, metadata

**Same pattern for IRB 2600 and IRB 6700.**

**Development Timeline:**
- Week 3-4: Build IK/collision controller + IRB 4600 config files
- Week 4: Add IRB 2600 and IRB 6700 config files (URDF, GLB, config.json)
- Week 8 MVP: All 3 robots fully functional via selector dropdown

**This means:** Noah is not "rebuilding the controller" for each robot. He's creating 3 sets of configuration files that the single controller consumes.

---

## Phase Breakdown

### Phase 1: Visualization Foundation (Weeks 1-3)

**Goal:** 3D scene working, robot loads and animates, obstacles uploadable, transform gizmo functional

**Dylane:**
- Babylon.js scene (camera, lighting, ground)
- Load IRB 4600 GLB
- Skeleton-based joint animation
- 6 joint sliders (testing FK)
- Obstacle STL loading
- Transform gizmo (PositionGizmo, RotationGizmo)

**Umaya:**
- App layout (Header, MainLayout, SidePanel)
- Robot selector dropdown
- File upload components (drag-drop)
- RAPID editor (textarea)
- StatusPanel (errors/warnings)
- Obstacle list sidebar

**Jason:**
- FastAPI router structure
- `GET /api/robots` endpoint
- `GET /api/robots/{id}/model` (serve GLB)
- CORS middleware
- Begin Lark research

**Noah (Backend):**
- Add IRB 4600 GLB to repo
- `POST /api/upload/rapid` endpoint
- `POST /api/upload/obstacle` endpoint
- Pydantic schemas (UploadResponse, etc.)
- File validation (size, extension, magic bytes)

**Noah (QA):**
- Vitest setup
- Pytest setup
- CI pipelines (GitHub Actions)
- Sample RAPID programs
- Integration test skeleton

---

### Phase 2: Logic Engine & Kinematics (Weeks 4-6)

**Goal:** RAPID parser complete, FK/IK working, trajectory generation, `/api/simulate` endpoint functional

**Dylane:**
- Obstacle rendering in scene
- Transform gizmo wired to backend API
- AnimationController (play/pause/stop)
- Collision highlighting (red material)

**Umaya:**
- StatusPanel displays parse errors
- Obstacle metadata display
- PlaybackControls component
- SimulationControls component
- Speed slider
- Progress bar
- Collision alerts

**Jason:**
- Complete Lark grammar (MoveL/MoveJ/MoveC)
- AST node dataclasses
- Transformer (parse tree → AST)
- Wire parser to `/api/upload/rapid`
- Trajectory generator (linear/joint/circular interpolation)
- `/api/simulate` endpoint
- SpeedData and ZoneData handling

**Noah (Backend):**
- PyBullet headless setup
- URDF for IRB 4600
- Forward kinematics solver
- Inverse kinematics solver
- URDF for IRB 2600 and IRB 6700
- Collision detector (PyBullet mesh-to-mesh)
- Obstacle mesh loader
- Collision detail reporting

**Noah (QA):**
- 20+ parser test cases
- FK validation (known configs vs. datasheet)
- IK tests (reachable/unreachable)
- Collision tests (overlapping meshes)
- Integration tests (upload→parse→simulate→trajectory)
- Performance benchmarks

---

### Phase 3: Student MVP Launch (Weeks 7-8) ⭐

**Goal:** Timeline scrubber, playback controls, collision detection, UAT, **MVP sign-off**

**Dylane:**
- TimelineScrubber component
- Step-through (next/prev frame)
- Keyboard shortcuts
- Rendering optimization
- Final visual polish

**Umaya:**
- SpeedControl component
- LoadingIndicator
- ErrorMessage components
- Responsive layout
- ARIA labels and accessibility

**Jason:**
- IK caching (LRU, 1000 entries)
- Edge case handling
- Swagger docs improvement
- Performance tuning

**Noah (Backend):**
- Input validation hardening
- Timeout handling (2s IK, 5s collision)
- Security review (file upload)
- Error code implementation

**Noah (QA):**
- Full regression testing
- UAT with 10+ real RAPID programs
- Multi-browser testing (Chrome, Firefox, Edge)
- MVP acceptance checklist (FR-1 through FR-7)
- Demo rehearsal (Day 4)
- MVP sign-off (Day 5)

---

### Phase 4: Expansion (Weeks 9-10) - Stretch Goals

**Goal:** IF/ELSE/FOR/WHILE control flow, all 3 robots fully validated, advanced features

**Dylane:**
- Multi-robot selector with thumbnails
- Robot info panel
- Smooth robot switching

**Umaya:**
- ControlFlowVisualizer (optional)
- VariableInspector (optional)
- Monaco Editor integration (syntax highlighting upgrade)

**Jason:**
- Extend Lark grammar (IF/ELSE, FOR, WHILE, PROC/ENDPROC)
- Boolean expressions
- AST interpreter
- Execution timeout (10K iterations)

**Noah (Backend):**
- Verify all 3 robot URDFs complete
- Robot config loader
- Multi-robot test matrix

**Noah (QA):**
- Control flow test suite
- Multi-robot testing (3 robots x 5 programs = 15 tests)

---

### Phase 5: Finalization (Week 11)

**Goal:** Documentation, deployment, demo, presentation, handoff

**Dylane:**
- Final UI polish
- Demo mode (pre-loaded data)
- Demo video (3-5 min)
- Code cleanup

**Umaya:**
- User guide with screenshots
- Step-by-step tutorials

**Jason:**
- API docs auto-generation (OpenAPI)
- Deployment config (Docker, env vars)
- Cloud VM test

**Noah (Backend):**
- Architecture docs
- Deployment scripts
- Developer guide

**Noah (QA):**
- Final test pass
- Presentation slides (15-20 slides)
- Handoff package

---

## MVP Success Criteria (Week 8)

**Functional Requirements (All Must Pass):**
- ✅ **FR-1:** Triple-model support (IRB 4600, 2600, 6700 selectable)
- ✅ **FR-2:** Environment upload (STL/OBJ obstacles)
- ✅ **FR-3:** Active transform gizmo (position/rotate obstacles)
- ✅ **FR-4:** RAPID interpretation (MoveL, MoveJ, MoveC)
- ✅ **FR-5:** Batch processing (server-side trajectory)
- ✅ **FR-6:** Playback controls (timeline scrubber, play/pause/seek/speed)
- ✅ **FR-7:** Basic collision detection (visual warning)

**Technical Requirements:**
- ✅ System runs without crashes for 30+ minute sessions
- ✅ `/api/simulate` completes in <5 seconds for typical programs
- ✅ Frontend animates at 60 FPS
- ✅ All automated tests pass (backend coverage ≥80%, frontend ≥60%)
- ✅ Multi-browser compatible (Chrome, Firefox, Edge)

**Documentation Requirements:**
- ✅ Complete user SOP
- ✅ Demo script ready
- ✅ API documentation (Swagger UI)

**Sign-Off:**
- ✅ Demo rehearsal completed (Week 8, Day 4)
- ✅ Stakeholder sign-off (Week 8, Day 5)

---

## Communication & Meetings

**Daily Standup:**
- **Time:** 9:00 AM (15 minutes)
- **Format:** What I did yesterday, what I'm doing today, blockers
- **Channels:** Slack `#abb-sim-dev`

**Sprint Reviews:**
- **When:** End of each 2-week sprint (30 min)
- **Exception:** Week 8 MVP sign-off (1 hour)

**Slack Channels:**
- `#abb-sim-dev` - General development
- `#abb-sim-frontend` - Dylane + Umaya coordination
- `#abb-sim-backend` - Jason + Noah coordination
- `#abb-sim-qa` - Testing, bugs, UAT

---

## Dependencies & Integration Points

**No Hard Blockers for Weeks 1-5:**
- Frontend can mock all API responses
- Backend can stub endpoints
- Both teams test independently

**Critical Integration Points:**

**Week 3 Day 1:**
- Jason creates `grammar.lark` skeleton → blocks Week 4 AST implementation

**Week 3 Day 2-3:**
- Noah sets up PyBullet + IRB 4600 URDF → blocks Week 4 IK solver

**Week 5 Day 1:**
- Jason defines SimulateRequest/Response schemas → blocks Dylane animation (Day 3-4)

**Week 6:**
- `/api/simulate` format finalized → used by both frontend and backend

**Week 7:**
- Trajectory animation must work with real `/api/simulate` output

**Week 8:**
- Collision detection integration (backend data → frontend rendering)

---

## Risk Management

| Risk | Owner | Mitigation |
|------|-------|-----------|
| Noah workload overload | Noah + PM | Weekly workload review, delegate docs to team where possible |
| PyBullet IK inaccurate | Noah | Validate against RobotStudio ground truth (Week 4) |
| RAPID parser incomplete | Jason | Phased grammar (movement-only MVP, control flow Phase 4) |
| Babylon.js performance | Dylane | Profile early (Week 2), simplify scene if needed |
| Timeline overrun | Noah (PM) | MVP gate at Week 8, defer stretch goals |
| URDF creation delays | Noah | Focus IRB 4600 first, 2600/6700 can be Week 9 if needed (not ideal) |

---

## Testing Checkpoints

**Weekly QA Schedule (Noah):**
- **Monday:** Review previous week's deliverables
- **Wednesday:** Mid-week integration testing
- **Friday:** Weekly demo and regression tests

**Critical Milestones:**
- **Week 3:** End of Phase 1 - Full visualization stack test
- **Week 6:** End of Phase 2 - RAPID → trajectory pipeline test
- **Week 8:** MVP LAUNCH - Comprehensive acceptance testing

---

**Last Updated:** 2026-02-11
**Owner:** Noah (PM Lead)
**Next Review:** End of Week 2 (Sprint 1 retro)

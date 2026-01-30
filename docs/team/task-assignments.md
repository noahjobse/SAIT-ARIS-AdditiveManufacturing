# Task Assignments - 11-Week MVP Development

**Team:**
- **Dylane** - Frontend (Babylon.js, 3D visualization)
- **Umaya** - Frontend (React UI, components)
- **Jason** - Backend Lead (FastAPI, kinematics, RAPID parser)
- **Noah** - Testing/QA & Documentation

**Approach:** Frontend and backend teams work in **parallel** throughout Weeks 1-6 using mock data. Both teams use mock API responses to develop independently, then **integrate at critical points** (Weeks 6-8) to create the final full-stack product.

**Student View Features (Weeks 1-8):**
1. **File Upload** (Week 1) - Students can upload RAPID programs as files
2. **Code Editor** (Week 4) - Students can type/paste RAPID code directly in the app
3. **Visualization** (Weeks 1-3, 5-7) - 3D robot animation and obstacle positioning
4. **Execution** (Week 6) - Submit code for execution and playback
5. **Timeline Controls** (Week 7) - Play, pause, seek through trajectory
6. **Collision Detection** (Week 8) - Visual feedback when robot hits obstacles

---

## Phase 1: Visualization Foundation (Weeks 1-3)

### Week 1: TypeScript Setup & 3D Scene Foundation

**Dylane (Frontend - Babylon.js)**
- [ ] Initialize Babylon.js 3D scene with camera controls
- [ ] Set up lighting system (hemispheric + directional lights)
- [ ] Create basic 3D environment (ground plane, grid)
- [ ] Test scene rendering and camera movement
- **Deliverables:** Working 3D scene with camera controls

**Umaya (Frontend - React UI)**
- [ ] Set up React component hierarchy and layout
- [ ] Design and implement file upload UI (Tailwind)
- [ ] Create drag-and-drop file input
- [ ] Add file type validation (STL, OBJ, GLB)
- [ ] Mock file upload response for testing
- **Deliverables:** Upload form component, responsive layout, mock data handler
- **Note:** Can work independently with mock `/api/upload` response

**Jason (Backend)**
- [ ] Set up FastAPI project structure and dependencies
- [ ] Research STL/OBJ parsing libraries
- [ ] Implement `/api/upload` endpoint
- [ ] Add file validation logic (size, type)
- [ ] Return sample response for frontend integration
- **Deliverables:** Upload API endpoint, file validation, example response
- **Note:** Parallel with frontend; can integrate Week 2 if early sync preferred

**Noah (Testing/QA)**
- [ ] Set up pytest framework for backend testing
- [ ] Create Vitest/Jest config for frontend tests
- [ ] Write unit tests for file upload validation
- [ ] Document testing setup in `/docs/guides/testing.md`
- **Deliverables:** Test framework, initial test coverage
- **Note:** Test frontend with mocks and backend independently

---

### Week 2: Robot Rigging & Forward Kinematics

**Dylane (Frontend - Babylon.js)**
- [ ] Load and render 3D robot models (GLB format for all 3 robots)
- [ ] Bind skeletal rigging to Babylon.js bones
- [ ] Test model loading and animation setup
- [ ] Create UI to select between robot models
- **Deliverables:** All 3 robot models rendering in scene
- **Note:** Can work independently; uses mock FK data for slider testing

**Umaya (Frontend - React UI)**
- [ ] Create joint angle slider controls for testing FK
- [ ] Build UI panel to display current joint positions
- [ ] Add robot model selector dropdown
- [ ] Implement responsive layout for controls
- [ ] Mock FK response to test UI
- **Deliverables:** Joint control UI, responsive layout, mock FK integration
- **Note:** Can test with mock FK data while backend develops solver

**Jason (Backend)**
- [ ] Research and document DH parameters for IRB 4600, 2600, 6700
- [ ] Implement forward kinematics solver (NumPy)
- [ ] Create `/api/forward-kinematics` endpoint with sample response
- [ ] Write unit tests with known joint positions
- **Deliverables:** FK solver, validated API endpoint, example responses
- **Note:** Parallel with frontend; integration Week 3 if early sync preferred

**Noah (Testing/QA)**
- [ ] Validate FK solver output against RobotStudio
- [ ] Test with 5+ known joint positions per robot model
- [ ] Test frontend UI with mock FK data
- [ ] Document FK validation results
- **Deliverables:** FK validation report
- **Note:** Test backend independently; frontend with mocks

---

### Week 3: Transform Gizmo & Obstacle Positioning

**Dylane (Frontend - Babylon.js)**
- [ ] Implement 3D transform gizmo (move/rotate/scale handles)
- [ ] Render uploaded STL/OBJ obstacles in scene
- [ ] Add gizmo snap-to-grid option
- [ ] Test gizmo interaction with mock obstacle data
- **Deliverables:** Working transform gizmo, obstacle rendering
- **Note:** Can work independently with mock obstacle positions

**Umaya (Frontend - React UI)**
- [ ] Create obstacle list UI panel
- [ ] Add properties display (position, rotation, scale)
- [ ] Implement save/load obstacle configuration UI
- [ ] Add delete and reset buttons for obstacles
- [ ] Mock obstacle API responses
- **Deliverables:** Obstacle management UI, mock integration
- **Note:** Can test with mock data while backend builds API

**Jason (Backend)**
- [ ] Load STL/OBJ meshes and validate geometry
- [ ] Implement `/api/obstacles` endpoint (in-memory storage)
- [ ] Create coordinate transformation utilities
- [ ] Add mesh validation and error reporting
- [ ] Return sample obstacle responses
- **Deliverables:** Obstacle API, mesh loading, example responses
- **Note:** Parallel with frontend; integration Week 3-4 if sync preferred

**Noah (Testing/QA)**
- [ ] Test gizmo with various obstacle sizes/shapes using mock data
- [ ] Test frontend UI independently
- [ ] Test backend mesh validation independently
- [ ] Plan integration testing for Week 4
- **Deliverables:** Gizmo validation report, test plan
- **Note:** Test frontend with mocks and backend separately

---

## Phase 2: The Brain - Logic Engine & Kinematics (Weeks 4-6)

### Week 4: RAPID Parser Implementation & Code Editor

**Dylane (Frontend)**
- [ ] Create RAPID code editor UI component (syntax highlighting for RAPID)
- [ ] Implement code input form with submit button
- [ ] Add line numbers and code formatting
- [ ] Mock parser response with sample AST data
- [ ] Test editor with sample RAPID programs
- **Deliverables:** RAPID code editor component, mock response handler
- **Feature:** Students can type/paste RAPID code directly in student view
- **Note:** Can work independently with mock data

**Umaya (Frontend)**
- [ ] Build UI for parser feedback (errors, warnings)
- [ ] Create waypoint visualization toggle
- [ ] Add execution status indicator
- [ ] Wire up mock parser responses to UI
- [ ] Implement error message display for parser/execution failures
- [ ] Integrate code editor into main student view layout
- **Deliverables:** Parser feedback UI, integrated editor layout, mock integration
- **Feature:** Students see real-time feedback (syntax errors, execution status)
- **Note:** Can test with mock data while backend develops parser

**Jason (Backend)**
- [ ] Implement RAPID lexer (tokenization)
- [ ] Build RAPID parser (AST generation)
- [ ] Support: MoveJ, MoveL, IF, FOR, WHILE commands
- [ ] Create `/api/parse-rapid` endpoint with sample response
- [ ] Write unit tests for common RAPID patterns
- [ ] **Deliverables:** Working RAPID parser, validated API, example responses
- **Note:** Parallel with frontend; can integrate mid-week if sync preferred

**Noah (Testing/QA)**
- [ ] Create test suite of RAPID programs
- [ ] Validate parser AST output with real API
- [ ] Test error handling (syntax errors, invalid commands)
- [ ] Integration test: frontend mocks → backend parser validation
- **Deliverables:** RAPID parser test suite, validation report
- **Note:** Test backend independently; mock integration with frontend

---

### Week 5: PyBullet Integration & Inverse Kinematics

**Dylane (Frontend)**
- [ ] Create trajectory visualization (waypoint markers in scene)
- [ ] Add animation preview for calculated trajectory
- [ ] Implement speed/playback slider
- **Deliverables:** Trajectory visualization UI

**Umaya (Frontend)**
- [ ] Build reachability status display (reachable/unreachable)
- [ ] Create error message display for IK failures
- [ ] Add trajectory smoothness indicator
- **Deliverables:** IK feedback UI

**Jason (Backend)**
- [ ] Convert ABB robot specs to PyBullet URDF format (or create custom)
- [ ] Implement IK solver with joint limit constraints
- [ ] Add reachability validation
- [ ] Create `/api/inverse-kinematics` endpoint
- [ ] Implement linear interpolation for MoveL commands
- [ ] Write trajectory quality tests
- **Deliverables:** IK solver, validated API, trajectory generation

**Noah (Testing/QA)**
- [ ] Validate IK solutions against RobotStudio
- [ ] Test reachability detection accuracy
- [ ] Integration test: waypoints → IK calculation → smooth trajectory
- [ ] Test joint limit constraints
- **Deliverables:** IK validation report, constraint test results
- **Blocked By:** Jason's IK solver

---

### Week 6: End-to-End Batch Execution Pipeline

**Dylane (Frontend)**
- [ ] Test full trajectory animation pipeline
- [ ] Optimize rendering for long trajectories
- [ ] Add performance profiling UI
- **Deliverables:** Optimized rendering, performance data

**Umaya (Frontend)**
- [ ] Create loading/progress indicator for batch processing
- [ ] Add execution status display
- [ ] Implement error handling UI
- **Deliverables:** Batch execution status UI

**Jason (Backend)**
- [ ] Create `/api/execute` endpoint (RAPID code + obstacles → trajectory)
- [ ] Define trajectory JSON schema (timestamp, joint angles, TCP position)
- [ ] Implement collision detection integration
- [ ] Add error handling and validation
- [ ] Optimize execution performance
- **Deliverables:** Complete `/api/execute` endpoint, trajectory schema
- **Testing:** Performance benchmark (<5s for typical programs)

**Noah (Testing/QA)**
- [ ] End-to-end integration test: RAPID code → execute → animation
- [ ] Test with 10+ RAPID programs and obstacle configs
- [ ] Performance testing (execution time, rendering)
- [ ] Error handling validation (bad code, unreachable targets)
- **Deliverables:** End-to-end test report, performance metrics
- **Blocked By:** Jason's `/api/execute` endpoint

---

## Phase 3: Student MVP Launch (Weeks 7-8)

### Week 7: Playback Engine & Timeline Controls

**Dylane (Frontend - Babylon.js)**
- [ ] Implement smooth animation loop (interpolate between trajectory points)
- [ ] Build animation timeline state management
- [ ] Test animation smoothness at various speeds
- [ ] Optimize rendering performance during playback
- **Deliverables:** Smooth trajectory animation, optimized rendering

**Umaya (Frontend - React UI)**
- [ ] Create timeline scrubber UI component
- [ ] Implement play/pause/stop buttons
- [ ] Add speed adjustment slider (0.5x - 2x)
- [ ] Build real-time display of current joint angles and TCP position
- [ ] Add animation progress indicator
- **Deliverables:** Playback controls, timeline UI, status displays

**Jason (Backend)**
- [ ] Optimize `/api/execute` endpoint performance
- [ ] Add trajectory caching (optional)
- [ ] Ensure robust error handling for all edge cases
- **Deliverables:** Optimized execution, robust error handling

**Noah (Testing/QA)**
- [ ] Test animation smoothness at all speeds (0.5x - 2x)
- [ ] Verify responsive control latency (<100ms)
- [ ] Test timeline scrubber seeking
- [ ] Validate joint position displays accuracy
- [ ] Integration test: full playback workflow
- **Deliverables:** Playback validation report, performance metrics

---

### Week 8: Collision Detection & MVP Polish ⭐ **MVP DEADLINE**

**Dylane (Frontend - Babylon.js)**
- [ ] Integrate collision detection into playback animation
- [ ] Implement collision visual feedback (robot turns red on collision)
- [ ] Add collision highlighting and UI feedback
- [ ] Final performance optimization
- **Deliverables:** Working collision detection, visual feedback

**Umaya (Frontend - React UI)**
- [ ] Create collision event log display
- [ ] Implement error message system for edge cases
- [ ] Add accessibility features (keyboard navigation)
- [ ] Finalize responsive design (mobile, tablet, desktop)
- [ ] Polish all UI components and transitions
- **Deliverables:** Collision UI, accessible interface, polished design

**Jason (Backend)**
- [ ] Integrate PyBullet collision detection into trajectory computation
- [ ] Implement collision event logging (time, location, robot link)
- [ ] Add error handling for edge cases (unreachable targets, etc.)
- [ ] Final API validation and robustness
- **Deliverables:** Collision detection API, robust error handling

**Noah (Testing/QA)**
- [ ] Comprehensive regression testing (all features)
- [ ] Test with 10+ RAPID programs with various obstacles
- [ ] Validate collision detection accuracy
- [ ] Edge case testing (unreachable targets, joint limits, etc.)
- [ ] Create comprehensive SOP/user guide
- [ ] Complete accessibility audit
- [ ] Demo preparation and validation
- **Deliverables:** Regression test report, complete SOP, demo script

---

## Phase 4: Expansion & Polish (Weeks 9-10) - *As Time Permits*

### Week 9: Engineer View Features

**Dylane (Frontend)**
- [ ] Add advanced overlay displays (TCP velocity, acceleration curves)
- [ ] Implement line-linked collision logging visualization
- [ ] Create engineer-specific diagnostic views
- **Deliverables:** Advanced visualization features

**Umaya (Frontend)**
- [ ] Build Engineer View UI toggle
- [ ] Create detailed collision log interface
- [ ] Implement diagnostic data display
- **Deliverables:** Engineer View UI

**Jason (Backend)**
- [ ] Map collisions to RAPID source line numbers
- [ ] Create detailed collision analysis data (velocity, energy, etc.)
- [ ] Add Engineer View data endpoints
- **Deliverables:** Engineer View API endpoints

**Noah (Testing/QA)**
- [ ] Validate collision-to-line mapping
- [ ] Test Engineer View features
- **Deliverables:** Engineer View test report

---

### Week 10: Advanced Features & Optimization

**Dylane & Umaya (Frontend)**
- [ ] Performance optimization across all components
- [ ] Add multi-robot model support if not complete
- [ ] Optimize rendering for large trajectories
- **Deliverables:** Optimized performance

**Jason (Backend)**
- [ ] Trajectory caching and optimization
- [ ] Database persistence (optional)
- [ ] Performance profiling and tuning
- **Deliverables:** Optimized execution, optional persistence

**Noah (Testing/QA)**
- [ ] Performance benchmarking
- [ ] Load testing
- **Deliverables:** Performance report

---

### Week 11: Finalization & Deployment

**All Team Members**

**Documentation (Noah Lead):**
- [ ] Complete OpenAPI/Swagger documentation
- [ ] User getting-started guide and SOP
- [ ] Developer setup instructions
- [ ] System architecture documentation
- [ ] Test coverage report
- [ ] Final presentation slides

**Deployment (Noah + Jason):**
- [ ] Docker configuration for deployment
- [ ] CI/CD pipeline setup (GitHub Actions)
- [ ] Final integration testing
- [ ] Production deployment

**Demo Preparation (Noah + Dylane + Umaya):**
- [ ] Create demo script and walkthrough
- [ ] Record demo video
- [ ] Prepare presentation materials
- [ ] Final bug fixes

**Testing (Noah):**
- [ ] Comprehensive regression test suite
- [ ] User acceptance testing
- [ ] Performance benchmarks
- [ ] Browser compatibility testing

---

## Summary by Team Member

### Dylane (Frontend - Babylon.js Specialist)
**Responsibilities:** 3D scene, robot models, animations, transform gizmo, RAPID code editor, collision rendering

- **Weeks 1-3:** Scene setup, robot rigging, gizmo implementation
- **Weeks 4-6:** RAPID code editor component, trajectory visualization, animation interpolation
- **Weeks 7-8:** Playback engine, collision visuals
- **Weeks 9-11:** Advanced overlays, optimization (as time permits)
- **Total Tasks:** ~32 across 8 weeks
- **Key Feature:** Builds the RAPID code editor UI that lets students type code directly

---

### Umaya (Frontend - React UI Specialist)
**Responsibilities:** User interface, component library, controls, responsive design, RAPID editor integration

- **Weeks 1-3:** Upload UI, robot selector, control panels
- **Weeks 4-6:** Code editor integration, parser error feedback, trajectory controls
- **Weeks 7-8:** Timeline scrubber, playback controls, accessibility, polish
- **Weeks 9-11:** Engineer View, advanced features (as time permits)
- **Total Tasks:** ~30 across 8 weeks
- **Key Feature:** Integrates code editor into student view and provides real-time error feedback

---

### Jason (Backend Lead)
**Responsibilities:** FastAPI, kinematics (FK/IK), RAPID parser, collision detection, pipeline orchestration

- **Weeks 1-3:** File upload API, forward kinematics
- **Weeks 4-6:** RAPID parser, IK solver, batch execution pipeline
- **Weeks 7-8:** Collision detection, optimization, error handling
- **Weeks 9-11:** Engineer View features, optimization (as time permits)
- **Total Tasks:** ~32 across 8 weeks
- **Support:** Noah assists with testing and validation

---

### Noah (Testing/QA & Documentation Lead)
**Responsibilities:** Test framework setup, integration testing, validation, SOP documentation, demo prep

- **Weeks 1-3:** Test framework, unit tests, integration tests
- **Weeks 4-6:** RAPID parser validation, kinematics validation
- **Weeks 7-8:** Full regression testing, SOP writing, demo preparation
- **Weeks 9-11:** Documentation, deployment, final testing
- **Total Tasks:** ~25 across 8 weeks

---

## Critical Dependencies & Parallel Workflow

### Frontend & Backend Work in Parallel

**Weeks 1-6:** Frontend and backend teams work independently with mock data/UI
- **Frontend:** Can build components and UI without waiting for backend APIs
- **Backend:** Can develop APIs without waiting for UI implementation

### Integration Points (Must Sync)

1. **Week 1:** No blockers - both teams start independently
   - Frontend: Build 3D scene, UI components with mock data
   - Backend: Build APIs with basic implementation

2. **Week 6-7 Integration:** Critical sync point
   - Frontend must consume `/api/execute` trajectory JSON format
   - Backend must finalize trajectory JSON schema
   - Joint implementation of playback + animation

3. **Week 8 Integration:** Final sync
   - Collision detection integration (backend collision data → frontend rendering)
   - Error handling alignment across stack
   - Full end-to-end testing

### Detailed Dependency Chain

**No Hard Blockers for Initial Development:**
- Frontend can mock API responses while backend is building
- Backend can stub endpoints while frontend is building UI
- Both teams test independently, then integrate at checkpoints

**Optional Early Integration (if preferred):**
- Week 2: Frontend can connect to Jason's `/api/upload` for real testing
- Week 4: Frontend can call Jason's `/api/parse-rapid` for real parser feedback
- Week 5: Frontend can test IK solver output with real API

**Hard Dependencies (Must be Complete):**
- Week 6: `/api/execute` endpoint format must be finalized (used by both teams)
- Week 7: Trajectory animation must work with real `/api/execute` output
- Week 8: Collision detection must integrate backend data with frontend rendering

---

## Testing Checkpoints

### Weekly QA Schedule (Noah)
- **Monday:** Review previous week's deliverables
- **Wednesday:** Mid-week integration testing
- **Friday:** Weekly demo and regression tests

### Critical Milestones
- **Week 3:** End of Phase 1 - Full visualization stack test
- **Week 6:** End of Phase 2 - RAPID → trajectory pipeline test
- **Week 8:** MVP LAUNCH - Comprehensive acceptance testing

---

## Success Criteria - MVP (Week 8)

✅ All 7 critical functional requirements working (FR-1 through FR-7)
✅ Student can upload RAPID code and see robot animate
✅ Collision detection provides visual feedback
✅ Timeline controls (play, pause, seek) are responsive
✅ UI is intuitive for non-programmers
✅ System runs without crashes for 30+ minute sessions
✅ Complete user SOP and demo-ready

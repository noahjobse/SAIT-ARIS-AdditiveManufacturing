# Task Assignments - 11-Week MVP Development

**Team:**
- **Dylane** - Frontend (Babylon.js, 3D visualization)
- **Umaya** - Frontend (React UI, components)
- **Jason** - Backend Lead (FastAPI, kinematics, RAPID parser)
- **Noah** - Testing/QA & Documentation

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
- **Deliverables:** Upload form component, responsive layout

**Jason (Backend)**
- [ ] Set up FastAPI project structure and dependencies
- [ ] Research STL/OBJ parsing libraries
- [ ] Implement `/api/upload` endpoint scaffolding
- [ ] Add file validation logic (size, type)
- **Deliverables:** Upload API endpoint, file validation

**Noah (Testing/QA)**
- [ ] Set up pytest framework for backend testing
- [ ] Create Vitest/Jest config for frontend tests
- [ ] Write unit tests for file upload validation
- [ ] Document testing setup in `/docs/guides/testing.md`
- **Deliverables:** Test framework, initial test coverage
- **Blocked By:** Jason's `/api/upload` endpoint

---

### Week 2: Robot Rigging & Forward Kinematics

**Dylane (Frontend - Babylon.js)**
- [ ] Load and render 3D robot models (GLB format for all 3 robots)
- [ ] Bind skeletal rigging to Babylon.js bones
- [ ] Test model loading and animation setup
- [ ] Create UI to select between robot models
- **Deliverables:** All 3 robot models rendering in scene

**Umaya (Frontend - React UI)**
- [ ] Create joint angle slider controls for testing FK
- [ ] Build UI panel to display current joint positions
- [ ] Add robot model selector dropdown
- [ ] Implement responsive layout for controls
- **Deliverables:** Joint control UI, responsive layout

**Jason (Backend)**
- [ ] Research and document DH parameters for IRB 4600, 2600, 6700
- [ ] Implement forward kinematics solver (NumPy)
- [ ] Create `/api/forward-kinematics` endpoint
- [ ] Write unit tests with known joint positions
- **Deliverables:** FK solver, validated API endpoint

**Noah (Testing/QA)**
- [ ] Validate FK solver output against RobotStudio
- [ ] Test with 5+ known joint positions per robot model
- [ ] Integration test: joint sliders → FK calculation → visual feedback
- [ ] Document FK validation results
- **Deliverables:** FK validation report
- **Blocked By:** Jason's FK solver

---

### Week 3: Transform Gizmo & Obstacle Positioning

**Dylane (Frontend - Babylon.js)**
- [ ] Implement 3D transform gizmo (move/rotate/scale handles)
- [ ] Render uploaded STL/OBJ obstacles in scene
- [ ] Add gizmo snap-to-grid option
- [ ] Test gizmo interaction and obstacle positioning
- **Deliverables:** Working transform gizmo, obstacle rendering

**Umaya (Frontend - React UI)**
- [ ] Create obstacle list UI panel
- [ ] Add properties display (position, rotation, scale)
- [ ] Implement save/load obstacle configuration UI
- [ ] Add delete and reset buttons for obstacles
- **Deliverables:** Obstacle management UI

**Jason (Backend)**
- [ ] Load STL/OBJ meshes and validate geometry
- [ ] Implement `/api/obstacles` endpoint (in-memory storage)
- [ ] Create coordinate transformation utilities
- [ ] Add mesh validation and error reporting
- **Deliverables:** Obstacle API, mesh loading

**Noah (Testing/QA)**
- [ ] Test gizmo with various obstacle sizes/shapes
- [ ] Validate coordinate transformations
- [ ] Integration test: upload STL → position gizmo → save config
- [ ] Test edge cases (overlapping obstacles, out of bounds)
- **Deliverables:** Gizmo validation report, test cases
- **Blocked By:** Dylane's gizmo, Jason's obstacle API

---

## Phase 2: The Brain - Logic Engine & Kinematics (Weeks 4-6)

### Week 4: RAPID Parser Implementation

**Dylane (Frontend)**
- [ ] Create code editor UI component (syntax highlighting for RAPID)
- [ ] Add error message display area
- [ ] Implement code input form with submit button
- **Deliverables:** RAPID code editor UI

**Umaya (Frontend)**
- [ ] Build UI for parser feedback (errors, warnings)
- [ ] Create waypoint visualization toggle
- [ ] Add execution status indicator
- **Deliverables:** Parser feedback UI components

**Jason (Backend)**
- [ ] Implement RAPID lexer (tokenization)
- [ ] Build RAPID parser (AST generation)
- [ ] Support: MoveJ, MoveL, IF, FOR, WHILE commands
- [ ] Create `/api/parse-rapid` endpoint
- [ ] Write unit tests for common RAPID patterns
- **Deliverables:** Working RAPID parser, validated API
- **Testing:** Test with 5+ real RAPID programs

**Noah (Testing/QA)**
- [ ] Create test suite of RAPID programs
- [ ] Validate parser AST output
- [ ] Test error handling (syntax errors, invalid commands)
- [ ] Integration test: upload RAPID → parse → display errors
- **Deliverables:** RAPID parser test suite, validation report
- **Blocked By:** Jason's parser implementation

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
**Responsibilities:** 3D scene, robot models, animations, transform gizmo, collision rendering

- **Weeks 1-3:** Scene setup, robot rigging, gizmo implementation
- **Weeks 4-6:** Trajectory visualization, animation interpolation
- **Weeks 7-8:** Playback engine, collision visuals
- **Weeks 9-11:** Advanced overlays, optimization (as time permits)
- **Total Tasks:** ~30 across 8 weeks

---

### Umaya (Frontend - React UI Specialist)
**Responsibilities:** User interface, component library, controls, responsive design

- **Weeks 1-3:** Upload UI, robot selector, control panels
- **Weeks 4-6:** Code editor, parser feedback, trajectory controls
- **Weeks 7-8:** Timeline scrubber, playback controls, accessibility, polish
- **Weeks 9-11:** Engineer View, advanced features (as time permits)
- **Total Tasks:** ~28 across 8 weeks

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

## Critical Dependencies

1. **Week 1:** No blockers - can start all in parallel
2. **Week 2:** Blocked by Jason's `/api/upload` (needed for model testing)
3. **Week 3:** Blocked by Jason's obstacle API
4. **Week 4:** Blocked by prior phases (Jason's parser is independent)
5. **Week 5:** Blocked by Jason's FK solver from Week 2
6. **Week 6:** Blocked by Jason's parser and IK solver
7. **Week 7:** Blocked by `/api/execute` endpoint from Week 6
8. **Week 8:** All features must be complete for MVP

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

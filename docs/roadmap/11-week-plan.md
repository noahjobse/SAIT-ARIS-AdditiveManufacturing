# 11-Week Development Roadmap - Student View MVP Strategy

## Overview

Detailed week-by-week plan for building the ABB Online Simulation Platform with focus on **Student View MVP by Week 8**.

**Total Duration:** 11 weeks
**Strategy:** Staged commitment to MVP, with Phase 2 extensions as time permits
**Target:** Polished, working Student View by end of Week 8

**Documentation Strategy:** API docs, architecture docs, and user SOP are drafted **continuously** throughout development (not deferred to Week 11). Week 11 is for finalization and polish only.

See [docs/PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) for complete specification.

---

## Phase 1: Visualization Foundation (Weeks 1-3)

### Week 1: TypeScript Setup & 3D Scene Foundation

**Goals:**
- Finalize TypeScript/Vite frontend setup
- Initialize Babylon.js 3D scene
- Begin STL uploader implementation

**Deliverables:**
- [x] Repository structure finalized
- [x] TypeScript + Babylon.js + React configured
- [ ] Babylon.js scene with camera/lighting
- [ ] File upload API endpoint (backend)
- [ ] React upload UI component

**Backend Focus:**
- FastAPI project setup
- STL/OBJ file parsing library selection
- `/api/upload` endpoint scaffolding

**Frontend Focus:**
- Babylon.js scene initialization
- React component hierarchy
- File upload UI in Tailwind

---

### Week 2: Robot Rigging & Forward Kinematics

**Goals:**
- Implement forward kinematics for IRB 4600
- Load and render rigged 3D robot model
- Validate FK with visual feedback

**Deliverables:**
- [ ] DH parameters researched for IRB 4600, 2600, 6700 (all 3 robots)
- [ ] Forward kinematics solver (NumPy)
- [ ] GLB model loader in Babylon.js (IRB 4600 first)
- [ ] Joint angle visualization UI
- [ ] Robot metadata API (`GET /api/robots`)

**Note:** DH parameters researched for all 3 robots this week. Implementation: IRB 4600 URDF in Week 3, IRB 2600/6700 URDFs in Week 4. All 3 robots functional by Week 8 MVP.

**Backend Focus:**
- DH parameter research for all 3 robots
- Forward kinematics implementation
- Test suite with known joint positions

**Frontend Focus:**
- GLB model import (all 3 robots)
- Articulated skeleton binding
- Joint slider controls for testing FK

---

### Week 3: Transform Gizmo & Obstacle Positioning

**Goals:**
- Implement 3D transform gizmo for obstacles
- Enable obstacle positioning (X, Y, Z, rotation)
- Finalize STL upload and rendering

**Deliverables:**
- [ ] Babylon.js transform gizmo (move/rotate)
- [ ] Obstacle rendering in scene
- [ ] Save/load obstacle positions (JSON)
- [ ] Gizmo snap-to-grid option
- [ ] `/api/obstacles` endpoint for persistence

**Backend Focus:**
- STL mesh loading and validation
- Obstacle persistence (in-memory for MVP)
- Coordinate transformation utilities

**Frontend Focus:**
- Gizmo implementation (3D handles)
- Obstacle mesh rendering
- UI for obstacle list and properties

---

## Phase 2: The Brain - Logic Engine & Kinematics (Weeks 4-6)

### Week 4: RAPID Parser Implementation

**Goals:**
- Implement RAPID lexer and parser
- Support MoveJ, MoveL, and basic control flow
- Generate trajectory waypoints from parsed code

**Deliverables:**
- [ ] RAPID lexer (tokenization)
- [ ] RAPID parser (AST generation)
- [ ] Support: MoveJ, MoveL, MoveC (control flow deferred to Phase 4)
- [ ] Waypoint extraction from AST
- [ ] `/api/upload/rapid` endpoint (parses and returns AST)
- [ ] Unit tests for common RAPID patterns

**Note:** Control flow (IF/ELSE, FOR, WHILE) is deferred to Weeks 9-10 (Phase 4 stretch goals).

**Backend Focus:**
- Python lexer/parser (PLY or custom)
- AST node structure
- Error reporting and validation

**Testing:**
- Test with 5+ real RAPID programs
- Validate against expected AST

---

### Week 5: PyBullet Integration & Inverse Kinematics

**Goals:**
- Integrate PyBullet for accurate IK solving
- Generate smooth trajectories between waypoints
- Support all 3 robot models

**Deliverables:**
- [ ] PyBullet robot models (URDF) for all 3 ABB robots
- [ ] IK solver with joint limit constraints
- [ ] Reachability validation
- [ ] Linear interpolation for MoveL
- [ ] `/api/inverse-kinematics` endpoint
- [ ] Trajectory smoothness testing

**Backend Focus:**
- PyBullet URDF conversion or creation
- IK solver configuration
- Joint limit validation
- Trajectory quality metrics

---

### Week 6: End-to-End Batch Execution Pipeline

**Goals:**
- Connect RAPID parser → IK solver → trajectory output
- Implement batch processing workflow
- Return complete trajectory JSON

**Deliverables:**
- [ ] `/api/execute` endpoint (accepts RAPID + obstacles)
- [ ] Trajectory JSON format (timestamp, joint angles, TCP)
- [ ] Collision detection API (PyBullet)
- [ ] Basic error handling and validation
- [ ] Performance testing (execution time)

**Backend Focus:**
- Pipeline orchestration
- JSON schema definition
- Error messages for invalid code
- Batch job management

---

## Phase 3: Student MVP Launch (Weeks 7-8)

### Week 7: Playback Engine & Timeline Controls

**Goals:**
- Implement trajectory playback animation
- Add timeline scrubber for seeking
- Polish UI for student-friendly interaction

**Deliverables:**
- [ ] Babylon.js animation loop (smooth robot motion)
- [ ] Timeline UI component (Tailwind)
- [ ] Play/Pause/Seek controls
- [ ] Speed adjustment slider
- [ ] Real-time TCP/joint display
- [ ] Error message display for failed simulations

**Frontend Focus:**
- Animation interpolation between trajectory points
- Timeline scrubber with drag-to-seek
- State management for playback
- Responsive UI for all screen sizes

**Quality Checklist:**
- Animation smooth at all speeds
- No visual stuttering
- Responsive controls (<100ms latency)

---

### Week 8: Collision Detection & MVP Polish

**Goals:**
- Implement collision detection in playback
- Visual feedback for collisions
- Final MVP testing and bug fixes
- **MVP Status: COMPLETE & READY FOR DEMO**

**Deliverables:**
- [ ] PyBullet collision detection integration
- [ ] Collision visual feedback (robot turns red)
- [ ] Collision event logging (time, location)
- [ ] Error handling for edge cases
- [ ] UI refinement and accessibility
- [ ] Complete user guide (SOP)

**Frontend Focus:**
- Collision highlighting
- Error messages and recovery
- Accessibility (keyboard navigation)
- Mobile responsiveness (if time)

**Testing:**
- 10+ test RAPID programs
- Various obstacle configurations
- Edge cases (unreachable targets, etc.)

**🎯 MVP LAUNCH: Student View is demo-ready**

---

## Phase 4: Expansion & Polish (Weeks 9-10) - As Time Permits

### Week 9: Engineer View Features

**Goals:**
- Line-linked collision logging
- Advanced diagnostics for engineers
- Multi-robot model support

**Deliverables:**
- [ ] Control flow support (IF/ELSE statements)
- [ ] Boolean expressions (comparisons, AND/OR)
- [ ] AST interpreter for conditional branching
- [ ] Multi-robot validation (verify all 3 robots work correctly)
- [ ] Collision → RAPID line number mapping (optional)
- [ ] TCP velocity and acceleration curves (optional)

**Note:** All 3 robots (IRB 4600, 2600, 6700) should already be functional from Week 4. This week validates completeness and adds control flow support.

---

### Week 10: Advanced Features & Optimization

**Goals:**
- Performance optimization
- Additional RAPID features (if needed)
- Production hardening

**Deliverables:**
- [ ] Loop support (FOR and WHILE loops)
- [ ] Procedure calls (PROC/ENDPROC)
- [ ] Nested control flow (IF within FOR, etc.)
- [ ] Rendering performance optimization
- [ ] Trajectory caching (IK result caching)
- [ ] Execution timeout for loops (prevent infinite execution)

**Note:** Focus on FOR loops first (higher priority); WHILE loops are stretch within this stretch goal.

---

### Week 11: Finalization & Deployment

**Goals:**
- Complete documentation
- Final testing and bug fixes
- Production deployment
- Demo preparation

**Deliverables:**
- [ ] Complete API documentation (OpenAPI/Swagger)
- [ ] User SOP and tutorial video
- [ ] Test coverage report (unit + integration)
- [ ] Docker deployment configuration
- [ ] CI/CD pipeline setup (GitHub Actions)
- [ ] Final presentation slides
- [ ] Demo script and video

**Testing:**
- Comprehensive regression testing
- Performance benchmarks
- User acceptance testing with students

**Documentation (Finalization):**
- System architecture diagram (finalize from Week 6 draft)
- API endpoint reference (finalize auto-generated Swagger docs)
- User getting-started guide (finalize from Week 7-8 draft)
- Developer setup instructions (finalize)
- Presentation slides and demo video (create new)

**Note:** Documentation has been drafted continuously since Week 1. Week 11 focuses on finalization, not initial creation.

---

## Milestones Summary

| Week | Milestone | MVP Status |
|------|-----------|-----------|
| 1 | TypeScript/Babylon.js Setup + STL Uploader | Foundation |
| 2 | Robot Rigging + Forward Kinematics (3 models) | Critical |
| 3 | Transform Gizmo + Obstacle Positioning | Critical |
| **4** | **RAPID Parser** | **Critical** |
| **5** | **PyBullet IK + Smooth Trajectories** | **Critical** |
| **6** | **End-to-End Batch Pipeline** | **Critical** |
| **7** | **Playback Engine + Timeline Controls** | **MVP Phase** |
| **8** | **Collision Detection + MVP Polish** | **🎯 MVP LAUNCH** |
| 9 | Engineer View (Stretch Goal) | As Time Permits |
| 10 | Advanced Features (Stretch Goal) | As Time Permits |
| 11 | Documentation + Deployment | Final Delivery |

**Key Decision:** Hard cutoff at Week 8 for MVP completion. Weeks 9-11 are for stretch goals and polish. |

---

## Risk Management

### Identified Risks

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **PyBullet IK accuracy** | Medium | Validate against RobotStudio; document accuracy limits |
| **RAPID parser complexity** | Medium | Start with core features (MoveJ/L/IF/FOR); defer advanced |
| **Babylon.js performance** | Low | Optimize LOD; profile early; cache trajectories |
| **Collision detection speed** | Low | Broad-phase culling; spatial hashing; async computation |
| **Scope creep** | High | **Hard cutoff at Week 8; defer all stretch goals** |

### Success Factors

1. **Clear MVP Definition** - Student View focused, no feature creep
2. **Early Testing** - Start testing with real RAPID programs by Week 4
3. **Weekly Checkpoints** - Review progress every Friday; adjust if needed
4. **Modular Design** - Decouple RAPID parser from rendering; enable parallel work
5. **Documentation** - Keep SOP and API docs updated continuously (not Week 11)
6. **Week 6 Critical** - End-to-end `/api/simulate` pipeline working by end of Week 6 is key to hitting MVP
7. **Scope Discipline** - Week 4 parser: MoveL/MoveJ/MoveC only; control flow deferred to Phase 4

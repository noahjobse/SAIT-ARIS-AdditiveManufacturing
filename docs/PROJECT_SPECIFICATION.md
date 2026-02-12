# ABB Online Simulation Platform - Project Specification

## Executive Summary

This project delivers a browser-based "Digital Twin" for the **ABB IRB 4600, 2600, and 6700** industrial robots. The **MVP (Minimum Viable Product)** focuses on a high-quality **Student View** for learning RAPID logic and kinematics. Advanced **Engineer View** diagnostics and **Production Readiness** are designated as Phase 2 extensions to be implemented as time permits.

**Timeline:** 11 weeks
**Target Users:** Students learning RAPID, junior engineers
**Platform:** Web-based (TypeScript/Babylon.js frontend, Python FastAPI backend)

---

## Technical Architecture

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | React 19 + TypeScript + Babylon.js 8.46 | Type-safe 3D rendering and UI |
| **Backend** | Python 3.11 + FastAPI 0.128 + PyBullet 3.2.6 | Kinematics solver and collision detection |
| **Data Model** | File-based (no database for MVP) | Server-side trajectory computation |
| **Parser** | Lark (Python parser generator) | RAPID grammar → AST transformation |
| **Robot Models** | GLB (frontend) + URDF (backend) | Dual format for rendering + physics |
| **Build Tools** | Vite 7 (frontend), pip (backend) | Fast development and production builds |
| **Styling** | Tailwind CSS 4 | Utility-first responsive design |

---

## Functional Requirements

### 3.1 MVP Requirements (Student View - Hard Commitment)

| ID | Requirement | Description | Priority |
|-----|-----------|-------------|----------|
| **FR-1** | Triple-Model Support | Provide rigged 3D models and kinematics for IRB 4600, 2600, and 6700 | CRITICAL |
| **FR-2** | Environment Upload | Users can upload custom workcell geometry (STL/OBJ) | CRITICAL |
| **FR-3** | Active Transform Gizmo | In-app 3D Gizmo for manual adjustment (X, Y, Z, R) of obstacles | CRITICAL |
| **FR-4** | RAPID Interpretation | Parse motion commands (MoveJ/MoveL/MoveC) for MVP; basic logic (IF, FOR, WHILE) in Phase 4 | CRITICAL |
| **FR-5** | Batch Processing | Calculate trajectory server-side before playback | CRITICAL |
| **FR-6** | Playback Controls | Timeline scrubber: play, pause, seek through simulation | CRITICAL |
| **FR-7** | Basic Collision | Visual warning (e.g., robot turns red) upon collision | CRITICAL |

### 3.2 Stretch Goals (Engineer View - Secondary Priority)

| ID | Requirement | Description | Priority |
|-----|-----------|-------------|----------|
| **FR-8** | Line-Linked Logging | Map collision events to RAPID source line numbers | STRETCH |
| **FR-9** | Link-Specific Diagnostics | Identify exact robot link involved in collision | STRETCH |
| **FR-10** | Advanced Overlays | Display TCP velocity and joint acceleration curves | STRETCH |

### 3.3 Production Readiness (Tertiary Priority)

| ID | Requirement | Description | Priority |
|-----|-----------|-------------|----------|
| **FR-11** | Persistence | Save/load workcell layouts and code via database | DEFER |
| **FR-12** | High-Precision Audit | Validate math against ABB RobotStudio decimals | DEFER |

---

## 11-Week Staged Roadmap

### Phase 1: Visualization & Foundation (Weeks 1-3)

**Goal:** Build 3D rendering, robot models, and environment tools

| Week | Focus | Deliverables | MVP Impact |
|------|-------|--------------|-----------|
| **1** | TypeScript setup, Babylon.js scene, STL uploader | Project scaffold, basic 3D scene, file upload API | Foundation |
| **2** | Robot rigging (IRB 4600 FK), model import | Rigged robot model, forward kinematics | Core Feature (FR-1) |
| **3** | Gizmo implementation, obstacle positioning | 3D transform gizmo for obstacles | Core Feature (FR-3) |

**Frontend Deliverables:**
- Babylon.js scene with camera/lighting
- React UI for file upload
- 3D gizmo for obstacle transformation
- Model viewer with debug info

**Backend Deliverables:**
- STL/OBJ parsing and validation
- Forward kinematics for IRB 4600
- `/api/upload` and `/api/models` endpoints

---

### Phase 2: The Brain - Logic & Kinematics (Weeks 4-6)

**Goal:** Implement RAPID parser and PyBullet integration

| Week | Focus | Deliverables | MVP Impact |
|------|-------|--------------|-----------|
| **4** | RAPID parser (MoveJ, MoveL, MoveC) | Working parser, AST structure | Core Feature (FR-4) |
| **5** | PyBullet IK, trajectory generation | Inverse kinematics, smooth interpolation | Core Feature (FR-5) |
| **6** | Batch execution, JSON trajectory output | End-to-end RAPID → trajectory pipeline | Core Feature (FR-5) |

**Backend Deliverables:**
- RAPID lexer + parser (Python)
- PyBullet physics engine integration
- `/api/parse-rapid` and `/api/execute` endpoints
- Trajectory JSON format

---

### Phase 3: Student MVP Launch (Weeks 7-8)

**Goal:** Polish UI/UX, implement playback, finalize Student View MVP

| Week | Focus | Deliverables | MVP Status |
|------|-------|--------------|-----------|
| **7** | Playback engine, timeline scrubber | Play/pause/seek controls, animation loop | Core Feature (FR-6) |
| **8** | Collision detection (basic), visual feedback | Red highlighting on collision, basic logs | Core Feature (FR-7) |

**Frontend Deliverables:**
- Timeline UI with scrubber
- Real-time robot animation
- Collision highlighting
- Basic error messages

**Status:** **MVP COMPLETE** - Ready for student testing

---

### Phase 4: Expansion (Weeks 9-10) - If Time Permits

**Goal:** Engineer View features and multi-robot support

| Week | Focus | Deliverables | Feature |
|------|-------|--------------|---------|
| **9** | Control flow (IF/ELSE), multi-robot validation | Conditional branching, verify all 3 robots work | FR-4 (extended), FR-1 (validation) |
| **10** | Loop support (FOR/WHILE), advanced overlays | Loop execution, velocity curves (optional) | FR-4 (extended), FR-10 |

**Note:** All 3 robots (IRB 4600, 2600, 6700) functional by Week 8 MVP. Weeks 9-10 add control flow and validate multi-robot support.

---

### Phase 5: Finalization (Week 11)

**Goal:** Documentation, testing, final delivery

**Deliverables:**
- Complete API documentation (OpenAPI/Swagger)
- User SOP (Standard Operating Procedure)
- Test coverage for core features
- Final presentation & demo video
- Production deployment checklist

---

## Final Scope Statement

> **"An 11-week project to develop a TypeScript/Babylon.js platform for the ABB IRB 4600, 2600, and 6700, focused on a Student View MVP that provides batch-processed RAPID logic simulation and workcell collision visualization, with modular paths toward engineer-grade diagnostics."**

---

## Success Criteria

### MVP (Weeks 1-8)
✅ Student can upload RAPID code
✅ Trajectory animates smoothly in 3D
✅ Collision detection works with obstacles
✅ UI is intuitive for non-programmers
✅ System runs without crashes for 30+ min sessions

### Phase 2 (Weeks 9-10)
- Line-linked collision reports
- Multi-robot (3 models) support
- Advanced diagnostics visible to engineers

### Production (Week 11)
- Full documentation
- Deployment ready
- Demo-ready for stakeholders

---

## Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| **MVP Focus** | Ensure polished, working deliverable by Week 8 |
| **Batch Processing** | Simpler than real-time; accurate server-side computation |
| **Lightweight Client** | All heavy computation (IK, collision) server-side for smooth 60 FPS rendering |
| **No Database** | File-based storage for MVP; no user accounts or persistence needed |
| **Lark Parser** | Grammar-based parser generator; faster to implement than hand-written parser |
| **Dual Model Formats** | GLB for Babylon.js rendering, URDF for PyBullet physics |
| **PyBullet** | Industry-standard, free, accurate kinematics solver |
| **TypeScript** | Type safety for complex geometry and state |
| **Babylon.js** | Built-in industrial tools, native TS support, WebGL rendering |

---

## Risk Management

| Risk | Mitigation |
|------|-----------|
| PyBullet IK accuracy | Validate against RobotStudio; document limitations |
| Babylon.js performance | Optimize mesh LOD; profile early |
| RAPID parser edge cases | Comprehensive test suite with real programs |
| Collision detection cost | Spatial hashing; broad-phase culling |
| Scope creep | Hard cutoff at Week 8 for MVP; document stretch goals |

---

## Team Responsibilities

| Role | Responsibility |
|------|-----------------|
| **Lead (SAIT)** | Timeline management, stakeholder updates, final delivery |
| **Frontend Team** | React UI, Babylon.js rendering, UX polish |
| **Backend Team** | RAPID parser, PyBullet integration, API design |
| **Testing** | Unit tests, integration tests, regression suite |
| **Documentation** | SOP, API docs, user guide |

---

## Deployment Plan

**Development:** Local (Vite + Uvicorn)
**Testing:** Docker containers (reproducible environment)
**Production:** AWS/Vercel (frontend) + AWS EC2/Lambda (backend)

See [docs/guides/deployment.md](guides/deployment.md) for details.

---

## Next Steps

1. **Immediate (Week 1):**
   - Finalize team assignments
   - Set up CI/CD pipeline
   - Complete Phase 1 Technical Checklist

2. **Week 2-3:**
   - Deliver robot models and FK solver
   - Implement STL uploader

3. **Week 4-6:**
   - Integrate PyBullet
   - Build RAPID parser

4. **Week 7-8:**
   - Finalize MVP with playback + collisions
   - Internal testing and polish

---

**Document Version:** 1.1
**Last Updated:** 2026-02-05
**Status:** Updated with Week 1-2 planning decisions

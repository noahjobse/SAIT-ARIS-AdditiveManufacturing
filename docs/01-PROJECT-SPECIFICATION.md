# Project Specification

**Project:** ABB Online Simulation Platform
**Version:** 2.0
**Date:** 2026-02-12
**Team:** SAIT Research Applications x ARIS Robotics

---

## Executive Summary

Browser-based "Digital Twin" for **ABB IRB 4600, 2600, and 6700** industrial robots. The **MVP** focuses on a **Student View** for learning RAPID logic and kinematics. Engineer View diagnostics and Production Readiness are Phase 2 extensions.

**Timeline:** 11 weeks | **MVP Target:** Week 8
**Target Users:** Students learning RAPID, junior engineers
**Platform:** Web-based (TypeScript/Babylon.js frontend, Python FastAPI backend)

## Technical Architecture

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | React 19 + TypeScript + Babylon.js 8.46 | Type-safe 3D rendering and UI |
| **Backend** | Python 3.11 + FastAPI 0.128 + PyBullet 3.2.6 | Kinematics solver and collision detection |
| **Data Model** | File-based (no database for MVP) | Server-side trajectory computation |
| **Parser** | Lark (Python parser generator) | RAPID grammar -> AST transformation |
| **Robot Models** | GLB (frontend) + URDF (backend) | Dual format for rendering + physics |
| **Build Tools** | Vite 7 (frontend), pip (backend) | Fast development and production builds |
| **Styling** | Tailwind CSS 4 | Utility-first responsive design |

## Functional Requirements

### MVP Requirements (Student View - Hard Commitment)

| ID | Requirement | Description | Priority |
|-----|-----------|-------------|----------|
| **FR-1** | Triple-Model Support | Provide rigged 3D models and kinematics for IRB 4600, 2600, and 6700 | CRITICAL |
| **FR-2** | Environment Upload | Users can upload custom workcell geometry (STL/OBJ) | CRITICAL |
| **FR-3** | Active Transform Gizmo | In-app 3D Gizmo for manual adjustment (X, Y, Z, R) of obstacles | CRITICAL |
| **FR-4** | RAPID Interpretation | Parse motion commands (MoveJ/MoveL/MoveC) for MVP; basic logic (IF, FOR, WHILE) in Phase 4 | CRITICAL |
| **FR-5** | Batch Processing | Calculate trajectory server-side before playback | CRITICAL |
| **FR-6** | Playback Controls | Timeline scrubber: play, pause, seek through simulation | CRITICAL |
| **FR-7** | Basic Collision | Visual warning (e.g., robot turns red) upon collision | CRITICAL |

### Stretch Goals (Engineer View)

| ID | Requirement | Description | Priority |
|-----|-----------|-------------|----------|
| **FR-8** | Line-Linked Logging | Map collision events to RAPID source line numbers | STRETCH |
| **FR-9** | Link-Specific Diagnostics | Identify exact robot link involved in collision | STRETCH |
| **FR-10** | Advanced Overlays | Display TCP velocity and joint acceleration curves | STRETCH |
| **FR-11** | Persistence | Save/load workcell layouts and code via database | DEFER |
| **FR-12** | High-Precision Audit | Validate math against ABB RobotStudio decimals | DEFER |

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
| **Synchronous API** | No WebSockets needed; frontend requests full trajectory, animates locally |

## Success Criteria

### MVP (Week 8)
- Student can upload RAPID code
- Trajectory animates smoothly in 3D
- Collision detection works with obstacles
- UI is intuitive for non-programmers
- System runs without crashes for 30+ min sessions
- `/api/simulate` completes in <5s for typical programs
- Frontend animates at 60 FPS
- Backend coverage >= 80%, frontend >= 60%

## Risk Management

| Risk | Impact | Mitigation |
|------|--------|-----------|
| PyBullet IK accuracy | High | Validate against RobotStudio; document limitations |
| RAPID parser complexity | Medium | Phased grammar: movement-only MVP, control flow Phase 4 |
| Babylon.js performance | Medium | Optimize LOD; profile early; cache trajectories |
| Collision detection speed | Low | Broad-phase culling; spatial hashing; async computation |
| Scope creep | High | Hard cutoff at Week 8; defer all stretch goals |
| Noah workload overload | Medium | Weekly workload review, delegate docs where possible |
| Timeline overrun | High | MVP gate at Week 8, defer stretch goals if needed |

---

**Last Updated:** 2026-02-12

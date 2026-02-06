# ABB Online Simulation Platform - Team Documentation Hub

**Welcome to the project!** This is your starting point for all project documentation.

---

## 🚀 Quick Start by Role

### Frontend Developer (Dylane, Umaya)
1. Read: [Project Specification](PROJECT_SPECIFICATION.md) - understand the MVP goals
2. Read: [System Design](architecture/system-design.md) - frontend architecture
3. Check: **Current Sprint Plan** (see [Sprint Plans](#-sprint-plans-roadmap) below)
4. Review: [Task Assignments](team/task-assignments.md) - your specific tasks
5. Setup: See [CLAUDE.md](../CLAUDE.md) - development commands

### Backend Developer (Jason, Noah)
1. Read: [Project Specification](PROJECT_SPECIFICATION.md) - understand the MVP goals
2. Read: [System Design](architecture/system-design.md) - backend architecture
3. Review: [API Specification](architecture/api-specification.md) - endpoint contracts
4. Check: **Current Sprint Plan** (see [Sprint Plans](#-sprint-plans-roadmap) below)
5. Review: [Task Assignments](team/task-assignments.md) - your specific tasks
6. Setup: See [CLAUDE.md](../CLAUDE.md) - development commands

### QA/PM (Noah)
1. Read: [Project Specification](PROJECT_SPECIFICATION.md) - MVP acceptance criteria
2. Review: [11-Week Plan](roadmap/11-week-plan.md) - overall timeline
3. Check: **Current Sprint Plan** (see [Sprint Plans](#-sprint-plans-roadmap) below)
4. Review: [Implementation Timeline](roadmap/implementation-timeline.md) - phased breakdown

### New to the Project?
1. Start with [Project Specification](PROJECT_SPECIFICATION.md) - **READ THIS FIRST**
2. Then read [System Design](architecture/system-design.md) - understand the architecture
3. Find your current sprint in [Sprint Plans](#-sprint-plans-roadmap)
4. Check [Task Assignments](team/task-assignments.md) for your work

---

## 📋 Documentation Hierarchy

### 1. **Project Overview** (Start Here)

#### Core Documents
- **[Project Specification](PROJECT_SPECIFICATION.md)** ⭐ **START HERE**
  - MVP requirements (FR-1 to FR-7)
  - Technical architecture
  - Success criteria
  - 11-week roadmap overview

- **[CLAUDE.md](../CLAUDE.md)** - Project instructions for Claude Code
  - Development commands (frontend & backend)
  - Architecture overview
  - Common development tasks
  - Testing commands

- **[README.md](../README.md)** - Repository overview
  - Quick start instructions
  - Project description
  - Technology stack

---

### 2. **Architecture & Design** (Technical Foundation)

#### System Architecture
- **[System Design](architecture/system-design.md)** ⭐ **CRITICAL**
  - Full pipeline workflow (RAPID → parse → simulate → render)
  - Component interaction diagrams
  - Technology stack details
  - Data flow architecture

- **[API Specification](architecture/api-specification.md)**
  - All endpoint definitions
  - Request/response schemas
  - Authentication (future)
  - Error codes

#### Reference Documents
- **Research Docs** (if needed):
  - RAPID language specification
  - ABB robot datasheets
  - Kinematics references

---

### 3. **🗓️ Sprint Plans & Roadmap** (Week-by-Week)

#### High-Level Planning
- **[11-Week Plan](roadmap/11-week-plan.md)** - Overview of all phases
  - Phase 1: Weeks 1-3 (Visualization foundation)
  - Phase 2: Weeks 4-6 (Logic & kinematics)
  - Phase 3: Weeks 7-8 (MVP polish)
  - Phase 4: Weeks 9-11 (Stretch goals & handoff)

- **[Implementation Timeline](roadmap/implementation-timeline.md)** - Person-by-person breakdown
  - Task assignments by team member
  - Dependencies between team members
  - Week-by-week deliverables

#### Detailed Sprint Plans (2-Week Sprints)

**📍 CURRENT SPRINT:** [Check here for which sprint you're in](#current-sprint-finder)

- **[Week 1-2 Sprint Plan](roadmap/week-1-2-sprint-plan.md)** - Foundation
  - 3D scene, robot loading, API structure, upload flow
  - **Deliverable:** Robot visible, sliders working, files uploadable

- **[Week 3-4 Sprint Plan](roadmap/week-3-4-sprint-plan.md)** - Parser & Kinematics
  - RAPID parser (MoveL/MoveJ/MoveC), FK/IK solver, obstacle gizmo
  - **Deliverable:** Upload RAPID → parsed AST, FK working, gizmo functional

- **[Week 5-6 Sprint Plan](roadmap/week-5-6-sprint-plan.md)** - Simulation Pipeline
  - End-to-end `/api/simulate`, trajectory generation, collision detection
  - **Deliverable:** Full simulation pipeline, collision highlighting

- **[Week 7-8 Sprint Plan](roadmap/week-7-8-sprint-plan.md)** ⭐ **MVP LAUNCH**
  - Timeline scrubber, playback controls, error states, UAT, MVP sign-off
  - **Deliverable:** **STUDENT MVP COMPLETE**

- **[Week 9-10 Sprint Plan](roadmap/week-9-10-sprint-plan.md)** - Stretch Goals
  - RAPID control flow (IF/ELSE/FOR/WHILE), multi-robot support
  - **Deliverable:** Control flow working, all 3 robots functional

- **[Week 11 Finalization](roadmap/week-11-finalization.md)** - Handoff
  - Documentation, testing, deployment, demo, presentation
  - **Deliverable:** Project handoff complete

---

### 4. **Team Coordination** (Who's Doing What)

- **[Task Assignments](team/task-assignments.md)**
  - Current sprint tasks by person
  - Task status (pending, in-progress, done)
  - Dependencies between tasks

- **Communication Channels:**
  - `#abb-sim-dev` - General development discussion
  - `#abb-sim-frontend` - Frontend-specific (Dylane, Umaya)
  - `#abb-sim-backend` - Backend-specific (Jason, Noah)
  - `#abb-sim-qa` - Testing and QA (Noah)

- **Daily Standup:** 9:00 AM (15 minutes)
  - What did you complete yesterday?
  - What are you working on today?
  - Any blockers?

---

### 5. **Development Guides** (How to Build)

#### Setup & Configuration
- **[CLAUDE.md](../CLAUDE.md)** - Development commands
  - Frontend setup (React + Vite)
  - Backend setup (FastAPI + PyBullet)
  - Docker setup
  - Running tests

#### Code Standards
- **Frontend:**
  - TypeScript strict mode
  - React functional components + hooks
  - Tailwind CSS for styling
  - ESLint enforced

- **Backend:**
  - Python 3.11
  - FastAPI best practices
  - Pydantic for validation
  - Ruff for linting

---

### 6. **Testing & Quality** (How to Test)

#### Testing Documentation
- **Testing Strategy** (to be created in Week 1-2)
  - Test pyramid (70% unit, 20% integration, 10% manual)
  - Coverage targets (80% backend, 60% frontend)
  - Testing tools (pytest, vitest)

#### Test Commands
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
pnpm test

# Run specific test
pytest tests/test_specific.py::TestClass::test_method
```

---

### 7. **Deployment & Operations** (How to Deploy)

#### Deployment Guides (Week 11)
- Deployment configuration (Docker Compose)
- Cloud deployment (AWS/Azure/GCP)
- Environment variables
- Monitoring and logging

---

## 🎯 Current Sprint Finder

**How to find your current sprint:**

1. **Check today's date:** [Current Date: 2026-02-05]

2. **Match to sprint:**
   - **Weeks 1-2** (Days 1-14): [Week 1-2 Sprint Plan](roadmap/week-1-2-sprint-plan.md)
   - **Weeks 3-4** (Days 15-28): [Week 3-4 Sprint Plan](roadmap/week-3-4-sprint-plan.md)
   - **Weeks 5-6** (Days 29-42): [Week 5-6 Sprint Plan](roadmap/week-5-6-sprint-plan.md)
   - **Weeks 7-8** (Days 43-56): [Week 7-8 Sprint Plan](roadmap/week-7-8-sprint-plan.md) ⭐ MVP
   - **Weeks 9-10** (Days 57-70): [Week 9-10 Sprint Plan](roadmap/week-9-10-sprint-plan.md)
   - **Week 11** (Days 71-77): [Week 11 Finalization](roadmap/week-11-finalization.md)

3. **Check your tasks:** [Task Assignments](team/task-assignments.md)

---

## 📊 Progress Tracking

### Sprint Completion Checklist

- [ ] **Week 1-2:** Foundation complete
  - [ ] 3D scene renders with robot
  - [ ] Joint sliders working
  - [ ] Upload UI functional
  - [ ] Backend endpoints working

- [ ] **Week 3-4:** Parser & kinematics complete
  - [ ] RAPID parser working
  - [ ] FK/IK solver functional
  - [ ] Obstacle gizmo working

- [ ] **Week 5-6:** Simulation pipeline complete
  - [ ] `/api/simulate` endpoint working
  - [ ] Trajectory animation functional
  - [ ] Collision detection working

- [ ] **Week 7-8:** MVP COMPLETE ⭐
  - [ ] Timeline scrubber working
  - [ ] All playback controls functional
  - [ ] MVP acceptance criteria met
  - [ ] UAT passed
  - [ ] **MVP SIGN-OFF APPROVED**

- [ ] **Week 9-10:** Stretch goals complete
  - [ ] Control flow (IF/ELSE/FOR/WHILE)
  - [ ] All 3 robots working

- [ ] **Week 11:** Project handoff complete
  - [ ] Documentation complete
  - [ ] Deployment tested
  - [ ] Demo video recorded
  - [ ] Final presentation delivered

---

## 🔍 Quick Reference

### MVP Functional Requirements (Must-Have by Week 8)

| ID | Requirement | Sprint |
|----|-------------|--------|
| **FR-1** | Triple-Model Support (IRB 4600, 2600, 6700) | Week 1-2, 3-4, 9-10 |
| **FR-2** | Environment Upload (STL/OBJ obstacles) | Week 1-2, 3-4 |
| **FR-3** | Active Transform Gizmo (X, Y, Z, R) | Week 3-4 |
| **FR-4** | RAPID Interpretation (MoveL/MoveJ/MoveC) | Week 3-4 |
| **FR-5** | Batch Processing (server-side trajectory) | Week 5-6 |
| **FR-6** | Playback Controls (timeline scrubber) | Week 5-6, 7-8 |
| **FR-7** | Basic Collision (visual warning) | Week 5-6 |

### Technology Stack Quick Reference

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 19 + TypeScript | UI framework |
| | Babylon.js 8.46 | 3D rendering |
| | Vite 7 | Build tool |
| | Tailwind CSS 4 | Styling |
| **Backend** | Python 3.11 | Language |
| | FastAPI 0.128 | Web framework |
| | PyBullet 3.2.6 | Physics & IK |
| | Lark | RAPID parser |

### Key API Endpoints

| Endpoint | Method | Purpose | Sprint |
|----------|--------|---------|--------|
| `/api/robots` | GET | List all robots | Week 1-2 |
| `/api/robots/{id}/model` | GET | Get robot GLB | Week 1-2 |
| `/api/upload/rapid` | POST | Upload RAPID file | Week 1-2, 3-4 |
| `/api/upload/obstacle` | POST | Upload obstacle STL | Week 1-2 |
| `/api/simulate` | POST | Run simulation | Week 5-6 |

---

## 📞 Getting Help

### Blocked on a Task?
1. Check sprint plan for dependencies and mitigation strategies
2. Ask in relevant Slack channel (`#abb-sim-frontend`, `#abb-sim-backend`)
3. Bring up in daily standup
4. Pair program with team member if needed

### Documentation Issues?
- If a document is unclear, create a GitHub issue
- Suggest improvements in `#abb-sim-dev`
- Update docs as you learn (keep docs current)

### Technical Questions?
- Frontend: Ask Dylane or Umaya
- Backend: Ask Jason or Noah
- Testing/QA: Ask Noah
- Project planning: Ask Noah (PM)

---

## 📝 Document Change Log

### Version History
- **2026-02-05:** Initial documentation hub created
  - All 6 sprint plans created (Week 1-2, 3-4, 5-6, 7-8, 9-10, Week 11)
  - Hybrid format (weekly overview + critical daily tasks)
  - Risk management and demo criteria included

### Contributing to Docs
- Keep docs up-to-date as project evolves
- Update sprint plans during sprint reviews
- Add new guides as needed (user guide, deployment guide, etc.)
- Fix typos and improve clarity whenever you spot issues

---

## 🎓 Learning Resources

### Babylon.js
- [Official Documentation](https://doc.babylonjs.com/)
- [Playground](https://playground.babylonjs.com/)
- [Examples](https://doc.babylonjs.com/features/featuresDeepDive)

### FastAPI
- [Official Documentation](https://fastapi.tiangolo.com/)
- [Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Advanced User Guide](https://fastapi.tiangolo.com/advanced/)

### PyBullet
- [Quick Start Guide](https://github.com/bulletphysics/bullet3/blob/master/examples/pybullet/quickstartguide.pdf)
- [PyBullet Examples](https://github.com/bulletphysics/bullet3/tree/master/examples/pybullet/examples)

### RAPID Programming
- ABB RAPID Reference Manual (in `/docs/research/`)
- RobotStudio examples

---

**Last Updated:** 2026-02-05
**Maintained By:** Noah (PM/QA Lead)
**Questions?** Post in `#abb-sim-dev` Slack channel

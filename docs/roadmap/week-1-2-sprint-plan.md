# Week 1-2 Sprint Plan

**Sprint Duration:** Weeks 1-2 (14 days)
**Sprint Goal:** Foundation - 3D scene working, robot loads and moves, API structure, upload flow
**Key Milestone:** Robot visible and joints controllable in browser

---

## Sprint Overview

By the end of Week 2, we should have:

✅ Babylon.js 3D scene with IRB 4600 robot loaded and orbitable
✅ 6 joint angle sliders that move the robot in real-time
✅ Frontend layout (Header, Viewport, Sidebar) styled with Tailwind
✅ Robot selector dropdown (UI only, switching in Week 3-4)
✅ File upload UI (drag & drop for RAPID + STL files)
✅ Backend API structure (`/api/robots`, `/api/robots/{id}/model`, upload endpoints)
✅ GLB file serving working (frontend loads robot from backend)
✅ Upload endpoints accepting files (parse logic comes in Week 3-4)
✅ Test infrastructure (pytest + vitest running in CI)
✅ Sample RAPID files for testing

---

## Weekly Goals

### Week 1 Overview

**Frontend - Dylane:**
- Initialize Babylon.js scene with camera, lighting, ground plane
- Load IRB 4600 GLB from backend API
- Ensure camera orbits robot with mouse controls

**Frontend - Umaya:**
- Build App layout shell (Header, MainLayout split pane, SidePanel)
- Create robot selector dropdown with 3 options
- Apply Tailwind CSS dark theme styling

**Backend - Jason:**
- Set up FastAPI router structure (robots, upload, simulate)
- Implement `GET /api/robots` endpoint (return 3 robots)
- Implement `GET /api/robots/{id}/model` endpoint (serve GLB binary)

**Backend - Noah:**
- Add IRB 4600 GLB file to repository
- Set up pytest configuration and write initial tests
- Verify test infrastructure runs in CI

**PM/QA - Noah:**
- Configure frontend test setup (Vitest)
- Create sample RAPID programs for testing
- Verify CI pipelines pass

### Week 2 Overview

**Frontend - Dylane:**
- Implement skeleton-based joint animation
- Build 6 joint angle sliders (-180° to +180°)
- Wire sliders to robot joints with real-time updates

**Frontend - Umaya:**
- Build file upload component (drag & drop + browse)
- Wire upload buttons to backend API
- Create RAPID editor panel to display uploaded code

**Backend - Jason:**
- Research Lark parser library
- Draft initial RAPID grammar for MoveL commands
- Implement `POST /api/upload/rapid` endpoint skeleton

**Backend - Noah:**
- Implement file upload handler for RAPID and obstacle files
- Create Pydantic schemas for all endpoints
- Add file validation (extension, size limits)

**PM/QA - Noah:**
- Write integration tests for upload endpoints
- Document testing strategy
- Prepare sprint review demo

---

## Critical Daily Tasks

### Cross-Team Integration Points

**Day 1 (Noah Backend):** Add GLB file to repository
- **Blocks:** Dylane Day 3 robot loading
- **Mitigation:** If delayed, Dylane uses placeholder cube mesh temporarily

**Day 1-2 (Jason):** FastAPI router setup complete
- **Blocks:** Umaya Day 8 upload endpoint wiring
- **Mitigation:** If delayed, Umaya mocks API responses in frontend

**Day 3 (Dylane):** Robot GLB loading functional
- **Integration:** Requires Jason's `/api/robots/{id}/model` endpoint working
- **Verification:** GLB loads in browser, no CORS errors

**Day 8 (Umaya):** Upload endpoint wiring complete
- **Integration:** Requires Jason's upload route and Noah's file handler
- **Verification:** Files upload successfully, response logged in console

---

## Weekly Task Breakdown

### Frontend - Dylane

**Week 1:**
- [ ] Create `SceneSetup.ts` in `src/babylon/`
- [ ] Initialize Babylon.js Engine, Scene, ArcRotateCamera, HemisphericLight
- [ ] Add ground plane (10m × 10m) and grid helper
- [ ] Create `RobotLoader.ts` utility
- [ ] Load IRB 4600 GLB from `/api/robots/irb4600/model` using SceneLoader
- [ ] Handle loading errors with friendly messages
- [ ] Configure camera limits (prevent flip, limit zoom)

**Week 2:**
- [ ] Create `JointController.ts` utility
- [ ] Inspect robot skeleton and map joint names to bone indices (J1-J6)
- [ ] Implement `setJointAngle(jointIndex, angleDegrees)` function
- [ ] Create `JointSliders.tsx` component with 6 range inputs
- [ ] Wire slider onChange events to JointController
- [ ] Add angle value display next to each slider
- [ ] Test all joints at extreme angles, verify smooth motion

**Deliverable:** Robot visible and orbitable, joints move smoothly via sliders, no console errors

---

### Frontend - Umaya

**Week 1:**
- [ ] Refactor `App.tsx` to remove placeholder counter
- [ ] Create `Header.tsx` component (60px height)
- [ ] Create `MainLayout.tsx` component (70% left, 30% right split)
- [ ] Create `SidePanel.tsx` component
- [ ] Create `RobotSelector.tsx` dropdown (IRB 4600, 2600, 6700)
- [ ] Create `UploadButtons.tsx` component (styled with Tailwind)
- [ ] Apply dark theme styling to all components

**Week 2:**
- [ ] Create `FileUpload.tsx` component (drag & drop + browse)
- [ ] Support RAPID (`.mod`) and STL (`.stl`) file types
- [ ] Validate file extensions, show error for invalid files
- [ ] Create `api.ts` with axios client
- [ ] Implement `uploadRapid(file)` and `uploadObstacle(file)` functions
- [ ] Create `RapidEditor.tsx` component (readonly textarea with monospace font)
- [ ] Wire upload success to display code in editor

**Deliverable:** Files uploadable through UI, layout responsive and styled, upload calls backend API

---

### Backend - Jason

**Week 1:**
- [ ] Create `routers/` directory with `robots.py`, `upload.py`, `simulate.py`
- [ ] Refactor `main.py` to use APIRouter
- [ ] Add CORS middleware (allow all origins for dev)
- [ ] Define `RobotInfo` Pydantic model in `schemas/responses.py`
- [ ] Implement `GET /api/robots` (return 3 robots with metadata)
- [ ] Implement `GET /api/robots/{robot_id}/model` (serve GLB with FileResponse)
- [ ] Test endpoints in Swagger UI at `/docs`

**Week 2:**
- [ ] Install Lark: `pip install lark-parser`
- [ ] Read Lark documentation and run examples
- [ ] Study RAPID language spec (focus on MoveL syntax)
- [ ] Draft `grammar.lark` for MoveL only (simplified)
- [ ] Define `UploadRapidResponse` Pydantic model
- [ ] Implement `POST /api/upload/rapid` skeleton (accept file, return placeholder AST)
- [ ] Add file validation (`.mod` extension, <1MB size)

**Deliverable:** Robot list and GLB serving working, upload endpoints accepting files, Lark parser researched

---

### Backend - Noah

**Week 1:**
- [ ] Copy IRB 4600 GLB from local path to `/models/robots/irb4600/visual.glb`
- [ ] Commit GLB file: `git add models/ && git commit -m "Add IRB 4600 GLB model"`
- [ ] Create `tests/conftest.py` with pytest fixtures
- [ ] Write `test_health.py` for `GET /api/health` endpoint
- [ ] Write `test_robots.py` for `GET /api/robots` endpoint
- [ ] Verify pytest runs successfully

**Week 2:**
- [ ] Implement file upload handler in `routers/upload.py` using FastAPI UploadFile
- [ ] Save uploaded files to `/uploads/` directory with unique filenames
- [ ] Define Pydantic schemas in `schemas/requests.py` and `schemas/responses.py`
- [ ] Implement `POST /api/upload/rapid` (save file, return placeholder response)
- [ ] Define `UploadObstacleResponse` Pydantic model
- [ ] Implement `POST /api/upload/obstacle` (save STL to `/models/obstacles/`)
- [ ] Add validation rules (file extension, max size)

**Deliverable:** GLB file in repo, upload endpoints save files to disk, Pydantic schemas defined

---

### PM/QA - Noah

**Week 1:**
- [ ] Verify Vitest installed in `frontend/package.json`
- [ ] Create `vitest.config.ts` (globals: true, environment: jsdom)
- [ ] Write `src/App.test.tsx` (basic render test)
- [ ] Verify `pnpm test` runs successfully
- [ ] Trigger backend and frontend CI pipelines
- [ ] Fix any CI failures, ensure green checkmarks on commits
- [ ] Create `tests/fixtures/rapid/` directory
- [ ] Write 3 sample RAPID programs: `simple_movel.mod`, `simple_movej.mod`, `simple_movec.mod`

**Week 2:**
- [ ] Create `test_upload_integration.py`
- [ ] Write test: upload `simple_movel.mod` → verify 200 OK
- [ ] Write test: upload invalid file (`.txt`) → verify 400 Bad Request
- [ ] Write test: upload file >1MB → verify 400 Bad Request
- [ ] Create `docs/testing-strategy.md` documenting test pyramid and coverage targets
- [ ] Create GitHub issue templates (bug report, feature request)
- [ ] Schedule Week 2 sprint review (30 minutes, all team members)
- [ ] Prepare demo script (robot loading, joint sliders, upload UI)

**Deliverable:** Tests running in CI, sample RAPID files created, testing strategy documented, sprint review scheduled

---

## Risk Management

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| GLB file delays block Dylane's Day 3 work | Medium | High | Dylane uses placeholder cube mesh, swaps to robot when GLB ready |
| Backend API delays block Umaya's Day 8 upload wiring | Medium | High | Umaya mocks API responses in frontend, swaps to real API later |
| Babylon.js skeleton animation issues | Low | Medium | Dylane pair-programs with Noah for debugging session |
| CORS errors prevent frontend from calling backend | Low | High | Jason adds CORS middleware on Day 1, test early with simple GET request |
| Pytest or Vitest configuration issues | Low | Medium | Noah dedicates Day 1-2 to test infrastructure, asks for help if blocked |

---

## Testing Requirements

**Week 1:**
- [ ] Test `GET /api/health` endpoint (Noah)
- [ ] Test `GET /api/robots` endpoint (Noah)
- [ ] Test `GET /api/robots/irb4600/model` returns GLB binary (Noah)
- [ ] Test frontend renders without console errors (Noah)
- [ ] Verify CI pipelines pass for both frontend and backend (Noah)

**Week 2:**
- [ ] Test `POST /api/upload/rapid` with valid .mod file (Noah)
- [ ] Test upload rejection for invalid file types (Noah)
- [ ] Test upload rejection for files >1MB (Noah)
- [ ] Test frontend upload component triggers API call (Umaya)
- [ ] Test all 6 joint sliders move robot (Dylane)

---

## Demo-Ready Acceptance Criteria

By end of this sprint, team can demo:

### Week 1 Demo Criteria:
- [ ] 3D scene renders with robot model loaded and orbitable
- [ ] Camera controls work smoothly (orbit, zoom, pan)
- [ ] App layout is responsive with dark theme styling
- [ ] Robot selector dropdown shows 3 options (UI only, not functional yet)

### Week 2 Demo Criteria:
- [ ] Can drag-drop RAPID file and see it uploaded to backend
- [ ] Uploaded RAPID code appears in editor panel
- [ ] Moving any of 6 joint sliders immediately updates robot joint position
- [ ] All backend endpoints return correct responses in Swagger UI
- [ ] Tests run in CI and all pass (green checkmarks on commits)

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
| **Dylane** | Babylon.js 3D scene + robot animation | Robot visible, joints move via sliders |
| **Umaya** | React UI layout + file upload | Layout responsive, files uploadable |
| **Jason** | FastAPI router structure + GLB serving | `/api/robots` and `/api/robots/{id}/model` working |
| **Noah (Backend)** | Upload endpoints + file handling | `/api/upload/rapid` and `/api/upload/obstacle` accepting files |
| **Noah (QA/PM)** | Test infrastructure + CI | pytest/vitest running, CI green, GLB in repo |

---

## Communication

**Slack Channels:**
- `#abb-sim-dev` - General development discussion
- `#abb-sim-frontend` - Frontend-specific questions (Dylane, Umaya)
- `#abb-sim-backend` - Backend-specific questions (Jason, Noah)
- `#abb-sim-qa` - Testing and QA updates (Noah)

**Daily Standup:** 9:00 AM (15 minutes, async updates on weekends)

**Sprint Review:** End of Week 2 (30-minute demo, retrospective)

---

## Success Metrics

By end of Week 2, we should achieve:

- [ ] **Frontend:** Robot visible in browser, sliders move joints
- [ ] **Frontend:** Layout responsive, upload UI functional
- [ ] **Backend:** 3 API endpoints working (robots, model, upload)
- [ ] **Backend:** Files accepted and saved to disk
- [ ] **QA:** Tests running in CI (both frontend and backend)
- [ ] **QA:** Sample RAPID programs created

**Sprint Goal Achievement:** 🟢 Green if all 6 items complete, 🟡 Yellow if 4-5 complete, 🔴 Red if <4 complete

---

## Next Sprint Planning

**Week 3-4 Preview:**
- Dylane: Obstacle STL loading + transform gizmo
- Umaya: StatusPanel + obstacle list sidebar
- Jason: Lark grammar + parser implementation
- Noah (Backend): PyBullet FK/IK solver + URDF creation
- Noah (QA): Parser tests + kinematics validation

**Week 3-4 Goal:** RAPID parser complete, FK/IK working, obstacles in scene

---

**Document Owner:** Noah (PM/QA Lead)
**Created:** 2026-02-05
**Last Updated:** 2026-02-05
**Next Update:** End of Week 2 (Sprint Review)

# Testing Strategy

**Project:** ABB Online Simulation Platform
**Version:** 1.0
**Date:** 2026-02-11
**Owner:** Noah (QA Lead)

## Overview

Comprehensive testing approach ensuring correctness, reliability, and performance of the RAPID simulation platform. Testing begins Week 1 and continues through Week 11 with emphasis on regression testing before MVP sign-off.

## Test Pyramid

```
        /\
       /  \  10% Manual/UAT
      /____\
     /      \  20% Integration
    /________\
   /          \  70% Unit Tests
  /____ ______\
```

**Distribution:**
- **70% Unit Tests** - Fast, isolated, test individual functions/components
- **20% Integration Tests** - Test API endpoints, component interactions
- **10% Manual/UAT** - Visual validation, real-world RAPID programs

## Coverage Targets

| Layer | Target | Measurement Tool | Minimum |
|-------|--------|------------------|---------|
| Backend | **80%** | coverage.py | 75% |
| Frontend | **60%** | Istanbul (Vitest) | 50% |
| E2E | **Critical paths only** | Manual testing | N/A |

**Philosophy:** High backend coverage (complex logic), moderate frontend coverage (visual components harder to test).

## Testing Tools

### Backend (Python)

| Tool | Purpose | Version |
|------|---------|---------|
| **pytest** | Test runner | 9.0.2 |
| **pytest-asyncio** | Async test support | Latest |
| **pytest-cov** | Coverage reporting | Latest |
| **coverage.py** | Coverage measurement | Latest |
| **pytest-mock** | Mocking fixtures | Latest |

**Commands:**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Run specific module
pytest tests/test_parser.py

# Run with markers
pytest -m integration
```

### Frontend (TypeScript)

| Tool | Purpose | Version |
|------|---------|---------|
| **Vitest** | Test runner | 4.0.17 |
| **@testing-library/react** | Component testing | Latest |
| **@testing-library/jest-dom** | DOM matchers | Latest |
| **jsdom** | DOM simulation | Latest |

**Commands:**
```bash
# Run all tests
pnpm test

# Run with coverage
pnpm test --coverage

# Run in watch mode
pnpm test --watch

# Run specific file
pnpm test viewport.test.tsx
```

## Test Categories

### 1. Unit Tests (70%)

**Backend:**

**Parser Tests** (`tests/test_parser.py`)
- Valid RAPID → correct AST
- Invalid syntax → error with line number
- Edge cases: empty file, comments, whitespace
- Each instruction type: MoveL, MoveJ, MoveC
- Target types: RobTarget, JointTarget
- Data types: SpeedData, ZoneData
- Minimum 20 test cases

**Kinematics Tests** (`tests/test_kinematics.py`)
- Forward kinematics: joint angles → TCP pose
- Inverse kinematics: TCP pose → joint angles
- Joint limits validation
- Workspace boundary checks
- Known poses from datasheet (ground truth)
- IK convergence for reachable poses
- IK failure for unreachable poses

**Collision Tests** (`tests/test_collision.py`)
- Mesh-to-mesh collision detection
- No collision when separated
- Collision when overlapping
- Penetration depth accuracy
- Contact point calculation
- Convex hull simplification

**Trajectory Tests** (`tests/test_trajectory.py`)
- MoveL → linear interpolation
- MoveJ → joint-space interpolation
- MoveC → circular arc interpolation
- SpeedData affects waypoint density
- ZoneData affects corner blending
- Timestamp calculation

**Frontend:**

**Component Tests** (`src/components/*.test.tsx`)
- Robot selector renders correctly
- Upload buttons trigger file dialog
- Playback controls (play/pause/stop/speed)
- Timeline scrubber updates on drag
- Collision alerts display correctly
- Loading spinner shows during simulation

**Babylon.js Tests** (minimal, mocked)
- Scene initialization
- Robot mesh loading (mocked)
- Joint angle updates (mocked)

### 2. Integration Tests (20%)

**Backend API Tests** (`tests/test_api.py`)

**Test Workflow:**
```python
def test_full_simulation_workflow():
    # 1. Health check
    response = client.get("/api/health")
    assert response.status_code == 200

    # 2. List robots
    response = client.get("/api/robots")
    assert len(response.json()) == 3

    # 3. Upload RAPID
    files = {"file": ("program.mod", rapid_code, "text/plain")}
    response = client.post("/api/upload/rapid", files=files)
    ast = response.json()["ast"]

    # 4. Upload obstacle
    files = {"file": ("table.stl", stl_bytes, "application/octet-stream")}
    response = client.post("/api/upload/obstacle", files=files)
    obstacle_id = response.json()["obstacle_id"]

    # 5. Simulate
    payload = {"robot_id": "irb4600", "ast": ast, "obstacles": [{"obstacle_id": obstacle_id}]}
    response = client.post("/api/simulate", json=payload)
    assert response.status_code == 200
    assert len(response.json()["trajectory"]) > 0
```

**Error Path Tests:**
- Invalid file types → 400
- File too large → 400
- Invalid robot ID → 404
- Malformed JSON → 422
- IK failure → 500 with error_code

**Frontend Integration Tests** (Vitest + Testing Library)

**Component Integration:**
```typescript
test("upload RAPID and start simulation", async () => {
  render(<App />);

  const file = new File([rapidCode], "program.mod", { type: "text/plain" });
  const input = screen.getByLabelText("Upload RAPID");
  await userEvent.upload(input, file);

  await waitFor(() => {
    expect(screen.getByText("Parsing complete")).toBeInTheDocument();
  });

  const simulateButton = screen.getByRole("button", { name: "Simulate" });
  await userEvent.click(simulateButton);

  await waitFor(() => {
    expect(screen.getByText("Simulation complete")).toBeInTheDocument();
  });
});
```

### 3. Manual/UAT (10%)

**User Acceptance Testing (Week 7-8)**

**Test Programs:** 10+ real RAPID programs from RobotStudio
- Simple pick-and-place (5 waypoints)
- Complex assembly (50+ waypoints)
- Circular arcs (MoveC validation)
- Joint moves (MoveJ validation)
- Programs with collisions
- Programs without collisions

**Visual Validation:**
- Robot animates smoothly (60 FPS)
- Collisions highlighted in red
- Timeline scrubber updates correctly
- Joint values display correctly
- TCP pose displays correctly

**Cross-Browser Testing:**
- Chrome (primary)
- Firefox
- Safari (if available)
- Edge

**Performance Testing:**
- `/api/simulate` completes in <5s for 100 waypoints
- Frontend animates without dropped frames
- Large STL files (<10MB) load successfully

## CI/CD Integration

**GitHub Actions Workflow** (`.github/workflows/test.yml`)

```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: cd backend && pip install -r requirements.txt
      - run: cd backend && pytest --cov=app --cov-report=xml
      - uses: codecov/codecov-action@v3
        with:
          files: ./backend/coverage.xml

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'pnpm'
          cache-dependency-path: frontend/pnpm-lock.yaml
      - run: cd frontend && pnpm install
      - run: cd frontend && pnpm test --coverage
      - uses: codecov/codecov-action@v3
        with:
          files: ./frontend/coverage/coverage-final.json
```

**Pre-Commit Hooks** (optional, via `pre-commit` package)
- Linting: ruff (backend), ESLint (frontend)
- Type checking: mypy (backend), tsc (frontend)
- Fast unit tests only (not integration)

## Test Data

**Sample RAPID Programs** (`backend/tests/fixtures/rapid/`)
- `simple_movel.mod` - Single MoveL instruction
- `simple_movej.mod` - Single MoveJ instruction
- `circular_arc.mod` - MoveC with via point
- `pick_and_place.mod` - 5 waypoint sequence
- `complex_program.mod` - 50+ waypoints with mixed instructions
- `invalid_syntax.mod` - Parse error test case
- `out_of_reach.mod` - IK failure test case

**Sample STL Obstacles** (`backend/tests/fixtures/stl/`)
- `cube.stl` - Simple 8-vertex cube
- `table.stl` - Flat surface for collision tests
- `complex_mesh.stl` - High-poly mesh for performance tests

**Robot Config Fixtures** (`backend/tests/fixtures/robots/`)
- Minimal URDF files for testing
- Known DH parameter sets
- Joint limit configurations

## Regression Testing

**MVP Regression Suite (Week 8)**

Before MVP sign-off, run complete regression suite:

1. **Automated Tests:** Full test suite (backend + frontend) with coverage report
2. **Integration Tests:** All API endpoints with valid/invalid inputs
3. **Sample Programs:** All 10+ real RAPID programs from RobotStudio
4. **Multi-Robot:** Test all 3 robots (IRB 4600, 2600, 6700)
5. **Performance:** Benchmark `/api/simulate` for 50, 100, 200 waypoints
6. **Visual QA:** Manual inspection of animations, collision highlighting

**Pass Criteria:**
- ✅ All automated tests pass
- ✅ Backend coverage ≥80%
- ✅ Frontend coverage ≥60%
- ✅ All sample programs simulate successfully
- ✅ Collisions detected and highlighted correctly
- ✅ No performance regressions (<5s simulation time)

## Continuous Testing

**During Development:**
- Developers run `pytest` / `pnpm test` before each commit
- CI runs on every push to feature branches
- PR reviews include test coverage report

**Weekly:**
- Regression test suite on `main` branch
- Performance benchmarks tracked over time
- Test coverage trends reviewed in sprint retro

## Test Responsibilities

| Person | Role | Test Responsibilities |
|--------|------|---------------------|
| **Noah** | QA Lead | CI setup, regression suite, UAT, test data creation, coverage monitoring |
| **Jason** | Backend Lead | Parser tests, trajectory tests, API integration tests |
| **Dylane** | Frontend (Babylon) | Viewport component tests (mocked) |
| **Umaya** | Frontend (React UI) | UI component tests, React Testing Library |

All developers are responsible for writing unit tests for their own code.

## Known Limitations

**Not Tested in MVP:**
- Multi-user concurrency (no database)
- Network failures / retry logic
- WebSocket fallback (not implemented)
- Browser compatibility beyond Chrome/Firefox
- Mobile devices (desktop-only UI)

**Deferred to Post-MVP:**
- Load testing (100+ concurrent users)
- Stress testing (1000+ waypoint trajectories)
- Security testing (penetration testing, fuzz testing)
- Accessibility testing (WCAG compliance)

## References

- [pytest Documentation](https://docs.pytest.org/)
- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

---

**Created:** 2026-02-11
**Owner:** Noah (QA Lead)
**Next Review:** End of Week 2 (validate test infrastructure is working)

# Testing Strategy

**Project:** ABB Online Simulation Platform
**Version:** 2.0
**Date:** 2026-02-12

---

## Test Pyramid

- **70% Unit Tests** - Fast, isolated, test individual functions/components
- **20% Integration Tests** - Test API endpoints, component interactions
- **10% Manual/UAT** - Visual validation, real-world RAPID programs

## Coverage Targets

| Layer | Target | Minimum | Tool |
|-------|--------|---------|------|
| Backend | 80% | 75% | coverage.py |
| Frontend | 60% | 50% | Istanbul (Vitest) |

## Tools

**Backend:** pytest 9.0.2, pytest-asyncio, pytest-cov, pytest-mock
**Frontend:** Frontend testing setup needs to be configured for Next.js (Vitest or Jest with next/jest transform). @testing-library/react and @testing-library/jest-dom are the intended assertion libraries once configured.
**E2E:** Playwright (`e2e/demo.py`) — smoke tests covering the full upload-simulate-playback workflow.

## Unit Test Areas

**Parser** (`tests/test_parser.py`): Valid RAPID -> correct AST, invalid syntax -> error with line number, edge cases, all instruction types. Min 20 test cases. ✅ Complete (PR #4).

**Kinematics** (`tests/test_kinematics.py`): FK (joint angles -> TCP pose), IK (TCP pose -> joint angles), joint limits, workspace boundaries, known poses from datasheet. ✅ 21 tests passing.

**Collision** (`tests/test_collision.py`): Mesh-to-mesh detection, no collision when separated, collision when overlapping, penetration depth, contact points. ✅ 13 tests passing.

**Trajectory** (`tests/test_trajectory.py`) — *Week 5-6, required before `/api/simulate`:*
- `test_movel_linear_interpolation`: verify waypoint count matches `ceil(distance / (speed * dt))` for v100/v500/v1000
- `test_movel_waypoints_on_line`: verify all MoveL waypoints lie on the straight-line path between start and end pose
- `test_movej_joint_space_interpolation`: verify joint angles lerp from start to target, not Cartesian straight-line
- `test_movec_circular_arc`: verify MoveC via-point lies on the arc and waypoints are arc-distance-spaced
- `test_speed_v100_timing`: v100 (100 mm/s) over 100mm path produces ~10 waypoints at 20ms timestep (distance/speed = 1s)
- `test_speed_v500_timing`: v500 (500 mm/s) over same path produces ~2 waypoints
- `test_timestamps_ascending`: all waypoint timestamps strictly ascending, starting at 0.0
- `test_joints_within_limits`: all joint values stay within URDF joint limits for all waypoints

**Frontend Components** (`frontend/src/components/*.test.tsx`): Robot selector, upload buttons, playback controls, timeline scrubber, collision alerts, loading spinner.
> **Note:** Frontend tests require a working Next.js-compatible test runner setup before component tests can run. `PlaybackControls` and `RapidPanel` tests should be written once the test infrastructure is configured.

## Integration Tests

Full workflow: health check -> list robots -> upload RAPID -> upload obstacle -> simulate -> verify trajectory. Error paths: invalid files (400), invalid robot ID (404), malformed JSON (422), IK failure (500).

**`/api/simulate` Integration Tests** (`tests/test_simulate.py`) — *Week 6, required for MVP:*
- `test_upload_and_simulate_basic`: upload a valid RAPID file → `POST /api/simulate` → assert response has non-empty `trajectory` array
- `test_trajectory_timestamps_ascending`: all `waypoint.timestamp` values are strictly ascending
- `test_trajectory_joints_within_limits`: every `waypoint.joints` array has values within IRB 4600 joint limits
- `test_simulate_timeout`: trajectory generation exceeding 5s returns 408 response
- `test_simulate_invalid_rapid`: malformed RAPID input returns 422 with descriptive error
- `test_simulate_out_of_reach`: target pose outside workspace returns 500 with IK failure message

## UAT (Week 7-8)

10+ real RAPID programs from RobotStudio. Visual validation: smooth animation, collision highlighting, correct joint values. Cross-browser: Chrome, Firefox, Edge. Performance: <5s simulation, no dropped frames.

## Test Data

**RAPID programs** (`tests/fixtures/rapid/`): simple_movel.mod, simple_movej.mod, circular_arc.mod, pick_and_place.mod, complex_program.mod, invalid_syntax.mod, out_of_reach.mod

**STL obstacles** (`tests/fixtures/stl/`): cube.stl, table.stl, complex_mesh.stl

## CI/CD

GitHub Actions on push/PR: backend (`pytest --cov`), frontend (`pnpm test --coverage`). Codecov integration.

## Test Responsibilities

| Person | Responsibilities |
|--------|-----------------|
| **Noah** | CI setup, regression suite, UAT, test data, coverage monitoring |
| **Jason** | Parser tests, trajectory tests, API integration tests |
| **Dylane** | Viewport component tests (mocked) |
| **Umaya** | UI component tests (React Testing Library) |

---

**Last Updated:** 2026-03-28

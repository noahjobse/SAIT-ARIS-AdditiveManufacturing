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
**Frontend:** Vitest 4.0.17, @testing-library/react, @testing-library/jest-dom, jsdom

## Unit Test Areas

**Parser** (`tests/test_parser.py`): Valid RAPID -> correct AST, invalid syntax -> error with line number, edge cases, all instruction types. Min 20 test cases.

**Kinematics** (`tests/test_kinematics.py`): FK (joint angles -> TCP pose), IK (TCP pose -> joint angles), joint limits, workspace boundaries, known poses from datasheet.

**Collision** (`tests/test_collision.py`): Mesh-to-mesh detection, no collision when separated, collision when overlapping, penetration depth, contact points.

**Trajectory** (`tests/test_trajectory.py`): MoveL linear interpolation, MoveJ joint-space, MoveC circular arc, SpeedData/ZoneData effects, timestamps.

**Frontend Components** (`src/components/*.test.tsx`): Robot selector, upload buttons, playback controls, timeline scrubber, collision alerts, loading spinner.

## Integration Tests

Full workflow: health check -> list robots -> upload RAPID -> upload obstacle -> simulate -> verify trajectory. Error paths: invalid files (400), invalid robot ID (404), malformed JSON (422), IK failure (500).

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

**Last Updated:** 2026-02-12

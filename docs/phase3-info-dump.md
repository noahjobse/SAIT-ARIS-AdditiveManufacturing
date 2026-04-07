# Phase 3 Report — Information Dump

Use this to draft your final report. All sections correspond to the report template.

---

## General Information

- **Team Members:** Noah Jobse, Jason, Umaya, Dylane
- **Date:** March 25, 2026
- **Git Repository Link:** https://github.com/noahjobse/SAIT-ARIS-AdditiveManufacturing

---

## Part A: Object-Oriented Design Principles

### Principles Used

**1. Single Responsibility Principle (SRP)**
Each class has exactly one reason to change. Examples:
- `KinematicsSolver` (backend/app/kinematics/solver.py) — exclusively handles forward/inverse kinematics calculations
- `CollisionDetector` (backend/app/collision/detector.py) — solely responsible for mesh-to-mesh collision checking
- `RapidTransformer` (backend/app/parser/transformer.py) — only transforms Lark parse trees into domain AST objects
- `TrajectoryGenerator` (backend/app/trajectory/generator.py) — converts motion commands into trajectory waypoints
- AST node dataclasses (backend/app/parser/ast_nodes.py) — each represents a single RAPID concept: `Position`, `Orientation`, `RobTarget`, `JointTarget`, `ToolData`, `MoveCommand`, `Procedure`, `Module`, `Program`
- Frontend: `Viewport3D` only manages the Babylon.js canvas; `createRobotScene()` only builds the 3D scene; separate functions for camera, lighting, ground grid, and joint computation

**2. Open/Closed Principle (OCP)**
Classes are open for extension but closed for modification:
- `RapidTransformer` uses a visitor/transformer pattern — new RAPID command types (e.g., MoveC, MoveAbsJ) are added as new methods without modifying existing handlers
- `TrajectoryGenerator._process_command()` dispatches to specific interpolation methods (`_move_l()`, `_move_j()`, `_move_c()`) — new motion types are added as new methods
- FastAPI routers — new endpoints are added in new router files without touching existing ones (e.g., `routers/simulate.py`, `routers/upload.py`, `routers/obstacles.py`, `routers/parse.py`, `routers/kinematics.py`)

**3. Liskov Substitution Principle (LSP)**
Subtypes are substitutable for their base types:
- Exception hierarchy: `KinematicsError` (base) → `RobotNotLoadedError`, `IKSolutionNotFoundError`, `InvalidJointAnglesError` — all can be caught by the parent type in router exception handlers
- Target types: `RobTarget` (Cartesian) and `JointTarget` (joint-space) both satisfy the `target` contract in `MoveCommand`, enabling polymorphic target handling in the simulation pipeline

**4. Interface Segregation Principle (ISP)**
Clients only depend on interfaces they use:
- Frontend `JointControls` interface exposes only `setJointAngle()` and `dispose()` — hides the full Babylon.js Engine/Scene internals
- `Viewport3DProps` accepts only `modelPath` and `onJointControlsReady` — doesn't leak unused props
- Pydantic schemas (backend/app/schemas/) define focused request/response models per endpoint rather than one monolithic API object

**5. Dependency Inversion Principle (DIP)**
High-level modules depend on abstractions, not concrete implementations:
- `TrajectoryGenerator` receives `KinematicsSolver` via constructor injection — doesn't instantiate its own solver
- `CollisionDetector` accepts an optional `RobotLoader` dependency — creates a default if not provided
- `get_solver()` factory function in kinematics router decouples endpoint handlers from solver instantiation
- Frontend components receive dependencies via React props (dependency injection pattern)

**6. Encapsulation**
Internal state is protected with controlled access:
- `KinematicsSolver`: private `_ik_cache`, `_movable_joints`, `_ee_link_index` with public methods for FK/IK
- `RobotLoader`: private `_movable_joints`, `_ee_link_index` dicts with getter methods like `get_movable_joint_indices()`
- `ObstacleRegistry`: private `_obstacles` dict with `register()`, `get()`, `list_all()`, `delete()` methods
- `TrajectoryGenerator`: private helpers `_resolve_target()`, `_parse_speed()`, `_apply_tool_offset()`
- Frontend `Viewport3D`: internal state (`controlsRef`, `loading`, `error`) hidden from parent components

**7. Composition over Inheritance**
Objects are built by composing dependencies rather than inheriting:
- `TrajectoryGenerator` composes `KinematicsSolver` (injected via constructor)
- `CollisionDetector` composes `RobotLoader`
- `RapidParser` composes `Lark` parser engine and `RapidTransformer`
- Simulation pipeline in `simulate.py` composes solver → generator → detector
- React components compose via props and children, not class inheritance

### Design Patterns Identified

| Pattern | Location | Purpose |
|---------|----------|---------|
| Strategy | `TrajectoryGenerator` — `_move_l()`, `_move_j()`, `_move_c()` | Different motion interpolation algorithms |
| Factory | `get_solver()` in kinematics router; `createRobotScene()` in frontend | Decoupled object creation |
| Adapter | `_build_robtarget()`, `_build_jointtarget()` in simulate.py | Convert JSON dicts to domain dataclasses |
| Template Method | `TrajectoryGenerator.generate()` — resolve → process → output | Fixed pipeline with pluggable steps |
| Visitor/Transformer | `RapidTransformer(Transformer)` | Walk parse tree, build AST nodes |

### How Principles Improve Scalability & Maintainability

- **Scalability:** The parser's open/closed design means adding new RAPID instructions (e.g., new motion types, I/O commands) requires only a new grammar rule and transformer method — existing code is untouched. The router-per-domain pattern means new API features are isolated files.
- **Maintainability:** SRP ensures that a bug in collision detection doesn't require understanding the parser. Encapsulation means internal caching strategies (e.g., IK LRU cache) can change without affecting callers. Composition via injection means each class can be unit-tested in isolation with mock dependencies.
- **Extensibility:** The contract-based frontend/backend separation (OpenAPI spec) means the backend could be rewritten in C# without changing the frontend — a real consideration for this project's future.

---

## Part B: Class Collaborations and Hierarchies

### Key Class Relationships

**Inheritance:**
- `RapidTransformer` → extends Lark's `Transformer` base class (framework inheritance for parse tree walking)
- `KinematicsError` → `RobotNotLoadedError`, `IKSolutionNotFoundError`, `InvalidJointAnglesError` (exception hierarchy)
- All Pydantic schemas → extend `BaseModel` (framework inheritance for validation)

**Composition:**
- `TrajectoryGenerator` *has-a* `KinematicsSolver` (injected via constructor)
- `CollisionDetector` *has-a* `RobotLoader` (injected or created internally)
- `RapidParser` *has-a* `Lark` parser + `RapidTransformer`
- `KinematicsSolver` *has-a* PyBullet physics client (encapsulated)
- Simulation router composes all three: solver, generator, detector

**Aggregation:**
- `Program` *has-many* `Procedure`s, which *have-many* `MoveCommand`s
- `MoveCommand` *has-a* target (`RobTarget` or `JointTarget`)
- `RobTarget` *has-a* `Position` + `Orientation`
- `Module` *has-many* declarations (`RobTarget`, `JointTarget`, `ToolData`)
- `ObstacleRegistry` *has-many* `ObstacleRecord`s

### Collaborations Summary

**Simulation Pipeline (main collaboration chain):**
```
User uploads RAPID code
    → RapidParser.parse(code) → uses Lark + RapidTransformer
        → Returns Program (AST with Procedures + MoveCommands)
    → TrajectoryGenerator.generate(program) → uses KinematicsSolver for FK/IK
        → Returns list of TrajectoryWaypoints
    → CollisionDetector.check(waypoints) → uses RobotLoader + PyBullet
        → Returns collision results
    → SimulateResponse assembled and sent to frontend
```

**Frontend Collaboration:**
```
Home (page) → composes Viewport3D + control panels
    → Viewport3D → calls createRobotScene() factory
        → createRobotScene → calls createEngineAndScene(), createCameraAndLight(), createGroundGrid(), buildJoints()
        → Returns JointControls interface to parent
    → Home receives JointControls → passes to joint jog/playback panels
```

**How classes improve modularity:**
- Each subsystem (parser, kinematics, collision, trajectory) is a self-contained module with its own router, schemas, and domain objects
- The simulation router orchestrates them without any subsystem knowing about the others
- Frontend components communicate through props and callbacks — no direct cross-component dependencies
- The OpenAPI contract decouples frontend from backend entirely — either side can be replaced independently

---

## Part C: UML Diagrams — Description Guide

### Class Diagram — What to Include

**Backend Core Classes:**

1. **`RapidParser`**
   - Attributes: `_lark_parser: Lark`, `_transformer: RapidTransformer`
   - Methods: `parse(code: str) → Program`

2. **`RapidTransformer`** (extends `Transformer`)
   - Methods: `position()`, `orientation()`, `robtarget()`, `jointtarget()`, `move_l()`, `move_j()`, `move_c()`, `procedure()`, `program()`

3. **`KinematicsSolver`**
   - Attributes: `_physics_client`, `_robot_id`, `_ik_cache: dict`, `_movable_joints: list`, `_ee_link_index: int`
   - Methods: `forward_kinematics(joint_angles) → (pos, orient)`, `inverse_kinematics(pos, orient) → joint_angles`, `load_robot(urdf_path)`

4. **`TrajectoryGenerator`**
   - Attributes: `solver: KinematicsSolver`, `variable_table: dict`
   - Methods: `generate(program) → list[Waypoint]`, `_process_command()`, `_move_l()`, `_move_j()`, `_move_c()`, `_resolve_target()`, `_apply_tool_offset()`

5. **`CollisionDetector`**
   - Attributes: `_loader: RobotLoader`, `obstacles: dict`
   - Methods: `check_collisions(joint_angles) → list[Collision]`, `add_obstacle()`, `remove_obstacle()`

6. **`RobotLoader`**
   - Attributes: `_movable_joints: dict`, `_ee_link_index: dict`
   - Methods: `load_robot(urdf_path) → robot_id`, `get_movable_joint_indices(robot_id) → list`

7. **AST Node Dataclasses** (group these):
   - `Position(x, y, z)`, `Orientation(q1, q2, q3, q4)`, `RobTarget(pos, orient, ...)`, `JointTarget(angles)`, `ToolData(robhold, tframe, ...)`, `MoveCommand(type, target, speed, zone, tool)`, `Procedure(name, commands)`, `Program(procedures, declarations)`

8. **Exception Hierarchy:**
   - `KinematicsError` → `RobotNotLoadedError`, `IKSolutionNotFoundError`, `InvalidJointAnglesError`

**Relationships to draw:**
- `RapidParser` ──comp──▶ `Lark`, `RapidTransformer`
- `RapidTransformer` ──extends──▶ `Transformer` (Lark)
- `TrajectoryGenerator` ──comp──▶ `KinematicsSolver`
- `CollisionDetector` ──comp──▶ `RobotLoader`
- `Program` ──aggr──▶ `Procedure` ──aggr──▶ `MoveCommand`
- `MoveCommand` ──assoc──▶ `RobTarget` | `JointTarget`
- `RobTarget` ──comp──▶ `Position`, `Orientation`
- `KinematicsError` ◁── `RobotNotLoadedError`, `IKSolutionNotFoundError`, `InvalidJointAnglesError`

**Frontend Classes (optional):**
- `Viewport3D` component ──uses──▶ `createRobotScene()` ──returns──▶ `JointControls`

---

### Use Case Diagram — What to Include

**Actor:** Student (primary user)

**Use Cases:**
1. Upload RAPID Code — student uploads .mod file or pastes code
2. Parse RAPID Code — system parses code into AST
3. Run Simulation — system generates trajectory + checks collisions
4. View 3D Animation — student watches robot movement in Babylon.js viewport
5. Control Playback — play, pause, stop, speed control, step-through
6. Jog Robot Joints — manually adjust individual joint angles via sliders
7. Upload Obstacle — upload STL/OBJ file as obstacle in scene
8. Manage Obstacles — add, remove, reposition obstacles
9. View Collision Results — see highlighted collision points
10. Select Robot Model — choose between IRB 4600, 2600, 6700

**System Boundary:** ABB Online Simulation Platform

**Relationships:**
- "Run Simulation" «includes» "Parse RAPID Code"
- "Run Simulation" «includes» "View 3D Animation"
- "View 3D Animation" «extends» "Control Playback"
- "Upload Obstacle" «extends» "Manage Obstacles"

---

## Part D: OOD Impact Evaluation

### Maintainability & Scalability Analysis

**Encapsulation improved maintenance:** The `KinematicsSolver` encapsulates PyBullet's physics engine behind a clean FK/IK interface. When we optimized IK performance by adding an LRU cache (`_ik_cache`), no code outside the solver needed to change. The caching strategy is an internal implementation detail — callers just see the same `inverse_kinematics()` method.

**SRP reduced debugging scope:** When trajectory generation had issues, debugging was confined to `TrajectoryGenerator` alone. The parser, solver, and collision detector were known-good because they were independently tested. Each module has its own test suite, and failures point directly to the responsible class.

**Composition enabled independent development:** Because `TrajectoryGenerator` receives `KinematicsSolver` via injection rather than creating it internally, team members could work on kinematics and trajectory generation in parallel. Unit tests for the generator used mock solvers, so kinematics bugs didn't block trajectory work.

**Open/Closed design simplified feature additions:** Adding new RAPID instructions (MoveC for circular motion, MoveAbsJ for absolute joint moves, ToolData for TCP offsets) required only new grammar rules and new transformer methods. Existing MoveL and MoveJ handling was untouched, eliminating regression risk.

**Contract-based separation future-proofs the system:** The frontend and backend communicate through a well-defined OpenAPI contract. This means the Python/PyBullet backend could be rewritten in an industry-standard language like C# without any frontend changes — a realistic scenario for this project's future adoption.

### Trade-offs and Challenges

**Speed vs. hardware requirements:** Our backend processes RAPID code through a full pipeline (parse → AST → trajectory generation → collision detection) on every simulation request. This is computationally heavier than a simpler approach, but it means the simulation runs on standard hardware without requiring a dedicated robot controller or specialized software. We traded execution speed for accessibility — any student with a browser can run simulations.

**Learning curve vs. long-term maintainability:** The layered architecture with dependency injection and composition patterns was harder to learn initially. Team members needed to understand how the pipeline flows through parser → generator → detector before they could make changes confidently. However, once understood, the separation made it significantly easier to add features without breaking existing functionality.

**Abstraction overhead:** Wrapping PyBullet behind domain-specific interfaces adds indirection. A developer must trace through `KinematicsSolver` → PyBullet calls to debug physics issues. This is the classic abstraction trade-off: cleaner API at the cost of an extra layer to navigate during debugging.

---

## Part E: Shell Scripts

### Scripts
1. **`start.sh`** — Checks prerequisites (Python 3.11+, Node 20+, pnpm), auto-installs dependencies on first run, then runs backend (FastAPI) and frontend (Next.js) concurrently with color-coded output and graceful shutdown. Supports `--check` flag for prereq validation only.
2. **`demo.sh`** — Launches Docker environment and runs Playwright e2e demo
3. **`scripts/deploy.sh`** — Preview and production deployment automation (Docker build, lint, test, smoke test)
4. **`scripts/seed-scenarios.sh`** — Seeds test scenarios by uploading sample RAPID programs to the running backend API

---

## Part F: Peer Feedback (Noah Jobse)

### Team Dynamics
Our team worked well together throughout the project. Communication was consistent and collaborative — we supported each other when blockers came up and maintained a positive working relationship. Roles emerged naturally based on each person's strengths and interests, and everyone was willing to step outside their comfort zone when needed.

### Division of Responsibilities
The division of work was roughly fair across the team:
- **Noah** — Backend development (FastAPI, kinematics, trajectory generation, collision detection), DevOps (Docker, CI/CD), project management, and infrastructure (Supabase, deployment)
- **Jason** — RAPID parser development (Lark grammar, AST transformer), frontend component migration to Next.js, CodeMirror editor, Docker production setup, and documentation
- **Umaya** — Frontend component porting (PlaybackControls, JointJogPanel, StatusPanel), API integration, execution UX (error banners, progress indicators), and UI polish
- **Dylane** — 3D visualization (Babylon.js scene, robot model loading, animation), obstacle management in scene, playback improvements, and capstone deliverables (poster, demo video)

Some members naturally took on more work than others, but the team was happy with the overall balance. Tasks were divided based on strengths — those comfortable with backend systems handled backend work, and those with frontend experience handled UI components.

### Challenges
- **Coordination and division of labour** was our biggest challenge. With four people working on interconnected systems (parser → backend → frontend → 3D), we needed clear boundaries and communication about what was ready and what was still in progress.
- **Steep learning curve** — technologies like PyBullet, Babylon.js, Lark parsing, and the RAPID language were new to most of the team. The initial ramp-up was slow, but once each person got comfortable with their domain, productivity increased significantly.
- We addressed these challenges through regular check-ins and by establishing clear API contracts between frontend and backend, so work could proceed in parallel even when dependencies weren't fully complete.

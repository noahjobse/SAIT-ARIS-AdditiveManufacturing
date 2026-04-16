# ArmStudio — Phase 4 Final Presentation
**Gamma Import Document**
Use this file as the source for your Gamma slide deck.
Each `---` is a slide break. Speaker notes follow each slide under **[NOTES]**.

---

# ArmStudio
### Browser-Based ABB Robot Trajectory Simulator

**Team:** Noah Jobse · Jason · Umaya · Dylane
**Course:** SAIT Research Applications
**Date:** April 23, 2026
**GitHub:** github.com/noahjobse/SAIT-ARIS-AdditiveManufacturing

[IMAGE: ArmStudio logo centered on a dark background — use /frontend/public/ArmStudio-Logo.png]

**[NOTES — Noah]**
Welcome. I'm Noah. Our team built ArmStudio — a browser-based simulator for ABB industrial robots. Over four phases we went from a blank canvas to a multithreaded production backend. I'll walk through the problem we solved and our roadmap, then hand off to Jason for the backend.

---

## The Problem We Solved

> ABB industrial robots cost **$80,000+** and require proprietary software to program.

**Students can't practice** without:
- Physical robot hardware
- RobotStudio licence (~$3,000/year)
- Dedicated lab access

**Our solution:** Any student, any browser, zero setup.

- Upload RAPID code → watch the robot simulate in real-time 3D
- Collision detection, trajectory playback, joint jogging
- Supports IRB 4600, IRB 2600, IRB 6700

[IMAGE: Split image — left: photo of a real ABB IRB 4600 arm in a factory; right: ArmStudio viewport screenshot showing the 3D robot in the browser]

**[NOTES — Noah]**
ABB's RAPID language is industry-standard — it's what engineers actually program these robots with. The gap we're filling is between learning RAPID and having access to a real robot. Our platform closes that gap completely.

---

## Four Phases — Project Timeline

| Phase | Weeks | What We Built | Status |
|-------|-------|---------------|--------|
| **1 — Visualization** | 1–3 | 3D scene, robot loading, obstacles, gizmo | ✅ Done |
| **2 — Logic Engine** | 4–6 | RAPID parser, IK/FK kinematics, simulation pipeline | ✅ Done |
| **3 — Migration** | 7 | Next.js App Router, TCP demo, FDM printing pipeline | ✅ Done |
| **4 — Multithreading** | 8–9 | ThreadPoolExecutor, asyncio.Lock, thread-safe data structures | ✅ Done |

[IMAGE: Horizontal timeline graphic with 4 milestones, checkmarks on all four, coloured left-to-right in a gradient (e.g. blue → purple)]

**[NOTES — Noah]**
Each phase built on the previous one. Phase 1 gave us the visual foundation. Phase 2 made it functional. Phase 3 made it production-grade. Phase 4 made it concurrent and safe under load. I'll now hand off to Jason who owns the backend.

---

## Backend Architecture
*Jason*

```
RAPID Code (.mod file)
        ↓
  RapidParser (Lark grammar → AST)
        ↓
  TrajectoryGenerator (IK-backed waypoints)
        ↓
  CollisionDetector (mesh-to-mesh via PyBullet)
        ↓
  JSON Response → Frontend Babylon.js
```

**Stack:** FastAPI · PyBullet · Lark · NumPy/SciPy · Pydantic · Pytest

**7 REST routers:** `/api/simulate` · `/api/parse` · `/api/kinematics` · `/api/robots` · `/api/obstacles` · `/api/upload` · `/api/printing`

[IMAGE: Architecture diagram — vertical pipeline with labelled boxes connected by arrows, matching the text above. Use a dark background with white text and colour-coded boxes per module]

**[NOTES — Jason]**
The backend is a FastAPI application with seven routers. Each router owns one domain — they don't know about each other. The simulate router is the orchestrator: it calls the parser, passes the AST to the trajectory generator, and feeds waypoints to the collision detector.

---

## RAPID Parser — Phase 2
*Jason*

ABB's RAPID language parsed with **Lark** (PEG grammar):

```python
# grammar.lark — MoveL/MoveJ/MoveC/MoveAbsJ
move_stmt: "MoveL" target "," speed "," zone "," tool ";"
         | "MoveJ" target "," speed "," zone "," tool ";"
         | "MoveC" via_target "," target "," speed "," zone "," tool ";"
```

**RapidTransformer** (Open/Closed Principle — new commands = new methods, zero existing edits):

```python
class RapidTransformer(Transformer):
    def move_l(self, items):
        return MoveCommand(command_type="MoveL", target=items[0],
                           speed=items[1], zone=items[2], tool=items[3])
    def move_j(self, items):
        return MoveCommand(command_type="MoveJ", ...)
    def move_c(self, items):
        return MoveCommand(command_type="MoveC", circular_point=items[0], ...)
```

**AST Node chain:** `Program → Module → Procedure → MoveCommand → RobTarget → Position + Orientation`

**IF/ELSE, FOR, WHILE** control flow supported (Phase 3 stretch goal ✅)

**[NOTES — Jason]**
The parser turns raw RAPID text into a structured Python AST. The Open/Closed Principle means we added MoveC, MoveAbsJ, IF/ELSE, and FOR/WHILE without touching the existing MoveL/MoveJ handlers — each new instruction is a new method.

---

## Kinematics + Simulation Pipeline
*Jason*

**PyBullet** physics engine (headless, no GUI):

```python
class KinematicsSolver:
    # FK: joint angles (radians) → TCP position + orientation
    def forward_kinematics(self, robot_id, joint_angles) -> dict

    # IK: target pose → joint angles (LRU cache, 1000 entries)
    def inverse_kinematics(self, robot_id, target_position, target_orientation) -> dict
```

**3 Robot URDFs:** IRB 4600 (2.05 m reach) · IRB 2600 · IRB 6700
**TrajectoryGenerator** composes KinematicsSolver (Dependency Inversion Principle):
- `MoveL` → linear Cartesian interpolation
- `MoveJ` → joint-space interpolation
- `MoveC` → circular arc (via-point)

**CollisionDetector** — mesh-to-mesh via PyBullet:
- Loads STL/OBJ obstacles dynamically
- Checks every waypoint against all obstacles
- Returns penetration depth + contact point

**Test coverage: 86 tests passing (34 kinematics + collision + 10 concurrency + 4 benchmarks + integration)**

[IMAGE: UML class diagram showing: KinematicsSolver ←composes— TrajectoryGenerator ←composes— CollisionDetector, with KinematicsError hierarchy (RobotNotLoadedError, IKSolutionNotFoundError, InvalidJointAnglesError) below. Include RobotLoader as a dependency of both KinematicsSolver and CollisionDetector]

**[NOTES — Jason]**
The IK solver uses an LRU cache with 1000 entries and 0.1mm position rounding as the cache key. This means repeated simulations with the same waypoints skip PyBullet entirely. The collision detector loads obstacle meshes into PyBullet's physics world and uses contact point queries — not bounding boxes.

---

## Phase 4 — Multithreading Architecture
*Jason*

**The problem:** PyBullet is single-client. Multiple concurrent requests would corrupt the physics simulation.

**Our solution:** `ThreadPoolExecutor` + `asyncio.Lock`

```python
# thread_pool.py — single shared module, avoids circular imports
MAX_WORKERS = int(os.environ.get("PYBULLET_THREADS", "4"))
executor: ThreadPoolExecutor | None = None
pybullet_lock: asyncio.Lock = asyncio.Lock()  # serializes ALL PyBullet calls
```

**Lifespan management** — pool created at startup, cleanly shut down:

```python
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    thread_pool.executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
    yield
    thread_pool.executor.shutdown(wait=True)  # drain in-flight work
```

**Request pattern** — async handler offloads CPU work to the pool:

```python
@router.post("/api/simulate")
async def simulate(request: SimulateRequest):
    loop = asyncio.get_event_loop()
    async with pybullet_lock:               # wait — yield to event loop
        result = await loop.run_in_executor(
            executor,
            functools.partial(_run_simulation_sync, request, start_ms)
        )
    return result
```

[IMAGE: Flow diagram — "FastAPI async handler" → "acquires pybullet_lock (asyncio.Lock)" → "run_in_executor → thread pool worker" → "PyBullet physics call" → "returns JSON". Show concurrent requests queuing at the lock, with health check endpoints bypassing the lock entirely]

**[NOTES — Jason]**
The key insight is that `asyncio.Lock` doesn't block the event loop — it yields to it. So while one simulation is running, health checks and metadata endpoints are still responsive. The lock is only held for CPU-bound PyBullet work, not for JSON serialization or network I/O.

---

## Thread Safety Mechanisms
*Jason*

Three lock types, each chosen for its access pattern:

| Component | Lock Type | Why |
|-----------|-----------|-----|
| `KinematicsSolver._ik_cache` | `threading.Lock` | Simple dict, short critical section, not held during IK solve |
| `ObstacleRegistry._obstacles` | `threading.RLock` | Reentrant — `delete()` calls `get()` internally |
| PyBullet physics client | `asyncio.Lock` | Async-safe, yields to event loop while waiting |

**Fine-grained locking on the IK cache:**

```python
# Lock only for cache lookup/store — NOT during the actual IK solve
with self._cache_lock:
    if cache_key in self._ik_cache:
        return {"joint_angles": list(self._ik_cache[cache_key])}

# ← IK solve happens here, OUTSIDE the lock (PyBullet call)
joint_angles = p.calculateInverseKinematics(...)

with self._cache_lock:
    self._ik_cache[cache_key] = result   # store result
    if len(self._ik_cache) > IK_CACHE_MAX:
        self._ik_cache.popitem(last=False)  # evict LRU entry
```

**ObstacleRegistry RLock:**

```python
class ObstacleRegistry:
    def __init__(self):
        self._lock = threading.RLock()   # reentrant

    def delete(self, obstacle_id):
        with self._lock:
            record = self._obstacles.pop(obstacle_id, None)
        # File I/O outside lock — never hold locks over I/O
        if os.path.exists(record.file_path):
            os.remove(record.file_path)
```

**Verification:** `test_concurrency.py` — 10 tests · 10 threads each · race condition detection
**Benchmarks:** `test_benchmark.py` — cache hit vs miss, IK throughput, event loop responsiveness

**[NOTES — Jason]**
The most important design decision here was NOT holding the cache lock during the actual IK solve. The IK call can take 50–200ms. Holding the lock that long would serialize all concurrent requests. By releasing the lock, doing the work, then re-acquiring to store the result, we allow parallel IK solves. The only constraint is that two threads might solve the same position simultaneously — the second one just overwrites the cache entry, which is safe.

---

## Phase 1–3: 3D Visualization
*Umaya*

**Babylon.js** WebGL scene — runs entirely in the browser, no plugins:

- **3 robot models** loaded as `.glb` (rigged skeletons): IRB 4600, IRB 2600, IRB 6700
- **Starfield background** — SolidParticleSystem, 2000 particles
- **Obstacle management** — drag-and-drop STL upload, position/rotation gizmo
- **Joint jogging** — 6 sliders map directly to joint angles in real-time
- **Playback engine** — play, pause, stop, step-through, speed: 0.25×, 0.5×, 1×, 2×
- **Timeline scrubber** — seek to any waypoint

[IMAGE: Full-width screenshot of the ArmStudio 3D viewport — robot arm visible in the starfield scene, with the sidebar panel on the right showing joint sliders. Crop to show the viewport clearly]

[IMAGE: Close-up of the playback controls bar at the bottom — play/pause/stop buttons, speed selector, timeline scrubber]

**[NOTES — Umaya]**
The Babylon.js scene is initialized once and reused across all interactions — we never tear down and rebuild the engine. Babylon's SolidParticleSystem lets us render 2000 star particles as a single draw call, keeping the frame rate high. The transform gizmo is a built-in Babylon feature we wired to the obstacle registry.

---

## Frontend Architecture
*Umaya*

**Next.js 16 App Router** — file-system routing, server components where possible

```
frontend/src/
├── app/
│   ├── layout.tsx        ← root layout, fonts, global styles
│   ├── page.tsx          ← landing page (ArmStudio branding)
│   └── app/
│       └── page.tsx      ← main simulator (Viewport3D + panels)
└── components/
    ├── Viewport3D.tsx    ← Babylon.js canvas (SRP: only manages WebGL)
    ├── PlaybackControls  ← play/pause/stop/speed/scrubber
    ├── JointJogPanel     ← 6 joint sliders
    ├── StatusPanel       ← errors, collision results, parse output
    └── RapidPanel        ← RAPID code editor (CodeMirror)
```

**Type-safe API client** — `openapi-fetch` generated from `docs/contract/openapi.json`:

```typescript
// Every API call is type-checked at compile time
const { data, error } = await client.POST("/api/simulate", {
  body: { robot_id: "irb4600", program: parsedProgram }
})
// data is typed as SimulateResponse — no any, no casting
```

**OOP in the frontend:**
- `Viewport3D` — SRP: only manages the Babylon.js canvas; exposes `JointControls` interface
- `JointControls` — ISP: only `setJointAngle()` and `dispose()`, hides engine internals
- Components receive all dependencies via React props (Dependency Inversion)

[IMAGE: Annotated screenshot of the full ArmStudio UI — label each panel: Viewport (3D scene), Sidebar (robot selector, RAPID editor), Bottom bar (playback controls), Status panel (parse/simulation output)]

**[NOTES — Umaya]**
The OpenAPI contract is the contract between frontend and backend — it's committed at docs/contract/openapi.json. openapi-fetch generates TypeScript types from it, so if the backend changes a response shape, the frontend gets a compile error immediately. This prevented several integration bugs during development.

---

## DevOps + Shell Scripts
*Dylane*

**`start.sh`** — single command to run the entire project:

```bash
./start.sh          # auto-install deps, start backend + frontend
./start.sh --check  # validate prerequisites only
./start.sh --prod   # production mode (Gunicorn + uvicorn workers)
```

Features:
- Checks Python 3.11+, Node 20+, pnpm — fails fast with colour-coded output
- Auto-installs backend venv and frontend `node_modules` on first run
- Runs backend (port 8000) + frontend (port 3000) **concurrently** with colour-coded logs
- Graceful shutdown: `Ctrl+C` kills both processes cleanly

**`scripts/deploy.sh`** — Docker build → lint → test → smoke test → push
**`scripts/seed-scenarios.sh`** — seeds 5 sample RAPID programs via the API for demos
**`docker-compose.yml`** — one command for the full stack: `docker compose up`
**GitHub Actions CI** — runs on every PR: backend ruff lint + pytest, frontend ESLint + build

```yaml
# .github/workflows — parallel jobs
backend-lint:   ruff check . && ruff format --check .
backend-test:   pytest (86 tests)
frontend-lint:  pnpm lint
frontend-build: pnpm build
```

[IMAGE: Terminal screenshot showing `./start.sh` output — green checkmarks for Python and Node prereqs, then colour-coded backend and frontend log lines running side-by-side]

**[NOTES — Dylane]**
The start script was one of the highest-value pieces of infrastructure we built. Before it, every team member had a different setup procedure. After it, cloning the repo and running `./start.sh` gives you a working development environment in under 2 minutes. The --prod flag switches to Gunicorn with multiple uvicorn workers — the same command works in development and production.

---

## Live Demo
*Dylane*

[IMAGE: Large centered text "Live Demo" with the ArmStudio logo above it]

**What we'll show:**

1. **Select robot** — switch between IRB 4600, IRB 2600, IRB 6700
2. **Upload RAPID code** — paste or upload a `.mod` file with MoveL/MoveJ commands
3. **Run simulation** — watch the pipeline: parse → IK → trajectory → animation
4. **Collision detection** — add an STL obstacle, re-simulate, see collision highlights
5. **Playback controls** — scrub the timeline, change speed, step through waypoints

**[NOTES — Dylane]**
Open the browser at localhost:3000. Walk through each step slowly. For the collision demo, use one of the seed scenarios from seed-scenarios.sh — it places an obstacle in the robot's path deliberately.

---

## Future Roadmap

**Near-term (Summer 2026):**

- **C#/.NET backend migration** — OpenAPI contract already frozen at `docs/contract/openapi.json`. The frontend won't change — only the backend is swapped. PyBullet → BulletSharp or custom IK.
- **Supabase auth + Postgres** — per-user obstacle persistence, saved simulation history
- **Stripe SaaS tier** — subscription model, team accounts for schools

**Longer-term:**

- **Real ABB controller integration** — bridge to RobotStudio for hardware-in-loop testing
- **Vercel + Render cloud deployment** — Next.js on Vercel, FastAPI on Render (Docker container)
- **Multi-robot scenes** — simulate two arms working in the same workspace
- **RAPID editor with IntelliSense** — syntax highlighting, error squiggles, autocomplete

[IMAGE: Simple roadmap graphic — two columns "Near-term" and "Longer-term" with icons for each bullet point]

**[NOTES — Dylane]**
The C# migration is the most important future work. ABB's own tooling is C#-based, and having a .NET backend would make integration with their controller API much more straightforward. The OpenAPI contract we maintain means this swap is feasible without any frontend changes.

---

## Thank You

[IMAGE: ArmStudio logo centered, large]

**Team**
| Name | Role |
|------|------|
| Noah Jobse | Backend, DevOps, Kinematics, Project Lead |
| Jason | RAPID Parser, Frontend Migration, Docker |
| Umaya | Frontend Components, API Integration, UI Polish |
| Dylane | 3D Visualization, Babylon.js, Obstacle Management |

**GitHub:** github.com/noahjobse/SAIT-ARIS-AdditiveManufacturing
**86 tests passing · 4 phases complete · 1 semester**

*Questions?*

**[NOTES — Dylane]**
Thank the audience and open for questions. Likely questions: How does the IK solver handle singularities? (We use PyBullet's built-in damped least squares with joint limits.) How did you handle PyBullet's thread-unsafety? (asyncio.Lock + run_in_executor pattern.) What was the hardest part? (Coordinating the parser → kinematics → simulation pipeline across four people.)

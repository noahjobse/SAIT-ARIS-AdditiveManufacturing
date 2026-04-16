# Project: ArmStudio — Phase 4 Report

## General Information

- **Team Members:** Noah Jobse, Jason, Umaya, Dylane
- **Date:** April 17, 2026
- **Git Repository Link:** https://github.com/noahjobse/SAIT-ARIS-AdditiveManufacturing

---

## Part A: Finalize Your Application Development

### Overview

ArmStudio is a browser-based ABB industrial robot trajectory simulator that allows students to upload RAPID programs and visualize robot motion in real-time 3D — without requiring physical hardware or proprietary software.

The application's final state includes:

- **Full simulation pipeline:** RAPID code is parsed into an AST via a Lark grammar, passed to a trajectory generator that uses PyBullet for forward/inverse kinematics, checked for collisions against user-uploaded STL obstacles, and returned as timestamped waypoints that the Babylon.js frontend animates in real-time.
- **Three robot models:** IRB 4600, IRB 2600, and IRB 6700, each with validated URDF files and DH parameters.
- **Complete RAPID support:** MoveL (linear), MoveJ (joint-space), MoveC (circular arc), MoveAbsJ (absolute joint), plus IF/ELSE, FOR, WHILE control flow.
- **Frontend:** Next.js 16 App Router with Babylon.js 3D viewport, joint jog sliders, playback controls (play/pause/stop, 0.25×–2× speed, step-through), timeline scrubber, obstacle upload with transform gizmo, and collision highlighting.
- **Backend:** FastAPI with 7 REST routers (`/api/simulate`, `/api/parse`, `/api/kinematics/fk`, `/api/kinematics/ik`, `/api/robots`, `/api/obstacles`, `/api/upload`), Pydantic validation, and an OpenAPI contract at `docs/contract/openapi.json`.
- **Testing:** 86 tests passing (kinematics, collision, parser, concurrency, benchmarks, integration).
- **DevOps:** Docker Compose, Gunicorn production config, GitHub Actions CI, start/deploy/seed shell scripts.

### Key Multithreading Features

Phase 4 introduced multithreading to handle concurrent simulation requests safely and improve backend responsiveness under load. The key additions:

1. **ThreadPoolExecutor (automatic thread management)**
   A shared `ThreadPoolExecutor` is created at application startup via FastAPI's lifespan context manager and cleanly shut down on exit. It defaults to 4 worker threads (configurable via `PYBULLET_THREADS` environment variable). All CPU-bound work — IK/FK solving, trajectory generation, collision detection — is offloaded from the async event loop to the thread pool using `asyncio.get_event_loop().run_in_executor()`. This ensures the event loop remains responsive for health checks, metadata endpoints, and concurrent request handling.

   ```python
   # backend/app/main.py — lifespan manages the pool
   @contextlib.asynccontextmanager
   async def lifespan(app: FastAPI):
       thread_pool.executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
       yield
       thread_pool.executor.shutdown(wait=True)
   ```

2. **asyncio.Lock for PyBullet serialization**
   PyBullet's physics client is not thread-safe — concurrent calls corrupt the simulation state. A single `asyncio.Lock` (`pybullet_lock`) serializes all PyBullet access. Because it is an `asyncio.Lock` rather than a `threading.Lock`, waiting coroutines yield to the event loop instead of blocking it, so non-PyBullet endpoints (health checks, robot model metadata) remain responsive during simulation.

   ```python
   # backend/app/routers/simulate.py — request pattern
   async with pybullet_lock:
       result = await loop.run_in_executor(
           executor, functools.partial(_run_simulation_sync, request, start_ms)
       )
   ```

3. **Fine-grained data structure locks**
   Shared mutable data structures are protected by the narrowest possible lock type:
   - `threading.Lock` on `KinematicsSolver._ik_cache` — protects the LRU cache dict, but is NOT held during the actual IK solve (which can take 50–200ms), allowing parallel solves for different targets.
   - `threading.RLock` on `ObstacleRegistry._obstacles` — reentrant lock, chosen because `delete()` may internally call `get()`.
   - `threading.Lock` on `CollisionDetector.obstacles` dict — snapshot pattern: the dict is copied under the lock, then iteration happens outside it.
   - `threading.Lock` on the printing router's `_uploads` dict.

4. **Double-checked locking for lazy initialization**
   The kinematics router uses double-checked locking to lazily initialize the global `KinematicsSolver` instance. The first check is lock-free (fast path for the common case), and the second check inside the lock prevents duplicate initialization from concurrent first requests.

   ```python
   # backend/app/routers/kinematics.py
   _solver: KinematicsSolver = None
   _solver_lock = threading.Lock()

   def get_solver() -> KinematicsSolver:
       global _solver
       if _solver is None:
           with _solver_lock:
               if _solver is None:
                   _solver = KinematicsSolver(headless=True)
       return _solver
   ```

5. **Production deployment with Gunicorn**
   A `gunicorn.conf.py` configures multiple uvicorn worker processes (default 2, configurable via `WEB_WORKERS`). Each worker runs its own asyncio event loop and PyBullet physics client, providing process-level parallelism in addition to the per-worker thread pool. The `start.sh --prod` flag starts the application in Gunicorn mode.

---

## Part B: Ensure Thread Safety and Synchronization

### Thread Safety Strategies

Our application faces a core threading challenge: PyBullet's C-based physics engine is not thread-safe, yet our FastAPI backend is asynchronous and must handle multiple concurrent simulation requests. Our strategy was built on three principles:

1. **Minimize lock scope.** Locks are held for the shortest possible duration. Data structure locks protect only dict reads/writes, never expensive computations. The IK cache lock is released before calling `p.calculateInverseKinematics()` (which can take 50–200ms) and re-acquired only to store the result.

2. **Choose the right lock type for the access pattern.** We use three different lock types:
   - `asyncio.Lock` — for the PyBullet physics client, because the calling code is async and we want to yield to the event loop rather than block it.
   - `threading.Lock` — for simple shared dicts (`_ik_cache`, `obstacles`, `_uploads`) where only one level of locking is needed.
   - `threading.RLock` — for `ObstacleRegistry`, where the `delete()` method may internally call `get()`, both of which acquire the lock. A non-reentrant lock would deadlock here.

3. **Avoid holding locks during I/O.** `ObstacleRegistry.delete()` releases the lock before calling `os.remove()` on the obstacle file. The collision detector takes a snapshot of the obstacles dict under the lock, then iterates the snapshot outside it. This prevents lock contention during expensive I/O or PyBullet calls.

### Synchronization Techniques

| Mechanism | Location | Protects | Why This Type |
|-----------|----------|----------|---------------|
| `asyncio.Lock` | `thread_pool.pybullet_lock` | PyBullet physics client | Async-safe; yields to event loop while waiting |
| `threading.Lock` | `KinematicsSolver._cache_lock` | `_ik_cache` OrderedDict | Simple mutex; short critical section |
| `threading.Lock` | `CollisionDetector._obstacles_lock` | `obstacles` dict | Snapshot pattern; copy under lock, iterate outside |
| `threading.RLock` | `ObstacleRegistry._lock` | `_obstacles` dict | Reentrant; `delete()` calls `get()` internally |
| `threading.Lock` | `printing._uploads_lock` | `_uploads` dict | Simple mutex; protects concurrent file uploads |
| `threading.Lock` | `kinematics._solver_lock` | Solver initialization | Double-checked locking; only used once at startup |
| `ThreadPoolExecutor` | `thread_pool.executor` | CPU-bound work dispatch | Managed pool; created at startup, drained at shutdown |

**Condition-like pattern:** The `asyncio.Lock` on PyBullet access acts like a condition variable — when a coroutine cannot acquire the lock, it suspends and yields to the event loop. The event loop continues serving other requests (health checks, metadata). When the lock is released, the next waiting coroutine is awakened. This is not a traditional `threading.Condition`, but it achieves the same effect within the async paradigm.

**Snapshot pattern (avoiding iteration-under-lock):**

```python
# backend/app/collision/detector.py — line 131
with self._obstacles_lock:
    obstacle_snapshot = dict(self.obstacles)  # copy under lock

# Iterate outside lock — PyBullet calls can take 10ms+ each
for obstacle_id, obstacle_body_id in obstacle_snapshot.items():
    contacts = p.getClosestPoints(...)  # expensive, no lock held
```

### Challenges and Solutions

**Challenge 1: PyBullet's single-client limitation.**
PyBullet's `DIRECT` mode physics client crashes or returns garbage when accessed from multiple threads simultaneously. We initially attempted to use a `threading.Lock`, which blocked the event loop during simulation. The fix was switching to `asyncio.Lock`, which yields to the event loop while waiting. Concurrent health checks now respond in <1ms even while a 5-second simulation is running.

**Challenge 2: IK cache corruption under concurrent access.**
Without locking, concurrent IK requests could see partially-written cache entries or exceed the maximum cache size (race between `len()` check and `popitem()`). We solved this with a `threading.Lock` on the cache dict, but critically, we do NOT hold the lock during the actual IK solve — only during cache lookup and storage. This means two threads solving the same position simultaneously may both compute the result, but the second write is idempotent (same value), so this is safe.

**Challenge 3: ObstacleRegistry reentrant access.**
The `delete()` method needs to look up the obstacle record (to get the file path) and then remove it from the dict. Initially both operations were separate calls, which meant `delete()` acquired the lock twice — deadlocking on a `threading.Lock`. Switching to `threading.RLock` (reentrant lock) solved this. We also moved the `os.remove()` file I/O outside the lock scope to avoid holding the lock during disk operations.

**Challenge 4: Graceful shutdown.**
The `ThreadPoolExecutor` must drain in-flight work before the application exits, otherwise active simulations would be interrupted mid-computation. We use `executor.shutdown(wait=True)` in the lifespan manager's shutdown phase, which blocks until all submitted tasks complete. The Gunicorn config also sets `graceful_timeout = 30` to allow workers time to finish before being killed.

---

## Part C: Describe Performance Optimization

### Performance Improvements

Multithreading improved three measurable aspects of system performance:

**1. Event loop responsiveness (non-blocking I/O)**
Before multithreading, CPU-bound PyBullet calls (IK solving, collision detection) ran directly in the async event loop. A single simulation request taking 3–5 seconds blocked ALL other requests — including health checks and robot model metadata queries. After offloading to `run_in_executor`, the event loop remains free to serve lightweight requests concurrently.

| Metric | Before (blocking) | After (thread pool) |
|--------|-------------------|---------------------|
| Health check during simulation | 3–5s (blocked) | <1ms (immediate) |
| Concurrent metadata requests | Serialized behind simulation | Served immediately |
| Event loop responsiveness | Blocked during IK solve | 100ms async sleep returns in 100.2ms |

**2. IK cache performance (200× speedup on repeated targets)**
The LRU cache on `KinematicsSolver._ik_cache` avoids redundant PyBullet IK solves for repeated or similar target positions. Cache keys are rounded to 0.1mm precision (4 decimal places), so positions within 0.1mm of each other share a cache entry.

| Metric | Cache Miss | Cache Hit | Speedup |
|--------|-----------|-----------|---------|
| Mean IK solve time | 0.404 ms/call | 0.002 ms/call | **202×** |
| 50 repeated calls total | 20.2 ms | 0.1 ms | **202×** |

**3. FK solve performance**
Forward kinematics is a simple matrix multiplication via PyBullet — no optimization was needed beyond the baseline implementation:

| Metric | Value |
|--------|-------|
| Mean FK solve | 0.029 ms/call |
| Max FK solve | 1.777 ms/call |
| 100 FK calls total | 2.9 ms |
| Budget | <10 ms/call |

### Bottlenecks and Fixes

**Bottleneck 1: PyBullet serialization via `pybullet_lock`.**
Because PyBullet is single-client, all physics calls are serialized through `pybullet_lock`. This means two simultaneous simulation requests run sequentially, not in parallel. This is a hard constraint of PyBullet's architecture, not a design choice.

*Fix:* In production, Gunicorn runs multiple worker processes (default 2). Each worker has its own PyBullet physics client, so inter-process parallelism compensates for intra-process serialization. The `WEB_WORKERS` environment variable controls worker count.

**Bottleneck 2: Large trajectory collision checking is O(waypoints × obstacles).**
Collision detection iterates every waypoint against every loaded obstacle. A 200-waypoint trajectory with 5 obstacles requires 1000 PyBullet contact queries.

*Fix:* The snapshot pattern (copy obstacles dict under lock, iterate outside) ensures collision checking doesn't hold the `_obstacles_lock` during the entire sweep. Additionally, the 10-second simulation timeout prevents runaway trajectories from blocking the pool indefinitely.

**Bottleneck 3: Solver initialization on first request.**
Loading a robot URDF into PyBullet takes ~50ms. The first request to each robot model pays this cost. Double-checked locking ensures only one thread performs initialization; subsequent requests find the solver already loaded.

### Benchmark Results

All benchmarks from `tests/test_benchmark.py`, run on WSL2 Linux (Python 3.12, PyBullet 3.2.6):

| Benchmark | Result | Target | Status |
|-----------|--------|--------|--------|
| IK cache hit (50 calls) | 0.1 ms total (0.002 ms/call) | Faster than misses | PASS |
| IK cache miss (50 calls) | 20.2 ms total (0.404 ms/call) | Baseline | PASS |
| FK solve (100 calls) | 2.9 ms total (0.029 ms/call) | <10 ms/call | PASS |
| FK mean across configs | 0.030 ms/call | <10 ms/call | PASS |
| FK worst-case | 1.777 ms/call | <10 ms/call | PASS |
| Event loop (100ms sleep) | 100.2 ms actual | <500 ms | PASS |
| Concurrent coroutines (10 × 50ms) | 50.6 ms total | <500 ms (not serialized) | PASS |

**Concurrency tests** (`tests/test_concurrency.py`): 10 tests verifying thread safety under concurrent access — IK cache (10 threads × 3 calls), obstacle registry (20 threads mixing register/get/list/delete), uploads dict (20 threads), health endpoint responsiveness while `pybullet_lock` is held, and structural checks on all lock types.

**Full test suite:** 86 passed, 1 skipped, in 1.86 seconds.

---

## Part D: Deployment Strategy

### Deployment Tools Used

| Tool | Purpose |
|------|---------|
| **Docker** | Containerized deployment — single `Dockerfile` packages Python 3.12, Node.js 20, pnpm, all backend/frontend dependencies |
| **Docker Compose** | Multi-service orchestration — configures ports, volumes, and environment variables |
| **Gunicorn** | Production WSGI/ASGI server — manages multiple uvicorn worker processes |
| **GitHub Actions** | CI/CD — runs lint (ruff, ESLint) and tests (pytest, build) on every pull request |
| **Shell scripts** | Automation — `start.sh`, `deploy.sh`, `seed-scenarios.sh` for setup, deployment, and demo seeding |

### Target Environments

**1. Local development**
Developers run `./start.sh` which auto-installs dependencies, starts the backend (FastAPI on port 8000) and frontend (Next.js on port 3000) concurrently. No Docker required for development.

**2. Docker container (local or cloud VM)**
`docker compose up` builds and runs the full stack in a single container. Suitable for demos, testing, and deployment to any Docker-capable host (AWS EC2, DigitalOcean, university servers).

**3. Production split deployment (planned)**
- Frontend: Vercel (Next.js hosting with edge CDN)
- Backend: Render (Docker container with persistent storage for PyBullet + robot models)
- Auth + DB: Supabase (auth + Postgres for per-user data)

### Installation Steps

**Option 1: Local development (recommended for development)**

```bash
# 1. Clone the repository
git clone https://github.com/noahjobse/SAIT-ARIS-AdditiveManufacturing.git
cd SAIT-ARIS-AdditiveManufacturing

# 2. Run the start script (auto-installs all dependencies)
./start.sh

# Backend: http://localhost:8000/docs (Swagger UI)
# Frontend: http://localhost:3000
```

Prerequisites: Python 3.11+, Node.js 20+. The start script checks for these and fails with a clear error message if they're missing. pnpm is auto-installed if not present.

**Option 2: Docker deployment**

```bash
# 1. Clone the repository
git clone https://github.com/noahjobse/SAIT-ARIS-AdditiveManufacturing.git
cd SAIT-ARIS-AdditiveManufacturing

# 2. Build and start via Docker Compose
docker compose up --build

# Backend: http://localhost:8000/docs
# Frontend: http://localhost:3000
```

Prerequisites: Docker and Docker Compose.

**Option 3: Production deployment**

```bash
# 1. Run the deploy script (builds, lints, tests, smoke tests)
./scripts/deploy.sh prod

# 2. Or start directly in production mode (Gunicorn)
./start.sh --prod
```

The deploy script runs pre-flight checks (Docker availability), backend lint (ruff), frontend lint (ESLint), backend tests (pytest — blocks production deploy if any fail), Docker build, and a smoke test (health endpoint check).

### Special Configurations

| Variable | Default | Purpose |
|----------|---------|---------|
| `PYBULLET_THREADS` | `4` | Thread pool size (workers per process for CPU-bound tasks) |
| `WEB_WORKERS` | `2` | Gunicorn worker processes (each gets its own PyBullet client) |
| `GUNICORN_BIND` | `0.0.0.0:8000` | Gunicorn listen address |
| `GUNICORN_TIMEOUT` | `60` | Request timeout in seconds (IK/trajectory can take up to 30s) |
| `LOG_LEVEL` | `info` | Gunicorn/uvicorn log verbosity |
| `PYTHONUNBUFFERED` | `1` | Flush Python stdout immediately (Docker logging) |

**Scaling considerations:**

- **Vertical scaling:** Increase `PYBULLET_THREADS` for more concurrent CPU work per process, increase `WEB_WORKERS` for more parallel PyBullet physics clients.
- **Horizontal scaling:** Deploy multiple Docker containers behind a load balancer. Each container is stateless (obstacles stored in temp files, no persistent database yet). A future Supabase integration would enable shared state across instances.
- **Resource requirements:** PyBullet loads robot URDFs into memory (~50MB per model per worker). With 3 robot models and 2 workers, expect ~300MB RAM for physics state alone. Total container memory usage is approximately 800MB–1GB.

"""
Shared thread pool and synchronization primitives.

Kept in a separate module to avoid circular imports
(main.py imports routers, routers import thread_pool).
"""
import asyncio
import os
from concurrent.futures import ThreadPoolExecutor

# Maximum PyBullet worker threads — PyBullet is single-client,
# so 1 worker plus the asyncio.Lock serializes PyBullet calls.
# More workers only help non-PyBullet CPU work.
MAX_WORKERS: int = int(os.environ.get("PYBULLET_THREADS", "4"))

# Executor — None until app startup sets it via lifespan
executor: ThreadPoolExecutor | None = None

# Serializes ALL PyBullet calls: only one coroutine accesses the physics
# client at a time. Waiting coroutines yield to the event loop, so
# health checks and metadata endpoints stay responsive during simulation.
pybullet_lock: asyncio.Lock = asyncio.Lock()

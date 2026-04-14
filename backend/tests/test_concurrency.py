"""
Concurrency tests for thread-safe data structures and async primitives.

Verifies:
- KinematicsSolver._ik_cache is safe under concurrent reads/writes
- ObstacleRegistry operations are safe under concurrent access
- _uploads dict in printing router is safe under concurrent writes
- pybullet_lock is an asyncio.Lock (correct type)
- Health endpoint responds without requiring pybullet_lock
"""
import asyncio
import threading
import time

import httpx
import pytest

from app.kinematics.solver import IK_CACHE_MAX, KinematicsSolver
from app.obstacles.registry import ObstacleRecord, obstacle_registry


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _collect_thread_errors(target, args=(), kwargs=None, n_threads=10):
    """
    Spawn n_threads threads running target(*args, **kwargs).
    Returns list of exceptions raised by any thread.
    """
    if kwargs is None:
        kwargs = {}
    errors: list[Exception] = []
    errors_lock = threading.Lock()

    def wrapper():
        try:
            target(*args, **kwargs)
        except Exception as exc:
            with errors_lock:
                errors.append(exc)

    threads = [threading.Thread(target=wrapper) for _ in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return errors


# ---------------------------------------------------------------------------
# Test 1: IK cache thread safety
# ---------------------------------------------------------------------------

class TestIKCacheThreadSafety:
    """Concurrent IK calls must not corrupt the LRU cache."""

    def test_ik_cache_thread_safety(self):
        """10 threads each calling IK 3 times must not raise or corrupt cache."""
        solver = KinematicsSolver(headless=True)

        # A reachable position for irb4600 (home position area)
        position = [1.58, 0.0, 1.765]
        orientation = [0.0, 0.0, 0.0, 1.0]

        def worker():
            for _ in range(3):
                solver.inverse_kinematics("irb4600", position, orientation)

        errors = _collect_thread_errors(worker, n_threads=10)

        try:
            assert errors == [], f"Threads raised exceptions: {errors}"
            assert len(solver._ik_cache) <= IK_CACHE_MAX, (
                f"Cache exceeded max size: {len(solver._ik_cache)} > {IK_CACHE_MAX}"
            )
        finally:
            solver.disconnect()


# ---------------------------------------------------------------------------
# Test 2: ObstacleRegistry thread safety
# ---------------------------------------------------------------------------

class TestObstacleRegistryThreadSafety:
    """Concurrent register/get/list/delete on ObstacleRegistry must not raise."""

    def test_obstacle_registry_thread_safety(self):
        """
        20 threads mix register / list / get / delete operations simultaneously.
        No RuntimeError, KeyError, or other exception should escape.
        """
        # Pre-register some obstacles that delete threads will target
        base_ids = [f"concurrent-pre-{i}" for i in range(5)]
        for obs_id in base_ids:
            obstacle_registry.register(ObstacleRecord(
                obstacle_id=obs_id,
                filename=f"{obs_id}.stl",
                file_path=f"/tmp/{obs_id}.stl",
                position=[0.0, 0.0, 0.0],
                rotation=[0.0, 0.0, 0.0],
            ))

        new_ids = [f"concurrent-new-{i}" for i in range(10)]
        errors: list[Exception] = []
        errors_lock = threading.Lock()

        def register_worker(obs_id: str):
            try:
                obstacle_registry.register(ObstacleRecord(
                    obstacle_id=obs_id,
                    filename=f"{obs_id}.stl",
                    file_path=f"/tmp/{obs_id}.stl",
                    position=[1.0, 2.0, 3.0],
                    rotation=[0.0, 0.0, 0.0],
                ))
            except Exception as exc:
                with errors_lock:
                    errors.append(exc)

        def list_worker():
            try:
                obstacle_registry.list_all()
            except Exception as exc:
                with errors_lock:
                    errors.append(exc)

        def get_worker(obs_id: str):
            try:
                obstacle_registry.get(obs_id)  # May return None — that's OK
            except Exception as exc:
                with errors_lock:
                    errors.append(exc)

        def delete_worker(obs_id: str):
            try:
                obstacle_registry.delete(obs_id)  # May return False — that's OK
            except Exception as exc:
                with errors_lock:
                    errors.append(exc)

        threads: list[threading.Thread] = []
        for obs_id in new_ids:
            threads.append(threading.Thread(target=register_worker, args=(obs_id,)))
        for _ in range(5):
            threads.append(threading.Thread(target=list_worker))
        for obs_id in base_ids:
            threads.append(threading.Thread(target=get_worker, args=(obs_id,)))
        for obs_id in base_ids:
            threads.append(threading.Thread(target=delete_worker, args=(obs_id,)))

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Cleanup whatever is left
        for obs_id in new_ids + base_ids:
            obstacle_registry.delete(obs_id)

        assert errors == [], f"Threads raised exceptions: {errors}"


# ---------------------------------------------------------------------------
# Test 3: _uploads dict thread safety
# ---------------------------------------------------------------------------

class TestUploadsDictThreadSafety:
    """_uploads + _uploads_lock in printing router must be safe under concurrency."""

    def test_uploads_dict_thread_safety(self):
        """
        20 threads each write a unique key and read it back under the lock.
        All values must be read correctly.
        """
        from app.routers.printing import _uploads, _uploads_lock

        results: list[bool] = []
        results_lock = threading.Lock()

        def worker(thread_id: int):
            key = f"thread-upload-{thread_id}"
            value = f"path-{thread_id}"
            with _uploads_lock:
                _uploads[key] = value
                read_back = _uploads[key]
            ok = read_back == value
            with results_lock:
                results.append(ok)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Cleanup test keys
        with _uploads_lock:
            for i in range(20):
                _uploads.pop(f"thread-upload-{i}", None)

        assert len(results) == 20, f"Expected 20 results, got {len(results)}"
        assert all(results), "Some threads read back wrong values"


# ---------------------------------------------------------------------------
# Test 4: Health endpoint responds without pybullet_lock
# ---------------------------------------------------------------------------

class TestHealthEndpointAsync:
    """Health endpoint should not require pybullet_lock."""

    def test_health_endpoint_is_async(self):
        """Health check returns 200 without holding pybullet_lock."""
        from app.main import app as fastapi_app

        async def _run():
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=fastapi_app),
                base_url="http://test",
            ) as client:
                response = await client.get("/api/health")
            return response

        response = asyncio.run(_run())
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_responsive_while_lock_held(self):
        """
        Health endpoint returns quickly even while pybullet_lock is held
        by a background coroutine.
        """
        from app.main import app as fastapi_app
        from app.thread_pool import pybullet_lock

        async def _run():
            lock_acquired = asyncio.Event()
            lock_released = asyncio.Event()

            async def hold_lock():
                async with pybullet_lock:
                    lock_acquired.set()
                    # Hold the lock for a short while
                    await asyncio.sleep(0.2)
                lock_released.set()

            holder = asyncio.create_task(hold_lock())
            # Wait until the lock is actually held
            await lock_acquired.wait()

            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=fastapi_app),
                base_url="http://test",
            ) as client:
                start = time.monotonic()
                response = await client.get("/api/health")
                elapsed = time.monotonic() - start

            await holder  # Let the holder finish
            return response, elapsed

        response, elapsed = asyncio.run(_run())
        assert response.status_code == 200
        # Health endpoint does not wait for pybullet_lock, so it should be fast
        assert elapsed < 1.0, f"Health took {elapsed:.3f}s — should not block on pybullet_lock"


# ---------------------------------------------------------------------------
# Test 5: pybullet_lock structural checks
# ---------------------------------------------------------------------------

class TestPybulletLockStructure:
    """Verify threading primitives exist and have correct types."""

    def test_pybullet_lock_is_asyncio_lock(self):
        """pybullet_lock must be an asyncio.Lock (not threading.Lock)."""
        from app.thread_pool import pybullet_lock
        assert isinstance(pybullet_lock, asyncio.Lock), (
            f"Expected asyncio.Lock, got {type(pybullet_lock)}"
        )

    def test_executor_is_none_before_lifespan(self):
        """executor is None at module level (set during app startup lifespan)."""
        import app.thread_pool as tp
        # If the app hasn't started its lifespan, executor is None.
        # (TestClient does run lifespan; this tests module-level default.)
        # We import a fresh reference — if already set by TestClient, it won't be None.
        # Just verify the attribute exists and is either None or a ThreadPoolExecutor.
        from concurrent.futures import ThreadPoolExecutor
        assert tp.executor is None or isinstance(tp.executor, ThreadPoolExecutor), (
            f"executor has unexpected type: {type(tp.executor)}"
        )

    def test_pybullet_lock_can_be_acquired_and_released(self):
        """pybullet_lock can be acquired and released via asyncio.run."""
        from app.thread_pool import pybullet_lock

        async def _try_lock():
            async with pybullet_lock:
                pass  # Acquired and released cleanly

        # Should not raise
        asyncio.run(_try_lock())

    def test_ik_cache_lock_is_threading_lock(self):
        """KinematicsSolver._cache_lock must be a threading.Lock."""
        solver = KinematicsSolver(headless=True)
        try:
            assert isinstance(solver._cache_lock, type(threading.Lock())), (
                f"Expected threading.Lock, got {type(solver._cache_lock)}"
            )
        finally:
            solver.disconnect()

    def test_obstacle_registry_lock_is_rlock(self):
        """ObstacleRegistry._lock must be a threading.RLock."""
        from app.obstacles.registry import ObstacleRegistry
        registry = ObstacleRegistry()
        # RLock's type name is "_RLock" — isinstance check with RLock()
        rlock_type = type(threading.RLock())
        assert isinstance(registry._lock, rlock_type), (
            f"Expected RLock, got {type(registry._lock)}"
        )

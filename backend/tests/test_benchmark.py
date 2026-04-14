"""
Benchmarks for kinematics performance and event loop responsiveness.

All tests are marked with `pytest.mark.benchmark` (custom mark).
These are timing-based sanity checks, not micro-benchmark comparisons
(the project does not depend on pytest-benchmark).

Run with: pytest tests/test_benchmark.py -v
"""
import asyncio
import time

import pytest

pytestmark = pytest.mark.benchmark  # marks every test in this file


# ---------------------------------------------------------------------------
# Benchmark 1: IK cache hit vs miss
# ---------------------------------------------------------------------------

class TestIKCacheHitVsMiss:
    """Verify that cache hits are meaningfully faster than cache misses."""

    def test_benchmark_ik_cache_hit_vs_miss(self):
        """
        50 repeated IK calls to the same position (cache hits after first)
        should complete faster in total than 50 calls to different positions
        (cache misses every time).
        """
        from app.kinematics.solver import KinematicsSolver

        solver = KinematicsSolver(headless=True)
        position_base = [1.5, 0.0, 1.7]
        orientation = [0.0, 0.0, 0.0, 1.0]

        try:
            # Warm-up — load robot and prime PyBullet
            solver.inverse_kinematics("irb4600", position_base, orientation)

            # --- Cache hits: same position every call ---
            n = 50
            start = time.perf_counter()
            for _ in range(n):
                solver.inverse_kinematics("irb4600", position_base, orientation)
            hit_time = time.perf_counter() - start

            # --- Cache misses: slightly different position each call ---
            # Step of 0.002 m (2 mm) — larger than the 0.1 mm rounding bucket so
            # each call is a real PyBullet solve, but all stay within robot reach.
            # IRB 4600 reach is ~2.05 m; starting at x=1.5 with y varying ±0.05 m
            # keeps us well inside the workspace.
            from app.kinematics.exceptions import IKSolutionNotFoundError

            start = time.perf_counter()
            miss_calls = 0
            for i in range(n):
                offset = (i - n // 2) * 0.002  # ±0.05 m around y=0
                pos = [position_base[0], offset, position_base[2]]
                try:
                    solver.inverse_kinematics("irb4600", pos, orientation)
                    miss_calls += 1
                except IKSolutionNotFoundError:
                    pass  # Some edge positions may be unreachable — skip them
            miss_time = time.perf_counter() - start

            # Need at least a few successful misses to compare fairly
            assert miss_calls > 0, "All cache-miss IK calls failed — check target positions"

            print(
                f"\n  Cache hits  ({n} calls): {hit_time * 1000:.1f} ms  "
                f"({hit_time / n * 1000:.3f} ms/call)"
            )
            print(
                f"  Cache misses ({n} calls): {miss_time * 1000:.1f} ms  "
                f"({miss_time / n * 1000:.3f} ms/call)"
            )

            # Hits should be faster than misses — each miss is a real PyBullet IK solve
            assert hit_time < miss_time, (
                f"Cache hits ({hit_time:.4f}s) were not faster than misses ({miss_time:.4f}s)"
            )

        finally:
            solver.disconnect()


# ---------------------------------------------------------------------------
# Benchmark 2: FK solve time
# ---------------------------------------------------------------------------

class TestFKSolveTime:
    """FK is simple matrix math — 100 calls must complete well under 1 second."""

    def test_benchmark_fk_solve_time(self):
        """100 FK solves for irb4600 should complete in < 1 second total."""
        from app.kinematics.solver import KinematicsSolver

        solver = KinematicsSolver(headless=True)
        joint_angles = [0.5, -0.3, 0.8, 0.0, 0.5, 0.0]  # Within joint limits

        try:
            n = 100
            start = time.perf_counter()
            for _ in range(n):
                result = solver.forward_kinematics("irb4600", joint_angles)
            elapsed = time.perf_counter() - start

            mean_ms = elapsed / n * 1000
            print(
                f"\n  FK solve: {n} calls in {elapsed * 1000:.1f} ms  "
                f"(mean {mean_ms:.3f} ms/call)"
            )

            assert elapsed < 1.0, (
                f"100 FK solves took {elapsed:.3f}s — expected < 1.0s"
            )
            # Spot-check the result is valid
            assert "position" in result
            assert len(result["position"]) == 3

        finally:
            solver.disconnect()

    def test_benchmark_fk_mean_per_call_reasonable(self):
        """Mean FK time per call should be < 10 ms."""
        from app.kinematics.solver import KinematicsSolver

        solver = KinematicsSolver(headless=True)
        # Several different joint configurations
        configs = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.5, -0.3, 0.8, 0.0, 0.5, 0.0],
            [1.0, -0.5, 0.5, 0.3, -0.3, 0.1],
            [-0.5, 0.2, -0.3, 0.1, 0.4, -0.2],
        ]
        n_repeats = 25

        try:
            times = []
            for angles in configs * n_repeats:
                t0 = time.perf_counter()
                solver.forward_kinematics("irb4600", angles)
                times.append(time.perf_counter() - t0)

            mean_ms = (sum(times) / len(times)) * 1000
            max_ms = max(times) * 1000
            print(f"\n  FK mean {mean_ms:.3f} ms/call, max {max_ms:.3f} ms/call")

            assert mean_ms < 10.0, f"Mean FK time {mean_ms:.3f} ms exceeds 10 ms budget"

        finally:
            solver.disconnect()


# ---------------------------------------------------------------------------
# Benchmark 3: Simulate computation (placeholder)
# ---------------------------------------------------------------------------

class TestSimulateBenchmark:
    """Placeholder — full simulation benchmark requires a RAPID fixture file."""

    def test_benchmark_simulate_computation(self):
        """Skipped: requires a full RAPID program fixture."""
        pytest.skip("requires full RAPID program fixture")


# ---------------------------------------------------------------------------
# Benchmark 4: Event loop responsiveness
# ---------------------------------------------------------------------------

class TestEventLoopResponsiveness:
    """
    Basic asyncio health check: a coroutine that sleeps 0.1 s must return
    within a reasonable wall-clock budget (< 0.5 s).
    """

    def test_benchmark_event_loop_responsiveness(self):
        """A 100 ms async sleep must complete within 500 ms wall-clock."""

        async def _work():
            start = time.perf_counter()
            await asyncio.sleep(0.1)
            return time.perf_counter() - start

        elapsed = asyncio.run(_work())
        print(f"\n  asyncio.sleep(0.1) returned in {elapsed * 1000:.1f} ms")
        assert elapsed < 0.5, (
            f"Event loop overhead too high: {elapsed:.3f}s for a 0.1s sleep"
        )

    def test_benchmark_concurrent_coroutines(self):
        """
        10 concurrent coroutines each sleeping 0.05 s must all complete
        in < 0.5 s wall-clock (not 10 × 0.05 s = 0.5 s serialized).
        """

        async def _run_all():
            async def sleeper(idx: int) -> float:
                t0 = time.perf_counter()
                await asyncio.sleep(0.05)
                return time.perf_counter() - t0

            start = time.perf_counter()
            results = await asyncio.gather(*[sleeper(i) for i in range(10)])
            total = time.perf_counter() - start
            return total, results

        total, per_task = asyncio.run(_run_all())
        print(
            f"\n  10 × 50 ms concurrent sleeps finished in {total * 1000:.1f} ms total"
        )
        # Should finish in roughly 50 ms, not 500 ms (concurrency)
        assert total < 0.5, (
            f"Concurrent coroutines took {total:.3f}s — event loop may be blocked"
        )
        assert len(per_task) == 10

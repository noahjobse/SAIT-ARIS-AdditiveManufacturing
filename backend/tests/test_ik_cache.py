"""Tests for IK LRU cache in KinematicsSolver."""
from app.kinematics.solver import IK_CACHE_MAX, KinematicsSolver, _ik_cache_key


class TestIKCacheKey:
    """Test cache key generation and rounding."""

    def test_rounding_groups_nearby_positions(self):
        """Positions within 0.1mm should produce the same cache key."""
        # 4 decimal rounding: 1.00001 and 1.00004 both round to 1.0
        key_a = _ik_cache_key("irb4600", [1.00001, 0.0, 0.5], [1, 0, 0, 0])
        key_b = _ik_cache_key("irb4600", [1.00004, 0.0, 0.5], [1, 0, 0, 0])
        assert key_a == key_b

    def test_distant_positions_differ(self):
        """Positions 1mm apart should produce different cache keys."""
        key_a = _ik_cache_key("irb4600", [1.0, 0.0, 0.5], [1, 0, 0, 0])
        key_b = _ik_cache_key("irb4600", [1.001, 0.0, 0.5], [1, 0, 0, 0])
        assert key_a != key_b

    def test_different_robots_differ(self):
        """Same position on different robots should produce different keys."""
        key_a = _ik_cache_key("irb4600", [1.0, 0.0, 0.5], [1, 0, 0, 0])
        key_b = _ik_cache_key("irb2600", [1.0, 0.0, 0.5], [1, 0, 0, 0])
        assert key_a != key_b

    def test_none_orientation(self):
        """Orientation=None should produce a valid key with empty tuple."""
        key = _ik_cache_key("irb4600", [1.0, 0.0, 0.5], None)
        assert key == ("irb4600", (1.0, 0.0, 0.5), ())


class TestIKCache:
    """Test cache hit/miss/eviction behavior."""

    def test_cache_hit_returns_same_result(self):
        """Repeated IK call with same target should return cached result."""
        solver = KinematicsSolver()

        target = [1.5, 0.0, 1.7]
        orientation = [0, 0, 0, 1]

        result_1 = solver.inverse_kinematics("irb4600", target, orientation)
        result_2 = solver.inverse_kinematics("irb4600", target, orientation)

        assert result_1["joint_angles"] == result_2["joint_angles"]
        # Cache should have exactly 1 entry (same key)
        assert len(solver._ik_cache) == 1

        solver.disconnect()

    def test_cache_miss_for_different_targets(self):
        """Different targets should produce separate cache entries."""
        solver = KinematicsSolver()

        # Both reachable positions for IRB 4600
        solver.inverse_kinematics("irb4600", [1.5, 0.0, 1.7], [0, 0, 0, 1])
        solver.inverse_kinematics("irb4600", [1.2, 0.0, 1.4], [0, 0, 0, 1])

        assert len(solver._ik_cache) == 2

        solver.disconnect()

    def test_cache_eviction_at_max_size(self):
        """Cache should evict oldest entry when exceeding IK_CACHE_MAX."""
        solver = KinematicsSolver()

        # Manually fill cache to max
        for i in range(IK_CACHE_MAX):
            solver._ik_cache[(f"fake_{i}",)] = [0.0] * 6

        assert len(solver._ik_cache) == IK_CACHE_MAX

        # One real IK call should evict the oldest
        solver.inverse_kinematics("irb4600", [1.5, 0.0, 1.7], [0, 0, 0, 1])

        assert len(solver._ik_cache) == IK_CACHE_MAX
        # First fake entry should be evicted
        assert ("fake_0",) not in solver._ik_cache

        solver.disconnect()

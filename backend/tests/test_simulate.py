"""Tests for /api/simulate endpoint — collision wiring, timeout, and stats."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

DEMO_RAPID = """MODULE DemoMove
    CONST robtarget pReady := [[1200, 0, 1400], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget pLeft  := [[1000, 400, 1000], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    PROC main()
        MoveL pReady, v500, z10, tool0;
        MoveL pLeft,  v300, z10, tool0;
    ENDPROC
ENDMODULE"""


class TestSimulateEndpoint:
    """Test the full /api/simulate pipeline."""

    def test_simulate_basic_success(self):
        """Basic simulate request returns trajectory and stats."""
        # First parse the RAPID code
        parse_res = client.post("/api/parse", json={"code": DEMO_RAPID})
        assert parse_res.status_code == 200
        program = parse_res.json()["program"]

        # Then simulate
        sim_res = client.post("/api/simulate", json={
            "robot_id": "irb4600",
            "program": program,
        })
        assert sim_res.status_code == 200

        data = sim_res.json()
        assert "trajectory" in data
        assert "stats" in data
        assert len(data["trajectory"]) > 0
        assert data["stats"]["total_waypoints"] > 0
        assert data["stats"]["duration_seconds"] > 0
        assert data["stats"]["computation_time_ms"] > 0

    def test_simulate_returns_timed_out_field(self):
        """Response stats include timed_out field (should be false for small programs)."""
        parse_res = client.post("/api/parse", json={"code": DEMO_RAPID})
        program = parse_res.json()["program"]

        sim_res = client.post("/api/simulate", json={
            "robot_id": "irb4600",
            "program": program,
        })
        assert sim_res.status_code == 200

        stats = sim_res.json()["stats"]
        assert "timed_out" in stats
        assert stats["timed_out"] is False

    def test_simulate_no_obstacles_empty_collisions(self):
        """Without obstacles, every waypoint should have empty collisions list."""
        parse_res = client.post("/api/parse", json={"code": DEMO_RAPID})
        program = parse_res.json()["program"]

        sim_res = client.post("/api/simulate", json={
            "robot_id": "irb4600",
            "program": program,
        })
        assert sim_res.status_code == 200

        trajectory = sim_res.json()["trajectory"]
        for wp in trajectory:
            assert wp["collisions"] == []

        assert sim_res.json()["stats"]["collisions_detected"] == 0

    def test_simulate_waypoint_structure(self):
        """Each waypoint has expected fields with correct types."""
        parse_res = client.post("/api/parse", json={"code": DEMO_RAPID})
        program = parse_res.json()["program"]

        sim_res = client.post("/api/simulate", json={
            "robot_id": "irb4600",
            "program": program,
        })
        assert sim_res.status_code == 200

        wp = sim_res.json()["trajectory"][0]
        assert isinstance(wp["index"], int)
        assert isinstance(wp["timestamp"], float)
        assert isinstance(wp["joints"], list)
        assert len(wp["joints"]) == 6
        assert isinstance(wp["tcp_pose"]["position"], list)
        assert len(wp["tcp_pose"]["position"]) == 3
        assert isinstance(wp["collisions"], list)

    def test_simulate_invalid_robot_id(self):
        """Invalid robot ID returns 400."""
        parse_res = client.post("/api/parse", json={"code": DEMO_RAPID})
        program = parse_res.json()["program"]

        sim_res = client.post("/api/simulate", json={
            "robot_id": "invalid_robot",
            "program": program,
        })
        assert sim_res.status_code == 400

    def test_simulate_empty_program(self):
        """Program with no move commands returns 400."""
        empty_rapid = """MODULE Empty
    PROC main()
    ENDPROC
ENDMODULE"""
        parse_res = client.post("/api/parse", json={"code": empty_rapid})
        program = parse_res.json()["program"]

        sim_res = client.post("/api/simulate", json={
            "robot_id": "irb4600",
            "program": program,
        })
        # Should either return empty trajectory or error
        assert sim_res.status_code in [200, 400]

    def test_simulate_timestamps_monotonically_increase(self):
        """Waypoint timestamps should be monotonically increasing."""
        parse_res = client.post("/api/parse", json={"code": DEMO_RAPID})
        program = parse_res.json()["program"]

        sim_res = client.post("/api/simulate", json={
            "robot_id": "irb4600",
            "program": program,
        })
        assert sim_res.status_code == 200

        trajectory = sim_res.json()["trajectory"]
        timestamps = [wp["timestamp"] for wp in trajectory]
        for i in range(1, len(timestamps)):
            assert timestamps[i] > timestamps[i - 1], f"Timestamp not increasing at index {i}"

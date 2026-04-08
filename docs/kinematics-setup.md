# Kinematics Setup Guide

## Overview

The kinematics module provides forward and inverse kinematics solvers for ABB robots using PyBullet.

## Components

### URDF Files

Located in `/models/robots/{robot_id}/`:
- `irb4600.urdf` - Robot kinematic chain definition
- `config.json` - Robot metadata (payload, reach, DOF)

### Backend Modules

- `app/kinematics/solver.py` - FK/IK solver wrapper
- `app/kinematics/robot_loader.py` - URDF loading and PyBullet management
- `app/kinematics/exceptions.py` - Custom exceptions

### API Endpoints

- `POST /api/kinematics/fk` - Forward kinematics
- `POST /api/kinematics/ik` - Inverse kinematics

## Usage

### Python API

```python
from app.kinematics.solver import KinematicsSolver

solver = KinematicsSolver()

# Forward kinematics
fk_result = solver.forward_kinematics("irb4600", [0, 0, 0, 0, 0, 0])
print(fk_result["position"])  # [1.58, 0.0, 1.765]

# Inverse kinematics
ik_result = solver.inverse_kinematics("irb4600", [1.2, 0.3, 1.4])
print(ik_result["joint_angles"])  # [j1, j2, j3, j4, j5, j6]

solver.disconnect()
```

### REST API

```bash
# Forward kinematics
curl -X POST http://localhost:8000/api/kinematics/fk \
  -H "Content-Type: application/json" \
  -d '{"robot_id": "irb4600", "joint_angles": [0,0,0,0,0,0]}'

# Inverse kinematics
curl -X POST http://localhost:8000/api/kinematics/ik \
  -H "Content-Type: application/json" \
  -d '{"robot_id": "irb4600", "target_position": [1.58, 0, 1.765]}'
```

## Testing

```bash
# Run all kinematics tests
pytest tests/test_kinematics.py tests/test_robot_loader.py tests/test_kinematics_api.py -v

# Run specific test
pytest tests/test_kinematics.py::TestForwardKinematics::test_fk_zero_position -v
```

## Supported Robots

IRB 4600, IRB 2600, and IRB 6700 are all implemented and supported. Each robot has a URDF file and config in `models/robots/{robot_id}/`.

To add support for an additional robot model:

1. Create URDF file: `models/robots/{robot_id}/{robot_id}.urdf`
2. Create config file: `models/robots/{robot_id}/config.json`
3. Add tests with known poses for validation
4. Update documentation

## Troubleshooting

### PyBullet connection errors

If you see "Not connected to physics server", ensure:
- Only one solver instance is active
- Call `solver.disconnect()` when done

### IK solution not found

Common causes:
- Target outside robot workspace (check reach limits)
- Unrealistic orientation constraints
- Joint limits too restrictive

Try relaxing orientation or providing `current_joints` seed.

### Joint limit violations

Check `config.json` joint limits match URDF `<limit>` tags.

## Performance

- FK: ~0.1ms per call
- IK: ~5-20ms per call (depends on solver iterations)
- URDF loading: ~50ms (cached after first load)

### IK LRU Cache

An LRU cache (1000 entries) has been added to the IK solver. Cache keys are derived from the target position rounded to the nearest 0.1mm, so repeated or near-identical IK queries are served from cache rather than re-solved by PyBullet. This significantly reduces latency for trajectory playback that revisits similar poses.

## Integration with Trajectory Generator

This module is used by Noah's trajectory generator (built in Weeks 5-6):

```python
# The trajectory generator uses IK like this:
from app.kinematics.solver import KinematicsSolver

solver = KinematicsSolver()

# Convert RAPID waypoint to joint angles
rapid_position = [1.0, 0.5, 1.5]  # From MoveL command
ik_result = solver.inverse_kinematics("irb4600", rapid_position)
joint_angles = ik_result["joint_angles"]

# Use joint_angles in trajectory JSON sent to frontend
trajectory_point = {
    "time": 0.5,
    "joints": joint_angles,
    "position": rapid_position  # For debugging
}
```

## References

- PyBullet Documentation: https://pybullet.org
- ROS Industrial ABB: https://github.com/ros-industrial/abb
- ABB IRB 4600 Datasheet: [Product specification]

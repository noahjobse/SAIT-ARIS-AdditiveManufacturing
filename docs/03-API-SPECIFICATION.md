# API Specification

**Project:** ABB Online Simulation Platform
**Version:** 2.0
**Date:** 2026-02-12
**Base URL:** `http://localhost:8000` (development)

---

**Design:** Synchronous REST, stateless, Pydantic validation, all computation server-side.
**Auth:** None for MVP. **Versioning:** No prefix for MVP.

## Sequence Diagrams

Visual documentation of key API flows:

- **[RAPID Upload & Parse](./diagrams/rapid-upload-parse.svg)** - File upload, validation, parsing, error handling
- **[Obstacle Management](./diagrams/obstacle-management.svg)** - Upload, transform, and delete obstacle workflows
- **[End-to-End Simulation](./diagrams/end-to-end-flow.svg)** - Complete pipeline from RAPID upload to 3D visualization

## Error Format

```json
{
  "detail": "Human-readable error message",
  "error_code": "MACHINE_READABLE_CODE"
}
```

**Status Codes:** 200 OK, 400 Bad Request, 404 Not Found, 422 Unprocessable Entity, 500 Internal Server Error

## Endpoints

### GET /api/health

Returns `{"status": "healthy", "version": "1.0.0", "timestamp": "..."}`.

### GET /api/robots

Returns array of robot metadata:

```json
[
  {
    "id": "irb4600",
    "name": "IRB 4600-60/2.05",
    "manufacturer": "ABB",
    "dof": 6,
    "payload_kg": 60,
    "reach_mm": 2050,
    "model_url": "/api/robots/irb4600/model"
  }
]
```

Three robots: `irb4600` (60kg/2050mm), `irb2600` (12kg/1650mm), `irb6700` (145kg/3200mm).

### GET /api/robots/{robot_id}/model

Serves GLB binary file (`application/octet-stream`). 404 for invalid robot ID.

### POST /api/upload/rapid

![RAPID Upload Flow](./diagrams/rapid-upload-parse.svg)

Upload `.mod` file (multipart/form-data, max 1MB). Returns parsed AST:

```json
{
  "filename": "program.mod",
  "ast": [
    {
      "type": "MoveL",
      "target": {"type": "RobTarget", "trans": [500.0, 0.0, 600.0], "rot": [1.0, 0.0, 0.0, 0.0], "robconf": [0,0,0,0], "extax": [0,0,0,0,0,0]},
      "speed": {"type": "SpeedData", "v_tcp": 1000.0, "v_ori": 500.0},
      "zone": {"type": "ZoneData", "finep": false, "pzone_tcp": 10.0}
    }
  ],
  "errors": [],
  "warnings": [{"line": 12, "message": "Zone data z10 may cause path deviation"}]
}
```

### POST /api/upload/obstacle

![Obstacle Management Flow](./diagrams/obstacle-management.svg)

Upload `.stl` file (multipart/form-data, max 10MB) with optional `position` ([x,y,z] mm) and `rotation` ([rx,ry,rz] degrees).

```json
{
  "obstacle_id": "obs_1707145800_abc123",
  "filename": "table.stl",
  "position": [500.0, 0.0, 0.0],
  "rotation": [0.0, 0.0, 45.0],
  "bounds": {"min": [400.0, -100.0, -50.0], "max": [600.0, 100.0, 50.0]},
  "vertices": 1200,
  "triangles": 400
}
```

### POST /api/parse

Parse raw RAPID code (JSON body `{"code": "..."}`) and return AST. Same response format as upload/rapid.

### GET /api/obstacles

List all uploaded obstacles. Returns array of obstacle objects.

### PUT /api/obstacles/{obstacle_id}/transform

Update obstacle position/rotation. Body: `{"position": [x,y,z], "rotation": [rx,ry,rz]}`.

### DELETE /api/obstacles/{obstacle_id}

Remove obstacle. Returns `{"obstacle_id": "...", "deleted": true}`.

### POST /api/simulate

Execute full simulation pipeline.

**Request:**
```json
{
  "robot_id": "irb4600",
  "ast": [...],
  "obstacles": [{"obstacle_id": "obs_...", "position": [500,0,0], "rotation": [0,0,45]}]
}
```

**Response:**
```json
{
  "trajectory": [
    {
      "index": 0,
      "timestamp": 0.0,
      "joints": [0.0, -30.0, 30.0, 0.0, 45.0, 0.0],
      "tcp_pose": {"position": [500.0, 0.0, 600.0], "orientation": [1.0, 0.0, 0.0, 0.0]},
      "collisions": []
    },
    {
      "index": 45,
      "timestamp": 1.485,
      "joints": [15.2, -25.3, 35.7, 2.1, 40.2, 0.0],
      "tcp_pose": {"position": [520.0, 5.0, 605.0], "orientation": [1.0, 0.0, 0.0, 0.0]},
      "collisions": [
        {"obstacle_id": "obs_...", "link": "link_5", "penetration_depth": 2.3, "contact_point": [515.0, 3.0, 603.0]}
      ]
    }
  ],
  "stats": {
    "total_waypoints": 125,
    "duration_seconds": 4.125,
    "collisions_detected": 12,
    "ik_failures": 0,
    "computation_time_ms": 2341
  }
}
```

## AST Data Types

**MoveL:** `{type, target: RobTarget|JointTarget, speed: SpeedData, zone: ZoneData}`
**MoveJ:** `{type, target: RobTarget|JointTarget, speed: SpeedData, zone: ZoneData}`
**MoveC:** `{type, via_point: RobTarget, target: RobTarget, speed: SpeedData, zone: ZoneData}`

**RobTarget:** `{trans: [x,y,z] mm, rot: [q1,q2,q3,q4] quaternion, robconf: [cf1,cf4,cf6,cfx], extax: [6 floats]}`
**JointTarget:** `{robax: [j1-j6] degrees, extax: [6 floats]}`
**SpeedData:** `{v_tcp: mm/s, v_ori: deg/s, v_leax?: mm/s, v_reax?: deg/s}`
**ZoneData:** `{finep: bool, pzone_tcp: mm, pzone_ori?: deg, pzone_eax?: mm, zone_ori?: deg, zone_leax?: mm, zone_reax?: deg}`

## Error Code Catalog

### General
| Code | Status | Description |
|------|--------|-------------|
| `VALIDATION_ERROR` | 422 | Pydantic schema validation failed |
| `INVALID_FILE_TYPE` | 400 | Unsupported file extension |
| `FILE_TOO_LARGE` | 400 | File exceeds size limit |
| `FILE_READ_ERROR` | 500 | Unable to read uploaded file |

### Parser
| Code | Status | Description |
|------|--------|-------------|
| `PARSE_ERROR` | 400 | RAPID syntax error |
| `UNSUPPORTED_INSTRUCTION` | 400 | Instruction not supported in MVP |
| `UNDEFINED_TARGET` | 400 | Referenced target not defined |
| `UNDEFINED_SPEED` | 400 | Speed data not defined |
| `UNDEFINED_ZONE` | 400 | Zone data not defined |

### Kinematics
| Code | Status | Description |
|------|--------|-------------|
| `IK_FAILURE` | 500 | IK solver failed |
| `IK_NO_SOLUTION` | 400 | No IK solution exists (out of reach) |
| `IK_TIMEOUT` | 500 | IK solver exceeded 2s limit |
| `FK_ERROR` | 500 | Forward kinematics failed |
| `JOINT_LIMIT_EXCEEDED` | 400 | Joint angles exceed limits |

### Collision
| Code | Status | Description |
|------|--------|-------------|
| `COLLISION_DETECTED` | 200 | Warning, included in trajectory |
| `MESH_LOAD_ERROR` | 500 | Unable to load obstacle STL |
| `INVALID_MESH` | 400 | STL mesh is malformed |

### Robot & Obstacle
| Code | Status | Description |
|------|--------|-------------|
| `INVALID_ROBOT_ID` | 404 | Use irb4600, irb2600, or irb6700 |
| `ROBOT_CONFIG_ERROR` | 500 | Failed to load robot config |
| `MODEL_NOT_FOUND` | 404 | GLB model file missing |
| `OBSTACLE_NOT_FOUND` | 404 | Obstacle ID not found |
| `OBSTACLE_LIMIT_EXCEEDED` | 400 | Too many obstacles (>10) |
| `INVALID_TRANSFORM` | 400 | Position/rotation values invalid |

### Simulation
| Code | Status | Description |
|------|--------|-------------|
| `EMPTY_AST` | 400 | AST array is empty |
| `SIMULATION_TIMEOUT` | 500 | Simulation exceeded 5s limit |
| `PYBULLET_ERROR` | 500 | PyBullet internal error |

---

**Last Updated:** 2026-02-12

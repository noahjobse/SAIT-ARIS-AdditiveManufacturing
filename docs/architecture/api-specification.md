# API Specification

**Project:** ABB Online Simulation Platform
**Version:** 1.0
**Date:** 2026-02-05
**Base URL:** `http://localhost:8000` (development)

## Overview

RESTful API for RAPID program simulation with inverse kinematics and collision detection. All endpoints return JSON except `/api/robots/{id}/model` which serves binary GLB files.

**Design Principles:**
- Synchronous request/response (no WebSockets for MVP)
- Stateless (no session storage on backend)
- Heavy computation server-side (client receives pre-computed results)
- Pydantic validation on all requests/responses

## Authentication

**MVP:** No authentication required. All endpoints are public.

**Post-MVP:** Consider API keys or JWT tokens for multi-user support.

## Error Handling

All errors follow FastAPI standard error format:

```json
{
  "detail": "Human-readable error message",
  "error_code": "OPTIONAL_MACHINE_READABLE_CODE"
}
```

**HTTP Status Codes:**
- `200 OK` - Request successful
- `400 Bad Request` - Invalid input (malformed JSON, validation failure)
- `404 Not Found` - Resource not found (invalid robot ID, file not found)
- `422 Unprocessable Entity` - Pydantic validation error
- `500 Internal Server Error` - Server-side error (PyBullet crash, parser crash)

## Endpoints

---

### 1. Health Check

**Endpoint:** `GET /api/health`

**Description:** Server status and version information.

**Request:** None

**Response:**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-02-05T14:30:00Z"
}
```

**Status Codes:**
- `200 OK` - Server is running

**Example:**

```bash
curl http://localhost:8000/api/health
```

---

### 2. List Available Robots

**Endpoint:** `GET /api/robots`

**Description:** Returns metadata for all supported robot models.

**Request:** None

**Response:**

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
  },
  {
    "id": "irb2600",
    "name": "IRB 2600-12/1.65",
    "manufacturer": "ABB",
    "dof": 6,
    "payload_kg": 12,
    "reach_mm": 1650,
    "model_url": "/api/robots/irb2600/model"
  },
  {
    "id": "irb6700",
    "name": "IRB 6700-145/3.2",
    "manufacturer": "ABB",
    "dof": 6,
    "payload_kg": 145,
    "reach_mm": 3200,
    "model_url": "/api/robots/irb6700/model"
  }
]
```

**Status Codes:**
- `200 OK` - Success

**Example:**

```bash
curl http://localhost:8000/api/robots
```

---

### 3. Get Robot 3D Model

**Endpoint:** `GET /api/robots/{robot_id}/model`

**Description:** Serves GLB binary file for 3D visualization in Babylon.js.

**Path Parameters:**
- `robot_id` (string, required) - Robot identifier (`irb4600`, `irb2600`, `irb6700`)

**Request:** None

**Response:** Binary stream (`application/octet-stream`)

**Headers:**
- `Content-Type: application/octet-stream`
- `Content-Disposition: inline; filename="irb4600.glb"`

**Status Codes:**
- `200 OK` - GLB file returned
- `404 Not Found` - Invalid robot ID

**Example:**

```bash
curl http://localhost:8000/api/robots/irb4600/model --output irb4600.glb
```

**Frontend Usage:**

```typescript
const url = `/api/robots/${robotId}/model`;
const mesh = await BABYLON.SceneLoader.ImportMeshAsync("", url, "", scene);
```

---

### 4. Upload RAPID Program

**Endpoint:** `POST /api/upload/rapid`

**Description:** Parse RAPID code and return AST (Abstract Syntax Tree) with validation errors/warnings.

**Request:** `multipart/form-data`

**Form Fields:**
- `file` (file, required) - RAPID source file (`.mod` extension, max 1MB)

**Response:**

```json
{
  "filename": "program.mod",
  "ast": [
    {
      "type": "MoveL",
      "target": {
        "type": "RobTarget",
        "trans": [500.0, 0.0, 600.0],
        "rot": [1.0, 0.0, 0.0, 0.0],
        "robconf": [0, 0, 0, 0],
        "extax": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
      },
      "speed": {"type": "SpeedData", "v_tcp": 1000.0, "v_ori": 500.0},
      "zone": {"type": "ZoneData", "finep": false, "pzone_tcp": 10.0}
    },
    {
      "type": "MoveJ",
      "target": {
        "type": "JointTarget",
        "robax": [0.0, -30.0, 30.0, 0.0, 45.0, 0.0],
        "extax": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
      },
      "speed": {"type": "SpeedData", "v_tcp": 1000.0, "v_ori": 500.0},
      "zone": {"type": "ZoneData", "finep": false, "pzone_tcp": 10.0}
    }
  ],
  "errors": [],
  "warnings": [
    {
      "line": 12,
      "message": "Zone data z10 may cause path deviation at sharp corners"
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Parsing successful (even if warnings present)
- `400 Bad Request` - File too large, invalid extension, or malformed RAPID syntax
- `422 Unprocessable Entity` - Validation error

**Error Example:**

```json
{
  "filename": "program.mod",
  "ast": null,
  "errors": [
    {
      "line": 5,
      "message": "Syntax error: expected 'MoveL' but found 'MoveX'"
    },
    {
      "line": 10,
      "message": "Undefined target: p10"
    }
  ],
  "warnings": []
}
```

**Example:**

```bash
curl -X POST http://localhost:8000/api/upload/rapid \
  -F "file=@program.mod"
```

---

### 5. Upload Obstacle

**Endpoint:** `POST /api/upload/obstacle`

**Description:** Upload STL mesh for collision detection, with optional transform.

**Request:** `multipart/form-data`

**Form Fields:**
- `file` (file, required) - STL mesh file (`.stl` extension, max 10MB)
- `position` (JSON string, optional) - `[x, y, z]` in mm (default: `[0, 0, 0]`)
- `rotation` (JSON string, optional) - `[rx, ry, rz]` in degrees (default: `[0, 0, 0]`)

**Response:**

```json
{
  "obstacle_id": "obs_1707145800_abc123",
  "filename": "table.stl",
  "position": [500.0, 0.0, 0.0],
  "rotation": [0.0, 0.0, 45.0],
  "bounds": {
    "min": [400.0, -100.0, -50.0],
    "max": [600.0, 100.0, 50.0]
  },
  "vertices": 1200,
  "triangles": 400
}
```

**Status Codes:**
- `200 OK` - Upload successful
- `400 Bad Request` - File too large, invalid format, or malformed STL
- `422 Unprocessable Entity` - Validation error

**Example:**

```bash
curl -X POST http://localhost:8000/api/upload/obstacle \
  -F "file=@table.stl" \
  -F 'position=[500, 0, 0]' \
  -F 'rotation=[0, 0, 45]'
```

---

### 6. Simulate Trajectory

**Endpoint:** `POST /api/simulate`

**Description:** Execute full simulation pipeline: AST → IK solving → collision detection → trajectory waypoints.

**Request:** `application/json`

```json
{
  "robot_id": "irb4600",
  "ast": [
    {
      "type": "MoveL",
      "target": {
        "type": "RobTarget",
        "trans": [500.0, 0.0, 600.0],
        "rot": [1.0, 0.0, 0.0, 0.0],
        "robconf": [0, 0, 0, 0],
        "extax": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
      },
      "speed": {"type": "SpeedData", "v_tcp": 1000.0, "v_ori": 500.0},
      "zone": {"type": "ZoneData", "finep": false, "pzone_tcp": 10.0}
    }
  ],
  "obstacles": [
    {
      "obstacle_id": "obs_1707145800_abc123",
      "position": [500.0, 0.0, 0.0],
      "rotation": [0.0, 0.0, 45.0]
    }
  ]
}
```

**Request Schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `robot_id` | string | Yes | Robot identifier |
| `ast` | array | Yes | Parsed AST from `/api/upload/rapid` |
| `obstacles` | array | No | List of obstacle IDs with transforms |

**Response:**

```json
{
  "trajectory": [
    {
      "index": 0,
      "timestamp": 0.0,
      "joints": [0.0, -30.0, 30.0, 0.0, 45.0, 0.0],
      "tcp_pose": {
        "position": [500.0, 0.0, 600.0],
        "orientation": [1.0, 0.0, 0.0, 0.0]
      },
      "collisions": []
    },
    {
      "index": 1,
      "timestamp": 0.033,
      "joints": [0.5, -29.8, 30.1, 0.1, 44.9, 0.0],
      "tcp_pose": {
        "position": [501.2, 0.1, 600.5],
        "orientation": [1.0, 0.0, 0.0, 0.0]
      },
      "collisions": []
    },
    {
      "index": 45,
      "timestamp": 1.485,
      "joints": [15.2, -25.3, 35.7, 2.1, 40.2, 0.0],
      "tcp_pose": {
        "position": [520.0, 5.0, 605.0],
        "orientation": [1.0, 0.0, 0.0, 0.0]
      },
      "collisions": [
        {
          "obstacle_id": "obs_1707145800_abc123",
          "link": "link_5",
          "penetration_depth": 2.3,
          "contact_point": [515.0, 3.0, 603.0]
        }
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

**Response Schema:**

**`trajectory[]` object:**

| Field | Type | Description |
|-------|------|-------------|
| `index` | integer | Waypoint index (0-based) |
| `timestamp` | float | Time in seconds from trajectory start |
| `joints` | float[6] | Joint angles in degrees [J1, J2, J3, J4, J5, J6] |
| `tcp_pose.position` | float[3] | TCP position in mm [x, y, z] |
| `tcp_pose.orientation` | float[4] | TCP orientation as quaternion [w, x, y, z] |
| `collisions[]` | array | List of collisions at this waypoint (empty if none) |

**`collisions[]` object:**

| Field | Type | Description |
|-------|------|-------------|
| `obstacle_id` | string | ID of colliding obstacle |
| `link` | string | Robot link that collided (`link_1` to `link_6`) |
| `penetration_depth` | float | Collision depth in mm |
| `contact_point` | float[3] | Collision location in mm [x, y, z] |

**`stats` object:**

| Field | Type | Description |
|-------|------|-------------|
| `total_waypoints` | integer | Number of trajectory waypoints |
| `duration_seconds` | float | Total trajectory duration |
| `collisions_detected` | integer | Total collision count |
| `ik_failures` | integer | Number of IK solve failures |
| `computation_time_ms` | integer | Server-side computation time |

**Status Codes:**
- `200 OK` - Simulation successful
- `400 Bad Request` - Invalid robot ID, empty AST, or malformed request
- `422 Unprocessable Entity` - Pydantic validation error
- `500 Internal Server Error` - IK solver crash, PyBullet error

**Error Example:**

```json
{
  "detail": "IK solver failed to find solution for target at [500, 0, 600]. Target may be out of reach.",
  "error_code": "IK_FAILURE"
}
```

**Example:**

```bash
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "robot_id": "irb4600",
    "ast": [...],
    "obstacles": []
  }'
```

---

## Data Types

### AST Node Types

**MoveL (Linear Move):**

```json
{
  "type": "MoveL",
  "target": RobTarget | JointTarget,
  "speed": SpeedData,
  "zone": ZoneData
}
```

**MoveJ (Joint Move):**

```json
{
  "type": "MoveJ",
  "target": RobTarget | JointTarget,
  "speed": SpeedData,
  "zone": ZoneData
}
```

**MoveC (Circular Move):**

```json
{
  "type": "MoveC",
  "via_point": RobTarget,
  "target": RobTarget,
  "speed": SpeedData,
  "zone": ZoneData
}
```

**RobTarget (Cartesian Target):**

```json
{
  "type": "RobTarget",
  "trans": [x, y, z],           // Position in mm
  "rot": [q1, q2, q3, q4],      // Orientation quaternion
  "robconf": [cf1, cf4, cf6, cfx], // Robot configuration flags
  "extax": [eax_a, eax_b, eax_c, eax_d, eax_e, eax_f] // External axes
}
```

**JointTarget (Joint-Space Target):**

```json
{
  "type": "JointTarget",
  "robax": [j1, j2, j3, j4, j5, j6], // Joint angles in degrees
  "extax": [eax_a, eax_b, eax_c, eax_d, eax_e, eax_f] // External axes
}
```

**SpeedData:**

```json
{
  "type": "SpeedData",
  "v_tcp": 1000.0,    // TCP speed in mm/s
  "v_ori": 500.0,     // Orientation speed in deg/s
  "v_leax": 5000.0,   // Linear external axes speed (optional)
  "v_reax": 1000.0    // Rotational external axes speed (optional)
}
```

**ZoneData:**

```json
{
  "type": "ZoneData",
  "finep": false,         // Fine point (true = stop exactly at target)
  "pzone_tcp": 10.0,      // TCP path zone radius in mm
  "pzone_ori": 5.0,       // Orientation zone radius in degrees
  "pzone_eax": 50.0,      // External axes zone radius (optional)
  "zone_ori": 5.0,        // Orientation zone radius (optional)
  "zone_leax": 50.0,      // Linear external axes zone (optional)
  "zone_reax": 5.0        // Rotational external axes zone (optional)
}
```

---

## Rate Limiting

**MVP:** No rate limiting.

**Post-MVP:** Consider:
- 100 requests/minute per IP for `/api/simulate`
- 1000 requests/minute per IP for all other endpoints

---

## CORS Policy

**Development:**

```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production:**

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://abb-sim.example.com"],  # Restrict to frontend domain
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)
```

---

## Versioning

**Current:** API version 1.0 (no version prefix in URL for MVP)

**Future:** Consider `/api/v1/`, `/api/v2/` for breaking changes

---

## Testing Endpoints

Use FastAPI's built-in Swagger UI for interactive testing:

**Development:** `http://localhost:8000/docs`

**ReDoc:** `http://localhost:8000/redoc` (alternative documentation UI)

---

## Example Workflow

**Complete simulation workflow from frontend:**

```typescript
// 1. Get available robots
const robots = await axios.get('/api/robots');
console.log(robots.data); // [{id: 'irb4600', ...}]

// 2. Load robot 3D model
const robotId = 'irb4600';
const mesh = await BABYLON.SceneLoader.ImportMeshAsync(
  "", `/api/robots/${robotId}/model`, "", scene
);

// 3. Upload RAPID program
const formData = new FormData();
formData.append('file', rapidFile);
const parseResponse = await axios.post('/api/upload/rapid', formData);
const ast = parseResponse.data.ast;

// 4. Upload obstacle (optional)
const obstacleFormData = new FormData();
obstacleFormData.append('file', stlFile);
obstacleFormData.append('position', JSON.stringify([500, 0, 0]));
const obstacleResponse = await axios.post('/api/upload/obstacle', obstacleFormData);
const obstacleId = obstacleResponse.data.obstacle_id;

// 5. Run simulation
const simulationResponse = await axios.post('/api/simulate', {
  robot_id: robotId,
  ast: ast,
  obstacles: [{obstacle_id: obstacleId, position: [500, 0, 0], rotation: [0, 0, 0]}]
});

// 6. Animate trajectory
const trajectory = simulationResponse.data.trajectory;
for (const waypoint of trajectory) {
  setJointAngles(robotMesh, waypoint.joints);
  await sleep(waypoint.timestamp * 1000 / playbackSpeed);
}
```

---

**Last Updated:** 2026-02-05
**Approved by:** Noah (PM/QA Lead)
**Next Review:** End of Week 2

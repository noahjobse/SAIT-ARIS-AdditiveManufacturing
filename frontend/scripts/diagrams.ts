export const diagrams = {
  'rapid-upload-parse': `
sequenceDiagram
    actor User
    participant Frontend as Frontend<br/>(React)
    participant API as Backend API<br/>(FastAPI)
    participant Validator as File Validator
    participant Parser as RAPID Parser<br/>(Lark)

    User->>Frontend: Upload .mod file (drag & drop)
    Frontend->>Frontend: Validate file type & size
    Frontend->>API: POST /api/upload/rapid<br/>(multipart/form-data)

    API->>Validator: Check file extension (.mod)
    API->>Validator: Check file size (<1MB)

    alt File validation fails
        Validator-->>API: ValidationError
        API-->>Frontend: 400 Bad Request<br/>{error_code: "INVALID_FILE_TYPE"}
        Frontend->>User: Show error message
    else File valid
        API->>Parser: Parse RAPID code
        Parser->>Parser: Lexer: Tokenize
        Parser->>Parser: Parser: Build parse tree
        Parser->>Parser: Transformer: Generate AST

        alt Parse error
            Parser-->>API: ParseError with line number
            API-->>Frontend: 400 Bad Request<br/>{errors: [{line, message}]}
            Frontend->>Frontend: Highlight error lines
            Frontend->>User: Show syntax errors
        else Parse success
            Parser-->>API: AST + warnings
            API-->>Frontend: 200 OK<br/>{ast, errors: [], warnings}
            Frontend->>Frontend: Store AST in state
            Frontend->>User: Show "Ready to simulate"
        end
    end
`,

  'obstacle-management': `
sequenceDiagram
    actor User
    participant Frontend as Frontend<br/>(React + Babylon.js)
    participant API as Backend API<br/>(FastAPI)
    participant Scene as Babylon Scene
    participant Storage as File Storage

    rect rgb(240, 248, 255)
    Note over User,Storage: Upload Obstacle
    User->>Frontend: Upload .stl file
    Frontend->>API: POST /api/upload/obstacle<br/>(file, position, rotation)
    API->>Storage: Save STL file
    API->>API: Parse STL mesh
    API->>API: Calculate bounds & stats
    API-->>Frontend: {obstacle_id, filename, bounds}
    Frontend->>Scene: Load mesh into Babylon
    Scene->>Scene: Create mesh from vertices
    Scene->>Scene: Apply position & rotation
    Scene-->>Frontend: Mesh ready
    Frontend->>User: Show obstacle in viewport
    end

    rect rgb(255, 250, 240)
    Note over User,Storage: Transform Obstacle
    User->>Frontend: Drag gizmo (move/rotate)
    Frontend->>Scene: Update mesh transform
    Scene-->>Frontend: Transform applied
    Frontend->>API: PUT /api/obstacles/{id}/transform<br/>{position, rotation}
    API->>Storage: Update obstacle metadata
    API-->>Frontend: 200 OK
    Frontend->>User: Transform confirmed
    end

    rect rgb(255, 240, 245)
    Note over User,Storage: Delete Obstacle
    User->>Frontend: Click delete button
    Frontend->>API: DELETE /api/obstacles/{id}
    API->>Storage: Remove STL file
    API-->>Frontend: {deleted: true}
    Frontend->>Scene: Remove mesh from scene
    Scene-->>Frontend: Mesh removed
    Frontend->>User: Obstacle removed from viewport
    end
`,

  'playback-controls': `
sequenceDiagram
    actor User
    participant Controls as Playback Controls<br/>(React UI)
    participant State as Animation State
    participant Scene as Babylon Scene
    participant Robot as Robot Mesh

    rect rgb(240, 255, 240)
    Note over User,Robot: Initial Load
    User->>Controls: Click "Simulate"
    Controls->>State: Load trajectory data
    State->>State: Set currentFrame = 0
    State->>State: Set isPlaying = false
    State-->>Controls: Ready
    Controls->>User: Enable playback controls
    end

    rect rgb(255, 248, 240)
    Note over User,Robot: Play Animation
    User->>Controls: Click Play
    Controls->>State: Set isPlaying = true
    State->>State: Start animation loop

    loop Every frame (60 FPS)
        State->>State: Increment currentFrame
        State->>Scene: Update robot pose
        Scene->>Robot: Apply joint rotations
        Robot-->>Scene: Render updated pose

        alt Collision at frame
            State->>Scene: Apply red material
            Scene->>Robot: Highlight in red
        end

        State->>Controls: Update timeline position
        Controls->>User: Show progress

        alt Reached end of trajectory
            State->>State: Set isPlaying = false
            State-->>Controls: Animation complete
        end
    end
    end

    rect rgb(240, 245, 255)
    Note over User,Robot: Scrub Timeline
    User->>Controls: Drag timeline scrubber
    Controls->>State: Set currentFrame = scrubValue
    State->>Scene: Jump to frame
    Scene->>Robot: Apply frame pose instantly
    Robot-->>Scene: Pose updated
    Scene-->>Controls: Frame rendered
    Controls->>User: Show robot at scrubbed position
    end

    rect rgb(255, 245, 240)
    Note over User,Robot: Speed Control
    User->>Controls: Change speed (0.25x - 2x)
    Controls->>State: Set playbackSpeed
    State->>State: Adjust frame increment
    State-->>Controls: Speed updated
    Controls->>User: Show speed indicator
    end
`,

  'end-to-end-flow': `
sequenceDiagram
    actor User
    participant Frontend as Frontend<br/>(React + Babylon.js)
    participant API as Backend API<br/>(FastAPI)
    participant Parser as RAPID Parser<br/>(Lark)
    participant PyBullet as PyBullet<br/>(IK + Collision)

    User->>Frontend: Upload RAPID file
    Frontend->>API: POST /api/upload/rapid
    API->>Parser: Parse RAPID code
    Parser->>Parser: Lexer → Tokens
    Parser->>Parser: Parser → AST
    Parser-->>API: AST + validation errors
    API-->>Frontend: {ast, errors}
    Frontend->>User: Show errors (if any)

    User->>Frontend: Click "Simulate"
    Frontend->>API: POST /api/simulate<br/>{robot_id, ast, obstacles}

    API->>PyBullet: Load robot URDF
    API->>PyBullet: Load obstacle meshes

    loop For each movement command
        API->>PyBullet: Compute target TCP pose
        PyBullet->>PyBullet: Run IK solver
        PyBullet-->>API: Joint angles
        API->>API: Interpolate waypoints
        API->>PyBullet: Check collision at waypoints
        PyBullet-->>API: Collision results
    end

    API-->>Frontend: {trajectory: [{joints, tcp_pose, collisions}]}
    Frontend->>Frontend: Load trajectory into Babylon.js
    Frontend->>User: Animate robot (60 FPS)

    alt Collision detected
        Frontend->>Frontend: Highlight robot in red
        Frontend->>User: Show collision warning
    end
`
} as const;

export type DiagramName = keyof typeof diagrams;

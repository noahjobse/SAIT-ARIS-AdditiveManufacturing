import { Engine, Scene, ArcRotateCamera, Vector3, HemisphericLight, MeshBuilder, ImportMeshAsync, Color3, TransformNode, Quaternion } from "@babylonjs/core";
import { registerBuiltInLoaders } from "@babylonjs/loaders/dynamic";
import { GridMaterial } from "@babylonjs/materials/grid";

type JointControls = {
    engine: Engine;
    scene: Scene;
    setJointAngle: (jointIndex: number, angleRad: number) => void;
    dispose: () => void;
};

function createEngineAndScene(canvas: HTMLCanvasElement): { engine: Engine; scene: Scene } {
    const engine = new Engine(canvas, true, {stencil: true});
    const scene = new Scene(engine);
    return { engine, scene };
}

function createCameraAndLight(scene: Scene, canvas: HTMLCanvasElement) {
    var camera: ArcRotateCamera = new ArcRotateCamera("Camera", Math.PI / 2, Math.PI / 2, 6, new Vector3(0, 1, 0), scene);
    camera.attachControl(canvas, true);
    camera.wheelPrecision = 100;            // for gradual zoom
    camera.wheelDeltaPercentage = 0.01;
    camera.inertia = 0.85; 

    new HemisphericLight("light1", new Vector3(1, 1, 0), scene);

    return { camera };
}

function createGroundGrid(scene: Scene) {
    var ground = MeshBuilder.CreateGround("ground", {width: 6, height: 6}, scene);
    
    const gridMat = new GridMaterial("gridMat", scene);
    gridMat.majorUnitFrequency = 5;         // thicker line every N cells
    gridMat.minorUnitVisibility = 0.75;     // faint small lines
    gridMat.gridRatio = 1;                  // cell size
    gridMat.backFaceCulling = false;

    gridMat.mainColor = new Color3(0.05, 0.05, 0.05); 
    gridMat.lineColor = Color3.White();                          
    gridMat.opacity = 0.98;     

    ground.material = gridMat;
    return {ground, gridMat};
}

async function loadRobotModel(scene: Scene, modelPath: string) {
    const robotModel = await ImportMeshAsync(modelPath, scene);
    console.log("Model loaded:", robotModel);
    return robotModel;
}

function extractBaseAndLinks(scene: Scene) {
    // Find parent mesh containing robot Base + Link1-6
    const baseNode = scene.getTransformNodeByName("Base");
    const parentMesh = baseNode?.parent as TransformNode | null
    
    if (!parentMesh) throw new Error("Could not find parent mesh containing the robot Base/Links.");
  

    // Treat child meshes (Base + Link1-6) as TransformNodes for reparenting and transformations
    const childByName = new Map(
        parentMesh.getChildren().map((child) => [child.name, child as TransformNode])
    );

    const base = childByName.get("Base");
    const links = [1, 2, 3, 4, 5, 6].map(i => childByName.get(`Link${i}`));

    if (!base || links.some((x) => !x)) throw new Error("Base or one or more links not found.");

    return { parentMesh, base, links: links as TransformNode[] };
}

// Keep child world transformation (PRS --> position, rotation, scaling) unchanged when reparenting
// Compute child's new local matrix so its world transform stays the same
// Formula: childLocalMatrix = childWorldMatrix * inverse(parentWorldMatrix)
function reparentKeepWorld(scene: Scene, parent: TransformNode, child: TransformNode) {
    scene.render();

    const childWorldMtx = child.getWorldMatrix().clone();

    child.setParent(parent);

    const parentWorldInvMtx = parent.getWorldMatrix().clone();
    parentWorldInvMtx.invert(); // Reverse what parent is doing to child in world space
    const localMtx = childWorldMtx.multiply(parentWorldInvMtx);

    // Break down child local matrix into PRS
    const scalingVec = new Vector3();
    const rotationQua = new Quaternion();
    const positionVec = new Vector3();
    localMtx.decompose(scalingVec, rotationQua, positionVec);

    child.scaling = scalingVec;
    child.rotationQuaternion = rotationQua;
    child.position = positionVec;
}

// Match joint position toa specific world joint center (instead of relative to parent)
function setWorldPosition(scene: Scene, node: TransformNode, worldPos: Vector3) {
    scene.render();

    const parent = node.parent as TransformNode | null;
    if (!parent) {
        node.position.copyFrom(worldPos);
        return;
    }

    const invParentWorldMtx = parent.getWorldMatrix().clone();
    invParentWorldMtx.invert();

    node.position = Vector3.TransformCoordinates(worldPos, invParentWorldMtx);
}

// Create pivot points/nodes (joints) at node's current world position
function createPivot(scene: Scene, name: string, atNode: TransformNode) {
    const pivot = new TransformNode(name, scene);

    pivot.position = atNode.getAbsolutePosition().clone();
    pivot.rotationQuaternion = Quaternion.Identity();

    return pivot;
}

function buildJoints(scene: Scene, base: TransformNode, links: TransformNode[]) {
    // Create pivots for each joint (Base + Link1-6)
    const basePivot = createPivot(scene, "pivot_base", base!);
    const joints = links!.map((link, i) =>
        createPivot(scene, `pivot_j${i + 1}`, link!)
    );

    // For correcting J6 pivot position
    const j6 = joints[5]; 
    const link6 = links[5];

    // Parent pivots/joints to form a chain
    let prev = basePivot;
    joints.forEach((joint) => {
        reparentKeepWorld(scene, prev, joint);
        prev = joint;
    });

    // Parent Base + Link1-5 (leave Link6 until after J6 is correctly positioned)
    reparentKeepWorld(scene, basePivot, base!);
    for (let i = 0; i < links.length - 1; i++) {
        reparentKeepWorld(scene, joints[i], links[i]!);
    }

    // Correct J6 pivot position to match the wrist joint center (instead of relative to Link5)
    const link6Mesh = link6!.getChildMeshes()[0];
    const bb = link6Mesh.getBoundingInfo().boundingBox;
    const link6CenterWorld = bb.centerWorld.clone();

    // Move j6 to that world space joint location (changes rotation center, not hierarchy)
    setWorldPosition(scene, j6, link6CenterWorld);
    reparentKeepWorld(scene, j6, link6!);

    return { basePivot, joints };
}

function computeJointAxes(links: TransformNode[]) {
    // Rotate joints with absolute angles (in world space)
    const jointAxes: Vector3[] = [
        Vector3.Up(),           // j1 rotates around Y-axis 
        Vector3.Forward(),      // j2 rotates around Z-axis 
        Vector3.Forward(),      // j3 rotates around Z-axis 
        Vector3.Right(),        // j4 rotates around X-axis 
        Vector3.Forward(),      // j5 rotates around Z-axis 
        Vector3.Right(),        // j6 rotates around X-axis 
    ];


    // Align J6 rotation axis to Link6's current orientation (or else it's slightly off)
    const link6 = links[5];
    const j6AxisWorldMtx = Vector3.TransformNormal(Vector3.Forward(), link6!.getWorldMatrix()).normalize();
    jointAxes[5] = j6AxisWorldMtx;

    return jointAxes;
}



async function createRobotScene(canvas: HTMLCanvasElement, modelPath: string): Promise<JointControls> {
    registerBuiltInLoaders();

    const { engine, scene } = createEngineAndScene(canvas);

    createCameraAndLight(scene, canvas);
    createGroundGrid(scene);

    // Load .glb model file from folder
    await loadRobotModel(scene, modelPath);
    
    // Extract robot base and links from the imported model
    const { base, links } = extractBaseAndLinks(scene);

    // Reparent robot nodes and create joints
    const { joints } = buildJoints(scene, base, links);

    const jointAxes = computeJointAxes(links);
    const jointAngles = [0, 0, 0, 0, 0, 0]; // Using radians!!

    // Store rest position so sliders rotate relative to initial orientation
    const restRotation = joints.map((p) => (p.rotationQuaternion ? p.rotationQuaternion.clone() : Quaternion.Identity()));


    // Set joint angle and update robot pose
    // Formula: absoluteRotation = restRotation * rotationAroundAxis(angle)
    function setJointAngle(jointIndex: number, angleRad: number) {
        jointAngles[jointIndex] = angleRad;

        const joint = joints[jointIndex];
        const jointAxis = jointAxes[jointIndex];
        const q = Quaternion.RotationAxis(jointAxis, angleRad);

        joint.rotationQuaternion = restRotation[jointIndex].multiply(q);
    }


    // Hide/show the Inspector
    window.addEventListener("keydown", (ev) => {
        // Shift+Ctrl+Alt+I
        if (ev.shiftKey && ev.ctrlKey && ev.altKey && (ev.key === "I" || ev.key === "i")) {
            if (scene.debugLayer.isVisible()) {
                scene.debugLayer.hide();
            } else {
                scene.debugLayer.show();
            }
        }
    });


    // Run the main render loop
    engine.runRenderLoop(() => {
        scene.render();
        
    });

    window.addEventListener("resize", () => {
        engine.resize();
    });

    function dispose() {
        engine.stopRenderLoop();
        scene.dispose();
        engine.dispose();
    }

    return { engine, scene, setJointAngle, dispose };
}

export default createRobotScene;
export type { JointControls };
import { Engine, Scene, ArcRotateCamera, Vector3, HemisphericLight, MeshBuilder, ImportMeshAsync, Color3, TransformNode, Quaternion, Color4, StandardMaterial } from "@babylonjs/core";
import { registerBuiltInLoaders } from "@babylonjs/loaders/dynamic";
import { GridMaterial } from "@babylonjs/materials/grid";

export type JointControls = {
    engine: Engine;
    scene: Scene;
    setJointAngle: (jointIndex: number, angleRad: number) => void;
    dispose: () => void;
};

function createEngineAndScene(canvas: HTMLCanvasElement): { engine: Engine; scene: Scene } {
    const engine = new Engine(canvas, true, { stencil: true });
    const scene = new Scene(engine);
    scene.clearColor = new Color4(0, 0, 0, 0);
    return { engine, scene };
}

function createCameraAndLight(scene: Scene, canvas: HTMLCanvasElement) {
    const camera = new ArcRotateCamera("Camera", Math.PI / 2, Math.PI / 2.4, 6, new Vector3(0, 1, 0), scene);
    camera.attachControl(canvas, true);
    camera.wheelPrecision = 100;
    camera.wheelDeltaPercentage = 0.01;
    camera.inertia = 0.85;

    new HemisphericLight("light1", new Vector3(1, 1, 0), scene);

    return { camera };
}

function createGroundGrid(scene: Scene) {
    const ground = MeshBuilder.CreateGround("ground", { width: 6, height: 6 }, scene);

    try {
        const gridMat = new GridMaterial("gridMat", scene);
        gridMat.majorUnitFrequency = 5;
        gridMat.minorUnitVisibility = 0.75;
        gridMat.gridRatio = 1;
        gridMat.backFaceCulling = false;
        gridMat.mainColor = new Color3(0.2, 0.2, 0.2);
        gridMat.lineColor = new Color3(0.8, 0.8, 0.8);
        gridMat.opacity = 0.99;
        ground.material = gridMat;
    } catch {
        const fallbackMat = new StandardMaterial("fallbackMat", scene);
        fallbackMat.diffuseColor = new Color3(0.5, 0.5, 0.5);
        fallbackMat.alpha = 0.5;
        fallbackMat.specularColor = new Color3(0, 0, 0);
        ground.material = fallbackMat;
    }
}

function extractBaseAndLinks(scene: Scene) {
    const baseNode = scene.getTransformNodeByName("Base");
    if (!baseNode) return null;

    const parentMesh = baseNode.parent as TransformNode | null;
    if (!parentMesh) return null;

    const childByName = new Map(
        parentMesh.getChildren().map((child) => [child.name, child as TransformNode])
    );

    const base = childByName.get("Base");
    const links = [1, 2, 3, 4, 5, 6].map(i => childByName.get(`Link${i}`));

    if (!base || links.some((x) => !x)) return null;

    return { parentMesh, base, links: links as TransformNode[] };
}

function createPivot(scene: Scene, name: string, atNode: TransformNode) {
    const pivot = new TransformNode(name, scene);
    pivot.setAbsolutePosition(atNode.getAbsolutePosition());
    pivot.rotationQuaternion = Quaternion.Identity();
    return pivot;
}

function buildJoints(scene: Scene, base: TransformNode, links: TransformNode[]) {
    const basePivot = createPivot(scene, "pivot_base", base);
    const joints = links.map((link, i) =>
        createPivot(scene, `pivot_j${i + 1}`, link)
    );

    const j6 = joints[5];
    const link6 = links[5];

    let prev: TransformNode = basePivot;
    joints.forEach((joint) => {
        joint.setParent(prev, true);
        prev = joint;
    });

    base.setParent(basePivot, true);
    for (let i = 0; i < links.length - 1; i++) {
        links[i].setParent(joints[i], true);
    }

    const link6Mesh = link6.getChildMeshes()[0];
    const bb = link6Mesh.getBoundingInfo().boundingBox;
    j6.setAbsolutePosition(bb.centerWorld);
    link6.setParent(j6, true);

    return { basePivot, joints };
}

function computeJointAxes(links: TransformNode[]) {
    const jointAxes: Vector3[] = [
        Vector3.Up(),
        Vector3.Forward(),
        Vector3.Forward(),
        Vector3.Right(),
        Vector3.Forward(),
        Vector3.Right(),
    ];

    const link6 = links[5];
    const j6AxisWorldMtx = Vector3.TransformNormal(Vector3.Forward(), link6.getWorldMatrix()).normalize();
    jointAxes[5] = j6AxisWorldMtx;

    return jointAxes;
}

export async function createRobotScene(canvas: HTMLCanvasElement, modelPath: string | null): Promise<JointControls> {
    registerBuiltInLoaders();

    const { engine, scene } = createEngineAndScene(canvas);
    createCameraAndLight(scene, canvas);
    createGroundGrid(scene);

    engine.runRenderLoop(() => {
        scene.render();
    });

    const resizeHandler = () => engine.resize();
    window.addEventListener("resize", resizeHandler);

    const keydownHandler = (ev: KeyboardEvent) => {
        if (ev.shiftKey && ev.ctrlKey && ev.altKey && (ev.key === "I" || ev.key === "i")) {
            if (scene.debugLayer.isVisible()) {
                scene.debugLayer.hide();
            } else {
                scene.debugLayer.show();
            }
        }
    };
    window.addEventListener("keydown", keydownHandler);

    if (modelPath) {
        try {
            await ImportMeshAsync(modelPath, scene);
            const extracted = extractBaseAndLinks(scene);

            if (extracted) {
                const { base, links } = extracted;
                const { joints } = buildJoints(scene, base, links);
                const jointAxes = computeJointAxes(links);
                const restRotation = joints.map((p) =>
                    p.rotationQuaternion ? p.rotationQuaternion.clone() : Quaternion.Identity()
                );

                const setJointAngle = (jointIndex: number, angleRad: number) => {
                    const joint = joints[jointIndex];
                    const jointAxis = jointAxes[jointIndex];
                    const q = Quaternion.RotationAxis(jointAxis, angleRad);
                    joint.rotationQuaternion = restRotation[jointIndex].multiply(q);
                };

                const dispose = () => {
                    engine.stopRenderLoop();
                    window.removeEventListener("keydown", keydownHandler);
                    window.removeEventListener("resize", resizeHandler);
                    scene.dispose();
                    engine.dispose();
                };

                return { engine, scene, setJointAngle, dispose };
            }
        } catch (err) {
            console.error("Error loading robot model:", err);
        }
    }

    const dispose = () => {
        engine.stopRenderLoop();
        window.removeEventListener("keydown", keydownHandler);
        window.removeEventListener("resize", resizeHandler);
        scene.dispose();
        engine.dispose();
    };

    return { engine, scene, setJointAngle: () => {}, dispose };
}

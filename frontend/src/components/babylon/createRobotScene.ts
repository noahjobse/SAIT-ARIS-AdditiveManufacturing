import { Engine, Scene, ArcRotateCamera, Vector3, HemisphericLight, MeshBuilder, ImportMeshAsync, Color3, TransformNode, Quaternion, Color4, StandardMaterial, SolidParticleSystem } from "@babylonjs/core";
import { registerBuiltInLoaders } from "@babylonjs/loaders/dynamic";
import { GridMaterial } from "@babylonjs/materials/grid";

export type JointControls = {
    engine: Engine;
    scene: Scene;
    setJointAngle: (jointIndex: number, angleRad: number) => void;
    setAngles?: (anglesDeg: number[]) => void;
    getJointLimits?: () => { min: number; max: number }[] | undefined;
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

function createStarfield(scene: Scene) {
    const starCount = 800;
    const spread = 40;

    const starMesh = MeshBuilder.CreateIcoSphere("starModel", { radius: 0.02, subdivisions: 1 }, scene);
    starMesh.isVisible = false;

    const sps = new SolidParticleSystem("starfield", scene);
    sps.addShape(starMesh, starCount);
    const mesh = sps.buildMesh();
    starMesh.dispose();

    const starMat = new StandardMaterial("starMat", scene);
    starMat.emissiveColor = new Color3(1, 1, 1);
    starMat.disableLighting = true;
    mesh.material = starMat;

    sps.initParticles = () => {
        for (let i = 0; i < sps.nbParticles; i++) {
            const p = sps.particles[i];
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos(2 * Math.random() - 1);
            const r = spread * (0.5 + Math.random() * 0.5);
            p.position.x = r * Math.sin(phi) * Math.cos(theta);
            p.position.y = r * Math.sin(phi) * Math.sin(theta);
            p.position.z = r * Math.cos(phi);
            const s = 0.5 + Math.random() * 2.0;
            p.scaling.setAll(s);
        }
    };

    sps.initParticles();
    sps.setParticles();
    sps.isAlwaysVisible = true;
    mesh.freezeWorldMatrix();
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
    createStarfield(scene);

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

                const setAngles = (anglesDeg: number[]) => {
                    anglesDeg.forEach((angleDeg, i) => {
                        if (i < joints.length) {
                            setJointAngle(i, angleDeg * (Math.PI / 180));
                        }
                    });
                };

                const getJointLimits = () => {
                    // Default realistic limits for typical ABB 6-axis robots
                    return [
                        { min: -180, max: 180 }, // J1
                        { min: -90, max: 150 },  // J2
                        { min: -180, max: 75 },  // J3
                        { min: -400, max: 400 }, // J4
                        { min: -125, max: 120 }, // J5
                        { min: -400, max: 400 }, // J6
                    ];
                };

                const dispose = () => {
                    engine.stopRenderLoop();
                    window.removeEventListener("keydown", keydownHandler);
                    window.removeEventListener("resize", resizeHandler);
                    scene.dispose();
                    engine.dispose();
                };

                return { engine, scene, setJointAngle, setAngles, getJointLimits, dispose };
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

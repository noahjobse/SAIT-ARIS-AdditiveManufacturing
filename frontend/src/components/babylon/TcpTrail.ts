import { Scene, Vector3, Color3, MeshBuilder, StandardMaterial, Mesh } from "@babylonjs/core";

// tcp_pose.position arrives in mm, PyBullet Z-up convention.
// Convert to Babylon.js Y-up meters: (x, y, z) → Vector3(x/1000, z/1000, y/1000)
function toScene(positionMm: number[]): Vector3 {
    return new Vector3(-positionMm[0] / 1000, positionMm[2] / 1000, positionMm[1] / 1000);
}

const TUBE_RADIUS = 0.003; // 3mm visible tube
const MIN_DIST_SQ = (0.5 / 1000) ** 2; // 0.5mm

export class TcpTrail {
    private scene: Scene;
    private segments: Vector3[][] = [];
    private meshes: (Mesh | null)[] = [];
    private material: StandardMaterial;
    private lastWasPenDown = false;
    private meshCounter = 0;

    constructor(scene: Scene) {
        this.scene = scene;
        this.material = new StandardMaterial("tcpTrailMat", scene);
        this.material.emissiveColor = new Color3(0, 1, 1); // cyan, self-lit
        this.material.disableLighting = true;
    }

    addPoint(positionMm: number[], penDown: boolean): void {
        if (!penDown) {
            this.lastWasPenDown = false;
            return;
        }

        const point = toScene(positionMm);
        const needNewSegment = this.segments.length === 0 || !this.lastWasPenDown;

        if (needNewSegment) {
            this.segments.push([point]);
            this.meshes.push(null);
            this.lastWasPenDown = true;
            return;
        }

        const current = this.segments[this.segments.length - 1];
        const prev = current[current.length - 1];

        if (Vector3.DistanceSquared(prev, point) < MIN_DIST_SQ) return;

        current.push(point);
        this.lastWasPenDown = true;

        if (current.length < 2) return;

        const idx = this.segments.length - 1;
        this.meshes[idx]?.dispose();

        const path = current;
        const mesh = MeshBuilder.CreateTube(
            `tcpTrail_${this.meshCounter++}`,
            { path, radius: TUBE_RADIUS, tessellation: 6, cap: Mesh.NO_CAP, updatable: false },
            this.scene,
        );
        mesh.material = this.material;
        this.meshes[idx] = mesh;
    }

    clear(): void {
        for (const mesh of this.meshes) {
            mesh?.dispose();
        }
        this.segments = [];
        this.meshes = [];
        this.lastWasPenDown = false;
    }

    dispose(): void {
        this.clear();
        this.material.dispose();
    }
}

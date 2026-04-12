import { Scene, Vector3, Color3, MeshBuilder, StandardMaterial, Mesh } from "@babylonjs/core";

// Same coordinate conversion as TcpTrail:
// tcp_pose.position arrives in mm, PyBullet Z-up → Babylon Y-up meters
function toScene(positionMm: number[]): Vector3 {
    return new Vector3(-positionMm[0] / 1000, positionMm[2] / 1000, positionMm[1] / 1000);
}

const BEAD_RADIUS = 0.002;        // 2mm — exaggerated for visibility
const MIN_DIST_SQ = (0.3 / 1000) ** 2; // 0.3mm minimum segment

export type HeatmapMode = "none" | "speed" | "layer";

export class ExtrusionTrail {
    private scene: Scene;
    private segments: Vector3[][] = [];
    private meshes: (Mesh | null)[] = [];
    private material: StandardMaterial;
    private heatmapCache: Map<string, StandardMaterial> = new Map();
    private meshCounter = 0;
    private lastExtrusion = 0;
    private wasExtruding = false;
    private currentMode: HeatmapMode = "none";

    constructor(scene: Scene) {
        this.scene = scene;
        this.material = new StandardMaterial("extrusionMat", scene);
        this.material.diffuseColor = new Color3(1.0, 0.55, 0.0);  // PLA orange
        this.material.specularColor = new Color3(0.3, 0.15, 0.0);
    }

    /**
     * Add a point to the extrusion trail.
     * Automatically determines if extruding based on delta-E.
     */
    addPoint(positionMm: number[], cumulativeExtrusion: number): void {
        const deltaE = cumulativeExtrusion - this.lastExtrusion;
        this.lastExtrusion = cumulativeExtrusion;

        if (deltaE < 0.01) {
            // Travel move — no extrusion
            this.wasExtruding = false;
            return;
        }

        const point = toScene(positionMm);

        if (!this.wasExtruding) {
            // Transition from travel → extrusion: start new segment
            this.segments.push([point]);
            this.meshes.push(null);
            this.wasExtruding = true;
            return;
        }

        // Continue current extrusion segment
        const current = this.segments[this.segments.length - 1];
        const prev = current[current.length - 1];

        if (Vector3.DistanceSquared(prev, point) < MIN_DIST_SQ) return;

        current.push(point);

        if (current.length < 2) return;

        // Rebuild tube mesh for this segment
        const idx = this.segments.length - 1;
        this.meshes[idx]?.dispose();

        const mesh = MeshBuilder.CreateTube(
            `extrusion_${this.meshCounter++}`,
            { path: current, radius: BEAD_RADIUS, tessellation: 6, cap: Mesh.NO_CAP, updatable: false },
            this.scene,
        );
        mesh.material = this._getMaterialForSegment(idx);
        this.meshes[idx] = mesh;
    }

    setHeatmapMode(mode: HeatmapMode): void {
        this.currentMode = mode;
        // Recolor all existing meshes
        for (let i = 0; i < this.meshes.length; i++) {
            const mesh = this.meshes[i];
            if (mesh) {
                mesh.material = this._getMaterialForSegment(i);
            }
        }
    }

    clear(): void {
        for (const mesh of this.meshes) mesh?.dispose();
        this.segments = [];
        this.meshes = [];
        this.lastExtrusion = 0;
        this.wasExtruding = false;
    }

    dispose(): void {
        this.clear();
        this.material.dispose();
        for (const mat of this.heatmapCache.values()) mat.dispose();
        this.heatmapCache.clear();
    }

    private _getMaterialForSegment(segmentIdx: number): StandardMaterial {
        if (this.currentMode === "none") {
            return this.material;
        }

        if (this.currentMode === "layer") {
            // Color by average Y position (height) of segment
            const seg = this.segments[segmentIdx];
            if (!seg || seg.length === 0) return this.material;
            const avgY = seg.reduce((sum, v) => sum + v.y, 0) / seg.length;
            const maxY = this._getMaxHeight();
            const t = maxY > 0 ? Math.min(1, avgY / maxY) : 0;
            const hue = t * 270; // red(0) → violet(270)
            return this._getOrCreateMaterial(`layer_${Math.round(hue)}`, hue);
        }

        // "speed" mode — use segment length as proxy for speed (longer = faster)
        const seg = this.segments[segmentIdx];
        if (!seg || seg.length < 2) return this.material;
        let totalLen = 0;
        for (let i = 1; i < seg.length; i++) {
            totalLen += Vector3.Distance(seg[i - 1], seg[i]);
        }
        const avgSegLen = totalLen / (seg.length - 1);
        const t = Math.min(1, avgSegLen / 0.005); // normalize
        const hue = (1 - t) * 240; // blue(slow) → red(fast)
        return this._getOrCreateMaterial(`speed_${Math.round(hue)}`, hue);
    }

    private _getMaxHeight(): number {
        let maxY = 0;
        for (const seg of this.segments) {
            for (const v of seg) {
                if (v.y > maxY) maxY = v.y;
            }
        }
        return maxY;
    }

    private _getOrCreateMaterial(key: string, hue: number): StandardMaterial {
        let mat = this.heatmapCache.get(key);
        if (mat) return mat;

        mat = new StandardMaterial(`extHeat_${key}`, this.scene);
        const color = Color3.FromHSV(hue, 0.9, 1.0);
        mat.diffuseColor = color;
        mat.specularColor = new Color3(0.2, 0.2, 0.2);
        this.heatmapCache.set(key, mat);
        return mat;
    }
}

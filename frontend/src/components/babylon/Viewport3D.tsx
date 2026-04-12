"use client";

import { useRef, useEffect, useCallback, useState } from "react";
import type { JointControls } from "./createRobotScene";
import type { HeatmapMode } from "./ExtrusionTrail";

export type TrailControls = {
  addTrailPoint: (pos: number[], penDown: boolean) => void;
  clearTrail: () => void;
  addExtrusionPoint?: (pos: number[], cumulativeExtrusion: number) => void;
  clearExtrusion?: () => void;
  setHeatmapMode?: (mode: HeatmapMode) => void;
  loadStlPreview?: (blobUrl: string) => Promise<void>;
  clearStlPreview?: () => void;
};

type Viewport3DProps = {
  modelPath: string | null;
  anglesDeg: number[];
  stlPreviewUrl?: string | null;
  onJointLimitsExtracted?: (limits: { min: number; max: number }[] | undefined) => void;
  onTrailControlsReady?: (controls: TrailControls | null) => void;
};

export default function Viewport3D({ modelPath, anglesDeg, stlPreviewUrl, onJointLimitsExtracted, onTrailControlsReady }: Viewport3DProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const controlsRef = useRef<JointControls | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const onTrailControlsReadyRef = useRef(onTrailControlsReady);
  onTrailControlsReadyRef.current = onTrailControlsReady;

  const initScene = useCallback(async () => {
    if (!canvasRef.current) return;

    // Dispose previous scene
    if (controlsRef.current) {
      controlsRef.current.dispose();
      controlsRef.current = null;
    }

    setLoading(true);
    setError(null);

    try {
      // Dynamic import to avoid SSR — this is the key Next.js pattern
      const { createRobotScene } = await import("./createRobotScene");
      const controls = await createRobotScene(canvasRef.current, modelPath);
      controlsRef.current = controls;

      if (controls.getJointLimits) {
        onJointLimitsExtracted?.(controls.getJointLimits());
      } else {
        onJointLimitsExtracted?.(undefined);
      }

      if (controls.addTrailPoint && controls.clearTrail) {
        onTrailControlsReadyRef.current?.({
          addTrailPoint: controls.addTrailPoint,
          clearTrail: controls.clearTrail,
          addExtrusionPoint: controls.addExtrusionPoint,
          clearExtrusion: controls.clearExtrusion,
          setHeatmapMode: controls.setHeatmapMode,
          loadStlPreview: controls.loadStlPreview,
          clearStlPreview: controls.clearStlPreview,
        });
      }
    } catch (err) {
      console.error("Failed to initialize Babylon.js scene:", err);
      setError(err instanceof Error ? err.message : "Failed to load 3D scene");
    } finally {
      setLoading(false);
    }
  }, [modelPath, onJointLimitsExtracted]);

  useEffect(() => {
    initScene();

    return () => {
      if (controlsRef.current) {
        controlsRef.current.dispose();
        controlsRef.current = null;
        onTrailControlsReadyRef.current?.(null);
      }
    };
  }, [initScene]);

  // React to joint angle changes and push them to the imperative Babylon scene
  useEffect(() => {
    if (controlsRef.current && controlsRef.current.setAngles) {
      controlsRef.current.setAngles(anglesDeg);
    }
  }, [anglesDeg]);

  // Load/clear STL preview when URL changes
  useEffect(() => {
    const controls = controlsRef.current;
    if (!controls) return;
    if (stlPreviewUrl) {
      controls.loadStlPreview?.(stlPreviewUrl);
    } else {
      controls.clearStlPreview?.();
    }
  }, [stlPreviewUrl]);

  return (
    <div className="relative w-full h-full">
      <canvas
        ref={canvasRef}
        className="w-full h-full outline-none"
        touch-action="none"
      />
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/50">
          <span className="text-white text-sm">Loading 3D scene...</span>
        </div>
      )}
      {error && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/50">
          <span className="text-red-400 text-sm">{error}</span>
        </div>
      )}
    </div>
  );
}

"use client";

import { useRef, useEffect, useCallback, useState } from "react";
import type { JointControls } from "./createRobotScene";

type Viewport3DProps = {
  modelPath: string | null;
  anglesDeg: number[];
  onJointLimitsExtracted?: (limits: { min: number; max: number }[] | undefined) => void;
};

export default function Viewport3D({ modelPath, anglesDeg, onJointLimitsExtracted }: Viewport3DProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const controlsRef = useRef<JointControls | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

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
      }
    };
  }, [initScene]);

  // React to joint angle changes and push them to the imperative Babylon scene
  useEffect(() => {
    if (controlsRef.current && controlsRef.current.setAngles) {
      controlsRef.current.setAngles(anglesDeg);
    }
  }, [anglesDeg]);

  return (
    <div className="relative w-full h-full bg-linear-to-br from-gray-900 via-gray-950 to-black">
      {/* Glow overlays */}
      <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-orange-500/10 rounded-full blur-3xl"></div>
          <div className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl"></div>
      </div>
      <canvas
        ref={canvasRef}
        className="w-full h-full outline-none z-10 relative "
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

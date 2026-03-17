"use client";

import { useState, useCallback } from "react";
import Viewport3D from "@/components/babylon/Viewport3D";
import type { JointControls } from "@/components/babylon/createRobotScene";

const ROBOTS = [
  { id: "irb4600", name: "ABB IRB 4600", model: "/models/robots/irb4600/Model_IRB_4600.glb" },
];

export default function Home() {
  const [selectedRobot, setSelectedRobot] = useState(ROBOTS[0]);
  const [controls, setControls] = useState<JointControls | null>(null);
  const [jointAngles, setJointAngles] = useState([0, 0, 0, 0, 0, 0]);

  const handleControlsReady = useCallback((c: JointControls) => {
    setControls(c);
  }, []);

  const handleSlider = (index: number, deg: number) => {
    const rad = (deg * Math.PI) / 180;
    const newAngles = [...jointAngles];
    newAngles[index] = deg;
    setJointAngles(newAngles);
    controls?.setJointAngle(index, rad);
  };

  return (
    <div className="flex h-screen bg-zinc-950 text-white">
      {/* Side panel */}
      <div className="w-72 border-r border-zinc-800 p-4 flex flex-col gap-4 overflow-y-auto">
        <h1 className="text-lg font-semibold">ArmStudio — Next.js</h1>
        <p className="text-xs text-zinc-400">
          Babylon.js verification in Next.js App Router
        </p>

        <div>
          <label className="text-xs text-zinc-400 block mb-1">Robot Model</label>
          <select
            value={selectedRobot.id}
            onChange={(e) => {
              const r = ROBOTS.find((r) => r.id === e.target.value);
              if (r) setSelectedRobot(r);
            }}
            className="w-full bg-zinc-900 border border-zinc-700 rounded px-2 py-1 text-sm"
          >
            {ROBOTS.map((r) => (
              <option key={r.id} value={r.id}>{r.name}</option>
            ))}
          </select>
        </div>

        <div className="flex flex-col gap-3">
          <h2 className="text-sm font-medium text-zinc-300">Joint Angles</h2>
          {jointAngles.map((angle, i) => (
            <div key={i} className="flex flex-col gap-1">
              <div className="flex justify-between text-xs text-zinc-400">
                <span>J{i + 1}</span>
                <span>{angle.toFixed(1)}°</span>
              </div>
              <input
                type="range"
                min={-180}
                max={180}
                value={angle}
                onChange={(e) => handleSlider(i, parseFloat(e.target.value))}
                className="w-full accent-orange-500"
              />
            </div>
          ))}
        </div>

        <div className="mt-auto p-3 rounded bg-zinc-900 border border-zinc-800">
          <h3 className="text-xs font-medium text-green-400 mb-1">Verification Status</h3>
          <ul className="text-xs text-zinc-400 space-y-1">
            <li>Next.js App Router: ✓</li>
            <li>Babylon.js Engine: {controls ? "✓" : "loading..."}</li>
            <li>GLB Model Load: {controls ? "✓" : "pending"}</li>
            <li>Joint Control: {controls ? "✓ move sliders" : "pending"}</li>
          </ul>
        </div>
      </div>

      {/* Viewport */}
      <div className="flex-1">
        <Viewport3D
          modelPath={selectedRobot.model}
          onJointControlsReady={handleControlsReady}
        />
      </div>
    </div>
  );
}

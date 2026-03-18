export type TrajectoryWaypoint = {
  index: number;
  timestamp: number;
  joints: number[];  // degrees, j1-j6
  tcp_pose: { position: number[]; orientation: number[] };
  collisions: unknown[];
};

export type SimulateResponse = {
  trajectory: TrajectoryWaypoint[];
  stats: { total_waypoints: number; duration_seconds: number; computation_time_ms: number };
};

// Derive robot_id from GLB model path, e.g. "/models/robots/irb4600/..." → "irb4600"
export function robotIdFromPath(modelPath: string | null): string | null {
  if (!modelPath) return null;
  const match = modelPath.match(/\/models\/robots\/([^/]+)\//);
  return match ? match[1] : null;
}

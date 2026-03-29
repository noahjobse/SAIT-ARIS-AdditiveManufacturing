/**
 * Types derived from the OpenAPI contract for the frontend MVP.
 */

export type TabType = "rapid" | "jog";

export const ROBOT_MODELS = [
  { path: "/models/robots/irb4600/Model_IRB_4600.glb", label: "ABB IRB 4600" },
  { path: "/models/robots/irb2600/Model_IRB_2600.glb", label: "ABB IRB 2600" },
  { path: "/models/robots/irb6700/Model_IRB_6700.glb", label: "ABB IRB 6700" },
];

export type CollisionInfo = {
  obstacle_id: string;
  link: string;
  penetration_depth: number;
  contact_point: number[];
};

export type TrajectoryWaypoint = {
  index: number;
  timestamp: number;
  joints: number[];
  tcp_pose: {
    position: number[];
    orientation: number[];
  };
  collisions: CollisionInfo[];
};

// Utility to extract "irb4600" from "/models/robots/irb4600/Model_IRB_4600.glb"
export function robotIdFromPath(modelPath: string | null): string | null {
  if (!modelPath) return null;
  const match = modelPath.match(/\/robots\/(irb\d+)\//);
  return match ? match[1] : null;
}

/**
 * Types derived from the OpenAPI contract for the frontend MVP.
 */

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
export function robotIdFromPath(modelPath: string | null): string | undefined {
  if (!modelPath) return undefined;
  const match = modelPath.match(/\/robots\/(irb\d+)\//);
  return match ? match[1] : undefined;
}

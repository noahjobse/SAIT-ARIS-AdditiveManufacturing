import { useEffect, useRef, useState, Suspense } from 'react';
import { Model, ILoadedModel, useScene } from 'react-babylonjs';
import { Vector3, Axis, TransformNode, AbstractMesh } from '@babylonjs/core';
import { useRobotContext } from '../../context/RobotContext';

// CONFIGURATION:
const ROBOT_CONFIG = [
  // IMPORTANT: The meshName must be EXACTLY what is in your GLB file.
  // Use the console log in onModelLoaded to see the real names.
  { idx: 0, meshName: "Link_1", pivot: new Vector3(0, 0, 0), axis: Axis.Y },
  { idx: 1, meshName: "Link_2", pivot: new Vector3(0.16, 0.5, 0), axis: Axis.Z },
  { idx: 2, meshName: "Link_3", pivot: new Vector3(0.16, 1.6, 0), axis: Axis.Z },
  { idx: 3, meshName: "Link_4", pivot: new Vector3(0.4, 1.6, 0), axis: Axis.X },
  { idx: 4, meshName: "Link_5", pivot: new Vector3(1.4, 1.6, 0), axis: Axis.Z },
  { idx: 5, meshName: "Link_6", pivot: new Vector3(1.6, 1.6, 0), axis: Axis.X },
];

const RobotModel = () => {
  const { jointAngles } = useRobotContext();
  const scene = useScene();
  const jointsRef = useRef<TransformNode[]>([]);
  const [isLoaded, setIsLoaded] = useState(false);

  // Rotation Logic
  useEffect(() => {
    if (!isLoaded || jointsRef.current.length === 0) return;

    jointAngles.forEach((angleDeg, i) => {
      const node = jointsRef.current[i];
      const config = ROBOT_CONFIG[i];
      if (node && config) {
        const rad = (angleDeg * Math.PI) / 180;
        node.rotation = Vector3.Zero();
        if (config.axis === Axis.X) node.rotation.x = rad;
        if (config.axis === Axis.Y) node.rotation.y = rad;
        if (config.axis === Axis.Z) node.rotation.z = rad;
      }
    });
  }, [jointAngles, isLoaded]);

  // Rigging Logic
  const onModelLoaded = (model: ILoadedModel) => {
    if (!scene || !model.meshes || model.meshes.length === 0) {
      console.error("Model loaded but scene or meshes are missing.");
      return;
    }
    
    // DEBUG: This will show you the exact names of all parts of your robot.
    console.log("Loaded Robot Parts:", model.meshes.map(m => m.name));

    const newJoints: TransformNode[] = [];
    let previousJoint: TransformNode | null = null;

    ROBOT_CONFIG.forEach((config) => {
      const joint = new TransformNode(`joint_${config.idx}`, scene);
      joint.position = config.pivot;
      if (previousJoint) joint.parent = previousJoint;
      newJoints.push(joint);
      previousJoint = joint;

      const mesh = scene.getMeshByName(config.meshName);
      if (mesh) {
        // Detach from any existing hierarchy and attach to our new joint
        mesh.setParent(null);
        mesh.setParent(joint);
      } else {
        console.warn(`Rigging failed: Mesh "${config.meshName}" not found. Check the names in the console log.`);
      }
    });

    jointsRef.current = newJoints;
    setIsLoaded(true);
  };

  return (
    <Model
      name="irb4600"
      rootUrl="/models/robots/irb4600/"
      sceneFilename="Model_IRB_4600.glb"
      onModelLoaded={onModelLoaded}
      position={new Vector3(0, 0, 0)}
    />
  );
};

// This is the component that MainScene actually imports.
export const Robot = () => (
  <Suspense fallback={null}>
    <RobotModel />
  </Suspense>
);
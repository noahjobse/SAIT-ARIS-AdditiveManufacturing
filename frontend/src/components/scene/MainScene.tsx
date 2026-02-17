import { Engine, Scene } from 'react-babylonjs';
import { Vector3, Color3 } from '@babylonjs/core';
import { GridMaterial } from '@babylonjs/materials/grid';
import { Robot } from './Robot';
import { ObstacleManager } from './ObstacleManager'; // <--- Import this

export const MainScene = () => {

  const onGroundCreated = (ground: any) => {
    const gridMat = new GridMaterial("gridMat", ground.getScene());
    gridMat.majorUnitFrequency = 5;
    gridMat.minorUnitVisibility = 0.45;
    gridMat.gridRatio = 1;
    gridMat.backFaceCulling = false;
    gridMat.mainColor = new Color3(1, 1, 1);
    gridMat.lineColor = new Color3(1, 1, 1);
    gridMat.opacity = 0.98;
    ground.material = gridMat;
    
    // FR-3: Ground should NOT be movable by Gizmo
    ground.isPickable = false; 
  };

  return (
    <div className="h-full w-full">
      <Engine 
        antialias 
        adaptToDeviceRatio 
        canvasId="babylon-canvas"
        style={{ height: '100%', width: '100%', outline: 'none' }}
      >
        <Scene>
          <arcRotateCamera
            name="camera1"
            target={Vector3.Zero()}
            alpha={-Math.PI / 2}
            beta={Math.PI / 2.5}
            radius={10}
            minZ={0.1}
            wheelPrecision={50}
          />
          
          <hemisphericLight
            name="light1"
            intensity={0.8}
            direction={new Vector3(0, 1, 0)}
          />

          <ground 
            name="ground" 
            width={20} 
            height={20} 
            onCreated={onGroundCreated} 
          />

          <Robot />
          
          {/* Handles STLs and Gizmos */}
          <ObstacleManager /> 
          
        </Scene>
      </Engine>
    </div>
  );
};
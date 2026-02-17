import { useEffect, useRef } from 'react';
import { useScene } from 'react-babylonjs';
import { 
  SceneLoader, 
  GizmoManager, 
  UtilityLayerRenderer, 
  Color3, 
  StandardMaterial, // <--- Imported directly
  Vector3,
  AbstractMesh
} from '@babylonjs/core';
import { useRobotContext } from '../../context/RobotContext';
import '@babylonjs/loaders/STL'; // <--- Critical: Enables .stl support

export const ObstacleManager = () => {
  const { uploadedFiles } = useRobotContext();
  const scene = useScene();
  
  // Track loaded files to prevent duplicates
  const loadedFileNames = useRef<Set<string>>(new Set());
  
  // Keep track of the Gizmo Manager so we only create it once
  const gizmoManagerRef = useRef<GizmoManager | null>(null);

  // 1. Initialize Gizmo Manager (FR-3: Active Transform Gizmo)
  useEffect(() => {
    if (!scene || gizmoManagerRef.current) return;

    // Create a utility layer for gizmos (so they draw on top of everything)
    const utilLayer = new UtilityLayerRenderer(scene);
    
    // Initialize the manager
    const gizmoManager = new GizmoManager(scene, 1, utilLayer);
    
    // Enable Position (Arrows) and Rotation (Rings) controls
    gizmoManager.positionGizmoEnabled = true;
    gizmoManager.rotationGizmoEnabled = true;
    
    // Allow clicking on empty space to deselect
    gizmoManager.usePointerToAttachGizmos = true;
    gizmoManager.clearGizmoOnEmptyPointerEvent = true;

    gizmoManagerRef.current = gizmoManager;
  }, [scene]);

  // 2. Load New Files (FR-2: Environment Upload)
  useEffect(() => {
    if (!scene) return;

    uploadedFiles.forEach((file) => {
      // Skip if already loaded
      if (loadedFileNames.current.has(file.name)) return;
      loadedFileNames.current.add(file.name);

      const reader = new FileReader();
      
      reader.onload = (evt) => {
        const result = evt.target?.result as ArrayBuffer;
        if (!result) return;

        // Create a Blob URL to load the STL from memory
        const blob = new Blob([result], { type: "application/octet-stream" });
        const url = URL.createObjectURL(blob);

        // Load the mesh
        SceneLoader.ImportMesh(
          "",           // No specific mesh name (load all)
          "",           // Root URL (empty because we use blob)
          url,          // The Blob URL
          scene,        // The Scene instance
          (meshes) => {
            // Callback when loaded
            meshes.forEach((mesh) => {
              mesh.name = file.name;
              
              // Scale fix: STL files are often in mm, Babylon is in meters.
              // We scale down by 0.001 just in case, or keep 1.0 if your STLs are meters.
              // mesh.scaling = new Vector3(0.001, 0.001, 0.001); 
              
              // Create Orange Material
              const material = new StandardMaterial(`${file.name}-mat`, scene);
              material.diffuseColor = Color3.FromHexString("#ff9900"); // Safety Orange
              material.backFaceCulling = false; // Show both sides of faces
              mesh.material = material;

              // Ensure Gizmo can pick it up
              mesh.isPickable = true;
            });
            
            // Clean up the blob URL to free memory
            URL.revokeObjectURL(url);
          },
          null, // Progress callback
          (scene, message) => {
            console.error("Error loading STL:", message);
          }, // Error callback
          ".stl" // <--- Important: Tells Babylon this blob is an STL
        );
      };

      reader.readAsArrayBuffer(file);
    });
  }, [uploadedFiles, scene]);

  return null; // This component is logic-only, no UI
};
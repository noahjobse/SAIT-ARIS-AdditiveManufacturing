# Phase 1 STL Geometry Files

## Test Geometries (Required)

- ✅ `tg1_wall.stl` - Test Geometry 1: Flat pad / straight wall type
  - Purpose: Layer stacking, starts/stops, baseline motion
  
- ✅ `tg2_cone.stl` - Test Geometry 2: Curved or vertical geometry
  - Purpose: Curvature, orientation, reach, smoothness

## Rocket Geometries (Required)

- ❌ `rocket_v1.stl` - Rocket v1: Baseline simulation
  - **Status: Missing - needs to be added**

- ❌ `rocket_v2.stl` - Rocket v2: One deliberate iteration
  - **Status: Missing - can be derived from v1 with parameter change, or provided separately**

## Naming Convention

All STL files use lowercase with underscores, matching the Phase 1 naming standards.

## Usage

These STL files are the input geometry for RobotStudio + 3DP PowerPac toolpath generation. They are tracked in git as authoritative geometry inputs.

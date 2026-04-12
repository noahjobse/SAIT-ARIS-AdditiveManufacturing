"""
STL mesh slicer using trimesh.

Converts an STL file into RAPID AST move commands for FDM 3D printing simulation.
Pipeline: STL -> trimesh cross-sections -> layer contours -> MoveL/MoveJ commands.
"""
import logging
from dataclasses import dataclass

import numpy as np
import trimesh

from app.parser.ast_nodes import (
    Declaration,
    Module,
    MoveCommand,
    Orientation,
    Position,
    Procedure,
    Program,
    RobTarget,
    ToolData,
)

logger = logging.getLogger(__name__)


@dataclass
class SliceResult:
    program: Program
    extrusion_values: list[float]  # cumulative E (mm) parallel to commands
    stats: dict


# Identity orientation — same as the working SAIT ARIS RAPID programs use at X=1200
_PRINT_ORI = Orientation(q1=1, q2=0, q3=0, q4=0)


def slice_stl(
    stl_path: str,
    layer_height: float = 0.2,
    nozzle_diameter: float = 0.4,
    x_offset: float = 1200.0,
    y_offset: float = 0.0,
    z_offset: float = 800.0,   # 800mm matches the tested workspace height range
    print_speed: float = 30.0,
    travel_speed: float = 100.0,
) -> SliceResult:
    """
    Slice an STL mesh into robot move commands using trimesh cross-sections.

    Args:
        stl_path: Path to STL file
        layer_height: Layer height in mm
        nozzle_diameter: Nozzle diameter in mm (affects bead width)
        x_offset: Robot workspace X offset in mm
        y_offset: Robot workspace Y offset in mm
        z_offset: Robot workspace Z offset in mm (print surface height)
        print_speed: Extrusion move speed in mm/s
        travel_speed: Travel move speed in mm/s

    Returns:
        SliceResult with RAPID Program AST and extrusion tracking
    """
    mesh = trimesh.load(stl_path, force="mesh")

    # Center on XY, place bottom at Z=0
    centroid = mesh.bounds.mean(axis=0)
    mesh.vertices -= centroid
    mesh.vertices[:, 2] -= mesh.bounds[0][2]

    max_z = float(mesh.bounds[1][2])
    if max_z < layer_height:
        raise ValueError(
            f"Mesh height ({max_z:.2f}mm) is less than layer height ({layer_height}mm)"
        )

    # Slice all layers at once for efficiency
    z_levels = np.arange(layer_height, max_z + layer_height / 2, layer_height)
    sections = mesh.section_multiplane(
        plane_origin=[0, 0, 0],
        plane_normal=[0, 0, 1],
        heights=z_levels.tolist(),
    )

    commands: list[MoveCommand] = []
    extrusion_values: list[float] = []
    cumulative_e = 0.0
    layer_count = 0

    speed_travel = f"v{int(travel_speed)}"
    speed_print = f"v{int(print_speed)}"

    for z, path_2d in zip(z_levels, sections):
        if path_2d is None:
            continue

        layer_count += 1
        contours = _extract_contours(path_2d)

        for contour in contours:
            if len(contour) < 2:
                continue

            # Travel to contour start (MoveJ — fast, no extrusion)
            start = contour[0]
            commands.append(
                _make_move(
                    "MoveJ",
                    float(start[0]) + x_offset,
                    float(start[1]) + y_offset,
                    float(z) + z_offset,
                    speed=speed_travel,
                    zone="z5",
                )
            )
            extrusion_values.append(cumulative_e)

            # Extrude along contour (MoveL — linear, with material deposition)
            for i in range(1, len(contour)):
                pt = contour[i]
                prev = contour[i - 1]
                seg_len = float(np.linalg.norm(pt - prev))
                cumulative_e += seg_len

                commands.append(
                    _make_move(
                        "MoveL",
                        float(pt[0]) + x_offset,
                        float(pt[1]) + y_offset,
                        float(z) + z_offset,
                        speed=speed_print,
                        zone="z1",
                    )
                )
                extrusion_values.append(cumulative_e)

    if not commands:
        raise ValueError("Slicing produced no toolpath commands — mesh may be degenerate")

    logger.info(
        "Sliced %d layers, %d commands, %.1f mm extrusion",
        layer_count,
        len(commands),
        cumulative_e,
    )

    # Build RAPID AST with extruder tool declaration
    extruder = ToolData(
        tcp_pos=Position(x=0, y=0, z=100),
        tcp_rot=Orientation(q1=1, q2=0, q3=0, q4=0),
    )
    program = Program(
        modules=[
            Module(
                name="PrintModule",
                procedures=[Procedure(name="main", commands=commands)],
                declarations=[
                    Declaration(
                        dtype="PERS",
                        type_name="tooldata",
                        name="extruder",
                        value=extruder,
                    )
                ],
            )
        ]
    )

    return SliceResult(
        program=program,
        extrusion_values=extrusion_values,
        stats={
            "layer_count": layer_count,
            "total_extrusion_mm": round(cumulative_e, 2),
            "move_commands": len(commands),
            "print_height_mm": round(max_z, 2),
        },
    )


def _extract_contours(path_2d) -> list[np.ndarray]:
    """Extract ordered contour polylines from a trimesh Path2D.

    Each contour is an (n, 2) array of XY coordinates forming a polyline.
    Closed contours have the closing segment appended.
    """
    contours = []
    for entity in path_2d.entities:
        try:
            indices = entity.points
            pts = path_2d.vertices[indices]
        except (AttributeError, IndexError):
            continue

        if len(pts) < 2:
            continue

        # Close contour if endpoints don't match
        if len(pts) >= 3 and np.linalg.norm(pts[0] - pts[-1]) > 1e-4:
            pts = np.vstack([pts, pts[0:1]])

        contours.append(pts)

    return contours


def _make_move(
    cmd_type: str, x: float, y: float, z: float, speed: str, zone: str
) -> MoveCommand:
    """Create a MoveCommand with the given parameters."""
    return MoveCommand(
        command_type=cmd_type,
        target=RobTarget(
            position=Position(x=x, y=y, z=z),
            orientation=_PRINT_ORI,
        ),
        speed=speed,
        zone=zone,
        tool="extruder",
    )

from dataclasses import dataclass, field


@dataclass
class Position:
    x: float
    y: float
    z: float

@dataclass
class Orientation:
    q1: float
    q2: float
    q3: float
    q4: float

@dataclass
class RobTarget:
    pos: Position
    rot: Orientation

@dataclass
class JointTarget:
    robax: list[float]
    extax: list[float]

@dataclass
class ToolData:
    """RAPID tooldata: TCP offset relative to flange."""
    tcp_pos: Position       # TCP position offset [x, y, z] in mm
    tcp_rot: Orientation    # TCP orientation offset [q1, q2, q3, q4]
    robhold: bool = True    # Robot holds tool (vs. stationary tool)

#This class should contain all the data we need to store for converting a RAPID command into Python.
#Each instance of a MoveCommand class stores its own individual data and then execute in sequence.
#target uses Union data type so it can handle raw data or variable instructions.
#cir_point is optional since only MoveC commands apply to it. Else is just left blank.
@dataclass
class MoveCommand:
    command_type: str
    target: str | RobTarget | JointTarget
    speed: str | list[float]
    zone: str | list[bool | float]
    tool: str
    wobj: str | None = None
    cir_point: str | RobTarget | JointTarget | None = None
    line_number: int = 0  # Just for error reporting

@dataclass
class Procedure:
    name: str
    commands: list[MoveCommand] = field(default_factory=list)
    params: list[str] = field(default_factory=list)

@dataclass
class Declaration:
    dtype: str
    type_name: str
    name: str
    value: str | RobTarget | JointTarget | ToolData | float | bool | None = None

@dataclass
class Module:
    name: str
    procedures: list[Procedure] = field(default_factory=list)
    declarations: list[Declaration] = field(default_factory=list)

@dataclass
class Program:
    modules: list[Module] = field(default_factory=list)

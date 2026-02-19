from dataclasses import dataclass, field
from typing import List, Optional, Union

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
    robax: List[float]
    extax: List[float]

#This class should contain all the data we need to store for converting a RAPID command into Python.
#Each instance of a MoveCommand class stores its own individual data and then execute in sequence.
#target uses Union data type so it can handle raw data or variable instructions.
#cir_point is optional since only MoveC commands apply to it. Else is just left blank.
@dataclass
class MoveCommand:
    command_type: str
    target: Union[str, RobTarget]
    speed: str 
    zone: str
    tool: str
    wobj: Optional[str] = None
    cir_point: Optional[Union[str, RobTarget, JointTarget]] = None
    line_number: int = 0  # Just for error reporting

@dataclass
class Procedure:
    name: str
    commands: List[MoveCommand] = field(default_factory=list)
    params: List[str] = field(default_factory=list)

@dataclass
class Declaration:
    dtype: str 
    type_name: str
    name: str
    value: Union[str, RobTarget, JointTarget, float, bool]

@dataclass
class Module:
    name: str
    procedures: List[Procedure] = field(default_factory=list)
    declarations: List[Declaration] = field(default_factory=list)

@dataclass
class Program:
    modules: List[Module] = field(default_factory=list)

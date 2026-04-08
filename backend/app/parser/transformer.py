
from lark import Token, Transformer

from .ast_nodes import (
    Declaration,
    Expression,
    ForStatement,
    IfStatement,
    JointTarget,
    Module,
    MoveCommand,
    Orientation,
    Position,
    Procedure,
    Program,
    RobTarget,
    ToolData,
    WhileStatement,
)


#Every rule that is defined inside of grammar.lark should be accounted for in RapidTransformer.
#Note: args is the list containing all children of the matching rule in grammar.lark.
class RapidTransformer(Transformer):
    def start(self, modules):
        return Program(modules=modules)

    def module(self, args):
        name = str(args[0])
        procedures = []
        declarations = []

        #iterates through all elements of the args list and sorts them into either Procedures or Declarations
        for item in args[1:]:
            if isinstance(item, Procedure):
                procedures.append(item)
            elif isinstance(item, Declaration):
                declarations.append(item)

        return Module(name=name, procedures=procedures, declarations=declarations)

    def procedure(self, args):
        name = str(args[0])
        params = []
        commands = []

        # same idea as module, but creates a list of either parameters or commands.
        for item in args[1:]:
            if isinstance(item, list):
                params = item
            elif isinstance(item, (MoveCommand, IfStatement, ForStatement, WhileStatement)):
                commands.append(item)

        return Procedure(name=name, commands=commands, params=params)

    #lines 42-95 should all be a "landing zone" for RAPID objects sorted and parsed by the rules in grammar.lark
    def parameter_list(self, args):
        return args

    def parameter(self, args):
        return f"{args[0]} {args[1]}"

    def declaration(self, args):
        return args[0]

    def const_decl(self, args):
        return Declaration(dtype="CONST", type_name=str(args[0]), name=str(args[1]), value=args[2])

    def var_decl(self, args):
        val = args[2] if len(args) > 2 else None
        return Declaration(dtype="VAR", type_name=str(args[0]), name=str(args[1]), value=val)

    def pers_decl(self, args):
        return Declaration(dtype="PERS", type_name=str(args[0]), name=str(args[1]), value=args[2])

    def type(self, args):
        return str(args[0])

    def value(self, args):
        if isinstance(args[0], Token):
            if args[0].type == 'NUMBER':
                return float(args[0])
            if args[0].type == 'BOOLEAN':
                return args[0].value == 'TRUE'
            return str(args[0])
        return args[0]

    def statement(self, args):
        return args[0]

    def expression(self, args):
        tokens = []
        for arg in args:
            if isinstance(arg, Token):
                tokens.append(str(arg))
            else:
                tokens.append(arg)
        return Expression(tokens=tokens)

    def if_stmt(self, args):
        condition = args[0]
        true_branch = []
        elif_branches = []
        false_branch = []

        for item in args[1:]:
            if isinstance(item, tuple) and item[0] == "ELIF":
                elif_branches.append((item[1], item[2]))
            elif isinstance(item, tuple) and item[0] == "ELSE":
                false_branch.extend(item[1])
            else:
                true_branch.append(item)

        return IfStatement(
            condition=condition,
            true_branch=true_branch,
            elif_branches=elif_branches,
            false_branch=false_branch
        )

    def elif_branch(self, args):
        # Returns a tuple to be caught by the if_stmt loop above
        return ("ELIF", args[0], args[1:])

    def else_branch(self, args):
        return ("ELSE", args)

    def for_stmt(self, args):
        var_name = str(args[0])
        start = args[1]
        end = args[2]
        step = args[3] if len(args) > 3 and isinstance(args[3], Expression) else None
        body_start = 4 if step else 3
        
        return ForStatement(var_name=var_name, start=start, end=end, step=step, body=args[body_start:])

    def while_stmt(self, args):
        return WhileStatement(condition=args[0], body=args[1:])

    def move_l(self, args):
        return self._create_move("MoveL", args)

    def move_j(self, args):
        return self._create_move("MoveJ", args)

    def move_abs_j(self, args):
        return self._create_move("MoveAbsJ", args)

    def move_c(self, args):
        cir_point = args[0]
        cmd = self._create_move("MoveC", args[1:])

        if isinstance(cir_point, Token):
            cmd.circular_point = str(cir_point)
        else:
            cmd.circular_point = cir_point

        return cmd

    def _create_move(self, cmd_type, args):
        target = args[0]
        speed = args[1]
        zone = args[2]
        tool = args[3]
        wobj = args[4] if len(args) > 4 else None

        # converts lark tokens into Python strings (e.g. Token('p10') -> 'p10')
        if isinstance(target, Token):
            target = str(target)
        if isinstance(speed, Token):
            speed = str(speed)
        if isinstance(zone, Token):
            zone = str(zone)
        if isinstance(tool, Token):
            tool = str(tool)
        if wobj and isinstance(wobj, Token):
            wobj = str(wobj)

        return MoveCommand(
            command_type=cmd_type,
            target=target,
            speed=speed,
            zone=zone,
            tool=tool,
            work_object=wobj
        )

    #lines 119-147 more "landing zones" sorted out in grammar.lark. These should populate our values for the MoveCommand class in ast_nodes.py
    def target(self, args):
        if isinstance(args[0], Token):
            return str(args[0])
        return args[0]

    def cir_point(self, args):
        return self.target(args)

    def speed(self, args):
        return args[0]

    def zone(self, args):
        return args[0]

    def tool(self, args):
        return args[0]

    def wobj(self, args):
        return args[0]

    def robtarget(self, args):
        return RobTarget(position=args[0], orientation=args[1])

    def pos(self, args):
        return Position(x=float(args[0]), y=float(args[1]), z=float(args[2]))

    def rot(self, args):
        return Orientation(q1=float(args[0]), q2=float(args[1]), q3=float(args[2]), q4=float(args[3]))

    def jointtarget(self, args):
        return JointTarget(robot_axes=args[0], external_axes=args[1])

    def joint_values(self, args):
        return [float(x) for x in args]

    def tooldata(self, args):
        robhold = args[0].value == "TRUE" if isinstance(args[0], Token) else bool(args[0])
        tool_frame = args[1]  # (Position, Orientation) tuple from tool_frame rule
        return ToolData(tcp_pos=tool_frame[0], tcp_rot=tool_frame[1], robhold=robhold)

    def tool_frame(self, args):
        return (args[0], args[1])  # (Position, Orientation)

    def load_data(self, args):
        return args  # Ignored for MVP — just consume the tokens

    def confdata(self, args): return args
    def extax(self, args): return [float(x) for x in args]

    def speeddata(self, args):
        return [float(x) for x in args]

    def zonedata(self, args):
        return [(x.value == "TRUE") if x.type == "BOOLEAN" else float(x) for x in args]

"""Tests for the RAPID Lark grammar parser."""

import pathlib

import pytest

from app.parser.ast_nodes import JointTarget
from app.parser.parser import RapidParser

# Resolve paths relative to this file so tests work regardless of cwd
GRAMMAR_PATH = pathlib.Path(__file__).parent.parent / "app" / "parser" / "grammar.lark"
FIXTURES_DIR = pathlib.Path(__file__).parent / "fixtures" / "rapid"


@pytest.fixture(scope="module")
def parser():
    """Build and return a RapidParser using the same LALR parser as production."""
    return RapidParser()


def _read_fixture(name: str) -> str:
    return (FIXTURES_DIR / name).read_text()


# ---------------------------------------------------------------------------
# Fixture-based parsing tests
# ---------------------------------------------------------------------------


def test_parse_simple_movel(parser):
    """Grammar parses a simple MODULE containing a MoveL statement."""
    source = _read_fixture("simple_movel.mod")
    tree = parser.parse(source)
    assert tree is not None


def test_parse_simple_movej(parser):
    """Grammar parses a MODULE using MoveJ with a jointtarget declaration."""
    source = _read_fixture("simple_movej.mod")
    tree = parser.parse(source)
    assert tree is not None


def test_parse_pick_and_place(parser):
    """Grammar parses a more complex pick-and-place MODULE with multiple moves."""
    source = _read_fixture("pick_and_place.mod")
    tree = parser.parse(source)
    assert tree is not None


# ---------------------------------------------------------------------------
# Inline CONST declaration tests
# ---------------------------------------------------------------------------


def test_inline_const_robtarget(parser):
    """Grammar parses an inline CONST robtarget declaration."""
    source = (
        "MODULE TestModule\n"
        "    CONST robtarget p1 := [[100, 200, 300], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];\n"
        "    PROC main()\n"
        "        MoveL p1, v1000, z10, tool0;\n"
        "    ENDPROC\n"
        "ENDMODULE\n"
    )
    tree = parser.parse(source)
    assert tree is not None


def test_inline_const_number(parser):
    """Grammar parses an inline CONST num declaration."""
    source = (
        "MODULE TestModule\n"
        "    CONST num mySpeed := 500;\n"
        "    PROC main()\n"
        "    ENDPROC\n"
        "ENDMODULE\n"
    )
    tree = parser.parse(source)
    assert tree is not None


# ---------------------------------------------------------------------------
# jointtarget syntax tests
# ---------------------------------------------------------------------------


def test_inline_jointtarget_declaration(parser):
    """Grammar parses an inline jointtarget CONST declaration."""
    source = (
        "MODULE TestModule\n"
        "    CONST jointtarget jpos := [[0, -30, 30, 0, 45, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];\n"
        "    PROC main()\n"
        "        MoveJ jpos, v500, fine, tool0;\n"
        "    ENDPROC\n"
        "ENDMODULE\n"
    )
    tree = parser.parse(source)
    assert tree is not None


def test_inline_movej_with_literal_jointtarget(parser):
    """Grammar parses MoveJ with a literal inline jointtarget value."""
    source = (
        "MODULE TestModule\n"
        "    PROC main()\n"
        "        MoveJ [[10, -20, 30, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]], v1000, fine, tool0;\n"
        "    ENDPROC\n"
        "ENDMODULE\n"
    )
    tree = parser.parse(source)
    assert tree is not None

# ---------------------------------------------------------------------------
# AST & Transformer Tests (Logic Verification)
# ---------------------------------------------------------------------------

def test_parse_basic_movement():
    code="""
    MODULE MainModule
        PROC main()
            MoveL p10, v1000, z50, tool0;
            MoveJ p20, v500, fine, tool0;
        ENDPROC
    ENDMODULE
    """
    parser = RapidParser()
    program = parser.parse(code)

    assert len(program.modules) == 1
    module = program.modules[0]
    assert module.name == "MainModule"

    assert len(module.procedures) == 1
    proc = module.procedures[0]
    assert proc.name == "main"

    assert len(proc.commands) == 2
    cmd1 = proc.commands[0]
    assert cmd1.command_type == "MoveL"
    assert cmd1.target == "p10"
    assert cmd1.speed == "v1000"
    assert cmd1.zone == "z50"

    cmd2 = proc.commands[1]
    assert cmd2.command_type == "MoveJ"
    assert cmd2.target == "p20"
    assert cmd2.zone == "fine"

def test_parse_declarations():
    code = """
    MODULE DataModule
        CONST num myConst := 10;
        VAR num myVar := 5;
        PROC main()
        ENDPROC
    ENDMODULE
    """
    parser = RapidParser()
    program = parser.parse(code)

    module = program.modules[0]
    assert len(module.declarations) == 2
    assert module.declarations[0].dtype == "CONST"
    assert module.declarations[0].name == "myConst"

def test_parse_jointtarget_ast():
    code = """
    MODULE JointTest
        PROC main()
            ! MoveJ with inline joint values: [robax, extax]
            MoveJ [[0, -90, 30, 0, 45, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]], v1000, z50, tool0;
        ENDPROC
    ENDMODULE
    """
    parser = RapidParser()
    program = parser.parse(code)

    cmd = program.modules[0].procedures[0].commands[0]
    assert cmd.command_type == "MoveJ"
    assert isinstance(cmd.target, JointTarget)
    assert cmd.target.robax == [0, -90, 30, 0, 45, 0]
    assert len(cmd.target.extax) == 6
    assert cmd.target.extax[0] == 9E9

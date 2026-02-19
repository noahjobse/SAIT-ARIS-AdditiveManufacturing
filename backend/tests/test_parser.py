"""Tests for the RAPID Lark grammar parser."""

import pathlib

import lark
import pytest

# Resolve paths relative to this file so tests work regardless of cwd
GRAMMAR_PATH = pathlib.Path(__file__).parent.parent / "app" / "parser" / "grammar.lark"
FIXTURES_DIR = pathlib.Path(__file__).parent / "fixtures" / "rapid"


@pytest.fixture(scope="module")
def parser():
    """Build and return a Lark parser from the RAPID grammar."""
    grammar = GRAMMAR_PATH.read_text()
    return lark.Lark(grammar, parser="earley")


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

import os

from lark import Lark
from lark.exceptions import LarkError, UnexpectedCharacters, UnexpectedToken

from .ast_nodes import Program
from .transformer import RapidTransformer


class RapidParseError(Exception):
    """Raised when RAPID source code cannot be parsed. Routers map this to HTTP 400."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class RapidParser:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        grammar_path = os.path.join(current_dir, 'grammar.lark')
        with open(grammar_path) as f:
            self.grammar = f.read()

        self.parser = Lark(self.grammar, start="start", parser="lalr")
        self.transformer = RapidTransformer()

    def parse(self, code: str) -> Program:
        try:
            tree = self.parser.parse(code)
            return self.transformer.transform(tree)
        except (UnexpectedToken, UnexpectedCharacters) as e:
            raise RapidParseError(
                f"Syntax error at line {e.line}, column {e.column}: {e}"
            )
        except LarkError as e:
            raise RapidParseError(f"Parsing error: {e}")

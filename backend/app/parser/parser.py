import os
from lark import Lark, LarkError
from lark.exceptions import LarkError, UnexpectedToken, UnexpectedCharacters
from fastapi import HTTPException
from .transformer import RapidTransformer
from .ast_nodes import Program

class RapidParser:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        grammar_path = os.path.join(current_dir, 'grammar.lark')
        with open(grammar_path, 'r') as f:
            self.grammar = f.read()

        self.parser = Lark(self.grammar, start="start", parser="lalr")
        self.transformer = RapidTransformer()

    def parse (self, code:str) -> Program:
        try: 
            tree = self.parser.parse(code)
            return self.transformer.transform(tree)
        except (UnexpectedToken, UnexpectedCharacters) as e:
            raise HTTPException(
                status_code=400,
                detail=f"Syntax error at line {e.line}, column {e.column}: {e}"
            )
        except LarkError as e:
            raise HTTPException(status_code=400, detail=f"Parsing error: {e}")
import os
from lark import Lark, LarkError
from .transformer import RapidTransformer
from .ast_nodes import Program

class RapidParser:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        grammar_path = os.path.join(current_dir, 'grammar.lark')
        with open(grammar_path, 'r') as f:
            self.grammar = f.read()

        self.parser - Lark(grammar, start="start", parser = "lalr")
        self.transformer = RapidTransformer()

    def parse (self, code:str) -> Program:
        tree = self.parser.parse(code)
        ast = self.transformer.transform(tree)

        return ast
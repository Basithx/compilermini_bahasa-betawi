from lexer import Lexer
from parser import Parser
from ast_nodes import print_ast

with open("tes.bt", "r", encoding="utf-8") as f:
    source = f.read()

lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

print("=" * 60)
print("HASIL PARSER (AST)")
print("=" * 60)

print_ast(ast)
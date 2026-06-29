from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from optimizer import Optimizer
from ast_nodes import print_ast

with open("tes.bt", "r", encoding="utf-8") as f:
    source = f.read()

lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

semantic = SemanticAnalyzer()
semantic.analyze(ast)

optimizer = Optimizer()
optimized_ast = optimizer.optimize(ast)

print("=" * 60)
print("AST SETELAH OPTIMIZER")
print("=" * 60)

print_ast(optimized_ast)
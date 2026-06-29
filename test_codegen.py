from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from optimizer import Optimizer
from code_generator import CodeGenerator

with open("tes.bt", "r", encoding="utf-8") as f:
    source = f.read()

lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

semantic = SemanticAnalyzer()
semantic.analyze(ast)

optimizer = Optimizer()
ast = optimizer.optimize(ast)

generator = CodeGenerator()
python_code = generator.generate(ast)

print("=" * 60)
print("HASIL CODE GENERATOR")
print("=" * 60)

print(python_code)
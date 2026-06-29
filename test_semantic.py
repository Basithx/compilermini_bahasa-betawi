from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer

with open("tes.bt", "r", encoding="utf-8") as f:
    source = f.read()

lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

semantic = SemanticAnalyzer()
semantic.analyze(ast)

print("=" * 60)
print("SEMANTIC ANALYSIS")
print("=" * 60)

print("✓ Tidak ditemukan Semantic Error\n")

print("Symbol Table")

for name, tipe in semantic.symbol_table.items():
    print(f"{name:15} -> {tipe}")
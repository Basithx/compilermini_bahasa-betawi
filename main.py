from ast_nodes import print_ast
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from optimizer import Optimizer
from code_generator import CodeGenerator

import sys


def compile_file(filename):

    with open(filename, "r", encoding="utf-8") as f:
        source = f.read()

    print("===================================")
    print("      BETAWI COMPILER v1.0")
    print("===================================")

    # Lexer
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)
    print("[✓] Lexical Analysis selesai")

    # Parser
    parser = Parser(tokens)
    ast = parser.parse()
    print("[✓] Parsing selesai")

    # Semantic
    semantic = SemanticAnalyzer()
    semantic.analyze(ast)
    print(semantic.symbol_table)
    print("[✓] Semantic Analysis selesai")

    # Optimizer
    optimizer = Optimizer()
    ast = optimizer.optimize(ast)
    optimized = optimizer.optimize(ast)
    print_ast(optimized)
    print("[✓] Optimisasi selesai")

    # Code Generator
    generator = CodeGenerator()
    python_code = generator.generate(ast)
    print(python_code)

    with open("hasil.py", "w", encoding="utf-8") as f:
        f.write(python_code)

    print("[✓] Code Generation selesai")
    print()
    print("Output : hasil.py")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Cara pakai:")
        print("python main.py contoh.bt")
    else:
        compile_file(sys.argv[1])
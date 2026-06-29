from lexer import Lexer

with open("tes.bt", "r", encoding="utf-8") as f:
    source = f.read()

lexer = Lexer(source)
tokens = lexer.tokenize()

print("=" * 60)
print("HASIL LEXICAL ANALYSIS")
print("=" * 60)

for token in tokens:
    print(token)
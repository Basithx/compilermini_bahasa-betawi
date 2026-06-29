import re
from collections import namedtuple

# Struktur token
Token = namedtuple("Token", ["type", "value", "line", "column"])

# Daftar keyword bahasa Betawi
KEYWORDS = {
    "kalo": "IF",
    "kaga": "ELSE",
    "ulang": "WHILE",
    "kelar": "END",
    "cetak": "PRINT",
    "masukin": "INPUT",
    "kata": "TYPE_STRING",
    "angka": "TYPE_NUMBER"
}

# Daftar token regex
TOKEN_SPECIFICATION = [
    ("NUMBER",   r"\d+"),
    ("STRING",   r'"[^"\n]*"'),
    ("EQ",       r"=="),
    ("NE",       r"!="),
    ("GTE",      r">="),
    ("LTE",      r"<="),
    ("GT",       r">"),
    ("LT",       r"<"),
    ("ASSIGN",   r"="),
    ("PLUS",     r"\+"),
    ("MINUS",    r"-"),
    ("MULTIPLY", r"\*"),
    ("DIVIDE",   r"/"),
    ("LPAREN",   r"\("),
    ("RPAREN",   r"\)"),
    ("ID",       r"[A-Za-z_][A-Za-z0-9_]*"),
    ("NEWLINE",  r"\n"),
    ("SKIP",     r"[ \t]+"),
    ("COMMENT",  r"\#.*"),
    ("MISMATCH", r"."),
]

# Gabungkan regex menjadi satu pola besar
token_regex = "|".join(
    f"(?P<{pair[0]}>{pair[1]})"
    for pair in TOKEN_SPECIFICATION
)


class Lexer:
    def __init__(self, code):
        self.code = code

    def tokenize(self):
        tokens = []
        line_num = 1
        line_start = 0

        for match in re.finditer(token_regex, self.code):
            kind = match.lastgroup
            value = match.group()
            column = match.start() - line_start + 1

            if kind == "NUMBER":
                value = int(value)
                tokens.append(Token("NUMBER", value, line_num, column))

            elif kind == "STRING":
                value = value[1:-1]  # hilangkan tanda kutip
                tokens.append(Token("STRING", value, line_num, column))

            elif kind == "ID":
                token_type = KEYWORDS.get(value, "IDENTIFIER")
                tokens.append(Token(token_type, value, line_num, column))

            elif kind == "NEWLINE":
                tokens.append(Token("NEWLINE", "\\n", line_num, column))
                line_num += 1
                line_start = match.end()

            elif kind == "SKIP" or kind == "COMMENT":
                continue

            elif kind == "MISMATCH":
                raise SyntaxError(
                    f"Karakter tidak dikenal '{value}' di baris {line_num}, kolom {column}"
                )

            else:
                tokens.append(Token(kind, value, line_num, column))

        # Penanda akhir file
        tokens.append(Token("EOF", None, line_num, 1))

        return tokens


# ----------------------------------------
# TEST SEDERHANA
# ----------------------------------------
if __name__ == "__main__":
    source_code = """
nama = masukin
nilai = 85

kalo nilai > 75
    cetak "Lulus"
kaga
    cetak "Gagal"
kelar
"""

    lexer = Lexer(source_code)
    token_list = lexer.tokenize()

    for token in token_list:
        print(token)
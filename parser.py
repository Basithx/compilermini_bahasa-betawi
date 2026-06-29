from lexer import Token
from ast_nodes import *

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    # ==========================
    # Utility Functions
    # ==========================

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def is_at_end(self):
        return self.peek().type == "EOF"

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def check(self, token_type):
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def match(self, *types):
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False

    def consume(self, token_type, message):

        if self.check(token_type):
            return self.advance()

        token = self.peek()

        raise SyntaxError(
            f"{message} "
            f"(Baris {token.line}, Kolom {token.column})"
        )

    # ==========================
    # Parse Program
    # ==========================

    def parse(self):

        statements = []

        while not self.is_at_end():

            if self.match("NEWLINE"):
                continue

            statements.append(self.statement())

        return Program(statements)

    # ==========================
    # Statement Dispatcher
    # ==========================

    def statement(self):

        token = self.peek()

        if token.type in ("IDENTIFIER", "TYPE_NUMBER", "TYPE_STRING"):
            return self.assignment()

        elif token.type == "PRINT":
            return self.print_statement()

        elif token.type == "IF":
            return self.if_statement()

        elif token.type == "WHILE":
            return self.while_statement()

        else:
            raise SyntaxError(
                f"Statement tidak dikenali : {token.value}"
            )
    # ==========================================
    # Assignment
    # ==========================================
    def assignment(self):

        var_type = None

    # Jika ada deklarasi tipe
        if self.match("TYPE_NUMBER", "TYPE_STRING"):
            var_type = self.previous().type

        identifier = Identifier(
            self.consume(
                "IDENTIFIER",
                "Nama variabel diharapkan."
            ).value
    )

        self.consume(
            "ASSIGN",
            "Tanda '=' diharapkan."
        )

        value = self.expression()

        while self.match("NEWLINE"):
            pass

        return Assignment(
            var_type,
            identifier,
            value
        )

    # ==========================================
    # Print
    # ==========================================

    def print_statement(self):

        self.consume(
            "PRINT",
            "Keyword 'cetak' diharapkan."
        )

        expr = self.expression()

        while self.match("NEWLINE"):
            pass

        return Print(expr)

    # ==========================================
    # IF
    # ==========================================

    def if_statement(self):

        self.consume(
            "IF",
            "Keyword 'kalo' diharapkan."
        )

        condition = self.expression()

        while self.match("NEWLINE"):
            pass

        true_branch = []

        while (
            not self.check("ELSE")
            and not self.check("END")
            and not self.is_at_end()
        ):
            true_branch.append(
                self.statement()
            )

        false_branch = []

        if self.match("ELSE"):

            while self.match("NEWLINE"):
                pass

            while (
                not self.check("END")
                and not self.is_at_end()
            ):
                false_branch.append(
                    self.statement()
                )

        self.consume(
            "END",
            "Keyword 'kelar' diharapkan."
        )

        while self.match("NEWLINE"):
            pass

        return If(
            condition,
            true_branch,
            false_branch
        )

    # ==========================================
    # WHILE
    # ==========================================

    def while_statement(self):

        self.consume(
            "WHILE",
            "Keyword 'ulang' diharapkan."
        )

        condition = self.expression()

        while self.match("NEWLINE"):
            pass

        body = []

        while (
            not self.check("END")
            and not self.is_at_end()
        ):
            body.append(
                self.statement()
            )

        self.consume(
            "END",
            "Keyword 'kelar' diharapkan."
        )

        while self.match("NEWLINE"):
            pass

        return While(
            condition,
            body
        )

    # ==================================
    # Expression
    # ==========================================

    def expression(self):
        return self.comparison()

    # ==========================================
    # Comparison
    # ==========================================

    def comparison(self):

        expr = self.term()

        while self.match(
            "GT",
            "LT",
            "GTE",
            "LTE",
            "EQ",
            "NE"
        ):

            operator = self.previous().value

            right = self.term()

            expr = BinaryOp(
                expr,
                operator,
                right
            )

        return expr

    # ==========================================
    # Term
    # ==========================================

    def term(self):

        expr = self.factor()

        while self.match(
            "PLUS",
            "MINUS"
        ):

            operator = self.previous().value

            right = self.factor()

            expr = BinaryOp(
                expr,
                operator,
                right
            )

        return expr

    # ==========================================
    # Factor
    # ==========================================

    def factor(self):

        expr = self.primary()

        while self.match(
            "MULTIPLY",
            "DIVIDE"
        ):

            operator = self.previous().value

            right = self.primary()

            expr = BinaryOp(
                expr,
                operator,
                right
            )

        return expr

    # ==========================================
    # Primary
    # ==========================================

    def primary(self):

        # angka
        if self.match("NUMBER"):
            return Number(
                self.previous().value
            )

        # string
        if self.match("STRING"):
            return String(
                self.previous().value
            )

        # identifier
        if self.match("IDENTIFIER"):
            return Identifier(
                self.previous().value
            )

        # input
        if self.match("INPUT"):
            return Input()

        # (
        if self.match("LPAREN"):

            expr = self.expression()

            self.consume(
                "RPAREN",
                "Diharapkan ')'"
            )

            return expr

        token = self.peek()

        raise SyntaxError(
            f"Expression tidak valid "
            f"di baris {token.line}, kolom {token.column}"
        )

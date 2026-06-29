from platform import node

from ast_nodes import *


class SemanticAnalyzer:

    def __init__(self):
        # Symbol Table
        # contoh:
        # {
        #   "nilai": "NUMBER",
        #   "nama": "STRING"
        # }
        self.symbol_table = {}

    # ===================================
    # Entry Point
    # ===================================

    def analyze(self, node):
        self.visit(node)

    # ===================================
    # Dispatcher
    # ===================================

    def visit(self, node):

        method_name = "visit_" + node.__class__.__name__

        visitor = getattr(
            self,
            method_name,
            self.generic_visit
        )

        return visitor(node)

    def generic_visit(self, node):
        raise Exception(
            f"Tidak ada visit untuk {node.__class__.__name__}"
        )

    # ===================================
    # Program
    # ===================================

    def visit_Program(self, node):

        for stmt in node.statements:
            self.visit(stmt)

    # ===================================
    # Assignment
    # ===================================

    def visit_Assignment(self, node):

    # Tipe dari nilai di sebelah kanan
        value_type = self.visit(node.value)

    # Jika tidak ada deklarasi tipe (cara lama)
        if node.var_type is None:
            self.symbol_table[node.identifier.name] = value_type
            return

    # -------------------------
    # Deklarasi angka
    # -------------------------
        if node.var_type == "TYPE_NUMBER":

        # input dianggap NUMBER jika variabel bertipe angka
            if isinstance(node.value, Input):
                value_type = "NUMBER"

            if value_type != "NUMBER":
                raise Exception(
                    f"Semantic Error: Variabel '{node.identifier.name}' bertipe NUMBER tetapi diberi nilai {value_type}."
            )

            self.symbol_table[node.identifier.name] = "NUMBER"
            return

    # -------------------------
    # Deklarasi kata
    # -------------------------
        if node.var_type == "TYPE_STRING":

        # input dianggap STRING jika variabel bertipe kata
            if isinstance(node.value, Input):
                value_type = "STRING"

            if value_type != "STRING":
                raise Exception(
                    f"Semantic Error: Variabel '{node.identifier.name}' bertipe STRING tetapi diberi nilai {value_type}."
            )

            self.symbol_table[node.identifier.name] = "STRING"
            return
    # ===================================
    # Identifier
    # ===================================

    def visit_Identifier(self, node):

        if node.name not in self.symbol_table:

            raise Exception(
                f"Semantic Error: Variabel '{node.name}' belum dideklarasikan."
            )

        return self.symbol_table[node.name]

    # ===================================
    # Number
    # ===================================

    def visit_Number(self, node):
        return "NUMBER"

    # ===================================
    # String
    # ===================================

    def visit_String(self, node):
        return "STRING"

    # ===================================
    # Input
    # ===================================

    def visit_Input(self, node):
        return "STRING"

    # ===================================
    # Print
    # ===================================

    def visit_Print(self, node):

        self.visit(node.expression)

    # ===================================
    # Binary Operation
    # ===================================

    def visit_BinaryOp(self, node):

        left = self.visit(node.left)

        right = self.visit(node.right)

        operator = node.operator

        arithmetic = [
            "+",
            "-",
            "*",
            "/"
        ]

        comparison = [
            ">",
            "<",
            ">=",
            "<=",
            "==",
            "!="
        ]

        # ----------------------------
        # Aritmatika
        # ----------------------------

        if operator in arithmetic:

            if left != "NUMBER" or right != "NUMBER":

                raise Exception(
                    f"Semantic Error: Operator '{operator}' hanya bisa digunakan untuk NUMBER."
                )

            return "NUMBER"

        # ----------------------------
        # Perbandingan
        # ----------------------------

        if operator in comparison:

            if left != right:

                raise Exception(
                    "Semantic Error: Perbandingan harus menggunakan tipe data yang sama."
                )

            return "BOOLEAN"

        raise Exception(
            f"Operator '{operator}' tidak dikenal."
        )

    # ===================================
    # IF
    # ===================================

    def visit_If(self, node):

        condition = self.visit(node.condition)

        if condition != "BOOLEAN":

            raise Exception(
                "Semantic Error: Kondisi IF harus BOOLEAN."
            )

        for stmt in node.true_branch:
            self.visit(stmt)

        for stmt in node.false_branch:
            self.visit(stmt)

    # ===================================
    # WHILE
    # ===================================

    def visit_While(self, node):

        condition = self.visit(node.condition)

        if condition != "BOOLEAN":

            raise Exception(
                "Semantic Error: Kondisi WHILE harus BOOLEAN."
            )

        for stmt in node.body:
            self.visit(stmt)
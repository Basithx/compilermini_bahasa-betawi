from platform import node

from ast_nodes import *


class CodeGenerator:

    def __init__(self):
        self.code = []
        self.indent = 0

    # ==================================
    # Entry Point
    # ==================================

    def generate(self, node):

        self.visit(node)

        return "\n".join(self.code)

    # ==================================
    # Dispatcher
    # ==================================

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
            f"Tidak ada generator untuk {node.__class__.__name__}"
        )

    # ==================================
    # Helper
    # ==================================

    def emit(self, text):
        self.code.append(
            "    " * self.indent + text
        )

    # ==================================
    # Program
    # ==================================

    def visit_Program(self, node):

        for stmt in node.statements:
            self.visit(stmt)

    # ==================================
    # Assignment
    # ==================================

    def visit_Assignment(self, node):

    # Kasus khusus: input
        if isinstance(node.value, Input):

            if node.var_type == "TYPE_NUMBER":
                value = "int(input())"

            elif node.var_type == "TYPE_STRING":
                value = "input()"

            else:
            # Jika tidak ada deklarasi tipe
                value = "input()"

        else:
            value = self.expression(node.value)

        self.emit(
            f"{node.identifier.name} = {value}"
    )

    # ==================================
    # Print
    # ==================================

    def visit_Print(self, node):

        expr = self.expression(
            node.expression
        )

        self.emit(
            f"print({expr})"
        )

    # ==================================
    # IF
    # ==================================

    def visit_If(self, node):

        condition = self.expression(
            node.condition
        )

        self.emit(
            f"if {condition}:"
        )

        self.indent += 1

        for stmt in node.true_branch:
            self.visit(stmt)

        self.indent -= 1

        if len(node.false_branch) > 0:

            self.emit("else:")

            self.indent += 1

            for stmt in node.false_branch:
                self.visit(stmt)

            self.indent -= 1

    # ==================================
    # WHILE
    # ==================================

    def visit_While(self, node):

        condition = self.expression(
            node.condition
        )

        self.emit(
            f"while {condition}:"
        )

        self.indent += 1

        for stmt in node.body:
            self.visit(stmt)

        self.indent -= 1

    # ==================================
    # Expression
    # ==================================

    def expression(self, node):

        if isinstance(node, Number):
            return str(node.value)

        elif isinstance(node, String):
            return repr(node.value)

        elif isinstance(node, Identifier):
            return node.name

        elif isinstance(node, Input):
            return "input()"

        elif isinstance(node, BinaryOp):

            left = self.expression(
                node.left
            )

            right = self.expression(
                node.right
            )

            return f"({left} {node.operator} {right})"

        else:
            raise Exception(
                f"Expression tidak dikenali : {node}"
            )
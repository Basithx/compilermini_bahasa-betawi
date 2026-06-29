from ast_nodes import *


class Optimizer:

    def optimize(self, node):
        return self.visit(node)

    # ======================================
    # Dispatcher
    # ======================================

    def visit(self, node):

        method = getattr(
            self,
            "visit_" + node.__class__.__name__,
            self.generic_visit
        )

        return method(node)

    def generic_visit(self, node):
        return node

    # ======================================
    # Program
    # ======================================

    def visit_Program(self, node):

        statements = []

        for stmt in node.statements:
            statements.append(
                self.visit(stmt)
            )

        node.statements = statements

        return node

    # ======================================
    # Assignment
    # ======================================

    def visit_Assignment(self, node):

        node.value = self.visit(node.value)

        return node

    # ======================================
    # Print
    # ======================================

    def visit_Print(self, node):

        node.expression = self.visit(node.expression)

        return node

    # ======================================
    # IF
    # ======================================

    def visit_If(self, node):

        node.condition = self.visit(node.condition)

        node.true_branch = [
            self.visit(stmt)
            for stmt in node.true_branch
        ]

        node.false_branch = [
            self.visit(stmt)
            for stmt in node.false_branch
        ]

        # ----------------------------------
        # Constant Condition
        # ----------------------------------

        if isinstance(node.condition, Number):

            if node.condition.value != 0:

                return Program(node.true_branch)

            else:

                return Program(node.false_branch)

        return node

    # ======================================
    # WHILE
    # ======================================

    def visit_While(self, node):

        node.condition = self.visit(node.condition)

        node.body = [
            self.visit(stmt)
            for stmt in node.body
        ]

        return node

    # ======================================
    # Binary Operation
    # ======================================

    def visit_BinaryOp(self, node):

        node.left = self.visit(node.left)
        node.right = self.visit(node.right)

        if (
            isinstance(node.left, Number)
            and
            isinstance(node.right, Number)
        ):

            a = node.left.value
            b = node.right.value

            if node.operator == "+":
                return Number(a + b)

            elif node.operator == "-":
                return Number(a - b)

            elif node.operator == "*":
                return Number(a * b)

            elif node.operator == "/":
                return Number(a // b)

            elif node.operator == ">":
                return Number(int(a > b))

            elif node.operator == "<":
                return Number(int(a < b))

            elif node.operator == ">=":
                return Number(int(a >= b))

            elif node.operator == "<=":
                return Number(int(a <= b))

            elif node.operator == "==":
                return Number(int(a == b))

            elif node.operator == "!=":
                return Number(int(a != b))

        return node

    # ======================================
    # Leaf Node
    # ======================================

    def visit_Number(self, node):
        return node

    def visit_String(self, node):
        return node

    def visit_Identifier(self, node):
        return node

    def visit_Input(self, node):
        return node
from dataclasses import dataclass
from typing import List, Optional, Any


# ======================================
# Base Node
# ======================================

class ASTNode:
    pass


# ======================================
# Program
# ======================================

@dataclass
class Program(ASTNode):
    statements: List[ASTNode]


# ======================================
# Expressions
# ======================================

@dataclass
class Number(ASTNode):
    value: int


@dataclass
class String(ASTNode):
    value: str


@dataclass
class Identifier(ASTNode):
    name: str


@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class Input(ASTNode):
    pass


# ======================================
# Statements
# ======================================

@dataclass
class Assignment(ASTNode):
    var_type: Optional[str]  # "angka" or "kata" or None
    identifier: Identifier
    value: ASTNode


@dataclass
class Print(ASTNode):
    expression: ASTNode


@dataclass
class If(ASTNode):
    condition: ASTNode
    true_branch: List[ASTNode]
    false_branch: List[ASTNode]


@dataclass
class While(ASTNode):
    condition: ASTNode
    body: List[ASTNode]

def print_ast(node, indent=0):
    space = " " * indent

    if isinstance(node, Program):
        print(space + "Program")
        for stmt in node.statements:
            print_ast(stmt, indent + 4)

    elif isinstance(node, Assignment):
        print(space + "Assignment")
        print_ast(node.identifier, indent + 4)
        print_ast(node.value, indent + 4)

    elif isinstance(node, Identifier):
        print(space + f"Identifier({node.name})")

    elif isinstance(node, Number):
        print(space + f"Number({node.value})")

    elif isinstance(node, String):
        print(space + f'String("{node.value}")')

    elif isinstance(node, Input):
        print(space + "Input()")

    elif isinstance(node, Print):
        print(space + "Print")
        print_ast(node.expression, indent + 4)

    elif isinstance(node, BinaryOp):
        print(space + f"BinaryOp({node.operator})")
        print_ast(node.left, indent + 4)
        print_ast(node.right, indent + 4)

    elif isinstance(node, If):
        print(space + "If")

        print(space + " Condition:")
        print_ast(node.condition, indent + 4)

        print(space + " True:")
        for stmt in node.true_branch:
            print_ast(stmt, indent + 4)

        print(space + " False:")
        for stmt in node.false_branch:
            print_ast(stmt, indent + 4)

    elif isinstance(node, While):
        print(space + "While")

        print(space + " Condition:")
        print_ast(node.condition, indent + 4)

        print(space + " Body:")
        for stmt in node.body:
            print_ast(stmt, indent + 4)
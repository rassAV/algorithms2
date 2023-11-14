from .token import Token

class Node:
    pass

class Number(Node):
    def __init__(self, token: Token):
        self.token = token

    def __str__(self):
        return f"Number ({self.token})"

class BinOp(Node):
    def __init__(self, left: Node, op: Token, right: Node):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f"BinOp{self.op.value} ({self.left}, {self.right})"

class UnOp(Node):
    def __init__(self, op: Token, number: Node):
        self.op = op
        self.number = number

    def __str__(self):
        return f"UnOp{self.op.value}{self.number}"

class Variable(Node):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"Variable({self.name})"
    
class Assignment(Node):
    def __init__(self, variable: Variable, data: Node):
        self.variable = variable
        self.data = data

    def __str__(self):
        return f"Assignment{self.variable}:={self.data}"
    
class Semicolon(Node):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right

    def __str__(self):
        return f"Semicolon ({self.left}, {self.right})"
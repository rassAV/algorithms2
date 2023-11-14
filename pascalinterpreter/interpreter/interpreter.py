from .parser import Parser
from .ast import Number, BinOp, UnOp, Variable, Assignment, Semicolon

class NodeVisitor:
    
    def visit(self):
        pass

class Interpreter(NodeVisitor):
    
    def __init__(self):
        self.parser = Parser()
        self.variables = {}

    def visit(self, node):
        if isinstance(node, Number):
            return self.visit_number(node)
        elif isinstance(node, BinOp):
            return self.visit_binop(node)
        elif isinstance(node, UnOp):
            return self.visit_unop(node)
        elif isinstance(node, Variable):
            return self.visit_variable(node)
        elif isinstance(node, Assignment):
            return self.visit_assignment(node)
        elif isinstance(node, Semicolon):
            return self.visit_semicolon(node)
        
    def visit_number(self, node):
        return float(node.token.value)

    def visit_binop(self, node):
        match node.op.value:
            case "+":
                return self.visit(node.left) + self.visit(node.right)
            case "-":
                return self.visit(node.left) - self.visit(node.right)
            case "*":
                return self.visit(node.left) * self.visit(node.right)
            case "/":
                return self.visit(node.left) / self.visit(node.right)    
            case _:
                raise SyntaxError("invalid operator")

    def visit_unop(self, node):
        match node.op.value:
            case "+":
                return self.visit(node.number)
            case "-":
                return self.visit(node.number)*(-1)
            case _:
                raise SyntaxError("invalid operator")
    
    def visit_variable(self, node):
        var_name = node.name.value
        if var_name in self.variables.keys():
            return self.variables[var_name]
        raise ValueError(f"invalid variable {var_name}")
        
    def visit_assignment(self, node):
        self.variables[node.variable.value] = self.visit(node.data)

    def visit_semicolon(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def eval(self, code):
        tree = self.parser.parse(code)
        self.visit(tree)
        return self.variables

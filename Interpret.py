from Parser import (
    FunctionCall,
    StringLiteral,
    IntegerLiteral,
    VariableDeclaration,
    VariableReference,
    BinaryExpression,
    IfStatement
)


class Interpreter:

    def __init__(self, ast):
        self.ast = ast
        self.variables = {}

    def run(self):

        for f in self.ast.functions:
            if f.name == "_start":
                self.exec_block(f.body)
                return

        raise Exception("No _start")

    def exec_block(self, body):
        for stmt in body:
            self.execute(stmt)

    def evaluate(self, node):

        if isinstance(node, StringLiteral):
            return node.value

        if isinstance(node, IntegerLiteral):
            return node.value

        if isinstance(node, VariableReference):
            return self.variables[node.name]

        if isinstance(node, BinaryExpression):

            left = self.evaluate(node.left)
            right = self.evaluate(node.right)

            if node.operator == "==":
                return left == right

        raise Exception(f"Bad eval {node}")

    def execute(self, node):

        if isinstance(node, VariableDeclaration):

            self.variables[node.name] = self.evaluate(node.value)
            return

        if isinstance(node, IfStatement):

            if self.evaluate(node.condition):
                self.exec_block(node.body)

            return

        if isinstance(node, FunctionCall):

            args = [self.evaluate(a) for a in node.args]

            if node.name == "print":
                print(args[0], end="")

            elif node.name == "println":
                print(args[0])

            else:
                raise Exception(f"Unknown fn {node.name}")
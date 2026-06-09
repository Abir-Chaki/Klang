from Parser import (
    FunctionCall,
    StringLiteral,
    IntegerLiteral,
    VariableDeclaration,
    VariableReference
)


class Interpreter:

    def __init__(self, ast):
        self.ast = ast
        self.variables = {}

    def run(self):

        for func in self.ast.functions:

            if func.name == "_start":
                self.execute_function(func)
                return

        raise Exception(
            "No _start() function found"
        )

    def execute_function(self, func):

        for statement in func.body:
            self.execute(statement)

    # -----------------
    # Expression Evaluation
    # -----------------

    def evaluate(self, node):

        if isinstance(node, StringLiteral):
            return node.value

        if isinstance(node, IntegerLiteral):
            return node.value

        if isinstance(node, VariableReference):

            if node.name not in self.variables:
                raise Exception(
                    f"Undefined variable: {node.name}"
                )

            return self.variables[node.name]

        raise Exception(
            f"Cannot evaluate {node}"
        )

    # -----------------
    # Statement Execution
    # -----------------

    def execute(self, node):

        if isinstance(node, VariableDeclaration):

            value = self.evaluate(
                node.value
            )

            self.variables[node.name] = value

            return

        if isinstance(node, FunctionCall):

            if len(node.args) != 1:
                raise Exception(
                    f"{node.name} expects 1 argument"
                )

            value = self.evaluate(
                node.args[0]
            )

            if node.name == "print":
                print(value, end="")
                return

            if node.name == "println":
                print(value)
                return

            raise Exception(
                f"Unknown function: {node.name}"
            )
from Parser import (
    FunctionCall,
    StringLiteral,
    IntegerLiteral,
    VariableDeclaration,
    VariableReference,
    BinaryExpression,
    IfStatement,
    InputExpression,
    TypeConversion,
    UnaryExpression,
    Assignment,
    WhileStatement
)


class Interpreter:

    def __init__(self, ast):
        self.ast = ast
        self.variables = {}
        self.variable_types = {}
        self.functions = {}

    def run(self):

        for f in self.ast.functions:
            self.functions[f.name] = f

        if "_start" not in self.functions:
            raise Exception("No _start")

        self.exec_block(
            self.functions["_start"].body
        )

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
        
        if isinstance(node, UnaryExpression):

            value = self.evaluate(
                node.operand
            )

            if node.operator == "-":
                return -value

        if isinstance(node, BinaryExpression):

            left = self.evaluate(
                node.left
            )

            right = self.evaluate(
                node.right
            )

            if node.operator == "==":
                return left == right

            if node.operator == "+":

                if (
                    isinstance(left, str)
                    or
                    isinstance(right, str)
                ):
                    return str(left) + str(right)

                return left + right
            
            if node.operator == "-":
                return left - right

            if node.operator == "*":
                return left * right

            if node.operator == "/":
                return left // right
            
            if node.operator == "%":
                return left % right

            if node.operator == "$":
                return left + left + right + right

            if node.operator == ">":
                return left > right

            if node.operator == "<":
                return left < right

            if node.operator == ">=":
                return left >= right

            if node.operator == "<=":
                return left <= right

            if node.operator == "!=":
                return left != right
            
            raise Exception(
                f"Unknown operator: {node.operator}"
            )
            
        if isinstance(node, InputExpression):

            prompt = ""

            if node.prompt:
                prompt = str(
                    self.evaluate(
                        node.prompt
                    )
                )

            return input(prompt)
        
        if isinstance(node, TypeConversion):

            value = self.evaluate(
                node.expression
            )

            if node.target_type == "str":
                return str(value)

            if node.target_type == "int":

                try:
                    return int(value)

                except:
                    raise Exception(
                        f"Cannot convert "
                        f"'{value}' to int"
                    )

            raise Exception(
                f"Unknown conversion "
                f"{node.target_type}"
            )

    def execute(self, node):

        if isinstance(node, VariableDeclaration):

            value = self.evaluate(node.value)

            if node.var_type == "int":

                if not isinstance(value, int):
                    raise Exception(
                        f"Type Error: "
                        f"{node.name} expects int"
                    )

            elif node.var_type == "str":

                if not isinstance(value, str):
                    raise Exception(
                        f"Type Error: "
                        f"{node.name} expects str"
                    )

            elif node.var_type == "bool":

                if not isinstance(value, bool):
                    raise Exception(
                        f"Type Error: "
                        f"{node.name} expects bool"
                    )

            self.variables[node.name] = value
            self.variable_types[node.name] = node.var_type

            return
        
        if isinstance(node, Assignment):

            if node.name not in self.variables:
                raise Exception(
                    f"Variable '{node.name}' not defined"
                )

            value = self.evaluate(
                node.value
            )

            expected_type = self.variable_types[
                node.name
            ]

            if (
                expected_type == "int"
                and
                not isinstance(value, int)
            ):
                raise Exception(
                    f"Type Error: {node.name} expects int"
                )

            if (
                expected_type == "str"
                and
                not isinstance(value, str)
            ):
                raise Exception(
                    f"Type Error: {node.name} expects str"
                )

            if (
                expected_type == "bool"
                and
                not isinstance(value, bool)
            ):
                raise Exception(
                    f"Type Error: {node.name} expects bool"
                )

            self.variables[node.name] = value

            return

        if isinstance(node, IfStatement):

            condition = self.evaluate(
                node.condition
            )

            if condition:

                for stmt in node.then_body:
                    self.execute(stmt)

            elif node.else_body:

                for stmt in node.else_body:
                    self.execute(stmt)

            return
        
        if isinstance(node, WhileStatement):

            while self.evaluate(
                node.condition
            ):

                for stmt in node.body:
                    self.execute(stmt)

            return

        if isinstance(node, FunctionCall):

            args = [
                self.evaluate(a)
                for a in node.args
            ]

            if node.name == "print":
                print(args[0], end="")
                return

            if node.name == "println":
                print(args[0])
                return

            if node.name in self.functions:

                func = self.functions[
                    node.name
                ]

                if len(args) != len(func.params):

                    raise Exception(
                        f"{node.name} expects "
                        f"{len(func.params)} "
                        f"arguments"
                    )

                old_vars = self.variables.copy()
                old_types = self.variable_types.copy()

                for i in range(
                    len(func.params)
                ):

                    param_type, param_name = (
                        func.params[i]
                    )

                    value = args[i]

                    if (
                        param_type == "int"
                        and
                        not isinstance(
                            value,
                            int
                        )
                    ):
                        raise Exception(
                            f"{param_name} "
                            f"expects int"
                        )

                    if (
                        param_type == "str"
                        and
                        not isinstance(
                            value,
                            str
                        )
                    ):
                        raise Exception(
                            f"{param_name} "
                            f"expects str"
                        )

                    if (
                        param_type == "bool"
                        and
                        not isinstance(
                            value,
                            bool
                        )
                    ):
                        raise Exception(
                            f"{param_name} "
                            f"expects bool"
                        )

                    self.variables[
                        param_name
                    ] = value

                    self.variable_types[
                        param_name
                    ] = param_type

                self.exec_block(
                    func.body
                )

                self.variables = old_vars
                self.variable_types = old_types

                return

            raise Exception(
                f"Unknown fn {node.name}"
            )
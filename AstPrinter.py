from Parser import *

class ASTPrinter:

    def print(self, node):
        self._print_node(node, 0)

    def indent(self, level):
        return "    " * level

    def _print_node(self, node, level):

        # -----------------
        # Program
        # -----------------

        if isinstance(node, Program):

            print(f"{self.indent(level)}", end="")
            print("{")

            for func in node.functions:
                self._print_node(func, level + 1)

            print(f"{self.indent(level)}", end="")
            print("}")
            return

        # -----------------
        # FunctionDef
        # -----------------

        if isinstance(node, FunctionDef):

            print(
                f"{self.indent(level)}"
                f"FunctionDef("
            )

            print(
                f"{self.indent(level + 1)}"
                f"{node.name},"
            )

            print(
                f"{self.indent(level + 1)}"
                f"PARAMS"
            )

            print(
                f"{self.indent(level + 1)}["
            )

            for param_type, param_name in node.params:

                print(
                    f"{self.indent(level + 2)}"
                    f"({param_type}, {param_name})"
                )

            print(
                f"{self.indent(level + 1)}]"
            )

            print(
                f"{self.indent(level + 1)}"
                f"BODY"
            )

            print(
                f"{self.indent(level + 1)}["
            )

            for stmt in node.body:
                self._print_node(
                    stmt,
                    level + 2
                )

            print(
                f"{self.indent(level + 1)}]"
            )

            print(
                f"{self.indent(level)}"
                f")"
            )

            return

        # -----------------
        # VariableDeclaration
        # -----------------

        if isinstance(node, VariableDeclaration):

            print(
                f"{self.indent(level)}"
                f"VariableDeclaration("
            )

            print(
                f"{self.indent(level + 1)}"
                f"{node.var_type},"
            )

            print(
                f"{self.indent(level + 1)}"
                f"{node.name},"
            )

            self._print_node(
                node.value,
                level + 1
            )

            print(
                f"{self.indent(level)})"
            )

            return

        # -----------------
        # Assignment
        # -----------------

        if isinstance(node, Assignment):

            print(
                f"{self.indent(level)}"
                f"Assignment("
            )

            print(
                f"{self.indent(level + 1)}"
                f"{node.name},"
            )

            self._print_node(
                node.value,
                level + 1
            )

            print(
                f"{self.indent(level)})"
            )

            return

        # -----------------
        # FunctionCall
        # -----------------

        if isinstance(node, FunctionCall):

            print(
                f"{self.indent(level)}"
                f"FunctionCall("
            )

            print(
                f"{self.indent(level + 1)}"
                f"{node.name},"
            )

            print(
                f"{self.indent(level + 1)}["
            )

            for arg in node.args:
                self._print_node(
                    arg,
                    level + 2
                )

            print(
                f"{self.indent(level + 1)}]"
            )

            print(
                f"{self.indent(level)})"
            )

            return

        # -----------------
        # TypeConversion
        # -----------------

        if isinstance(node, TypeConversion):

            print(
                f"{self.indent(level)}"
                f"TypeConversion("
            )

            print(
                f"{self.indent(level + 1)}"
                f"{node.target_type},"
            )

            self._print_node(
                node.expression,
                level + 1
            )

            print(
                f"{self.indent(level)})"
            )

            return

        # -----------------
        # InputExpression
        # -----------------

        if isinstance(node, InputExpression):

            print(
                f"{self.indent(level)}"
                f"InputExpression("
            )

            if node.prompt:
                self._print_node(
                    node.prompt,
                    level + 1
                )

            print(
                f"{self.indent(level)})"
            )

            return

        # -----------------
        # VariableReference
        # -----------------

        if isinstance(node, VariableReference):

            print(
                f"{self.indent(level)}"
                f"VariableReference("
                f"{node.name}"
                f")"
            )

            return

        # -----------------
        # StringLiteral
        # -----------------

        if isinstance(node, StringLiteral):

            print(
                f"{self.indent(level)}"
                f'StringLiteral("{node.value}")'
            )

            return

        # -----------------
        # IntegerLiteral
        # -----------------

        if isinstance(node, IntegerLiteral):

            print(
                f"{self.indent(level)}"
                f"IntegerLiteral({node.value})"
            )

            return

        # -----------------
        # UnaryExpression
        # -----------------

        if isinstance(node, UnaryExpression):

            print(
                f"{self.indent(level)}"
                f"UnaryExpression("
            )

            print(
                f"{self.indent(level + 1)}"
                f"{node.operator}"
            )

            self._print_node(
                node.operand,
                level + 1
            )

            print(
                f"{self.indent(level)})"
            )

            return

        # -----------------
        # BinaryExpression
        # -----------------

        if isinstance(node, BinaryExpression):

            print(
                f"{self.indent(level)}"
                f"BinaryExpression("
            )

            self._print_node(
                node.left,
                level + 1
            )

            print(
                f"{self.indent(level + 1)}"
                f"{node.operator}"
            )

            self._print_node(
                node.right,
                level + 1
            )

            print(
                f"{self.indent(level)})"
            )

            return

        # -----------------
        # IfStatement
        # -----------------

        if isinstance(node, IfStatement):

            print(
                f"{self.indent(level)}"
                f"IfStatement("
            )

            self._print_node(
                node.condition,
                level + 1
            )

            print(
                f"{self.indent(level + 1)}"
                f"THEN"
            )

            print(
                f"{self.indent(level + 1)}["
            )

            for stmt in node.then_body:
                self._print_node(
                    stmt,
                    level + 2
                )

            print(
                f"{self.indent(level + 1)}]"
            )

            if node.else_body is not None:

                print(
                    f"{self.indent(level + 1)}"
                    f"ELSE"
                )

                print(
                    f"{self.indent(level + 1)}["
                )

                for stmt in node.else_body:
                    self._print_node(
                        stmt,
                        level + 2
                    )

                print(
                    f"{self.indent(level + 1)}]"
                )

            print(
                f"{self.indent(level)}"
                f")"
            )

            return

        # -----------------
        # WhileStatement
        # -----------------

        if isinstance(node, WhileStatement):

            print(
                f"{self.indent(level)}"
                f"WhileStatement("
            )

            self._print_node(
                node.condition,
                level + 1
            )

            print(
                f"{self.indent(level + 1)}"
                f"DO"
            )

            print(
                f"{self.indent(level + 1)}["
            )

            for stmt in node.body:

                self._print_node(
                    stmt,
                    level + 2
                )

            print(
                f"{self.indent(level + 1)}]"
            )

            print(
                f"{self.indent(level)}"
                f")"
            )

            return

        print(
            f"{self.indent(level)}"
            f"{node}"
        )


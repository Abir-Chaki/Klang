from Lexer import TokenType


# =====================
# AST Nodes
# =====================

class Program:
    def __init__(self, functions):
        self.functions = functions

    def __repr__(self):
        return f"Program({self.functions})"


class FunctionDef:
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def __repr__(self):
        return f"FunctionDef({self.name}, {self.body})"


class FunctionCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"FunctionCall({self.name}, {self.args})"


class StringLiteral:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'String("{self.value}")'


class IntegerLiteral:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Integer({self.value})"


class VariableReference:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"VariableReference({self.name})"


class VariableDeclaration:
    def __init__(self, var_type, name, value):
        self.var_type = var_type
        self.name = name
        self.value = value

    def __repr__(self):
        return (
            f"VariableDeclaration("
            f"{self.var_type}, "
            f"{self.name}, "
            f"{self.value})"
        )


# =====================
# Parser
# =====================

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def advance(self):
        self.pos += 1

    def eat(self, token_type):

        token = self.current()

        if token.type != token_type:
            raise Exception(
                f"Expected {token_type.name}, got {token.type.name}"
            )

        self.advance()

        return token

    # -----------------
    # Literals
    # -----------------

    def parse_string(self):

        token = self.eat(TokenType.STRING)

        return StringLiteral(token.value)

    def parse_number(self):

        token = self.eat(TokenType.NUMBER)

        return IntegerLiteral(token.value)

    # -----------------
    # Expressions
    # -----------------

    def parse_expression(self):

        if self.current().type == TokenType.STRING:
            return self.parse_string()

        if self.current().type == TokenType.NUMBER:
            return self.parse_number()

        if self.current().type == TokenType.IDENTIFIER:

            name = self.eat(
                TokenType.IDENTIFIER
            ).value

            return VariableReference(name)

        raise Exception(
            f"Unexpected token {self.current()}"
        )

    # -----------------
    # Variables
    # -----------------

    def parse_variable_declaration(self):

        var_type = self.current().value
        self.advance()

        name = self.eat(
            TokenType.IDENTIFIER
        ).value

        self.eat(TokenType.EQUAL)

        value = self.parse_expression()

        return VariableDeclaration(
            var_type,
            name,
            value
        )

    # -----------------
    # Function Calls
    # -----------------

    def parse_function_call(self):

        name = self.eat(
            TokenType.IDENTIFIER
        ).value

        self.eat(TokenType.LPAREN)

        args = []

        if self.current().type != TokenType.RPAREN:
            args.append(
                self.parse_expression()
            )

        self.eat(TokenType.RPAREN)

        return FunctionCall(
            name,
            args
        )

    # -----------------
    # Statements
    # -----------------

    def parse_statement(self):

        if self.current().type in (
            TokenType.STR,
            TokenType.INT,
            TokenType.BOOL
        ):
            return self.parse_variable_declaration()

        return self.parse_function_call()

    # -----------------
    # Functions
    # -----------------

    def parse_function(self):

        self.eat(TokenType.DEFINE)

        name = self.eat(
            TokenType.IDENTIFIER
        ).value

        self.eat(TokenType.LPAREN)
        self.eat(TokenType.RPAREN)

        self.eat(TokenType.LBRACE)

        body = []

        while self.current().type != TokenType.RBRACE:
            body.append(
                self.parse_statement()
            )

        self.eat(TokenType.RBRACE)

        return FunctionDef(
            name,
            body
        )

    # -----------------
    # Program
    # -----------------

    def parse(self):

        functions = []

        while self.current().type != TokenType.EOF:
            functions.append(
                self.parse_function()
            )

        return Program(functions)
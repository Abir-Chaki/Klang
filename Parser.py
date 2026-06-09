from Lexer import TokenType


class Program:
    def __init__(self, functions):
        self.functions = functions


class FunctionDef:
    def __init__(self, name, body):
        self.name = name
        self.body = body


class FunctionCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args


class StringLiteral:
    def __init__(self, value):
        self.value = value


class IntegerLiteral:
    def __init__(self, value):
        self.value = value


class VariableReference:
    def __init__(self, name):
        self.name = name


class VariableDeclaration:
    def __init__(self, var_type, name, value):
        self.var_type = var_type
        self.name = name
        self.value = value


class BinaryExpression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class IfStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


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
            raise Exception(f"Expected {token_type}, got {token.type}")

        self.advance()
        return token

    def parse_string(self):
        return StringLiteral(self.eat(TokenType.STRING).value)

    def parse_number(self):
        return IntegerLiteral(self.eat(TokenType.NUMBER).value)

    def parse_expression(self):

        left = self.parse_primary()

        while (
            self.current().type
            == TokenType.PLUS
        ):

            self.eat(TokenType.PLUS)

            right = self.parse_primary()

            left = BinaryExpression(
                left,
                "+",
                right
            )

        return left
    
    def parse_primary(self):

        if self.current().type == TokenType.STRING:
            return self.parse_string()

        if self.current().type == TokenType.NUMBER:
            return self.parse_number()

        if self.current().type == TokenType.IDENTIFIER:

            return VariableReference(
                self.eat(
                    TokenType.IDENTIFIER
                ).value
            )

        raise Exception(
            f"Unexpected token {self.current()}"
        )
    

    def parse_variable_declaration(self):

        var_type = self.current().value
        self.advance()

        name = self.eat(TokenType.IDENTIFIER).value
        self.eat(TokenType.EQUAL)
        value = self.parse_expression()

        return VariableDeclaration(var_type, name, value)

    def parse_function_call(self):

        name = self.eat(TokenType.IDENTIFIER).value
        self.eat(TokenType.LPAREN)

        args = []
        if self.current().type != TokenType.RPAREN:
            args.append(self.parse_expression())

        self.eat(TokenType.RPAREN)

        return FunctionCall(name, args)

    def parse_condition(self):

        left = self.parse_expression()
        self.eat(TokenType.EQUAL_EQUAL)
        right = self.parse_expression()

        return BinaryExpression(left, "==", right)

    def parse_if(self):

        self.eat(TokenType.IF)
        condition = self.parse_condition()
        self.eat(TokenType.THEN)
        self.eat(TokenType.LBRACE)

        body = []
        while self.current().type != TokenType.RBRACE:
            body.append(self.parse_statement())

        self.eat(TokenType.RBRACE)

        return IfStatement(condition, body)

    def parse_statement(self):

        if self.current().type == TokenType.IF:
            return self.parse_if()

        if self.current().type in (TokenType.STR, TokenType.INT, TokenType.BOOL):
            return self.parse_variable_declaration()

        return self.parse_function_call()

    def parse_function(self):

        self.eat(TokenType.DEFINE)
        name = self.eat(TokenType.IDENTIFIER).value

        self.eat(TokenType.LPAREN)
        self.eat(TokenType.RPAREN)

        self.eat(TokenType.LBRACE)

        body = []
        while self.current().type != TokenType.RBRACE:
            body.append(self.parse_statement())

        self.eat(TokenType.RBRACE)

        return FunctionDef(name, body)

    def parse(self):

        funcs = []

        while self.current().type != TokenType.EOF:
            funcs.append(self.parse_function())

        return Program(funcs)
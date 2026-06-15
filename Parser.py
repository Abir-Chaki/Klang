from Lexer import TokenType


class Program:
    def __init__(self, functions):
        self.functions = functions

    def __repr__(self):
        return f"Program({self.functions})"


class FunctionDef:
    def __init__(
        self,
        name,
        params,
        body
    ):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return (
            f"FunctionDef("
            f"{self.name}, "
            f"{self.params}, "
            f"{self.body})"
        )


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
    
class Assignment:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return (
            f"Assignment("
            f"{self.name}, "
            f"{self.value})"
        )


class BinaryExpression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return (
            f"BinaryExpression("
            f"{self.left}, "
            f"{self.operator}, "
            f"{self.right})"
        )
    
class UnaryExpression:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return (
            f"UnaryExpression("
            f"{self.operator}, "
            f"{self.operand})"
        )


class InputExpression:
    def __init__(self, prompt=None):
        self.prompt = prompt

    def __repr__(self):
        return f"InputExpression({self.prompt})"


class IfStatement:
    def __init__(
        self,
        condition,
        then_body,
        else_body=None
    ):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body

    def __repr__(self):
        return (
            f"IfStatement("
            f"{self.condition}, "
            f"{self.then_body}, "
            f"{self.else_body})"
        )
    
class WhileStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return (
            f"WhileStatement("
            f"{self.condition}, "
            f"{self.body})"
        )


class TypeConversion:
    def __init__(self, target_type, expression):
        self.target_type = target_type
        self.expression = expression

    def __repr__(self):
        return (
            f"TypeConversion("
            f"{self.target_type}, "
            f"{self.expression})"
        )


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
                f"Expected {token_type}, got {token.type}"
            )

        self.advance()
        return token

    def parse_string(self):
        return StringLiteral(
            self.eat(TokenType.STRING).value
        )

    def parse_number(self):
        return IntegerLiteral(
            self.eat(TokenType.NUMBER).value
        )

    def parse_expression(self):

        left = self.parse_primary()

        operator_map = {
            TokenType.PLUS: "+",
            TokenType.MINUS: "-",
            TokenType.MULTIPLY: "*",
            TokenType.DIVIDE: "/",
            TokenType.MODULO: "%",
            TokenType.DOLLAR: "$"
        }

        while self.current().type in operator_map:

            op = operator_map[
                self.current().type
            ]

            self.advance()

            right = self.parse_primary()

            left = BinaryExpression(
                left,
                op,
                right
            )

        return left
    def parse_primary(self):

        if self.current().type == TokenType.STRING:
            return self.parse_string()
        
        if self.current().type == TokenType.MINUS:

            self.eat(TokenType.MINUS)

            return UnaryExpression(
                "-",
                self.parse_primary()
            )

        if self.current().type == TokenType.NUMBER:
            return self.parse_number()

        if self.current().type in (
            TokenType.INT,
            TokenType.STR
        ):

            target_type = self.current().value

            self.advance()

            self.eat(TokenType.LPAREN)

            expr = self.parse_expression()

            self.eat(TokenType.RPAREN)

            return TypeConversion(
                target_type,
                expr
            )

        if self.current().type == TokenType.IDENTIFIER:

            name = self.eat(
                TokenType.IDENTIFIER
            ).value

            if (
                name == "input"
                and
                self.current().type == TokenType.LPAREN
            ):

                self.eat(TokenType.LPAREN)

                prompt = None

                if self.current().type != TokenType.RPAREN:
                    prompt = self.parse_expression()

                self.eat(TokenType.RPAREN)

                return InputExpression(prompt)

            return VariableReference(name)

        raise Exception(
            f"Unexpected token {self.current()}"
        )

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
    
    def parse_assignment(self):

        name = self.eat(
            TokenType.IDENTIFIER
        ).value

        self.eat(TokenType.EQUAL)

        value = self.parse_expression()

        return Assignment(
            name,
            value
        )

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

            while (
                self.current().type
                == TokenType.COMMA
            ):

                self.eat(TokenType.COMMA)

                args.append(
                    self.parse_expression()
                )

        self.eat(TokenType.RPAREN)

        return FunctionCall(
            name,
            args
        )

    def parse_condition(self):

        left = self.parse_expression()

        operator_map = {
            TokenType.EQUAL_EQUAL: "==",
            TokenType.NOT_EQUAL: "!=",
            TokenType.LESS: "<",
            TokenType.GREATER: ">",
            TokenType.LESS_EQUAL: "<=",
            TokenType.GREATER_EQUAL: ">="
        }

        if self.current().type not in operator_map:
            raise Exception(
                f"Expected comparison operator, got {self.current()}"
            )

        op = operator_map[
            self.current().type
        ]

        self.advance()

        right = self.parse_expression()

        return BinaryExpression(
            left,
            op,
            right
        )

    def parse_if(self):

        self.eat(TokenType.IF)

        condition = self.parse_condition()

        self.eat(TokenType.THEN)

        self.eat(TokenType.LBRACE)

        then_body = []

        while self.current().type != TokenType.RBRACE:
            then_body.append(
                self.parse_statement()
            )

        self.eat(TokenType.RBRACE)

        else_body = None

        if self.current().type == TokenType.ELSE:

            self.eat(TokenType.ELSE)

            self.eat(TokenType.LBRACE)

            else_body = []

            while self.current().type != TokenType.RBRACE:
                else_body.append(
                    self.parse_statement()
                )

            self.eat(TokenType.RBRACE)

        return IfStatement(
            condition,
            then_body,
            else_body
        )
    
    def parse_while(self):

        self.eat(TokenType.WHILE)

        condition = self.parse_condition()

        self.eat(TokenType.DO)

        self.eat(TokenType.LBRACE)

        body = []

        while self.current().type != TokenType.RBRACE:
            body.append(
                self.parse_statement()
            )

        self.eat(TokenType.RBRACE)

        return WhileStatement(
            condition,
            body
        )
    def parse_statement(self):
        if self.current().type == TokenType.IF:
            return self.parse_if()
        
        if self.current().type == TokenType.WHILE:
            return self.parse_while()

        if self.current().type in (
            TokenType.STR,
            TokenType.INT,
            TokenType.BOOL
        ):
            return self.parse_variable_declaration()

        if (
            self.current().type == TokenType.IDENTIFIER
            and
            self.tokens[self.pos + 1].type == TokenType.EQUAL
        ):
            return self.parse_assignment()

        return self.parse_function_call()

    def parse_function(self):

        self.eat(TokenType.DEFINE)

        name = self.eat(
            TokenType.IDENTIFIER
        ).value

        self.eat(TokenType.LPAREN)

        params = []

        if self.current().type != TokenType.RPAREN:

            param_type = self.current().value
            self.advance()

            param_name = self.eat(
                TokenType.IDENTIFIER
            ).value

            params.append(
                (param_type, param_name)
            )

            while self.current().type == TokenType.COMMA:

                self.eat(TokenType.COMMA)

                param_type = self.current().value
                self.advance()

                param_name = self.eat(
                    TokenType.IDENTIFIER
                ).value

                params.append(
                    (param_type, param_name)
                )

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
            params,
            body
        )

    def parse(self):

        funcs = []

        while self.current().type != TokenType.EOF:
            funcs.append(
                self.parse_function()
            )

        return Program(funcs)
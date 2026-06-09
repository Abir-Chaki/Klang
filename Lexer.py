from enum import Enum, auto


class TokenType(Enum):
    DEFINE = auto()

    IF = auto()
    THEN = auto()

    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()

    STR = auto()
    INT = auto()
    BOOL = auto()

    EQUAL = auto()
    EQUAL_EQUAL = auto()

    EOF = auto()


KEYWORDS = {
    "define": TokenType.DEFINE,
    "if": TokenType.IF,
    "then": TokenType.THEN,

    "str": TokenType.STR,
    "int": TokenType.INT,
    "bool": TokenType.BOOL,
}


class Token:
    def __init__(self, token_type, value=None):
        self.type = token_type
        self.value = value

    def __repr__(self):
        if self.value is None:
            return self.type.name
        return f"{self.type.name}({self.value})"


class Lexer:

    def __init__(self, text):
        self.text = text
        self.pos = 0

    def current(self):
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]

    def peek(self):
        if self.pos + 1 >= len(self.text):
            return None
        return self.text[self.pos + 1]

    def advance(self):
        self.pos += 1

    def skip_whitespace(self):
        while self.current() and self.current().isspace():
            self.advance()

    def skip_comment(self):
        while self.current() and self.current() != "\n":
            self.advance()

    def identifier(self):
        result = ""

        while self.current() and (self.current().isalnum() or self.current() == "_"):
            result += self.current()
            self.advance()

        if result in KEYWORDS:
            return Token(KEYWORDS[result], result)

        return Token(TokenType.IDENTIFIER, result)

    def string(self):
        self.advance()
        result = ""

        while self.current() and self.current() != '"':
            result += self.current()
            self.advance()

        self.advance()
        return Token(TokenType.STRING, result)

    def number(self):
        result = ""

        while self.current() and self.current().isdigit():
            result += self.current()
            self.advance()

        return Token(TokenType.NUMBER, int(result))

    def tokenize(self):
        tokens = []

        while self.current():

            if self.current().isspace():
                self.skip_whitespace()
                continue

            if self.current() == "?" and self.peek() == "?":
                self.skip_comment()
                continue

            # ==
            if self.current() == "=" and self.peek() == "=":
                tokens.append(Token(TokenType.EQUAL_EQUAL))
                self.advance()
                self.advance()
                continue

            if self.current() == "=":
                tokens.append(Token(TokenType.EQUAL))
                self.advance()
                continue

            if self.current().isalpha() or self.current() == "_":
                tokens.append(self.identifier())
                continue

            if self.current() == '"':
                tokens.append(self.string())
                continue

            if self.current().isdigit():
                tokens.append(self.number())
                continue

            if self.current() == "(":
                tokens.append(Token(TokenType.LPAREN))
                self.advance()
                continue

            if self.current() == ")":
                tokens.append(Token(TokenType.RPAREN))
                self.advance()
                continue

            if self.current() == "{":
                tokens.append(Token(TokenType.LBRACE))
                self.advance()
                continue

            if self.current() == "}":
                tokens.append(Token(TokenType.RBRACE))
                self.advance()
                continue

            raise Exception(f"Unknown char: {self.current()}")

        tokens.append(Token(TokenType.EOF))
        return tokens
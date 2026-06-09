from enum import Enum, auto


# =====================
# Token Types
# =====================

class TokenType(Enum):
    DEFINE = auto()

    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    LPAREN = auto()      # (
    RPAREN = auto()      # )
    LBRACE = auto()      # {
    RBRACE = auto()      # }
    STR = auto()         # str
    INT = auto()         # int
    BOOL = auto()        # bool
    EQUAL = auto()       # = 

    EOF = auto()


# =====================
# Keywords
# =====================

KEYWORDS = {
    "define": TokenType.DEFINE,
    "str": TokenType.STR,
    "int": TokenType.INT,
    "bool": TokenType.BOOL
}


# =====================
# Token Class
# =====================

class Token:
    def __init__(self, token_type, value=None):
        self.type = token_type
        self.value = value

    def __repr__(self):
        if self.value is None:
            return self.type.name

        return f"{self.type.name}({self.value})"


# =====================
# Lexer
# =====================

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

    # -----------------
    # Whitespace
    # -----------------

    def skip_whitespace(self):
        while self.current() and self.current().isspace():
            self.advance()

    # -----------------
    # Single-line comments
    # ?? comment
    # -----------------

    def skip_comment(self):
        while self.current() and self.current() != "\n":
            self.advance()

    # -----------------
    # Identifiers
    # -----------------

    def identifier(self):
        result = ""

        while (
            self.current()
            and (self.current().isalnum() or self.current() == "_")
        ):
            result += self.current()
            self.advance()

        if result in KEYWORDS:
            return Token(KEYWORDS[result], result)

        return Token(TokenType.IDENTIFIER, result)

    # -----------------
    # Strings
    # -----------------

    def string(self):
        self.advance()  # skip opening "

        result = ""

        while self.current() and self.current() != '"':
            result += self.current()
            self.advance()

        self.advance()  # skip closing "

        return Token(TokenType.STRING, result)

    # -----------------
    # Numbers
    # -----------------

    def number(self):
        result = ""

        while self.current() and self.current().isdigit():
            result += self.current()
            self.advance()

        return Token(TokenType.NUMBER, int(result))

    # -----------------
    # Main Tokenizer
    # -----------------

    def tokenize(self):
        tokens = []

        while self.current():

            # whitespace
            if self.current().isspace():
                self.skip_whitespace()
                continue

            # ?? comments
            if self.current() == "?" and self.peek() == "?":
                self.skip_comment()
                continue

            # identifiers
            if self.current().isalpha() or self.current() == "_":
                tokens.append(self.identifier())
                continue

            # strings
            if self.current() == '"':
                tokens.append(self.string())
                continue

            # numbers
            if self.current().isdigit():
                tokens.append(self.number())
                continue

            # symbols

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
            if self.current() == "=":
                tokens.append(Token(TokenType.EQUAL))
                self.advance()
                continue

            raise Exception(
                f"Unknown character: {self.current()}"
            )

        tokens.append(Token(TokenType.EOF))
        return tokens
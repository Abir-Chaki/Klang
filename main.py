import sys

from Lexer import Lexer
from Parser import Parser
from Interpret import Interpreter


def main():

    if len(sys.argv) != 2:
        print("Klang Interpreter")
        print("Usage:")
        print("    python main.py <file.kl>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    lexer = Lexer(code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter(ast)
    interpreter.run()


if __name__ == "__main__":
    main()
    
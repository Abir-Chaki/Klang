import sys

from Lexer import Lexer
from Parser import Parser
from Interpret import Interpreter
from AstPrinter import ASTPrinter


VERSION = "Beta-0010"


def print_help():
    print("Klang Interpreter")
    print()
    print("Usage:")
    print("    kl <file.kl>")
    print("    kl <file.kl> -t")
    print("    kl <file.kl> -a")
    print()
    print("Options:")
    print("    -t          Print tokens only")
    print("    -a          Print AST only")
    print("    --version   Show version")
    print("    --help      Show help")


def main():

    # -------------------------
    # No arguments
    # -------------------------

    if len(sys.argv) == 1:
        print_help()
        sys.exit(0)

    # -------------------------
    # Special commands
    # -------------------------

    if sys.argv[1] == "--version":
        print(f"Klang Interpreter {VERSION}")
        sys.exit(0)

    if sys.argv[1] == "--help":
        print_help()
        sys.exit(0)

    # -------------------------
    # Parse args
    # -------------------------

    filename = sys.argv[1]

    mode = "run"

    if len(sys.argv) >= 3:
        mode = sys.argv[2]

    # -------------------------
    # Read file
    # -------------------------

    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    # -------------------------
    # Lexing
    # -------------------------

    lexer = Lexer(code)
    tokens = lexer.tokenize()

    if mode == "-t":

        for token in tokens:
            print(token)

        sys.exit(0)

    # -------------------------
    # Parsing
    # -------------------------

    parser = Parser(tokens)
    ast = parser.parse()

    if mode == "-a":

        printer = ASTPrinter()
        printer.print(ast)

        sys.exit(0)

    # -------------------------
    # Execute
    # -------------------------

    interpreter = Interpreter(ast)
    interpreter.run()


if __name__ == "__main__":
    main()
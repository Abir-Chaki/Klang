# Klang

Klang is a hobby programming language written in Python.

Current features:

- Variables
- User input
- Type checking
- String concatenation
- Addition, Subtraction, Multiplication, Division
- Functions
- if statements
- else statements
- Operators
- variable reassignment
- while loops
- user-defined functions
- functions with parameters
- AST generation
- Token inspection

## Example

```kl
define chk() {
    str name = input("Name: ")
    int age = int(input("Age: "))

    println("Hello " + name)

    if age == 18 then {
        println("You are 18")
    }
    else {
        println("You are not 18")
    }
}

define _start() {
    chk()
}
```

## Usage

Run a program:

```powershell
kl hello.kl
```

Print tokens:

```powershell
kl hello.kl -t
```

Print AST:

```powershell
kl hello.kl -a
```

Show version:

```powershell
kl --version
```

## Example AST

```text
{
    FunctionDef(
        add,
        PARAMS
        [
            (int, a)
            (int, b)
        ]
        BODY
        [
            FunctionCall(
                println,
                [
                    BinaryExpression(
                        VariableReference(a)
                        +
                        VariableReference(b)
                    )
                ]
            )
        ]
    )
    FunctionDef(
        _start,
        PARAMS
        [
        ]
        BODY
        [
            VariableDeclaration(
                int,
                num1,
                TypeConversion(
                    int,
                    InputExpression(
                        StringLiteral("Enter first number: ")
                    )
                )
            )
            VariableDeclaration(
                int,
                num2,
                TypeConversion(
                    int,
                    InputExpression(
                        StringLiteral("Enter second number: ")
                    )
                )
            )
            FunctionCall(
                add,
                [
                    VariableReference(num1)
                    VariableReference(num2)
                ]
            )
        ]
    )
}
```

## Roadmap


- return values
- elif/else if/elseif statement
- Booleans
- and/or/not keywords
- compiler (klcc.exe)
- Standard Libararies
- Arrays
- Array Indexing
- for loops
- file API
- Future OS

## Status

Current version: Beta Build 0011

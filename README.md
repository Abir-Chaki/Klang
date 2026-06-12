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
- AST generation
- Token inspection

## Example

```kl
define _start() {

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
        _start,
        [
            VariableDeclaration(
                int,
                age,
                TypeConversion(
                    int,
                    InputExpression(
                        StringLiteral("Age: ")
                    )
                )
            )
        ]
    )
}
```

## Roadmap

- variable reassignment
- while loops
- user-defined functions
- functions with parameters
- return values
- compiler (klcc)
- Booleans
- Arrays
- Future OS

## Status

Current version: Beta Build 0007

# Cimple Compiler
A compiler for the Cimple programming language, written in Python.

## Overview

This project is a fully-featured compiler for a custom programming language called "cimple". The compiler is implemented in Python and translates cimple source code into RISC-V assembly code. It manages the entire compilation pipeline, from lexical analysis to final code generation, making it a comprehensive tool for understanding compiler design principles.

## The 'cimple' Language

Cimple is a procedural programming language with a C-like syntax. Below are some of its key features:

### Program Structure
A cimple program starts with the `program` keyword, followed by the program name and a block of code enclosed in curly braces `{}`. The program must end with a period `.`.

```c
program myProgram {
    // declarations and statements
}.
```

### Comments
Comments are enclosed in hash symbols `#`.

```c
# This is a comment #
```

### Variables and Data Types
Variables are declared using the `declare` keyword. The language appears to primarily support integer data types.

```c
declare my_variable, another_variable;
```

### Control Flow
Cimple supports several control flow statements:
- **If-Else:** `if (<condition>) { ... } else { ... }`
- **While:** `while (<condition>) { ... }`
- **Switch-Case:** `switchcase case (<condition>) { ... } default { ... }`
- **For-Case:** `forcase case (<condition>) { ... } default { ... }`
- **In-Case:** `incase case (<condition>) { ... }`

### Functions and Procedures
- **Functions:** Declared with the `function` keyword, can return a value.
- **Procedures:** Declared with the `procedure` keyword, do not return a value.
- **Parameters:** Can be passed by value (`in`) or by reference (`inout`).

```c
function factorial(in n) {
    # function body
}
```

### Input/Output
- **Input:** `input(variable);`
- **Print:** `print(expression);`

## Compiler Architecture

The compiler is designed in a modular way, with different components responsible for specific phases of the compilation process:

- **`FileParser.py`**: A simple utility to read the source file character by character.
- **`LexicalAnalyser.py`**: Implements the lexical analysis phase. It uses a state machine to scan the source code and produce a stream of tokens.
- **`SyntaxAnalyser.py`**: This is the heart of the compiler, performing syntax analysis using a recursive descent parser. It enforces the grammar of the 'cimple' language and orchestrates the generation of intermediate code.
- **`SymbolsTable.py`**: Manages the symbol table, which stores information about identifiers like variables, functions, and procedures, along with their scope and attributes.
- **`IntermediateCode.py`**: Handles the generation of intermediate code in the form of quadruples. It also includes functionality to convert the intermediate code into a C program for verification purposes.
- **`FinalCode.py`**: The final stage of the compiler, which translates the intermediate code into RISC-V assembly code.
- **`cimple.py`**: The main driver of the compiler. It takes a 'cimple' source file as input and runs it through the entire compilation pipeline.

## Usage

To compile a 'cimple' source file, run the `cimple.py` script from your terminal, passing the path to the source file as an argument.

```bash
python cimple.py tests/factorial.c
```

### Output Files

The compiler generates the following output files in the root directory:

- **`test.int`**: The intermediate code, represented as a series of quadruples.
- **`test.c`**: A C language representation of the intermediate code, which can be used for verification.
- **`test.symb`**: A dump of the symbol table, showing all declared identifiers and their scopes.
- **`test.asm`**: The final RISC-V assembly code.

## Code Example

Here is an example of a 'cimple' program that calculates the factorial of a number:

### `factorial.c`

```c
program factorial
{
    declare x;
    declare i, fact;

    input(x);
    fact := 1;
    i := 1;
    while(i <= x)
    {
        fact := fact * i;
        i := i + 1;
    };
    print(fact);
}.
```

### Generated Intermediate Code (`test.int`)

```
100: begin_block, factorial, _, _
101: in, x, _, _
102: :=, 1, _, fact
103: :=, 1, _, i
104: <=, i, x, 106
105: jump, _, _, 112
106: *, fact, i, T_1
107: :=, T_1, _, fact
108: +, i, 1, T_2
109: :=, T_2, _, i
110: jump, _, _, 104
111: out, fact, _, _
112: halt, _, _, _
113: end_block, factorial, _, _
```

### Generated Final Code (`test.asm`)
```assembly
L000:
		j main
main:
L100:
		addi sp, sp, 24
		mv gp, sp
L101:
		li a7, 5
		ecall
		sw a0, -12(gp)
L102:
		li t1, 1
		sw t1, -20(gp)
L103:
		li t1, 1
		sw t1, -16(gp)
L104:
		lw t1, -16(gp)
		lw t2, -12(gp)
		ble t1, t2, L106
L105:
		j L112
L106:
		lw t1, -20(gp)
		lw t2, -16(gp)
		mul t1, t1, t2
		sw t1, -24(gp)
L107:
		lw t1, -24(gp)
		sw t1, -20(gp)
L108:
		lw t1, -16(gp)
		li t2, 1
		add t1, t1, t2
		sw t1, -28(gp)
L109:
		lw t1, -28(gp)
		sw t1, -16(gp)
L110:
		j L104
L111:
		lw a0, -20(gp)
		li a7, 1
		ecall
L112:
		li a0, 0
		li a7, 93
		ecall
L113:
```

## Project Structure

The repository is organized as follows:

- **`cimple.py`**: The main entry point for the compiler.
- **`FileParser.py`**: Handles file reading operations.
- **`LexicalAnalyser.py`**: Contains the lexical analyzer and token definitions.
- **`SyntaxAnalyser.py`**: Implements the syntax analyzer and parsing logic.
- **`IntermediateCode.py`**: Manages intermediate code generation.
- **`SymbolsTable.py`**: Contains the symbol table implementation.
- **`FinalCode.py`**: Handles the final code generation.
- **`tests/`**: A directory containing sample 'cimple' source files for testing.
- **`Phase1/`**, **`Phase2/`**, **`Phase3/`**: These directories may contain earlier versions or specific components of the compiler from different development phases.
- **`Report/`**, **`diagrams/`**, **`ss/`**: These directories likely contain project-related documentation, such as reports, diagrams, and screenshots.
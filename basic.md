# Tiny BASIC Interpreter

A complete BASIC interpreter written in Python that supports integer arithmetic, variables, arrays, control flow, and file I/O.

## Features

- **Integer arithmetic**: Addition, subtraction, multiplication, division with proper operator precedence
- **Variables**: Single-letter variables A-Z (automatically initialized to 0)
- **Arrays**: Single-letter arrays A-Z with DIM statement
- **Control flow**: GOTO, IF-THEN with comparison operators
- **I/O**: PRINT statement with strings and expressions
- **File operations**: LOAD and SAVE programs
- **Interactive mode**: Execute statements directly or build programs line-by-line

#

## Running

```bash
python basic.py
```

## Language Reference

### Commands (Interactive Mode)

- **NEW** - Clear the current program and reset all variables
- **LIST** - Display the current program
- **RUN** - Execute the current program
- **LOAD filename** - Load a program from a file
- **SAVE filename** - Save the current program to a file
- **QUIT** - Exit the interpreter

### Statements

#### PRINT
Print comma-separated values and string literals.

```basic
10 PRINT "Hello, World!"
20 PRINT "The answer is", 42
30 PRINT A, B, C
40 PRINT "X =", X, "Y =", Y
```

#### LET
Assign values to variables or array elements.

```basic
10 LET A = 10
20 LET B = A + 5
30 LET C = (A + B) * 2
40 LET D[0] = 100
50 LET D[I] = D[I-1] + 1
```

The LET keyword is optional:
```basic
10 A = 10
20 B = A + 5
```

#### GOTO
Jump to a specific line number.

```basic
10 LET I = 0
20 PRINT I
30 LET I = I + 1
40 IF I < 10 GOTO 20
50 END
```

#### IF
Conditional execution with comparison operators: =, <, >, <=, >=, <>, !=

```basic
10 LET A = 5
20 IF A > 0 PRINT "Positive"
30 IF A = 5 GOTO 100
40 IF A < 10 THEN PRINT "Less than 10"
50 IF A <> 0 THEN GOTO 200
```

#### DIM
Declare an array with a specified size.

```basic
10 DIM A[100]
20 DIM B[50]
30 LET A[0] = 1
40 LET A[1] = 2
```

Arrays are zero-indexed and all elements are initialized to 0.

#### END
Mark the end of the program.

```basic
100 END
```

### Operators

**Arithmetic operators** (in order of precedence):
- `*` - Multiplication
- `/` - Integer division
- `+` - Addition
- `-` - Subtraction

**Comparison operators**:
- `=` or `==` - Equal to
- `<` - Less than
- `>` - Greater than
- `<=` - Less than or equal to
- `>=` - Greater than or equal to
- `<>` or `!=` - Not equal to

### Variables and Arrays

- **Variables**: A-Z (single letters, case-insensitive)
- **Arrays**: A-Z (must be declared with DIM before use)
- All variables start at 0
- Arrays support subscript expressions: `A[I+1]`, `B[I*2]`

## Usage Examples

### Example 1: Simple Calculation

```basic
> 10 PRINT "Enter calculation example:"
> 20 LET A = 10
> 30 LET B = 20
> 40 LET C = (A + B) * 2
> 50 PRINT "Result:", C
> 60 END
> RUN
Enter calculation example:
Result: 60
```

### Example 2: Loop with Counter

```basic
> 10 LET I = 1
> 20 PRINT I
> 30 LET I = I + 1
> 40 IF I <= 10 GOTO 20
> 50 END
> RUN
1
2
3
4
5
6
7
8
9
10
```

### Example 3: Fibonacci Sequence (Using Arrays)

See `fibonacci.bas`:

```basic
10 PRINT "Fibonacci Sequence Generator"
20 PRINT "How many terms? (max 20)"
30 LET N = 15
40 DIM F[20]
50 LET F[0] = 0
60 LET F[1] = 1
70 LET I = 2
80 IF I >= N GOTO 120
90 LET F[I] = F[I-1] + F[I-2]
100 LET I = I + 1
110 GOTO 80
120 PRINT "First", N, "Fibonacci numbers:"
130 LET I = 0
140 IF I >= N GOTO 180
150 PRINT F[I]
160 LET I = I + 1
170 GOTO 140
180 END
```

Load and run:
```bash
> LOAD fibonacci.bas
> RUN
```

### Example 4: Prime Number Checker

See `prime.bas`:

```basic
10 PRINT "Prime Number Checker"
20 LET N = 29
30 PRINT "Checking if", N, "is prime..."
40 IF N < 2 GOTO 200
50 LET I = 2
60 IF I * I > N GOTO 180
70 LET R = N / I
80 LET T = R * I
90 IF T = N GOTO 200
100 LET I = I + 1
110 GOTO 60
180 PRINT N, "is PRIME"
190 GOTO 210
200 PRINT N, "is NOT prime"
210 END
```

### Example 5: Direct Statement Execution

You can also execute statements directly without line numbers:

```bash
> LET A = 100
> PRINT "The value is", A
The value is 100
> LET B = A * 2
> PRINT B
200
```

### Example 6: File Operations

Save your program:
```bash
> SAVE myprogram.bas
Program saved to myprogram.bas
```

Load a program:
```bash
> LOAD myprogram.bas
Program loaded from myprogram.bas
> LIST
```

Clear and start fresh:
```bash
> NEW
Program cleared.
```

## Sample Session

```
Tiny BASIC Interpreter
Commands: NEW, LIST, RUN, LOAD <file>, SAVE <file>, QUIT
Statements: PRINT, LET, GOTO, IF, DIM, END

> 10 PRINT "Counting down..."
> 20 LET N = 5
> 30 PRINT N
> 40 LET N = N - 1
> 50 IF N > 0 GOTO 30
> 60 PRINT "Blastoff!"
> 70 END
> LIST
10 PRINT "Counting down..."
20 LET N = 5
30 PRINT N
40 LET N = N - 1
50 IF N > 0 GOTO 30
60 PRINT "Blastoff!"
70 END
> RUN
Counting down...
5
4
3
2
1
Blastoff!
> QUIT
Goodbye!
```

## Implementation Notes

### Memory Limits
- Maximum 1000 program lines
- Maximum 256 characters per line
- 26 variables (A-Z)
- 26 arrays (A-Z)
- Maximum array size: 1000 elements

### Parser Features
- Recursive descent parser for expressions
- Proper operator precedence (multiplication/division before addition/subtraction)
- Parentheses support in expressions
- Case-insensitive keywords and variable names

### Error Handling
- Division by zero detection
- Array bounds checking
- Undefined array detection
- Line number validation

## Limitations

- Integer arithmetic only (no floating-point)
- No string variables (only string literals in PRINT)
- No INPUT statement (must modify program to change values)
- No FOR/NEXT loops (use IF/GOTO instead)
- No subroutines (GOSUB/RETURN)
- Single-letter variable and array names only

## Future Enhancements

Potential improvements:
- INPUT statement for user input
- FOR/NEXT loops
- GOSUB/RETURN for subroutines
- String variables
- More built-in functions (ABS, SQR, RND, etc.)
- Line editing capabilities
- Floating-point arithmetic

## License

This is a educational/demonstration project. Feel free to use and modify as needed.

#!/usr/bin/env python3
"""Tiny BASIC Interpreter"""

import sys

# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

class Token:
    def __init__(self, kind, value):
        self.kind = kind   # 'NUM', 'STR', 'ID', 'OP', 'KW', 'EOF'
        self.value = value

    def __repr__(self):
        return f"Token({self.kind}, {self.value!r})"


KEYWORDS = {'PRINT', 'LET', 'GOTO', 'IF', 'THEN', 'DIM', 'END',
            'NEW', 'LIST', 'RUN', 'LOAD', 'SAVE', 'QUIT'}


def tokenize(line):
    tokens = []
    i = 0
    while i < len(line):
        c = line[i]
        if c in ' \t':
            i += 1
        elif c == '"':
            j = i + 1
            while j < len(line) and line[j] != '"':
                j += 1
            tokens.append(Token('STR', line[i+1:j]))
            i = j + 1
        elif c.isdigit():
            j = i
            while j < len(line) and line[j].isdigit():
                j += 1
            tokens.append(Token('NUM', int(line[i:j])))
            i = j
        elif c.isalpha():
            j = i
            while j < len(line) and line[j].isalnum():
                j += 1
            word = line[i:j].upper()
            if word in KEYWORDS:
                tokens.append(Token('KW', word))
            else:
                tokens.append(Token('ID', word))
            i = j
        elif c in '<>!':
            if i + 1 < len(line) and line[i+1] in '=>':
                tokens.append(Token('OP', line[i:i+2]))
                i += 2
            else:
                tokens.append(Token('OP', c))
                i += 1
        elif c == '=':
            if i + 1 < len(line) and line[i+1] == '=':
                tokens.append(Token('OP', '=='))
                i += 2
            else:
                tokens.append(Token('OP', '='))
                i += 1
        elif c in '+-*/(),[]':
            tokens.append(Token('OP', c))
            i += 1
        else:
            i += 1  # skip unknown chars
    tokens.append(Token('EOF', None))
    return tokens


# ---------------------------------------------------------------------------
# Parser / Evaluator
# ---------------------------------------------------------------------------

class Parser:
    def __init__(self, tokens, variables, arrays):
        self.tokens = tokens
        self.pos = 0
        self.variables = variables
        self.arrays = arrays

    def peek(self):
        return self.tokens[self.pos]

    def consume(self, kind=None, value=None):
        tok = self.tokens[self.pos]
        if kind and tok.kind != kind:
            raise RuntimeError(f"Expected {kind}, got {tok}")
        if value and tok.value != value:
            raise RuntimeError(f"Expected {value!r}, got {tok.value!r}")
        self.pos += 1
        return tok

    def match(self, kind=None, value=None):
        tok = self.peek()
        if kind and tok.kind != kind:
            return False
        if value and tok.value != value:
            return False
        return True

    # Expression parser (recursive descent)
    def parse_expr(self):
        return self.parse_add()

    def parse_add(self):
        left = self.parse_mul()
        while self.match('OP') and self.peek().value in ('+', '-'):
            op = self.consume().value
            right = self.parse_mul()
            left = (left + right) if op == '+' else (left - right)
        return left

    def parse_mul(self):
        left = self.parse_unary()
        while self.match('OP') and self.peek().value in ('*', '/'):
            op = self.consume().value
            right = self.parse_unary()
            if op == '/':
                if right == 0:
                    raise RuntimeError("Division by zero")
                left = int(left / right)  # integer division, truncate toward zero
            else:
                left = left * right
        return left

    def parse_unary(self):
        if self.match('OP', '-'):
            self.consume()
            return -self.parse_primary()
        if self.match('OP', '+'):
            self.consume()
        return self.parse_primary()

    def parse_primary(self):
        tok = self.peek()
        if tok.kind == 'NUM':
            self.consume()
            return tok.value
        if tok.kind == 'OP' and tok.value == '(':
            self.consume('OP', '(')
            val = self.parse_expr()
            self.consume('OP', ')')
            return val
        if tok.kind == 'ID':
            name = self.consume().value[0]  # single letter
            if self.match('OP', '['):
                self.consume('OP', '[')
                idx = self.parse_expr()
                self.consume('OP', ']')
                if name not in self.arrays:
                    raise RuntimeError(f"Array {name} not declared")
                arr = self.arrays[name]
                if idx < 0 or idx >= len(arr):
                    raise RuntimeError(f"Array {name} index {idx} out of bounds")
                return arr[idx]
            return self.variables.get(name, 0)
        raise RuntimeError(f"Unexpected token in expression: {tok}")

    def parse_comparison(self):
        left = self.parse_expr()
        if self.match('OP') and self.peek().value in ('=', '==', '<', '>', '<=', '>=', '<>', '!='):
            op = self.consume().value
            right = self.parse_expr()
            return self._compare(left, op, right)
        return left  # just a value, treat nonzero as true

    def _compare(self, left, op, right):
        if op in ('=', '=='):  return left == right
        if op == '<':          return left < right
        if op == '>':          return left > right
        if op == '<=':         return left <= right
        if op == '>=':         return left >= right
        if op in ('<>', '!='): return left != right
        return False


# ---------------------------------------------------------------------------
# Interpreter
# ---------------------------------------------------------------------------

class Interpreter:
    def __init__(self):
        self.program = {}       # line_num -> source string
        self.variables = {}     # A-Z -> int
        self.arrays = {}        # A-Z -> list
        self._reset_state()

    def _reset_state(self):
        self.variables = {chr(c): 0 for c in range(ord('A'), ord('Z') + 1)}
        self.arrays = {}

    def load_file(self, filename):
        with open(filename, 'rb') as f:
            raw = f.read()
        # detect encoding by BOM
        if raw[:2] in (b'\xff\xfe', b'\xfe\xff'):
            content = raw.decode('utf-16')
        elif raw[:3] == b'\xef\xbb\xbf':
            content = raw[3:].decode('utf-8')
        else:
            content = raw.decode('utf-8', errors='replace')
        for line in content.splitlines():
            if line.strip():
                self._add_line(line)
        print(f"Program loaded from {filename}")

    def save_file(self, filename):
        with open(filename, 'w') as f:
            for num in sorted(self.program):
                f.write(self.program[num] + '\n')
        print(f"Program saved to {filename}")

    def _add_line(self, line):
        tokens = tokenize(line)
        if tokens[0].kind == 'NUM':
            num = tokens[0].value
            self.program[num] = line.strip()
        else:
            self._exec_tokens(tokens)

    def list_program(self):
        for num in sorted(self.program):
            print(self.program[num])

    def run(self):
        lines = sorted(self.program.keys())
        if not lines:
            return
        pc = 0  # index into lines list
        while pc < len(lines):
            num = lines[pc]
            src = self.program[num]
            tokens = tokenize(src)
            tokens = tokens[1:]  # skip line number token
            result = self._exec_tokens(tokens, line_num=num)
            if result == 'END':
                break
            elif isinstance(result, int):
                # GOTO target
                if result not in self.program:
                    raise RuntimeError(f"Undefined line {result}")
                pc = lines.index(result)
            else:
                pc += 1
            # refresh lines in case program was modified (not typical but safe)
            lines = sorted(self.program.keys())

    def _exec_tokens(self, tokens, line_num=None):
        """Execute a token list. Returns None, 'END', or int (goto target)."""
        p = Parser(tokens, self.variables, self.arrays)
        tok = p.peek()

        if tok.kind == 'EOF':
            return None

        if tok.kind == 'KW':
            kw = p.consume().value

            if kw == 'PRINT':
                return self._do_print(p)

            elif kw == 'LET':
                return self._do_let(p)

            elif kw == 'GOTO':
                target = p.parse_expr()
                return int(target)

            elif kw == 'IF':
                return self._do_if(p)

            elif kw == 'DIM':
                return self._do_dim(p)

            elif kw == 'END':
                return 'END'

            elif kw == 'NEW':
                self.program = {}
                self._reset_state()
                print("Program cleared.")

            elif kw == 'LIST':
                self.list_program()

            elif kw == 'RUN':
                self._reset_state()
                self.run()

            elif kw == 'LOAD':
                filename = self._rest_as_string(p)
                self.load_file(filename)

            elif kw == 'SAVE':
                filename = self._rest_as_string(p)
                self.save_file(filename)

            elif kw == 'QUIT':
                print("Goodbye!")
                sys.exit(0)

        elif tok.kind == 'ID':
            # Implicit LET: VAR = expr  or  VAR[idx] = expr
            return self._do_let(p)

        else:
            raise RuntimeError(f"Unexpected token: {tok}")

        return None

    def _rest_as_string(self, p):
        """Collect remaining tokens as a filename string."""
        parts = []
        while p.peek().kind != 'EOF':
            tok = p.consume()
            if tok.kind == 'STR':
                parts.append(tok.value)
            else:
                parts.append(str(tok.value))
        return ''.join(parts).strip()

    def _do_print(self, p):
        parts = []
        while p.peek().kind != 'EOF':
            tok = p.peek()
            if tok.kind == 'STR':
                p.consume()
                parts.append(tok.value)
            else:
                val = p.parse_expr()
                parts.append(str(val))
            if p.match('OP', ','):
                p.consume()
        print(' '.join(parts))
        return None

    def _do_let(self, p):
        tok = p.consume('ID')
        name = tok.value[0]
        if p.match('OP', '['):
            p.consume('OP', '[')
            idx = p.parse_expr()
            p.consume('OP', ']')
            p.consume('OP', '=')
            val = p.parse_expr()
            if name not in self.arrays:
                raise RuntimeError(f"Array {name} not declared")
            arr = self.arrays[name]
            if idx < 0 or idx >= len(arr):
                raise RuntimeError(f"Array {name} index {idx} out of bounds")
            arr[idx] = val
        else:
            p.consume('OP', '=')
            val = p.parse_expr()
            self.variables[name] = val
        return None

    def _do_if(self, p):
        cond = p.parse_comparison()
        # optional THEN
        if p.match('KW', 'THEN'):
            p.consume()
        # what follows: GOTO or a statement
        if p.match('KW', 'GOTO'):
            p.consume()
            target = p.parse_expr()
            if cond:
                return int(target)
            return None
        # inline statement
        if cond:
            return self._exec_tokens(p.tokens[p.pos:])
        return None

    def _do_dim(self, p):
        tok = p.consume('ID')
        name = tok.value[0]
        p.consume('OP', '[')
        size = p.parse_expr()
        p.consume('OP', ']')
        if size <= 0 or size > 1000:
            raise RuntimeError(f"Invalid array size {size}")
        self.arrays[name] = [0] * size
        return None

    def repl(self):
        print("Tiny BASIC Interpreter")
        print("Commands: NEW, LIST, RUN, LOAD <file>, SAVE <file>, QUIT")
        print("Statements: PRINT, LET, GOTO, IF, DIM, END")
        print()
        while True:
            try:
                line = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break
            if not line:
                continue
            try:
                self._add_line(line)
            except RuntimeError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Error: {e}")


if __name__ == '__main__':
    interp = Interpreter()
    if len(sys.argv) > 1:
        interp.load_file(sys.argv[1])
        interp.run()
    else:
        interp.repl()

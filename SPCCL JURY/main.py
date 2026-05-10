import re

class MiniLangCompiler:

    def __init__(self):

        self.variables = {}
        self.tokens = []
        self.errors = []

    def lexer(self, code):

        token_specification = [

            ('NUMBER', r'\d+'),
            ('KEYWORD', r'LET|IF|THEN|PRINT|END'),
            ('OPERATOR', r'==|>=|<=|>|<|='),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('SEMICOLON', r';'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),

            ('NEWLINE', r'\r\n|\r|\n'),

            ('SKIP', r'[ \t]+'),
            ('MISMATCH', r'.')
        ]

        tok_regex = '|'.join(
            f'(?P<{pair[0]}>{pair[1]})'
            for pair in token_specification
        )

        line_num = 1

        for mo in re.finditer(tok_regex, code):

            kind = mo.lastgroup
            value = mo.group()

            if kind == 'NEWLINE':
                line_num += 1
                continue

            elif kind == 'SKIP':
                continue

            elif kind == 'MISMATCH':

                self.errors.append(
                    f'Lexical Error at line {line_num}: Unexpected "{value}"'
                )

            else:

                self.tokens.append({
                    'type': kind,
                    'value': value,
                    'line': line_num
                })

    def parse(self):

        i = 0
        execution_log = []

        while i < len(self.tokens):

            token = self.tokens[i]

            if token['value'] == 'LET':

                try:

                    identifier = self.tokens[i + 1]
                    operator = self.tokens[i + 2]
                    value = self.tokens[i + 3]
                    semicolon = self.tokens[i + 4]

                    if identifier['type'] != 'IDENTIFIER':
                        self.errors.append(
                            f"Syntax Error at line {identifier['line']}: Identifier expected"
                        )

                    if operator['value'] != '=':
                        self.errors.append(
                            f"Syntax Error at line {operator['line']}: '=' expected"
                        )

                    if value['type'] != 'NUMBER':
                        self.errors.append(
                            f"Syntax Error at line {value['line']}: Number expected"
                        )

                    if semicolon['type'] != 'SEMICOLON':
                        self.errors.append(
                            f"Syntax Error at line {semicolon['line']}: ';' missing"
                        )

                    self.variables[identifier['value']] = int(value['value'])

                    execution_log.append(
                        f"Variable '{identifier['value']}' assigned value {value['value']}"
                    )

                    i += 5

                except:
                    self.errors.append(
                        "Unexpected end of assignment statement"
                    )
                    break


            elif token['value'] == 'PRINT':

                try:

                    identifier = self.tokens[i + 1]
                    semicolon = self.tokens[i + 2]

                    if identifier['value'] not in self.variables:

                        self.errors.append(
                            f"Semantic Error at line {identifier['line']}: Variable '{identifier['value']}' not declared"
                        )

                    else:

                        execution_log.append(
                            f"OUTPUT => {identifier['value']} = {self.variables[identifier['value']]}"
                        )

                    if semicolon['type'] != 'SEMICOLON':

                        self.errors.append(
                            f"Syntax Error at line {semicolon['line']}: ';' missing"
                        )

                    i += 3

                except:
                    self.errors.append("Invalid PRINT statement")
                    break

            # ---------------- IF CONDITION ----------------

            elif token['value'] == 'IF':

                try:

                    lp = self.tokens[i + 1]
                    left = self.tokens[i + 2]
                    op = self.tokens[i + 3]
                    right = self.tokens[i + 4]
                    rp = self.tokens[i + 5]
                    then = self.tokens[i + 6]

                    if lp['type'] != 'LPAREN':
                        self.errors.append("Missing '(' in IF")

                    if rp['type'] != 'RPAREN':
                        self.errors.append("Missing ')' in IF")

                    if then['value'] != 'THEN':
                        self.errors.append("THEN keyword missing")

                    condition_result = False

                    left_val = self.variables.get(left['value'], 0)
                    right_val = int(right['value'])

                    if op['value'] == '>':
                        condition_result = left_val > right_val

                    elif op['value'] == '<':
                        condition_result = left_val < right_val

                    execution_log.append(
                        f"IF Condition Evaluated => {condition_result}"
                    )

                    i += 7

                except:
                    self.errors.append("Invalid IF statement")
                    break

            else:

                self.errors.append(
                    f"Unknown token '{token['value']}' at line {token['line']}"
                )

                i += 1

        return execution_log

    def compile(self, code):

        self.lexer(code)

        logs = self.parse()

        return {
            "tokens": self.tokens,
            "variables": self.variables,
            "logs": logs,
            "errors": self.errors
        }
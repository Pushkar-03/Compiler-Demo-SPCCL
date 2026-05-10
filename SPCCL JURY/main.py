import re


class MiniLangCompiler:

    def __init__(self):

        self.tokens = []
        self.errors = []
        self.variables = {}
        self.logs = []


    def lexer(self, code):

        token_specification = [

            ('NUMBER', r'\d+'),
            ('STRING', r'"[^"]*"'),

            ('KEYWORD', r'\b(var|if|then|else|end|print)\b'),

            ('OPERATOR', r'==|!=|>=|<=|>|<|='),

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

        while i < len(self.tokens):

            token = self.tokens[i]

            if token['value'] == 'var':

                try:

                    identifier = self.tokens[i + 1]
                    equals = self.tokens[i + 2]
                    value = self.tokens[i + 3]
                    semicolon = self.tokens[i + 4]

                    if identifier['type'] != 'IDENTIFIER':

                        self.errors.append(
                            f"Syntax Error at line {identifier['line']}: Identifier expected"
                        )

                    if equals['value'] != '=':

                        self.errors.append(
                            f"Syntax Error at line {equals['line']}: '=' expected"
                        )

                    if value['type'] not in ['NUMBER', 'STRING']:

                        self.errors.append(
                            f"Syntax Error at line {value['line']}: Invalid value"
                        )

                    if semicolon['type'] != 'SEMICOLON':

                        self.errors.append(
                            f"Syntax Error at line {semicolon['line']}: ';' missing"
                        )


                    if value['type'] == 'NUMBER':
                        self.variables[identifier['value']] = int(value['value'])

                    else:
                        self.variables[identifier['value']] = value['value'].replace('"', '')

                    self.logs.append(
                        f"Variable '{identifier['value']}' declared"
                    )

                    i += 5

                except:

                    self.errors.append(
                        "Invalid variable declaration"
                    )

                    break


            elif token['value'] == 'print':

                try:

                    value = self.tokens[i + 1]
                    semicolon = self.tokens[i + 2]

                    if semicolon['type'] != 'SEMICOLON':

                        self.errors.append(
                            f"Syntax Error at line {semicolon['line']}: ';' missing"
                        )


                    if value['type'] == 'IDENTIFIER':

                        if value['value'] not in self.variables:

                            self.errors.append(
                                f"Semantic Error at line {value['line']}: Variable '{value['value']}' not declared"
                            )

                        else:

                            output = self.variables[value['value']]

                            self.logs.append(
                                f"OUTPUT => {output}"
                            )


                    elif value['type'] == 'STRING':

                        output = value['value'].replace('"', '')

                        self.logs.append(
                            f"OUTPUT => {output}"
                        )

                    else:

                        self.errors.append(
                            f"Syntax Error at line {value['line']}: Invalid print value"
                        )

                    i += 3

                except:

                    self.errors.append(
                        "Invalid print statement"
                    )

                    break

            elif token['value'] == 'if':

                try:

                    left = self.tokens[i + 1]
                    operator = self.tokens[i + 2]
                    right = self.tokens[i + 3]
                    then = self.tokens[i + 4]

                    if left['value'] not in self.variables:

                        self.errors.append(
                            f"Semantic Error: Variable '{left['value']}' not declared"
                        )

                    if then['value'] != 'then':

                        self.errors.append(
                            f"Syntax Error at line {then['line']}: 'then' expected"
                        )

                    left_value = self.variables.get(left['value'], 0)
                    right_value = int(right['value'])

                    condition = False

                    if operator['value'] == '>':
                        condition = left_value > right_value

                    elif operator['value'] == '<':
                        condition = left_value < right_value

                    elif operator['value'] == '==':
                        condition = left_value == right_value

                    self.logs.append(
                        f"IF condition evaluated to {condition}"
                    )

                    i += 5

                except:

                    self.errors.append(
                        "Invalid IF statement"
                    )

                    break


            elif token['value'] == 'else':

                self.logs.append("ELSE block detected")

                i += 1


            elif token['value'] == 'end':

                self.logs.append("END block detected")

                i += 1


            else:

                self.errors.append(
                    f"Unknown syntax near '{token['value']}' at line {token['line']}"
                )

                i += 1


    def compile(self, code):

        code = code.replace('\r\n', '\n')
        code = code.replace('\r', '\n')

        self.lexer(code)

        self.parse()

        return {

            "tokens": self.tokens,

            "variables": self.variables,

            "logs": self.logs,

            "errors": self.errors
        }

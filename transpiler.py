import ply.lex as lex
import ply.yacc as yacc

# ----------------- Lexer ------------------
tokens = (
    'IDENTIFIER', 'NUMBER', 'STRING', 'INT', 'FLOAT', 'CLASS', 'IF', 'ELSE', 'FOR', 'WHILE',
    'RETURN', 'COUT', 'ENDL', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'COMMA',
    'EQUALS', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'LT', 'GT', 'AND', 'OR', 'NOT',
    'COLON', 'ARROW', 'LBRACKET', 'RBRACKET', 'INCLUDE', 'STRING_H', 'IOSTREAM', 'NAMESPACE', 'STD',
    'PLUSPLUS'
)

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_COMMA = r','
t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_LT = r'<'
t_GT = r'>'
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_COLON = r':'
t_ARROW = r'->'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_STRING = r'"[^"]*"'
t_INCLUDE = r'\#include\s*<\w+>'
t_PLUSPLUS = r'\+\+'

reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'class': 'CLASS',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'return': 'RETURN',
    'cout': 'COUT',
    'endl': 'ENDL',
    'include': 'INCLUDE',
    'string': 'STRING_H',
    'iostream': 'IOSTREAM',
    'namespace': 'NAMESPACE',
    'std': 'STD'
}

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

t_ignore = ' \t'
t_ignore_COMMENT = r'//.*|/\*.*?\*/'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    raise SyntaxError(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")

lexer = lex.lex()

# ----------------- Parser ------------------
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('right', 'PLUSPLUS')
)

class Node:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.children = children or []
        self.value = value

def p_program(p):
    '''program : includes statements
               | statements'''
    if len(p) == 3:
        p[0] = Node('program', [p[2]])
    else:
        p[0] = Node('program', [p[1]])

def p_includes(p):
    '''includes : include
                | includes include'''
    if len(p) == 2:
        p[0] = Node('includes', [p[1]])
    else:
        p[0] = p[1]
        p[0].children.append(p[2])

def p_statements(p):
    '''statements : statement
                  | statements statement'''
    if len(p) == 2:
        p[0] = Node('statements', [p[1]])
    else:
        p[0] = p[1]
        p[0].children.append(p[2])

def p_statement(p):
    '''statement : declaration
                 | assignment
                 | increment
                 | if_stmt
                 | for_stmt
                 | while_stmt
                 | function_def
                 | class_def
                 | output
                 | return_stmt'''
    p[0] = p[1]

def p_include(p):
    'include : INCLUDE'
    p[0] = Node('include', value=p[1])

def p_declaration(p):
    '''declaration : INT IDENTIFIER EQUALS expression SEMICOLON
                   | FLOAT IDENTIFIER EQUALS expression SEMICOLON
                   | INT IDENTIFIER SEMICOLON'''
    if len(p) == 6:
        p[0] = Node('declaration', [p[4]], value=p[2])
    else:
        p[0] = Node('declaration', value=p[2])

def p_assignment(p):
    'assignment : IDENTIFIER EQUALS expression SEMICOLON'
    p[0] = Node('assignment', [p[3]], value=p[1])

def p_increment(p):
    'increment : IDENTIFIER PLUSPLUS SEMICOLON'
    p[0] = Node('increment', value=p[1])

def p_if_stmt(p):
    '''if_stmt : IF LPAREN expression RPAREN LBRACE statements RBRACE
               | IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE'''
    children = [p[3], p[6]] + ([p[10]] if len(p) > 8 else [])
    p[0] = Node('if', children)

def p_for_stmt(p):
    'for_stmt : FOR LPAREN INT IDENTIFIER EQUALS expression SEMICOLON expression SEMICOLON IDENTIFIER PLUSPLUS RPAREN LBRACE statements RBRACE'
    p[0] = Node('for', [p[6], p[8], p[14]], value=p[4])

def p_while_stmt(p):
    'while_stmt : WHILE LPAREN expression RPAREN LBRACE statements RBRACE'
    p[0] = Node('while', [p[3], p[6]])

def p_function_def(p):
    'function_def : INT IDENTIFIER LPAREN params RPAREN LBRACE statements RBRACE'
    p[0] = Node('function', [p[4], p[7]], value=p[2])

def p_params(p):
    '''params : param
              | params COMMA param
              | empty'''
    if len(p) == 2 and p[1]:
        p[0] = Node('params', [p[1]])
    elif len(p) == 4:
        p[0] = Node('params', p[1].children + [p[3]])
    else:
        p[0] = Node('params')

def p_param(p):
    'param : INT IDENTIFIER'
    p[0] = Node('param', value=p[2])

def p_class_def(p):
    'class_def : CLASS IDENTIFIER LBRACE declarations RBRACE SEMICOLON'
    p[0] = Node('class', [p[4]], value=p[2])

def p_declarations(p):
    '''declarations : declaration
                    | declarations declaration
                    | INT IDENTIFIER SEMICOLON
                    | declarations INT IDENTIFIER SEMICOLON'''
    if len(p) == 2:
        p[0] = Node('declarations', [p[1]])
    elif len(p) == 3:
        p[0] = p[1]
        p[0].children.append(p[2])
    elif len(p) == 4:
        p[0] = Node('declarations', [Node('declaration', value=p[2])])
    else:
        p[0] = p[1]
        p[0].children.append(Node('declaration', value=p[3]))

def p_output(p):
    '''output : COUT LT LT expression SEMICOLON
              | COUT LT LT expression LT LT ENDL SEMICOLON'''
    p[0] = Node('output', [p[4]], value='endl' if len(p) > 6 else '')

def p_return_stmt(p):
    'return_stmt : RETURN expression SEMICOLON'
    p[0] = Node('return', [p[2]])

def p_expression(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULTIPLY expression
                  | expression DIVIDE expression
                  | expression LT expression
                  | expression GT expression
                  | expression AND expression
                  | expression OR expression
                  | NOT expression
                  | NUMBER
                  | IDENTIFIER
                  | STRING'''
    if len(p) == 4:
        p[0] = Node('binop', [p[1], p[3]], value=p[2])
    elif len(p) == 3:
        p[0] = Node('unop', [p[2]], value=p[1])
    else:
        p[0] = Node('literal', value=p[1])

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        raise SyntaxError(f"Syntax error at '{p.value}' on line {p.lineno}")
    else:
        raise SyntaxError("Unexpected end of input")

parser = yacc.yacc()

# ----------------- Code Generator ------------------
def generate_code(node, indent=0):
    if not node:
        return ''
    result = ''
    indent_str = '    ' * indent

    if node.type == 'program' or node.type == 'statements':
        for child in node.children:
            result += generate_code(child, indent)
    elif node.type == 'declaration':
        result += f"{indent_str}{node.value} = {generate_code(node.children[0], 0) if node.children else 0}\n"
    elif node.type == 'assignment':
        result += f"{indent_str}{node.value} = {generate_code(node.children[0], 0)}\n"
    elif node.type == 'increment':
        result += f"{indent_str}{node.value} = {node.value} + 1\n"
    elif node.type == 'if':
        result += f"{indent_str}if {generate_code(node.children[0], 0)}:\n"
        result += generate_code(node.children[1], indent + 1)
        if len(node.children) > 2:
            result += f"{indent_str}else:\n"
            result += generate_code(node.children[2], indent + 1)
    elif node.type == 'for':
        result += f"{indent_str}for {node.value} in range({generate_code(node.children[0], 0)}, {generate_code(node.children[1], 0)}):\n"
        result += generate_code(node.children[2], indent + 1)
    elif node.type == 'while':
        result += f"{indent_str}while {generate_code(node.children[0], 0)}:\n"
        result += generate_code(node.children[1], indent + 1)
    elif node.type == 'function':
        params = ', '.join(c.value for c in node.children[0].children)
        result += f"{indent_str}def {node.value}({params}):\n"
        result += generate_code(node.children[1], indent + 1)
    elif node.type == 'class':
        result += f"{indent_str}class {node.value}:\n"
        result += f"{indent_str}    def __init__(self):\n"
        for decl in node.children[0].children:
            result += f"{indent_str}        self.{decl.value} = 0\n"
    elif node.type == 'output':
        newline = "\\n" if node.value == 'endl' else ''
        result += f"{indent_str}print({generate_code(node.children[0], 0)}, end='{newline}')\n"
    elif node.type == 'return':
        result += f"{indent_str}return {generate_code(node.children[0], 0)}\n"
    elif node.type == 'binop':
        op_map = {'+': '+', '-': '-', '*': '*', '/': '/', '<': '<', '>': '>', '&&': 'and', '||': 'or'}
        result += f"{generate_code(node.children[0], 0)} {op_map[node.value]} {generate_code(node.children[1], 0)}"
    elif node.type == 'unop':
        result += f"not {generate_code(node.children[0], 0)}"
    elif node.type == 'literal':
        result += str(node.value)
    return result

# ----------------- Transpile Function ------------------
def transpile(cpp_code):
    try:
        lexer.input(cpp_code)
        ast = parser.parse(cpp_code, lexer=lexer)
        return generate_code(ast)
    except SyntaxError as e:
        return str(e)

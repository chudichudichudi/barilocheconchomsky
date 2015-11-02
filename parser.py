
# -----------------------------------------------------------------------------
# parser.py
#
# A simple calculator with variables -- all in one file.
# -----------------------------------------------------------------------------

tokens = (
    'CARACTER', 'DIVISION', 'SUB', 'SUPER', 'PARENIZQ', 'PARENDER',
    'LLAVEIZQ', 'LLAVEDER'
)

# Tokens

t_CARACTER     = r'[^\_\^\(\)\{\}\/]'
t_DIVISION     = r'/'
t_SUB    = r'\_'
t_SUPER  = r'\^'
t_PARENDER     = r'\)'
t_PARENIZQ     = r'\('
t_LLAVEDER     = r'\}'
t_LLAVEIZQ     = r'\{'

# IGNORAMOS EL CARACTER ESPACIO
t_ignore = " "

def t_error(t):
    print("Caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left','DIVISION'),
    ('left','SUB','SUPER'),
    )

# dictionary of names
names = { }

def p_statement_expr(t):
    '''statement : expression
                 | expression2'''
    print(t[1])

def p_expression_binop(t):
    '''expression2 : expression SUPER expression
                  | expression SUB expression
                  | expression2 DIVISION expression2
                  | expression2 DIVISION expression
                  | expression DIVISION expression2
                  | expression DIVISION expression
    '''
    if   t[2] == '^': t[0] = "{%s ^ %s}" % (t[1], t[3])
    elif t[2] == '_': t[0] = "{%s _ %s}" % (t[1], t[3])
    elif t[2] == '/': t[0] = "{%s / %s}" % (t[1], t[3])

def p_expression_terop(t):
    '''expression2 : expression SUPER expression SUB expression
                   | expression SUB expression SUPER expression'''
    if   t[2] == '^' and t[4] == '_': t[0] = "{%s ^ %s _ %s}" % (t[1], t[3], t[5])
    elif t[2] == '_' and t[4] == '^': t[0] = "{%s _ %s ^ %s}" % (t[1], t[3], t[5])

def p_expression_group(t):
    '''expression : LLAVEIZQ expression2 LLAVEDER
                  | LLAVEIZQ expression LLAVEDER
                  | PARENIZQ expression2 PARENDER
                  | PARENIZQ expression PARENDER'''
    if   t[1] == '(': t[0] = '(%s)' % t[2]
    elif t[1] == '{': t[0] = '{%s}' % t[2]

def p_expression_concat(t):
    '''expression2 : expression2 expression2
                   | expression expression2
                   | expression2 expression
                   | expression expression'''
    t[0] = '{%s %s}' % (t[1], t[2])

def p_expression_caracter(t):
    'expression : CARACTER'
    t[0] = t[1]

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')   # Use raw_input on Python 2
    except EOFError:
        break
    parser.parse(s)

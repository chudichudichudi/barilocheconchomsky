
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
t_DIVISION     = r'\/'
t_SUB          = r'\_'
t_SUPER        = r'\^'
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
    '''statement : div'''
    out = open('output.svg', 'w')
    out.write('''<?xml version="1.0" standalone="no"?>
        <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
        <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
            <g transform="translate(0, 200) scale(200)" font-family="Courier">
    ''')
    out.write(t[1])
    out.write('''
        </g>
    </svg>
    ''')
    out.close()

def p_term(t):
    '''term : factor factor1
    '''
    t[0] = "%s%s" % (t[1], t[2])

def p_factor1(t):
    '''factor1 : lambda
               | SUPER factor factor2
               | SUB factor factor3
    '''
    if t[1] != 'lambda':
        t[0] = ' %s %s%s' % (t[1], t[2], t[3])
    else:
        t[0] = ''

def p_factor2(t):
    '''factor2 : lambda
               | SUB factor
       factor3 : lambda
               | SUPER factor
    '''
    if t[1] != 'lambda':
        t[0] = ' %s %s' % (t[1], t[2])
    else:
        t[0] = ''

def p_expression(t):
    '''expression : term1 term
    '''
    t[0] = "%s%s" % (t[1], t[2])

def p_term1(t):
    '''term1 : lambda
            | term1 term
    '''
    if t[1] != 'lambda':
        t[0] = ' %s%s' % (t[1], t[2])
    else:
        t[0] = ''

def p_div(t):
    '''div : div1 expression
    '''
    t[0] = "%s%s" % (t[1], t[2])

def p_div1(t):
    '''div1 : lambda
            | div1 expression DIVISION
    '''
    if t[1] != 'lambda':
        t[0] = ' %s%s /' % (t[1], t[2])
    else:
        t[0] = ''

def p_group(t):
    '''factor : PARENIZQ div PARENDER'''
    t[0] = '%s' % t[2]

def p_expression_caracter(t):
    'factor : CARACTER'
    t[0] = t[1]

def p_error(t):
    print("Syntax error at '%s'" % t.value)

def p_lambda(t):
    'lambda :'
    t[0] = 'lambda'

import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')   # Use raw_input on Python 2
    except EOFError:
        break
    parser.parse(s)

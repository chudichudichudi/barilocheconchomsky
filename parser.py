# -----------------------------------------------------------------------------
# parser.py
#
# Parser that outputs a SVG 
# -----------------------------------------------------------------------------
LAMBDA = ''

class Nodo(object):
    texto = None
    ancho = None
    alto = None
    division = False

    def __init__(self, texto='', ancho=0, alto=0):
        self.texto = texto
        self.ancho = ancho
        self.alto = alto

    def __str__(self):
        return self.texto

    def __bool__(self):
        return self.texto != ''

    def concatenar(self, nodo):
        if nodo.texto == '':
            return self
        
        return Nodo('''
            %s
            <g transform="translate(%s, 0)">
            %s
            </g>
        ''' % (self.texto, self.ancho, nodo.texto),
        self.ancho + nodo.ancho,
        max(self.alto, nodo.alto))

    def superponer(self, nodo):
        return Nodo('''
        %s %s
        ''' % (self.texto, nodo.texto),
        max(self.ancho, nodo.ancho),
        max(self.alto, nodo.alto))

    def subir(self):
        nodo = self.a_indice()
        return Nodo('''
        <g transform="translate(0, -3)">
            %s
        </g>
        ''' % nodo.texto,
        nodo.ancho,
        self.alto * 1.3)

    def bajar(self):
        nodo = self.a_indice()
        return Nodo('''
        <g transform="translate(0, 3)">
            %s
        </g>
        ''' % nodo.texto,
        nodo.ancho,
        self.alto * 1.3)

    def a_indice(self):
        return Nodo('''
        <g transform="scale(.7)">
            %s
        </g>
        ''' % self.texto,
        self.ancho * 0.7,
        self.alto * 0.7)

    def dividir(self, nodo):
        DIV_ALTO = 0.0

        if not self:
            return nodo

        ancho_barra = max(self.ancho, nodo.ancho)
        offset_x_arriba = ( ancho_barra - self.ancho ) / 2
        offset_x_abajo = ( ancho_barra - nodo.ancho ) / 2

        return Nodo('''

                <g transform="translate({offset_x_arriba}, {alto_arriba})">
                    {texto_arriba}
                </g>

                <g transform="translate(0, {DIV_ALTO})">                
                    <line x1="0" x2="{ancho_barra}" stroke-width="0.07" stroke="black"/>
                </g>

                <g transform="translate({offset_x_abajo}, {alto_abajo})">
                    {texto_abajo}
                </g>
                '''.format(**{
               'offset_x_arriba': offset_x_arriba,
               'texto_arriba': self.texto,
               'alto_arriba': - DIV_ALTO, 
               'ancho_barra': ancho_barra,
               'offset_x_abajo': offset_x_abajo,
               'alto_abajo': DIV_ALTO + nodo.alto,
               'texto_abajo': nodo.texto,
               'DIV_ALTO': DIV_ALTO,
               }),
        ancho_barra,
        self.alto + nodo.alto + DIV_ALTO * 2)

    def parentizar(self):
        return Nodo('''
            <g transform="scale(1, %s)">
                <text>(</text>
            </g>
            <g transform="translate(%s, -%s)">
                %s
            </g>
            <g transform="translate(%s,0) scale(1, %s)">
                <text>)</text>
            </g>
        ''' % (self.alto / 10,
               6, 
               self.alto / 2, 
               self.texto, 
               self.ancho + 6, #adelanto el texto un ancho del parentesis 
               self.alto / 10),
               self.ancho + 12 , #adelando el ancho con 12 por los parentesis
               self.alto * (self.alto / 10) )

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
            <g transform="translate(0, 200) scale(10)" font-family="Courier" font-size="10">
    ''')
    out.write(t[1].texto)
    out.write('''
        </g>
    </svg>
    ''')
    out.close()

def p_term(t):
    '''term : factor factor1
    '''
    t[0] = t[1].concatenar(t[2])

def p_factor1(t):
    '''factor1 : lambda
               | SUPER factor factor2
               | SUB factor factor3
    '''
    if t[1] != LAMBDA:
        if t[1] == '^':
            t[0] = t[2].subir().superponer(t[3])
        elif t[1] == '_':
            t[0] = t[2].bajar().superponer(t[3])
    else:
        t[0] = Nodo('')

def p_factor2(t):
    '''factor2 : lambda
               | SUB factor
       factor3 : lambda
               | SUPER factor
    '''
    if t[1] != LAMBDA:
        if t[1] == '^':
            t[0] = t[2].subir()
        elif t[1] == '_':
            t[0] = t[2].bajar()
    else:
        t[0] = Nodo('')

def p_expression(t):
    '''expression : term1 term
    '''
    t[0] = t[1].concatenar(t[2])

def p_term1(t):
    '''term1 : lambda
            | term1 term
    '''
    if t[1] != LAMBDA:
        t[0] = t[1].concatenar(t[2])
    else:
        t[0] = Nodo()

def p_div(t):
    '''div : div1 expression
    '''
    # mirar si es division div1, si lo es mover abajo y centrar en el ancho de expression
    t[0] = t[1].dividir(t[2])
    
def p_div1(t):
    '''div1 : lambda
            | div1 expression DIVISION
    '''
    if t[1] != LAMBDA:
        t[0] = t[1].dividir(t[2])
    else:
        t[0] = Nodo()

def p_group(t):
    '''factor : PARENIZQ div PARENDER'''
    t[0] = t[2].parentizar()

def p_expression_caracter(t):
    'factor : CARACTER'
    t[0] = Nodo('''<text>%s</text>''' % t[1], 6, 10)

def p_error(t):
    print("Syntax error at '%s'" % t.value)

def p_lambda(t):
    '''lambda :'''
    t[0] = LAMBDA

import ply.yacc as yacc
parser = yacc.yacc()

import sys
parser.parse(str(sys.argv[1]))

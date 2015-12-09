import sys
import ply.yacc as yacc

# -----------------------------------------------------------------------------
# parser.py
#
# Parser that outputs a SVG 
# -----------------------------------------------------------------------------
LAMBDA = ''
ESCALA = 2

class Nodo(object):
    texto = None
    ancho = None
    alto_arriba = None
    alto_abajo = None
    division = False

    def __init__(self, texto='', ancho=0, alto_arriba=0, alto_abajo=0):
        self.texto = texto
        self.ancho = ancho
        self.alto_arriba = alto_arriba
        self.alto_abajo = alto_abajo

    def __str__(self):
        return self.texto

    def __bool__(self):
        return self.texto != ''

    def concatenar(self, nodo):
        '''Dado un nodo, si no es el nodo vacio se concatenan uno al lado del otro y se calcula el nuevo ancho'''
        if nodo.texto == '':
            return self
        
        return Nodo('''
            %s
            <g transform="translate(%s, 0)">
            %s
            </g>
        ''' % (self.texto, self.ancho, nodo.texto),
        self.ancho + nodo.ancho,
        max(self.alto_arriba, nodo.alto_arriba),
        min(self.alto_abajo, nodo.alto_abajo),
        )

    def superponer(self, nodo):
        '''Dado un nodo se posicionan los nodos uno encima del otro, sirve para las producciones E^E, E_E, E_E^E E^E_E '''
        return Nodo('''
        %s %s
        ''' % (self.texto, nodo.texto),
        max(self.ancho, nodo.ancho),
        max(self.alto_arriba, nodo.alto_arriba),
        
        min(self.alto_abajo, nodo.alto_abajo)
        )

    def subir(self):
        '''Se achica y se mueve hacia arriba 3 puntos'''
        nodo = self.a_indice()
        nodo2 = Nodo('''
        <g transform="translate(0, -3)">
            %s
        </g>
        ''' % nodo.texto,
        nodo.ancho,
        nodo.alto_arriba + 3 ,
        min(0, nodo.alto_abajo + 3),
        )
        return nodo2

    def bajar(self):
        '''Se achica y se mueve hacia abajo 3 puntos'''
        nodo = self.a_indice()
        return Nodo('''
        <g transform="translate(0, 3)">
            %s
        </g>
        ''' % nodo.texto,
        nodo.ancho,
        max(0, nodo.alto_arriba - 1.2),
        nodo.alto_abajo - 1.2,
        )

    def a_indice(self):
        '''Se achica el nodo en un 30%'''
        return Nodo('''
        <g transform="scale(.7) translate(0, -1.15)">
            %s
        </g>
        ''' % self.texto,
        self.ancho * 0.7,
        self.alto_arriba * 0.7,
        self.alto_abajo * 0.7,
        )

    def dividir(self, nodo):
        '''
        Si el nodo actual no es el nodo vacio, es que tengo una division a mi izquierda
        Se calculan los offset_x_arriba y offset_x_abajo para centrar horizontalmente ambas partes
        de la division. 
        
        Se dibuja el numerador desde la base del nodo actual mas el alto de la division sumado un espacio en blanco
        para respetar las proporciones.
        
        Se dibuja el denominador corriendolo en y tanto como el techo mas el alto de la division sumado un espacio en blanco
        para respetar las proporciones.
        '''
        DIV_SEPARACION = 1
        DIV_ALTO = 2

        if not self:
            return nodo

        ancho_barra = max(self.ancho, nodo.ancho)
        offset_x_arriba = ( ancho_barra - self.ancho ) / 2
        offset_x_abajo = ( ancho_barra - nodo.ancho ) / 2

        nodo = Nodo('''

                <g transform="translate(0, {DIV_ALTO})">
                    <g transform="translate({offset_x_arriba}, {offset_y_arriba})">
                        {texto_arriba}
                    </g>

                    <g transform="translate(0, {DIV_SEPARACION})">                
                        <line x1="0" x2="{ancho_barra}" stroke-width="0.07" stroke="black"/>
                    </g>

                    <g transform="translate({offset_x_abajo}, {offset_y_abajo})">
                        {texto_abajo}
                    </g>
                </g>
                '''.format(**{
               'offset_x_arriba': offset_x_arriba,
               'offset_x_abajo': offset_x_abajo,
               'ancho_barra': ancho_barra,

               'texto_arriba': self.texto,
               'texto_abajo': nodo.texto,

               'offset_y_arriba': - 3 * DIV_SEPARACION + self.alto_abajo,
               'offset_y_abajo': nodo.alto_arriba - 2 * DIV_SEPARACION, 

               'DIV_SEPARACION': -DIV_SEPARACION,
               'DIV_ALTO': -DIV_ALTO,
               }),
        ancho_barra,
        self.alto_arriba - self.alto_abajo + DIV_SEPARACION + DIV_ALTO,
        - (nodo.alto_arriba + abs(nodo.alto_abajo)) - DIV_SEPARACION + DIV_ALTO,
        )

        return nodo

    def parentizar(self):
        '''
        El nodo se envuelve a si mismo en parentesis, se escala el mismo de acorde a su alto
        '''
        OFFSET_X = 6
        CORR = 0
        if abs(self.alto_abajo) > 4:
            CORR = 5

        return Nodo('''
            <g transform="translate(0, {OFFSET_Y_PARENTESIS}) scale(1, {ESCALA_PAREN_IZQ})">
                <text>(</text>
            </g>
            <g transform="translate({OFFSET_TEXTO_X}, 0)">
                {TEXTO}
            </g>
            <g transform="translate({OFFSET_X_PARENTESIS},{OFFSET_Y_PARENTESIS}) scale(1, {ESCALA_PAREN_DER})">
                <text>)</text>
            </g>
        '''.format(**{
               'ESCALA_PAREN_DER': (abs(self.alto_arriba) + abs(self.alto_abajo))  / 7,
               'ESCALA_PAREN_IZQ': (abs(self.alto_arriba) + abs(self.alto_abajo))  / 7,
               'TEXTO': self.texto,
               'OFFSET_X_PARENTESIS': self.ancho + OFFSET_X,
               'OFFSET_Y_PARENTESIS': abs(self.alto_abajo) - CORR,
               'OFFSET_TEXTO_X': OFFSET_X,
               }),
        self.ancho + OFFSET_X * 2,
        self.alto_arriba,
        self.alto_abajo
        )

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
    print("Caracter ilegal '%s'" % t.value[0], file=sys.stderr)
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
    t[0] = t[1]

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
        t[0] = Nodo()

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
        t[0] = Nodo()

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
    '''factor : PARENIZQ div PARENDER
              | LLAVEIZQ div LLAVEDER
    '''
    if t[1] == '(':
        t[0] = t[2].parentizar()
    else:
        t[0] = t[2]

def p_expression_caracter(t):
    'factor : CARACTER'
    t[0] = Nodo('''<text>%s</text>''' % t[1], 6, 10, 0)

def p_error(t):
    print("Syntax error at '%s'" % t.value, file=sys.stderr)

def p_lambda(t):
    '''lambda :'''
    t[0] = LAMBDA

parser = yacc.yacc()

if __name__ == '__main__':
    out = parser.parse(str(sys.argv[1]))
    print('''<?xml version="1.0" standalone="no"?>
        <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
        <svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewbox="0 0 {ALTO_TOTAL} {ANCHO_TOTAL}">
            <g transform="translate(0, {ALTO_TOTAL}) scale({ESCALA})" font-family="Courier" font-size="10">
    '''.format(**{
        'ALTO_TOTAL': (abs(out.alto_arriba) +  abs(out.alto_abajo) ) * ESCALA,
        'ANCHO_TOTAL': out.ancho * ESCALA,
        'ESCALA': ESCALA
        }), file=sys.stdout)
    print(out.texto, file=sys.stdout)
    print('''
        </g>
    </svg>
    ''', file=sys.stdout)

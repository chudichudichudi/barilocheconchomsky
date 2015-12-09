from tlen_tp import parser, ESCALA

formulas = [
    ("C", "Un sólo caracter"),
    ("(C)", "Un sólo caracter entre paréntesis"),
    ("(E^E_E)", "Alineación de super sub índice (1)"),
    ("(E_E^E)", "Alineación de super sub índice (2)"),
    ("(A_{D_{D_{D_{D_{D_{D_{D}}}}}}}^{D^{D^{D^{D^{D^{D}}}}}})", "Alineación de super sub índice (3)"),
    ("(C / {A + {D/E}} )-I", ""),
    ("({A + {D/E}} / C)-I", ""),
    ("(A^B_DC^D/E^F_G+H)-I", ""),
    ("(D)", ""),
    ("(A/B/C/D)", ""),
]

template = """
<!DOCTYPE html>
<!-- Based on HTML5 Bones | http://html5bones.com -->
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Teoria de Lenguajes - Trabajo Practico</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style type="text/css">
    img {{
        width: 100%;
        height: auto;
    }}
    svg {{
        border: 1px solid #000;
    }}
    </style>
</head>
<body>
    <main role="main">
        <ol>
            {lista}
        </ol>
    </main>
</body>
</html>
"""

render = ''
for formula, descripcion in formulas:
    out = parser.parse(formula)
    render += """
    <li>
        <h3>Fórmula: {formula}</h3>
        <p>{descripcion}</p>
        <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{ANCHO_TOTAL}" height="{ALTO_TOTAL}" viewbox="0 0 {ANCHO_TOTAL} {ALTO_TOTAL}">
            <g transform="translate(0, {ALTO_TOTAL}) scale({ESCALA})" font-family="Courier" font-size="10">
                {render}
            </g>
        </svg>
    </li>
    """.format(
        formula=formula,
        descripcion=descripcion,
        render=out,
        ALTO_TOTAL=(abs(out.alto_arriba) +  abs(out.alto_abajo) ) * ESCALA,
        ANCHO_TOTAL=out.ancho * ESCALA,
        ESCALA=ESCALA
    )

salida = open('tests.html', 'w')
salida.write(template.format(lista=render))
salida.close()

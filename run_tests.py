from tlen_tp import parser, ESCALA

formulas = [
    ("█EÑ?$¿", "Un sólo caracter"),
    ("E_E", "Sub Altura"),
    ("E^E", "Super Altura"),
    ("E^E_E", "Alineación de super sub índice (1/3)"),
    ("E_E^E", "Alineación de sub super índice (2/3)"),
    ("E_{E_{E_{E_{E_{E_{E_{E}}}}}}}^{E^{E^{E^{E^{E^{E^E}}}}}}", "Alineación de super sub índice (3/3)"),
    ("A/B", "División"),
    ("A/B/C", "División múltiple"),
    ("ABC/BC/C", "División ancho (1/3)"),
    ("A/AB/ABC", "División ancho (2/3)"),
    ("A/{AB/ABC}", "División ancho (3/3)"),
    ("+{A/B}-", "División alineado a - y + (1/3)"),
    ("{C / {A + {D/E}} } - I", "División alineado a - y + (2/3)"),
    ("{C_C^C / {A_A + {D_D/E^E}} } - I", "División alineado a - y + (3/3)"),
    ("(E)", "Un sólo caracter entre paréntesis"),
    ("(E/E)", "Paréntesis en división"),
    ("(E/E/E)", "Paréntesis en división"),
    ("({A + {D/E}} / C)-I", ""),
    ("(A^B_DC^D/E^F_G+H)-I", ""),
    ("(A/B/C/D/E)", ""),
    ("(A^BC^D/E^F_G+H)-I", "Ejemplo de la cátedra"),
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
        margin: 10px 0 20px 0;
    }}
    dl dd {{
        display: inline;
        margin: 0;
    }}
    dl dd:after {{
        display: block;
        content: '';
    }}
    dl dt {{
        display: inline-block;
        min-width: 150px;
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
        <dl>
            <dt>Altura arriba</dt><dd>{ALTO_ARRIBA}</dd>
            <dt>Altura abajo</dt><dd>{ALTO_ABAJO}</dd>
            <dt>Altura total</dt><dd>{ALTO}</dd>
            <dt>Ancho</dt><dd>{ANCHO}</dd>
        </dl>
        <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{ANCHO_ESCALADO}" height="{ALTO_ESCALADO_MARGEN}" viewbox="0 0 {ANCHO_ESCALADO} {ALTO_ESCALADO}">
            <g transform="translate(0, {ALTO_ARRIBA_ESCALADO}) scale({ESCALA})" font-family="Courier" font-size="10">
                {render}
            </g>
        </svg>
    </li>
    """.format(
        formula=formula,
        descripcion=descripcion,
        render=out,
        ALTO=abs(out.alto_arriba) +  abs(out.alto_abajo),
        ALTO_ESCALADO=(abs(out.alto_arriba) +  abs(out.alto_abajo) ) * ESCALA,
        ALTO_ESCALADO_MARGEN=(abs(out.alto_arriba) +  abs(out.alto_abajo) + 4) * ESCALA,
        ALTO_ARRIBA=out.alto_arriba,
        ALTO_ARRIBA_ESCALADO=out.alto_arriba * ESCALA,
        ALTO_ABAJO=out.alto_abajo,
        ALTO_ABAJO_ESCALADO=out.alto_abajo * ESCALA,
        ANCHO=out.ancho,
        ANCHO_ESCALADO=out.ancho * ESCALA,
        ESCALA=ESCALA
    )

salida = open('tests.html', 'w')
salida.write(template.format(lista=render))
salida.close()

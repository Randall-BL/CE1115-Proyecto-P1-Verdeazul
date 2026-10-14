#!/usr/bin/env python3
"""Genera los paneles (tablas y diagramas) de las laminas para la version de Canva.

La presentacion de la defensa se arma en Canva sobre la plantilla
«Pixelated Retro Interface». El titulo, el numero y el nombre de quien expone
son texto de Canva; el cuerpo de cada lamina (tabla o diagrama) es una imagen
PNG con fondo transparente que sale de este script.

El contenido NO se copia a mano: se lee de ../P1_Presentacion_grupo6.tex, asi
que la fuente de verdad sigue siendo ese archivo. Solo cambian los colores,
para que el panel se lea sobre la ventana morada de la plantilla.

Uso (desde esta carpeta):   python generar_paneles.py
Requiere: pdflatex (MiKTeX o TeX Live) y PyMuPDF (pip install pymupdf).

Salida, en build/ (no se versiona):
  paneles.tex, paneles.pdf   una pagina por lamina, recortada al contenido
  png/panel_NN.png           un PNG por lamina (NN = numero de lamina)
  laminas.json               titulo, expositor, notas y tamano de cada panel
"""
import json
import pathlib
import re
import subprocess
import sys

AQUI = pathlib.Path(__file__).resolve().parent
FUENTE = AQUI.parent / "P1_Presentacion_grupo6.tex"
BUILD = AQUI / "build"
ANCHO_IN = 12.133  # ancho del texto en la lamina original (13,333 in - 2 x 0,6 in)
DPI = 257          # 2x del tamano con que el panel se muestra en Canva

PREAMBULO = r"""
\documentclass{article}
\usepackage[paperwidth=16in,paperheight=14in,margin=0.5in]{geometry}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[spanish,es-noshorthands,es-tabla]{babel}
\usepackage[default]{lato}
\usepackage[table]{xcolor}
\usepackage{booktabs,array,colortbl}
\usepackage{tikz}
\usetikzlibrary{positioning,arrows.meta,calc,shadows}
\usepackage[active,tightpage]{preview}
\setlength\PreviewBorder{8pt}

% Paleta de la plantilla: ventana morada (#5E38DE), botones grises, alerta amarilla.
\definecolor{tinta}{HTML}{FFFFFF}        % texto sobre la ventana
\definecolor{gris}{HTML}{D9D2FF}         % texto secundario y flechas
\definecolor{acento}{HTML}{FFE94A}       % el dato importante
\definecolor{resalte}{HTML}{FFE94A}      % caja destacada de un diagrama
\definecolor{plano}{HTML}{C6C6C6}        % caja normal: gris de boton antiguo
\definecolor{negado}{HTML}{A6A6A6}       % caja de «denegar» o del sistema
\definecolor{reglatabla}{HTML}{A593F5}   % lineas de las tablas
\definecolor{cabecera}{HTML}{3A1FA6}     % fila de encabezado de la matriz
\definecolor{sinacceso}{HTML}{4A2BC2}    % celda sin acceso de la matriz

\newcommand{\tUno}{\fontsize{40}{45}\selectfont}
\newcommand{\tDos}{\fontsize{28}{35}\selectfont}
\newcommand{\tTres}{\fontsize{18}{25}\selectfont}
\newcommand{\tCuatro}{\fontsize{13}{17.5}\selectfont}
\makeatletter
\renewcommand\normalsize{\@setfontsize\normalsize{18}{25}}
\renewcommand\small{\@setfontsize\small{13}{17.5}}
\renewcommand\footnotesize{\@setfontsize\footnotesize{13}{17.5}}
\renewcommand\scriptsize{\@setfontsize\scriptsize{13}{17.5}}
\renewcommand\tiny{\@setfontsize\tiny{13}{17.5}}
\renewcommand\large{\@setfontsize\large{28}{35}}
\renewcommand\Large{\@setfontsize\Large{40}{45}}
\makeatother
\setlength{\parindent}{0pt}

\newcommand{\dato}[1]{\textcolor{acento}{\textbf{#1}}}
\newcommand{\pie}[1]{\leavevmode{\tCuatro\color{gris}#1}}
\newcommand{\cabt}[1]{\leavevmode{\tCuatro\bfseries\color{gris}#1}}
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
\arrayrulecolor{reglatabla}
\setlength{\arrayrulewidth}{0.8pt}
\renewcommand{\arraystretch}{1.5}
\newcommand{\vb}[2]{\mbox{#1\,{\color{acento}\bfseries #2}}}
\newcommand{\sinacc}{\cellcolor{sinacceso}\leavevmode{\color{gris}---}}
\newcommand{\suj}[1]{\leavevmode{\tTres\bfseries #1}}

\begin{document}
\normalsize\color{tinta}
"""

SOMBRA = "drop shadow={opacity=1,fill=black,shadow xshift=5pt,shadow yshift=-5pt}"


def grupo(texto, i):
    """Devuelve (contenido, posicion_siguiente) del grupo {...} que empieza en i."""
    assert texto[i] == "{", texto[i:i + 30]
    nivel, j = 0, i
    while True:
        c = texto[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            nivel += 1
        elif c == "}":
            nivel -= 1
            if nivel == 0:
                return texto[i + 1:j], j + 1
        j += 1


def texto_plano(tex):
    """Quita el marcado de LaTeX de un titulo o de una nota."""
    t = tex
    t = re.sub(r"\\textcolor\{[^}]*\}\{([^}]*)\}", r"\1", t)
    t = re.sub(r"\\(?:emph|textbf|dato)\{([^}]*)\}", r"\1", t)
    t = t.replace("\\ldots", "…").replace("--", "–").replace("\\&", "&").replace("\\%", "%")
    t = t.replace("$_2$", "₂").replace("~", " ")
    return t


def adaptar(cuerpo):
    """Ajusta el cuerpo de una lamina a la paleta de la plantilla."""
    c = cuerpo
    # cajas destacadas: relleno amarillo y borde negro, como la alerta de la plantilla
    c = re.sub(r"draw=acento,(line width=[\d.]+pt),fill=acentoclaro",
               r"draw=black,\1,fill=resalte,text=black," + SOMBRA, c)
    c = c.replace("[caja,draw=acento,line width=1.6pt]", "[caja,fill=resalte,line width=1.6pt]")
    # cajas normales: gris de boton, borde negro grueso y sombra dura
    c = re.sub(r"draw=(?:regla|gris),line width=[\d.]+pt,fill=(plano|negado|white)",
               lambda m: "draw=black,line width=1.6pt,fill="
               + ("plano" if m.group(1) == "white" else m.group(1))
               + ",text=black," + SOMBRA, c)
    # encabezado de la matriz
    c = c.replace(r"\rowcolor{acentoclaro}", r"\rowcolor{cabecera}")
    # las columnas de beamer no existen fuera de beamer
    c = c.replace(r"\begin{columns}[T,onlytextwidth]", "")
    c = c.replace(r"\end{columns}", "")
    c = re.sub(r"\\begin\{column\}\{([^}]*)\}", r"\\begin{minipage}[t]{\1}", c)
    c = c.replace(r"\end{column}", r"\end{minipage}\hfill")
    return c


def leer_laminas():
    fuente = FUENTE.read_text(encoding="utf-8")
    documento = fuente.split(r"\begin{document}", 1)[1].split(r"\end{document}")[0]
    laminas = []
    for n, m in enumerate(re.finditer(r"\\begin\{frame\}(.*?)\\end\{frame\}", documento, re.S), 1):
        f = m.group(1)
        lam = {"n": n, "titulo": "", "quien": "", "notas": "", "cuerpo": ""}
        if f.startswith("[plain]"):
            f = f[len("[plain]"):]
        elif f.startswith("{"):
            titulo, fin = grupo(f, 0)
            lam["titulo"] = "\n".join(p.strip() for p in texto_plano(titulo).split("\\\\"))
            f = f[fin:]
        q = re.search(r"\\quien\{([^}]*)\}\n?", f)
        if q:
            lam["quien"] = q.group(1)
            f = f[:q.start()] + f[q.end():]
        k = f.find("\\note{")
        if k >= 0:
            nota, fin = grupo(f, k + len("\\note"))
            lam["notas"] = "\n\n".join(" ".join(p.split()) for p in texto_plano(nota).split("\n\n"))
            f = f[:k] + f[fin:]
        f = re.sub(r"^\s*\\vspace\*?\{[^}]*\}\s*\n", "", f.strip() + "\n")  # espacio inicial
        lam["cuerpo"] = f.strip()
        laminas.append(lam)
    return laminas


def main():
    try:
        import fitz  # PyMuPDF
    except ImportError:
        sys.exit("Falta PyMuPDF: pip install pymupdf")
    BUILD.mkdir(exist_ok=True)
    (BUILD / "png").mkdir(exist_ok=True)
    laminas = leer_laminas()
    con_panel = [l for l in laminas if l["n"] > 1]  # la portada es solo texto de Canva

    partes = [PREAMBULO]
    for l in con_panel:
        # el color va dentro del panel: preview descarta lo que queda fuera de el
        partes.append("%% ---- lamina %d ----\n\\begin{preview}\\begin{minipage}{%.3fin}"
                      "\\normalsize\\color{tinta}\n%s\n"
                      "\\end{minipage}\\end{preview}\n" % (l["n"], ANCHO_IN, adaptar(l["cuerpo"])))
    partes.append("\\end{document}\n")
    (BUILD / "paneles.tex").write_text("\n".join(partes), encoding="utf-8")

    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "paneles.tex"],
                       cwd=BUILD, capture_output=True, text=True, errors="replace")
    if r.returncode != 0:
        print(r.stdout[-3000:])
        sys.exit("pdflatex fallo: revisar build/paneles.log")

    pdf = fitz.open(BUILD / "paneles.pdf")
    assert len(pdf) == len(con_panel), (len(pdf), len(con_panel))
    for pagina, l in zip(pdf, con_panel):
        pix = pagina.get_pixmap(matrix=fitz.Matrix(DPI / 72, DPI / 72), alpha=True)
        pix.save(BUILD / "png" / ("panel_%02d.png" % l["n"]))
        l["ancho_in"] = round(pagina.rect.width / 72, 3)
        l["alto_in"] = round(pagina.rect.height / 72, 3)
    for l in laminas:
        del l["cuerpo"]
    (BUILD / "laminas.json").write_text(json.dumps(laminas, ensure_ascii=False, indent=1),
                                        encoding="utf-8")
    print("%d paneles en %s" % (len(con_panel), BUILD / "png"))


if __name__ == "__main__":
    main()

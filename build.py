# -*- coding: utf-8 -*-
"""Build del sito Green Mihawk OP17.

1) cuce le trascrizioni per striscia (scratchpad/parts) in trascrizioni/<autore>/<capitolo>.md
2) converte il markdown verbatim in HTML, rendendo graficamente carte / board / note
3) genera le pagine delle guide

Uso:  python build.py
"""
import html
import json
import os
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SCRATCH = pathlib.Path(
    r"C:\Users\bened\AppData\Local\Temp\claude"
    r"\c--Users-bened-Desktop-PARA-3--Resources-OP-Guide-OP-Mihawk"
    r"\420c3572-c78d-4159-b08c-ded0a9bb5b6f\scratchpad"
)
PARTS = SCRATCH / "parts"
TRASC = ROOT / "trascrizioni"
CARTE = ROOT / "carte"

# ---------------------------------------------------------------- 1. stitching

# capitolo -> (autore, titolo, [sorgenti in ordine])
# sorgente = "parts:<dir>" oppure "file:<path relativo a trascrizioni>"
CHAPTERS = [
    ("raphterra", "00-welcome",   "Welcome and Introduction",              ["file:raphterra/00-welcome.md"]),
    ("raphterra", "01-deckcore",  "Deck Core and Deckbuilding Fundamentals",["parts:raph-01-deckcore"]),
    ("raphterra", "02-gameplay",  "Gameplay Fundamentals",                 ["parts:raph-02-gameplay"]),
    ("raphterra", "04-meta",      "Green Mihawk in the OP17 Meta",         ["file:raphterra/04-meta.md"]),
    ("raphterra", "05-mu-meta",   "Matchup Strategies vs The Meta",
     ["file:raphterra/05-matchup-meta-parte1.md", "parts:raph-05-mu-meta"]),
    ("raphterra", "06-mu-field",  "Matchup Strategies vs The Field (WIP)", ["file:raphterra/06-matchup-field.md"]),

    ("rondino", "01-intro",     "1. Intro chapter",        ["file:rondino/01-intro.md"]),
    ("rondino", "02-meta",      "2. Meta analysis",        ["file:rondino/02-meta-analysis.md"]),
    ("rondino", "03-decklist",  "3. The decklist",         ["parts:rond-03-decklist"]),
    ("rondino", "04-strategy",  "4. General deck strategy",["file:rondino/04-general-deck-strategy.md"]),
    ("rondino", "05-mu-bible",  "5. The matchups bible",   ["parts:rond-05-mu-bible"]),

    ("nebulus", "13-whatis",     "What is Mihawk?",            ["parts:neb-13-whatis"]),
    ("nebulus", "14-cards",      "Cards & Decklist",           ["parts:neb-14-cards"]),
    ("nebulus", "15-tech",       "TECH CARDS",                 ["parts:neb-15-tech"]),
    ("nebulus", "16-carddraw",   "Card Draw",                  ["parts:neb-16-carddraw"]),
    ("nebulus", "17-philosophy", "Philosophy & Don Management",["parts:neb-17-philosophy"]),
    ("nebulus", "18-looping",    "Looping Your Deck",          ["parts:neb-18-looping"]),
    ("nebulus", "19-trashevent", "Trash Event Tech",           ["parts:neb-19-trashevent"]),
    ("nebulus", "20-rapidfire",  "Rapidfire MU Spread 9/1",    ["parts:neb-20-rapidfire"]),
    ("nebulus", "21-pyrobin",    "PY Robin",                   ["parts:neb-21-pyrobin"]),
    ("nebulus", "22-ylinlin",    "Y Linlin",                   ["parts:neb-22-ylinlin"]),
    ("nebulus", "23-uyboa",      "UY Boa",                     ["parts:neb-23-uyboa"]),
    ("nebulus", "24-pypudding",  "PY Pudding",                 ["parts:neb-24-pypudding"]),
    ("nebulus", "25-pkaido",     "P Kaido",                    ["parts:neb-25-pkaido"]),
    ("nebulus", "26-rocks",      "Rocks",                      ["parts:neb-26-rocks"]),
    ("nebulus", "27-elbo",       "ELBO (Elbaph Sabo)",         ["parts:neb-27-elbo"]),
    ("nebulus", "28-bluffy",     "Black Luffy",                ["parts:neb-28-bluffy"]),
]

AUTORI = {
    "raphterra": dict(nome="Raphterra", badge="b-raph", colore="var(--raph)",
                      fonte="Metafy — «OP17 Mihawk Ultimate Guide»"),
    "rondino":   dict(nome="Rondino", badge="b-rond", colore="var(--rond)",
                      fonte="Metafy — guida Green Mihawk OP17"),
    "nebulus":   dict(nome="NebulusTCG", badge="b-neb", colore="var(--neb)",
                      fonte="Metafy — guida Green Mihawk OP17"),
}


def stitch():
    """Concatena le trascrizioni per striscia in un file per capitolo."""
    out = {}
    for autore, slug, titolo, sources in CHAPTERS:
        buf = []
        for src in sources:
            kind, path = src.split(":", 1)
            if kind == "file":
                f = TRASC / path
                if f.exists():
                    txt = f.read_text(encoding="utf-8")
                    # via intestazione e note di servizio del file singolo
                    txt = re.sub(r"\A#[^\n]*\n", "", txt)
                    txt = re.sub(r"^> Fonte:[^\n]*\n", "", txt, flags=re.M)
                    txt = re.sub(r"^> Copre le strisce[^\n]*\n", "", txt, flags=re.M)
                    txt = re.sub(r"<!--[^>]*-->", "", txt)
                    buf.append(txt.strip())
            else:
                d = PARTS / path
                if d.exists():
                    for f in sorted(d.glob("s*.md")):
                        t = f.read_text(encoding="utf-8").strip()
                        t = re.sub(r"<!--[^>]*-->", "", t)
                        if t:
                            buf.append(t)
        if not buf:
            print(f"  [vuoto] {autore}/{slug}")
            continue
        body = "\n\n".join(buf)
        dest = TRASC / autore / f"{slug}.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(
            f"# {AUTORI[autore]['nome']} — {titolo}\n\n"
            f"> Fonte: {AUTORI[autore]['fonte']}. Trascrizione verbatim EN.\n\n{body}\n",
            encoding="utf-8")
        out.setdefault(autore, []).append((slug, titolo, body))
        print(f"  {autore}/{slug}.md  ({len(body):,} char)")
    return out


# ---------------------------------------------------------- 2. markdown -> html

CARD_IDS = set()


def _cards_on_disk():
    return {p.stem for p in CARTE.glob("*.png")}


ON_DISK = _cards_on_disk() if CARTE.exists() else set()


def inline(t):
    """grassetto, corsivo, codice, link, carte citate a meta' frase — su testo gia' escapato."""
    t = re.sub(r"\[Cards?:\s*([^\[\]]+?)\s*\(([^()\[\]]*)\)\s*\]",
               lambda m: card_chip(m.group(1), m.group(2)), t)
    t = re.sub(r"\[Cards?:\s*([^\[\]()]+?)\s*\]",
               lambda m: card_chip(m.group(1), ""), t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"&lt;u&gt;(.+?)&lt;/u&gt;", r"<u>\1</u>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)",
               r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    return t


def card_chip(nome, cid):
    """Chip con l'immagine ufficiale se l'abbiamo, altrimenti solo testo."""
    cid = (cid or "").strip()
    base = re.sub(r"_p\d+$", "", cid)
    if base in ON_DISK:
        CARD_IDS.add(base)
        return (f'<span class="cardchip"><img src="{{REL}}carte/{base}.png" alt="" loading="lazy">'
                f'{html.escape(nome)} <code style="color:var(--dim2);font-size:.75em">{base}</code></span>')
    extra = f' <code style="color:var(--dim2);font-size:.75em">{html.escape(cid)}</code>' if cid and cid != "ID?" else ""
    return f'<span class="cardchip" style="padding-left:10px">{html.escape(nome)}{extra}</span>'


def visual(line):
    """Rende [Card: ...] [Board diagram: ...] [Video embed: ...] ecc."""
    m = re.match(r"\[Cards?:\s*(.+?)\]\s*$", line)
    if m:
        body = m.group(1)
        chips = []
        for piece in re.split(r"\s*(?:,|·)\s*(?![^()]*\))", body):
            cm = re.match(r"(.+?)\s*\(([^)]*)\)\s*$", piece.strip())
            if cm:
                chips.append(card_chip(cm.group(1), cm.group(2)))
            elif piece.strip():
                chips.append(card_chip(piece.strip(), ""))
        return '<div class="cardrow">' + "".join(chips) + "</div>"

    m = re.match(r"\[Board diagram:\s*(.+)\]\s*$", line, re.S)
    if m:
        return f'<div class="board"><b>Board</b>{inline(html.escape(m.group(1)))}</div>'

    m = re.match(r"\[Decklist image:\s*(.+)\]\s*$", line, re.S)
    if m:
        return f'<div class="board"><b>Decklist</b>{inline(html.escape(m.group(1)))}</div>'

    m = re.match(r"\[Video embed:\s*(.+?)\]\s*$", line)
    if m:
        return (f'<div class="vid"><span class="ic">▶</span><span>Video nella guida: '
                f'<b>{html.escape(m.group(1))}</b></span></div>')

    m = re.match(r"\[Banner:\s*(.+?)\]\s*$", line)
    if m:
        return f'<p style="color:var(--dim2);font-size:.82rem;margin:10px 0">🖼 {html.escape(m.group(1))}</p>'

    m = re.match(r"\[Table:\s*(.+?)\]\s*$", line)
    if m:
        return f'<p style="color:var(--gold);font-size:.82rem;font-weight:700;margin:16px 0 4px">▦ {html.escape(m.group(1))}</p>'

    if line.strip() == "[ILLEGGIBILE]":
        return '<p class="note warn">[porzione illeggibile nello screenshot della fonte]</p>'
    return None


def md2html(md):
    out, i = [], 0
    lines = md.split("\n")
    n = len(lines)
    while i < n:
        ln = lines[i]
        s = ln.strip()

        if not s:
            i += 1
            continue

        # tabelle
        if s.startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:\-|]+\|\s*$", lines[i + 1]):
            head = [c.strip() for c in s.strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            th = "".join(f"<th>{inline(html.escape(c))}</th>" for c in head)
            tb = "".join("<tr>" + "".join(f"<td>{inline(html.escape(c))}</td>" for c in r) + "</tr>"
                         for r in rows)
            out.append(f'<div class="tscroll"><table><thead><tr>{th}</tr></thead>'
                       f"<tbody>{tb}</tbody></table></div>")
            continue

        # heading
        m = re.match(r"^(#{2,5})\s+(.*)$", s)
        if m:
            lvl = min(len(m.group(1)), 4)
            out.append(f"<h{lvl}>{inline(html.escape(m.group(2)))}</h{lvl}>")
            i += 1
            continue
        if re.match(r"^#\s+", s):           # titolo file: gia' nel template
            i += 1
            continue

        # citazioni / note
        if s.startswith(">"):
            block = []
            while i < n and lines[i].strip().startswith(">"):
                block.append(lines[i].strip().lstrip(">").strip())
                i += 1
            txt = " ".join(x for x in block if x)
            cls = "note"
            if "TRONCAMENTO" in txt.upper():
                cls = "note trunc"
            elif "⚠" in txt:
                cls = "note warn"
            out.append(f'<div class="{cls}">{inline(html.escape(txt))}</div>')
            continue

        # hr
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", s):
            out.append("<hr>")
            i += 1
            continue

        # elementi visivi (anche su piu' righe: accumula fino alla parentesi di chiusura)
        if re.match(r"^\[(Cards?|Board diagram|Decklist image|Video embed|Banner|Table|ILLEGGIBILE)", s):
            blk, j = [s], i
            while not blk[-1].rstrip().endswith("]") and j + 1 < n and lines[j + 1].strip():
                j += 1
                blk.append(lines[j].strip())
            joined = " ".join(blk)
            v = visual(joined)
            if v:
                out.append(v)
                i = j + 1
                continue

        # liste
        if re.match(r"^([-*+]|\d+[.)])\s+", s):
            ordered = bool(re.match(r"^\d+[.)]\s+", s))
            items = []
            while i < n and re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[i]):
                items.append(re.sub(r"^\s*([-*+]|\d+[.)])\s+", "", lines[i]).strip())
                i += 1
                # continuazioni indentate
                while i < n and lines[i].startswith("   ") and lines[i].strip() \
                        and not re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[i]):
                    items[-1] += " " + lines[i].strip()
                    i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(html.escape(x))}</li>" for x in items) + f"</{tag}>")
            continue

        # paragrafo
        para = [s]
        i += 1
        while i < n and lines[i].strip() and not re.match(
                r"^\s*(#{1,5}\s|[-*+]\s|\d+[.)]\s|>|\||\[(Card|Cards|Board|Video|Banner|Table|Decklist)|-{3,})",
                lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(html.escape(' '.join(para)))}</p>")
    return "\n".join(out)


# ------------------------------------------------------------- 3. pagine guida

NAV = """<header class="top"><div class="wrap topbar">
<div class="brand"><span class="dot"></span><a href="{REL}index.html">Green Mihawk OP17</a></div>
<nav class="main">
<a href="{REL}index.html">Home</a>
<a href="{REL}quiz-player.html">Quiz stile</a>
<a href="{REL}quiz-deck.html">Quiz lista</a>
<a href="{REL}matchup.html">Matchup</a>
<a href="{REL}mirror.html">Mirror</a>
<a href="{REL}guide/raphterra.html">Raphterra</a>
<a href="{REL}guide/rondino.html">Rondino</a>
<a href="{REL}guide/nebulus.html">NebulusTCG</a>
<a href="{REL}guide/impact.html">Impact</a>
<a href="{REL}guide/samsans.html">samsansOP</a>
<a href="{REL}video.html">Video</a>
<a href="{REL}carte.html">Carte</a>
</nav></div></header>"""

FOOT = """<footer><div class="wrap">
<p><b>Green Mihawk OP17 — hub delle guide.</b> Il contenuto strategico è trascritto <b>verbatim</b> dalle
fonti originali (inglese), le sintesi e i confronti sono in italiano.</p>
<p>Immagini carte © Bandai / Shueisha. Le guide Metafy appartengono ai rispettivi autori: i PDF sorgente
non sono ridistribuiti in questo repository. Uso personale di studio.</p>
</div></footer>
<script src="{REL}assets/app.js"></script></body></html>"""


def page(title, rel, body, desc=""):
    return f"""<!DOCTYPE html><html lang="it"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🗡️</text></svg>">
<link rel="stylesheet" href="{rel}assets/style.css">
</head><body>
{NAV.replace('{REL}', rel)}
{body}
{FOOT.replace('{REL}', rel)}"""


def build_guide_pages(chapters_by_author):
    (ROOT / "guide").mkdir(exist_ok=True)
    for autore, chaps in chapters_by_author.items():
        meta = AUTORI[autore]
        tabs = "".join(
            f'<button data-tab="{slug}">{html.escape(tit)}</button>' for slug, tit, _ in chaps)
        panes = []
        for slug, tit, body in chaps:
            h = md2html(body).replace("{REL}", "../")
            panes.append(
                f'<div class="tabpane" data-pane="{slug}">'
                f'<h2 class="sec" style="border:0;margin-bottom:4px">{html.escape(tit)}</h2>'
                f'<p class="lede">Trascrizione verbatim dalla guida di {meta["nome"]}.</p>'
                f'<div class="verb">{h}</div></div>')
        body = f"""<div class="hero"><div class="wrap">
<span class="badge {meta['badge']}">{html.escape(meta['nome'])}</span>
<h1 style="margin-top:12px">Guida di <em>{html.escape(meta['nome'])}</em></h1>
<p class="sub">{html.escape(meta['fonte'])} — testo integrale, capitolo per capitolo, nelle parole dell'autore.</p>
</div></div>
<section><div class="wrap">
<div data-tabs="panes"><div class="tabs">{tabs}</div></div>
<div id="panes">{''.join(panes)}</div>
</div></section>"""
        out = ROOT / "guide" / f"{autore}.html"
        out.write_text(page(f"{meta['nome']} — Green Mihawk OP17", "../", body,
                            f"Guida Green Mihawk OP17 di {meta['nome']}, trascrizione verbatim."),
                       encoding="utf-8")
        print(f"  guide/{autore}.html")


if __name__ == "__main__":
    print("1) cucitura trascrizioni")
    ch = stitch()
    print("2) pagine guida")
    build_guide_pages(ch)
    print("carte usate:", len(CARD_IDS))

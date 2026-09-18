# -*- coding: utf-8 -*-
"""Build del sito Green Mihawk OP17.

1) (solo con --stitch) cuce le trascrizioni per striscia (scratchpad/parts) in
   trascrizioni/<autore>/<capitolo>.md — i file cuciti sono gia' nel repo
2) converte il markdown verbatim in HTML impaginato (render.py)
3) genera le pagine delle guide e riallinea il menu delle pagine scritte a mano

Uso:  python build.py            (rigenera le pagine dai .md esistenti)
      python build.py --stitch   (ricuce prima i capitoli dalle strisce)
"""
import html
import pathlib
import re
import sys

from render import render, md2html, chapter_map, load_sintesi, CARD_IDS, ON_DISK  # noqa: F401

ROOT = pathlib.Path(__file__).parent
SCRATCH = pathlib.Path(
    r"C:\Users\bened\AppData\Local\Temp\claude"
    r"\c--Users-bened-Desktop-PARA-3--Resources-OP-Guide-OP-Mihawk"
    r"\420c3572-c78d-4159-b08c-ded0a9bb5b6f\scratchpad"
)
PARTS = SCRATCH / "parts"
TRASC = ROOT / "trascrizioni"
CARTE = ROOT / "carte"

# ---------------------------------------------------------------- 1. capitoli

# capitolo -> (autore, slug, titolo, [sorgenti in ordine], gruppo di tab)
# sorgente = "parts:<dir>" oppure "file:<path relativo a trascrizioni>"
CHAPTERS = [
    ("raphterra", "00-welcome",   "Welcome and Introduction",              ["file:raphterra/00-welcome.md"], "Fondamentali"),
    ("raphterra", "01-deckcore",  "Deck Core and Deckbuilding Fundamentals",["parts:raph-01-deckcore"], "Fondamentali"),
    ("raphterra", "02-gameplay",  "Gameplay Fundamentals",                 ["parts:raph-02-gameplay"], "Fondamentali"),
    ("raphterra", "04-meta",      "Green Mihawk in the OP17 Meta",         ["file:raphterra/04-meta.md"], "Meta e matchup"),
    ("raphterra", "05-mu-meta",   "Matchup Strategies vs The Meta",
     ["file:raphterra/05-matchup-meta-parte1.md", "parts:raph-05-mu-meta"], "Meta e matchup"),
    ("raphterra", "06-mu-field",  "Matchup Strategies vs The Field (WIP)", ["file:raphterra/06-matchup-field.md"], "Meta e matchup"),

    ("rondino", "01-intro",     "1. Intro chapter",        ["file:rondino/01-intro.md"], "La guida (Metafy)"),
    ("rondino", "02-meta",      "2. Meta analysis",        ["file:rondino/02-meta-analysis.md"], "La guida (Metafy)"),
    ("rondino", "03-decklist",  "3. The decklist",         ["parts:rond-03-decklist"], "La guida (Metafy)"),
    ("rondino", "04-strategy",  "4. General deck strategy",["file:rondino/04-general-deck-strategy.md"], "La guida (Metafy)"),
    ("rondino", "05-mu-bible",  "5. The matchups bible",   ["parts:rond-05-mu-bible"], "La guida (Metafy)"),
    # nessuna sorgente da cucire: il file e' gia' la trascrizione finale del PDF
    ("rondino", "06-masterclass-16-09", "Masterclass 16/09 · aggiornamento", [], "Sessioni (Dog of Wisdom)"),

    ("nebulus", "13-whatis",     "What is Mihawk?",            ["parts:neb-13-whatis"], "Il mazzo"),
    ("nebulus", "14-cards",      "Cards & Decklist",           ["parts:neb-14-cards"], "Il mazzo"),
    ("nebulus", "15-tech",       "TECH CARDS",                 ["parts:neb-15-tech"], "Il mazzo"),
    ("nebulus", "16-carddraw",   "Card Draw",                  ["parts:neb-16-carddraw"], "Il mazzo"),
    ("nebulus", "17-philosophy", "Philosophy & Don Management",["parts:neb-17-philosophy"], "Il mazzo"),
    ("nebulus", "18-looping",    "Looping Your Deck",          ["parts:neb-18-looping"], "Il mazzo"),
    ("nebulus", "19-trashevent", "Trash Event Tech",           ["parts:neb-19-trashevent"], "Il mazzo"),
    ("nebulus", "20-rapidfire",  "Rapidfire MU Spread 9/1",    ["parts:neb-20-rapidfire"], "Matchup"),
    ("nebulus", "21-pyrobin",    "PY Robin",                   ["parts:neb-21-pyrobin"], "Matchup"),
    ("nebulus", "22-ylinlin",    "Y Linlin",                   ["parts:neb-22-ylinlin"], "Matchup"),
    ("nebulus", "23-uyboa",      "UY Boa",                     ["parts:neb-23-uyboa"], "Matchup"),
    ("nebulus", "24-pypudding",  "PY Pudding",                 ["parts:neb-24-pypudding"], "Matchup"),
    ("nebulus", "25-pkaido",     "P Kaido",                    ["parts:neb-25-pkaido"], "Matchup"),
    ("nebulus", "26-rocks",      "Rocks",                      ["parts:neb-26-rocks"], "Matchup"),
    ("nebulus", "27-elbo",       "ELBO (Elbaph Sabo)",         ["parts:neb-27-elbo"], "Matchup"),
    ("nebulus", "28-bluffy",     "Black Luffy",                ["parts:neb-28-bluffy"], "Matchup"),
]

# leader nel bottone del tab
TAB_LEADER = {"21-pyrobin": "OP09-062", "22-ylinlin": "OP17-099", "23-uyboa": "OP14-041",
              "24-pypudding": "OP08-058", "25-pkaido": "OP17-058", "26-rocks": "OP17-039",
              "27-elbo": "OP13-004", "28-bluffy": "OP17-079"}

AUTORI = {
    "raphterra": dict(nome="Raphterra", badge="b-raph", colore="var(--raph)",
                      fonte="Metafy — «OP17 Mihawk Ultimate Guide»"),
    "rondino":   dict(nome="Rondino", badge="b-rond", colore="var(--rond)",
                      fonte="Metafy — guida Green Mihawk OP17"),
    "nebulus":   dict(nome="NebulusTCG", badge="b-neb", colore="var(--neb)",
                      fonte="Metafy — guida Green Mihawk OP17"),
}

# introduzione del tab, dove il capitolo non e' un capitolo della guida
LEDE = {
    "06-masterclass-16-09": "Le note di sessione (Dog of Wisdom) della masterclass del 16/09: è la posizione più recente di "
                            "Rondino — lista senza Bonney e Perona 5c, starve come default, verdetti matchup aggiornati. "
                            "Trascrizione verbatim del PDF.",
}

G = "img/guide/"
# immagini originali delle guide, agganciate al marcatore [Banner/Table/Decklist...] che le descrive
FIGS = {
    "raphterra/00-welcome": [(r"foto di tre giocatori", [G + "raphterra-foto.png"])],
    "raphterra/01-deckcore": [
        (r"DECKBUILDING FUNDAMENTALS CHEATSHEET", [G + "raph-cheatsheet-deckbuilding.png"]),
        (r"TECH CHEATSHEET AGAINST THE META", [G + "raph-cheatsheet-tech-meta.png"]),
        (r"cardkaizoku\.com deck view", [G + "raph-deck1-standard-law.png", G + "raph-deck2-standard-tech.png",
                                          G + "raph-deck3-hybrid.png", G + "raph-deck4-trash.png"])],
    "raphterra/04-meta": [(r"^Tier List", [G + "raph-tier-list.png"])],
    "raphterra/05-mu-meta": [
        (r"VS MIRROR", [G + "raph-cs-mirror.png"]), (r"VS OP09 ROBIN", [G + "raph-cs-py-robin.png"]),
        (r"VS OP16 ACE", [G + "raph-cs-red-ace.png"]), (r"^VS\. BLACK LUFFY", [G + "raph-cs-op17-luffy.png"])],
    "rondino/03-decklist": [(r"^deck builder screenshot", [G + "rond-decklist-mera-mera.png"]),
                            (r"^updated deck builder", [G + "rond-decklist-update.png"])],
    "nebulus/14-cards": [(r"cardkaizoku\.com watermark", [G + "nebulus-decklist.png"])],
    "nebulus/17-philosophy": [(r"Probability of Drawing", [G + "nebulus-card-draw-results.png"])],
    "nebulus/25-pkaido": [(r"Kaido \[OP17-058\] Curve", [G + "nebulus-kaido-curve.png"])],
    "impact/pptx": [(r"^decklist standard", ["img/decklist-impact-law-yasopp.png"])],
}


def _read_chapter(autore, slug):
    f = TRASC / autore / f"{slug}.md"
    if not f.exists():
        return None
    txt = f.read_text(encoding="utf-8")
    txt = re.sub(r"\A#[^\n]*\n", "", txt)
    txt = re.sub(r"^> Fonte:[^\n]*\n", "", txt, count=1, flags=re.M)
    return txt.strip()


def load_chapters():
    """Legge i capitoli gia' cuciti da trascrizioni/<autore>/<slug>.md."""
    out = {}
    for autore, slug, titolo, _src, grp in CHAPTERS:
        body = _read_chapter(autore, slug)
        if body is None:
            print(f"  [manca] {autore}/{slug}.md")
            continue
        out.setdefault(autore, []).append((slug, titolo, body, grp))
    return out


def stitch():
    """Concatena le trascrizioni per striscia in un file per capitolo."""
    for autore, slug, titolo, sources, _grp in CHAPTERS:
        buf = []
        for src in sources:
            kind, path = src.split(":", 1)
            if kind == "file":
                f = TRASC / path
                if f.exists():
                    txt = f.read_text(encoding="utf-8")
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
            print(f"  [vuoto, non tocco il file] {autore}/{slug}")
            continue
        body = "\n\n".join(buf)
        dest = TRASC / autore / f"{slug}.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(
            f"# {AUTORI[autore]['nome']} — {titolo}\n\n"
            f"> Fonte: {AUTORI[autore]['fonte']}. Trascrizione verbatim EN.\n\n{body}\n",
            encoding="utf-8")
        print(f"  {autore}/{slug}.md  ({len(body):,} char)")


# ------------------------------------------------------------- 2. template

NAV = """<header class="top"><div class="wrap topbar">
<div class="brand"><span class="dot"></span><a href="{REL}index.html">Green Mihawk OP17</a></div>
<button class="navtoggle" type="button" aria-label="Apri il menu" aria-expanded="false"><span></span></button>
<nav class="main">
<a href="{REL}index.html">Home</a>
<div class="dd"><button class="dd-b" type="button" aria-expanded="false">Quiz <i>▾</i></button><div class="dd-m">
 <a href="{REL}quiz-deck.html"><b>Quale lista fa per te</b><span>11 domande, compresi i matchup che soffri tu</span></a>
 <a href="{REL}quiz-player.html"><b>Che giocatore sei</b><span>A quale dei cinque autori somigli</span></a>
</div></div>
<a href="{REL}matchup.html">Matchup</a>
<a href="{REL}mirror.html">Mirror</a>
<a href="{REL}confronto.html">LawSopp vs HawkRona</a>
<div class="dd"><button class="dd-b" type="button" aria-expanded="false">Guide <i>▾</i></button><div class="dd-m">
 <a href="{REL}guide/raphterra.html"><b><i class="sw" style="background:var(--raph)"></i>Raphterra</b><span>La più sistematica · 6 capitoli</span></a>
 <a href="{REL}guide/rondino.html"><b><i class="sw" style="background:var(--rond)"></i>Rondino</b><span>La matchups bible · masterclass 16/09</span></a>
 <a href="{REL}guide/nebulus.html"><b><i class="sw" style="background:var(--neb)"></i>NebulusTCG</b><span>Tech, probabilità, mazzi gialli</span></a>
 <a href="{REL}guide/impact.html"><b><i class="sw" style="background:var(--impact)"></i>Impact</b><span>Law + Yasopp · slide, video, Q&amp;A 17/09</span></a>
 <a href="{REL}guide/samsans.html"><b><i class="sw" style="background:var(--sam)"></i>samsansOP</b><span>Mihawk 6c + Perona 5c · video</span></a>
 <a href="{REL}guide/dojo.html"><b><i class="sw" style="background:var(--dojo)"></i>The Dojo</b><span>Sessioni: VOD review e ladder di Elijah</span></a>
</div></div>
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


def sync_nav():
    """Riallinea il menu delle pagine scritte a mano a quello del template."""
    for name in ["index.html", "quiz-player.html", "quiz-deck.html", "matchup.html", "mirror.html"]:
        f = ROOT / name
        if not f.exists():
            continue
        s = f.read_text(encoding="utf-8")
        new = re.sub(r'<header class="top">.*?</header>', lambda m: NAV.replace("{REL}", ""), s, count=1, flags=re.S)
        if new != s:
            f.write_text(new, encoding="utf-8")
            print(f"  menu aggiornato: {name}")


# ------------------------------------------------------------ 3. pagine guida

def tab_buttons(chaps, rel):
    out, last = [], None
    for c in chaps:
        slug, tit, grp = c[0], c[1], c[3] if len(c) > 3 else ""
        if grp and grp != last:
            out.append(f'<span class="tg">{html.escape(grp)}</span>')
            last = grp
        ld = TAB_LEADER.get(slug)
        img = f'<img src="{rel}carte/{ld}.png" alt="">' if ld and ld in ON_DISK else ""
        out.append(f'<button data-tab="{slug}">{img}{html.escape(tit)}</button>')
    return "".join(out)


# guide in prosa fitta: paragrafi spezzati in gruppi di frasi + sintesi per sezione (sintesi/<autore>/<slug>.md)
PROSE = {"nebulus"}


def pane(key, titolo, lede, md, rel, figs=None, autore=None):
    sint = load_sintesi(ROOT / "sintesi" / autore / f"{key}.md") if autore in PROSE else None
    h, heads = render(md, rel, figs, prose=autore in PROSE, sintesi=sint)
    if sint:
        lede = ("In testa a ogni sezione la <b>sintesi in italiano</b>; sotto, la trascrizione verbatim "
                "spezzata in blocchi di poche frasi (le parole dell'autore non cambiano).")
        lede += (' <button type="button" class="sint-tg" aria-pressed="false">'
                 '⚡ Solo sintesi</button>')
    return (f'<div class="tabpane" data-pane="{key}">'
            f'<h2 class="sec pane-t">{html.escape(titolo)}</h2>'
            f'<p class="lede">{lede}</p>{chapter_map(heads, rel)}'
            f'<div class="verb">{h}</div></div>')


def guide_body(badge, nome, sub, tabs_html, panes_html):
    return f"""<div class="hero hero-s"><div class="wrap">
<span class="badge {badge}">{html.escape(nome)}</span>
<h1 style="margin-top:12px">Guida di <em>{html.escape(nome)}</em></h1>
<p class="sub">{sub}</p>
</div></div>
<section class="gpage"><div class="wrap">
<div data-tabs="panes"><div class="tabs">{tabs_html}</div></div>
<div class="glayout">
<aside class="gtoc"><button class="gtoc-b" type="button">Indice del capitolo <i>▾</i></button><nav id="gtoc"></nav></aside>
<div id="panes">{panes_html}</div>
</div>
</div></section>"""


def build_guide_pages(chapters_by_author):
    (ROOT / "guide").mkdir(exist_ok=True)
    for autore, chaps in chapters_by_author.items():
        meta = AUTORI[autore]
        panes = "".join(
            pane(slug, tit, LEDE.get(slug, f"Trascrizione verbatim dalla guida di {meta['nome']}."), body, "../",
                 FIGS.get(f"{autore}/{slug}"), autore)
            for slug, tit, body, _g in chaps)
        body = guide_body(meta["badge"], meta["nome"],
                          f"{html.escape(meta['fonte'])} — testo integrale, capitolo per capitolo, nelle parole dell'autore.",
                          tab_buttons(chaps, "../"), panes)
        out = ROOT / "guide" / f"{autore}.html"
        out.write_text(page(f"{meta['nome']} — Green Mihawk OP17", "../", body,
                            f"Guida Green Mihawk OP17 di {meta['nome']}, trascrizione verbatim."),
                       encoding="utf-8")
        print(f"  guide/{autore}.html")


if __name__ == "__main__":
    if "--stitch" in sys.argv:
        print("1) cucitura trascrizioni")
        stitch()
    print("2) pagine guida")
    build_guide_pages(load_chapters())
    print("3) menu delle pagine a mano")
    sync_nav()
    print("carte usate:", len(CARD_IDS))

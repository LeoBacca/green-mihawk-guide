# -*- coding: utf-8 -*-
"""Genera le pagine semplici del sito (video, carte) riusando il template di build.py."""
import pathlib
import re

from build import page, ROOT, CARTE

# ------------------------------------------------------------------ video.html
VIDEO_BODY = """<div class="hero"><div class="wrap">
<span class="badge b-sint">Videoteca</span>
<h1 style="margin-top:12px">Tutti i <em>video</em> delle guide</h1>
<p class="sub">Le due lezioni complete di Impact e samsansOP, più i 23 video di Raphterra
divisi per argomento. Ogni voce dice a quale matchup serve.</p>
<input class="searchbox" style="max-width:520px" placeholder="Filtra: mirror, robin, kaido, lethal…" data-searchfor=".vcard">
</div></div>
<section><div class="wrap"><div id="vidWrap"></div></div></section>
<script src="data/video.js"></script>
<script>
const cats = [...new Set(VIDEO.map(v=>v.cat))];
document.getElementById('vidWrap').innerHTML = cats.map(c=>{
  const items = VIDEO.filter(v=>v.cat===c);
  return `<h2 class="sec" style="margin-top:34px">${c}
    <span style="color:var(--dim2);font-weight:400;font-size:.9rem">· ${items.length} video</span></h2>
    <div class="vgrid">` + items.map(v=>`
      <a class="vcard" href="${v.u}" target="_blank" rel="noopener">
        <div class="pl">\\u25b6 ${v.src}</div>
        <h4>${v.t}</h4>
        <p>${v.note||''}</p>
        <p style="margin-top:7px"><span class="pill">${v.mu}</span></p>
      </a>`).join('') + `</div>`;
}).join('');
</script>"""


def build_video():
    (ROOT / "video.html").write_text(
        page("Video — Green Mihawk OP17", "", VIDEO_BODY,
             "Tutti i video YouTube delle guide Green Mihawk OP17, divisi per argomento e matchup."),
        encoding="utf-8")
    print("  video.html")


# ------------------------------------------------------------------ carte.html
NOMI = {
 "OP14-020":"Dracule Mihawk (Leader)","OP17-022":"Shanks 10c","OP17-031":"Yasopp 5c",
 "ST32-002":"Kouzuki Oden 5c","OP13-031":"Trafalgar Law 6c","OP12-023":"Kawamatsu 5c",
 "OP12-034":"Perona 1c","OP14-033":"Perona 5c","OP07-022":"Otama 1c","ST32-001":"Kin'emon 1c",
 "OP06-033":"Vander Decken IX 2c","OP08-036":"Electrical Luna","OP01-055":"You Can Be My Samurai!!",
 "OP06-038":"The Billion-fold World Trichiliocosm","OP14-039":"Coffin Boat","OP14-023":"Kikunojo 1c",
 "OP07-026":"Jewelry Bonney 5c","ST24-004":"Law & Bepo 10c","ST32-003":"Dracule Mihawk 6c",
 "OP14-037":"For Fun","OP14-038":"I Never Bother to Remember the Faces of Trash","OP13-040":"I Know You're Strong…",
 "OP12-037":"Asura Dead Man's Game","OP06-035":"Hody Jones 7c","OP10-030":"Smoker","OP14-036":"Strive to Surpass Me, Zoro!!",
 "OP13-001":"Trafalgar Law (altro)","OP16-028":"—","OP15-058":"Enel (Leader)","OP17-058":"Kaido (Leader)",
 "OP17-039":"Rocks.D.Xebec (Leader)","OP13-004":"Sabo (Leader)","OP16-001":"Portgas.D.Ace (Leader)",
 "OP09-062":"Nico Robin (Leader)","OP17-079":"Monkey.D.Luffy (Leader)","OP14-041":"Boa Hancock (Leader)",
 "OP08-058":"Charlotte Pudding (Leader)","OP17-099":"Charlotte Linlin (Leader)","ST30-001":"Luffy & Ace (Leader)",
 "OP17-040":"Edward Newgate 6c","OP17-048":"Shiki","OP17-044":"Captain John","OP17-045":"Kyo",
 "EB04-031":"King","ST34-004":"Charlotte Linlin 10c","OP17-089":"Jaguar D. Saul","OP17-091":"Brook",
 "OP17-093":"Monkey.D.Luffy (trash)","OP17-081":"Gerd","OP17-080":"Usopp","OP17-109":"Charlotte Pudding",
 "OP17-111":"Charlotte Mont-d'or","OP17-064":"—","OP17-046":"—","OP17-049":"—","OP17-112":"—",
 "OP17-118":"—","OP17-119":"—","EB02-015":"—","EB02-030":"—","EB04-031 ":"King","OP17-100":"—",
 "OP17-101":"—","OP17-114":"—","OP12-001":"—","EB02-001":"—","OP13-041":"—","ST30-002":"—",
 "OP16-001 ":"Ace","OP10-030 ":"Smoker",
}
GRUPPI = [
 ("Il core del mazzo", ["OP14-020","OP17-022","OP17-031","ST32-002","OP13-031","OP12-023",
                        "OP12-034","OP07-022","ST32-001","OP06-033","OP08-036","OP01-055",
                        "OP06-038","OP14-039"]),
 ("Tech e alternative", ["OP14-033","OP07-026","ST24-004","ST32-003","OP14-023","OP14-037",
                         "OP14-038","OP13-040","OP12-037","OP06-035","OP10-030","OP14-036"]),
 ("Leader avversari", ["OP17-058","OP17-039","OP13-004","OP16-001","OP09-062","OP17-079",
                       "OP15-058","OP14-041","OP08-058","OP17-099","ST30-001"]),
 ("Carte avversarie citate", ["OP17-040","OP17-048","OP17-044","OP17-045","EB04-031","ST34-004",
                              "OP17-089","OP17-091","OP17-093","OP17-081","OP17-109","OP17-111"]),
]


def build_carte():
    have = {p.stem for p in CARTE.glob("*.png")}
    used = set()
    blocks = []
    for titolo, ids in GRUPPI:
        cards = []
        for cid in ids:
            if cid not in have:
                continue
            used.add(cid)
            nome = NOMI.get(cid, "")
            cards.append(f'<div class="cardbox" style="width:128px"><img src="carte/{cid}.png" '
                         f'alt="{nome}" loading="lazy"><span>{cid}<br>{nome}</span></div>')
        if cards:
            blocks.append(f'<h2 class="sec" style="margin-top:32px">{titolo} '
                          f'<span style="color:var(--dim2);font-weight:400;font-size:.9rem">· {len(cards)} carte</span></h2>'
                          f'<div class="cardrow">{"".join(cards)}</div>')
    resto = sorted(have - used)
    if resto:
        cards = "".join(f'<div class="cardbox" style="width:112px"><img src="carte/{c}.png" alt="" loading="lazy">'
                        f'<span>{c}</span></div>' for c in resto)
        blocks.append(f'<h2 class="sec" style="margin-top:32px">Altre carte scaricate '
                      f'<span style="color:var(--dim2);font-weight:400;font-size:.9rem">· {len(resto)}</span></h2>'
                      f'<div class="cardrow">{cards}</div>')
    body = f"""<div class="hero"><div class="wrap">
<span class="badge b-sint">Riferimento</span>
<h1 style="margin-top:12px">Le <em>carte</em> citate dalle guide</h1>
<p class="sub">{len(have)} immagini ufficiali Bandai, raggruppate per ruolo. Utile quando una guida
nomina una carta con un soprannome e non sai quale sia.</p>
<input class="searchbox" style="max-width:420px" placeholder="Filtra per ID o nome…" data-searchfor=".cardbox">
</div></div>
<section><div class="wrap">{''.join(blocks)}</div></section>"""
    (ROOT / "carte.html").write_text(
        page("Carte — Green Mihawk OP17", "", body,
             "Riferimento visivo delle carte citate dalle guide Green Mihawk OP17."),
        encoding="utf-8")
    print(f"  carte.html ({len(have)} carte)")


# ------------------------------------------- guide "piatte" (Impact / samsansOP)
from build import md2html, TRASC  # noqa: E402

FLAT = {
 "impact": dict(
   nome="Impact", badge="b-impact",
   fonte='«Why is 10c Shanks So Broken? Srsly» — PowerPoint + video-lezione «Hawk Guide Law/Yasopp Version»',
   occhiello="Versione Law + Yasopp",
   tabs=[("pptx",  "Il PowerPoint (34 slide)", "impact-law-yasopp-pptx.md"),
         ("note",  "Appunti della video-lezione", "impact-lezione-video-note.md"),
         ("vs",    "Video vs appunti", "impact-lezione-video-vs-note.md"),
         ("trascr","Trascrizione integrale del video", "impact-lezione-video-trascrizione.md")]),
 "samsans": dict(
   nome="samsansOP", badge="b-sam",
   fonte='«op17 mihawk deep dive» — video di 2 ore + note ordinate',
   occhiello="Versione Mihawk 6c + Perona 5c",
   tabs=[("note",  "Note ordinate del video", "samsans-mihawk-perona-note.md"),
         ("vs",    "Video vs note", "samsans-video-vs-note.md"),
         ("trascr","Trascrizione integrale del video", "samsans-video-trascrizione.md")]),
}


def build_flat():
    for slug, meta in FLAT.items():
        tabs, panes = [], []
        for key, titolo, fname in meta["tabs"]:
            f = TRASC / fname
            if not f.exists():
                print(f"    [manca] {fname}")
                continue
            md = f.read_text(encoding="utf-8")
            md = re.sub(r"\A#[^\n]*\n", "", md)
            tabs.append(f'<button data-tab="{key}">{titolo}</button>')
            panes.append(f'<div class="tabpane" data-pane="{key}">'
                         f'<h2 class="sec" style="border:0">{titolo}</h2>'
                         f'<div class="verb">{md2html(md).replace("{REL}", "../")}</div></div>')
        body = f"""<div class="hero"><div class="wrap">
<span class="badge {meta['badge']}">{meta['nome']}</span>
<h1 style="margin-top:12px">Guida di <em>{meta['nome']}</em></h1>
<p class="sub">{meta['fonte']} — {meta['occhiello']}. Testo integrale, nelle parole dell'autore.</p>
</div></div>
<section><div class="wrap">
<div data-tabs="panes"><div class="tabs">{''.join(tabs)}</div></div>
<div id="panes">{''.join(panes)}</div>
</div></section>"""
        (ROOT / "guide" / f"{slug}.html").write_text(
            page(f"{meta['nome']} — Green Mihawk OP17", "../", body,
                 f"Guida Green Mihawk OP17 di {meta['nome']}, trascrizione verbatim."),
            encoding="utf-8")
        print(f"  guide/{slug}.html")


# --------------------------------------------------- LawSopp vs HawkRona
def build_confronto():
    f = TRASC / "lawsopp-vs-hawkrona.md"
    if not f.exists():
        return
    md = re.sub(r"\A#[^\n]*\n", "", f.read_text(encoding="utf-8"))
    body = f"""<div class="hero"><div class="wrap">
<span class="badge b-sint">Documento comparativo</span>
<h1 style="margin-top:12px">LawSopp vs <em>HawkRona</em></h1>
<p class="sub">Le due versioni del mazzo messe a confronto argomento per argomento —
Law + Yasopp (Impact) contro Mihawk 6c + Perona 5c (samsansOP) — più la tavola decisionale finale.</p>
</div></div>
<section><div class="wrap"><div class="verb">{md2html(md).replace('{REL}', '')}</div></div></section>"""
    (ROOT / "confronto.html").write_text(
        page("LawSopp vs HawkRona — Green Mihawk OP17", "", body,
             "Le due versioni di Green Mihawk OP17 a confronto argomento per argomento."),
        encoding="utf-8")
    print("  confronto.html")


if __name__ == "__main__":
    build_video()
    build_carte()
    build_flat()
    build_confronto()

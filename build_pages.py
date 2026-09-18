# -*- coding: utf-8 -*-
"""Genera le pagine semplici del sito (video, carte, guide "piatte", confronto)
riusando il template di build.py."""
import html
import re

from build import page, ROOT, CARTE, TRASC, FIGS, pane, guide_body, tab_buttons
from render import esc

# ------------------------------------------------------------------ video.html
VIDEO_BODY = """<div class="hero"><div class="wrap">
<span class="badge b-sint">Videoteca</span>
<h1 style="margin-top:12px">Tutti i <em>video</em> delle guide</h1>
<p class="sub">Le due lezioni complete di Impact e samsansOP, le sessioni di settembre (il Q&amp;A di Impact
e la masterclass di Rondino) e i 23 video di Raphterra divisi per argomento. Ogni voce dice a quale matchup serve.</p>
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
 "OP17-111":"Charlotte Mont-d'or",
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
FLAT = {
 "impact": dict(
   nome="Impact", badge="b-impact",
   fonte='«Why is 10c Shanks So Broken? Srsly» — PowerPoint + video-lezione «Hawk Guide Law/Yasopp Version» + Q&amp;A del Dojo del 17/09',
   occhiello="Versione Law + Yasopp",
   tabs=[("pptx",  "Il PowerPoint (34 slide)", "impact-law-yasopp-pptx.md", "Le slide della guida, una per riquadro.", "La guida"),
         ("note",  "Appunti della video-lezione", "impact-lezione-video-note.md", "Gli appunti ordinati della lezione.", "La guida"),
         ("vs",    "Video vs appunti", "impact-lezione-video-vs-note.md", "Cosa c'è solo nel video, e dove video e appunti non coincidono.", "La guida"),
         ("trascr", "Trascrizione integrale del video", "impact-lezione-video-trascrizione.md",
          "Sottotitoli automatici, a blocchi di ~45 secondi: ogni orario apre il video in quel punto.", "La guida"),
         ("qa1709", "Deep Dive Q&A 17/09 · note di sessione", "impact-dojo-qa-17-09.md",
          "Le note di sessione (20 pagine) del Q&amp;A pre-Finals sul Dojo: il «rest spell», le tre build, i matchup "
          "rivisti e il weekend di torneo. È la fonte più recente di Impact.", "Q&A Dojo 17/09"),
         ("qa1709dojo", "Q&A 17/09 · note ufficiali del Dojo", "dojo/s1-impact-meta-qa-17-09.md",
          "La stessa sessione nelle note ufficiali della Training Library del Dojo (Codex, sessione 1): "
          "più discorsive, con qualche passaggio che nelle note di sessione è riassunto.", "Q&A Dojo 17/09")]),
 "samsans": dict(
   nome="samsansOP", badge="b-sam",
   fonte='«op17 mihawk deep dive» — video di 2 ore + note ordinate',
   occhiello="Versione Mihawk 6c + Perona 5c",
   tabs=[("note",  "Note ordinate del video", "samsans-mihawk-perona-note.md", "Le note della sessione, sezione per sezione.", ""),
         ("vs",    "Video vs note", "samsans-video-vs-note.md", "Cosa c'è solo nel video, e dove video e note non coincidono.", ""),
         ("trascr", "Trascrizione integrale del video", "samsans-video-trascrizione.md",
          "Sottotitoli automatici, a blocchi di ~45 secondi: ogni orario apre il video in quel punto.", "")]),
 "dojo": dict(
   nome="The Dojo", badge="b-dojo",
   fonte='Session Notes della Training Library di thedojo.gg («The Codex», le sessioni nei preferiti)',
   occhiello="VOD review e ladder di Elijah («Equinby»)",
   tabs=[("s2", "VOD review · Mihawk vs Robin · 9/09", "dojo/s2-vod-robin-09-09.md",
          "Il matchup con Robin analizzato su VOD: tempo prima del primo Big Mom, Dead Man's Game, Shanks + Luna, "
          "gestione della vita. Attenzione: sul turno la fonte si contraddice (è segnalato nel punto esatto).", "Sessioni"),
         ("s3", "Ladder con Elijah · 3/09", "dojo/s3-ladder-elijah-03-09.md",
          "Elijah in ladder sceglie fra Law + Yasopp e Mihawk + Perona: tre Decken, tre Boat, Law/Bepo, mirror, Enel e Robin.", "Sessioni"),
         ("s6", "VOD review con Equinby · 27/08", "dojo/s6-vod-equinby-27-08.md",
          "VOD review condotta da Elijah su più mazzi: Sabo vs Mihawk, Robin vs Rocks, Mihawk vs P Enel e vs Ace Luffy, "
          "e un metodo generale per leggere vita, carte, board e DON!!.", "Sessioni"),
         ("codex", "Il Codex: cosa c'è e dove", "dojo/codex-indice.md",
          'Le sei sessioni che il Codex raccoglie. Nel sito: la <b>1</b> (Q&amp;A di Impact del 17/09) è nella '
          '<a href="impact.html#qa1709dojo">pagina di Impact</a>; la <b>4</b> (Impact, deep dive del 31/08) coincide con gli '
          '<a href="impact.html#note">appunti della video-lezione di Impact</a>; la <b>5</b> (samsansOP, 28/08) coincide con le '
          '<a href="samsans.html#note">note di samsansOP</a>. Qui ci sono le altre tre, più l\'indice originale.', "Indice")]),
}


def build_flat():
    for slug, meta in FLAT.items():
        tabs, panes = [], []
        for key, titolo, fname, lede, grp in meta["tabs"]:
            f = TRASC / fname
            if not f.exists():
                print(f"    [manca] {fname}")
                continue
            md = re.sub(r"\A#[^\n]*\n", "", f.read_text(encoding="utf-8"))
            md = re.sub(r"^> Fonte:[^\n]*\n", "", md, count=1, flags=re.M)
            tabs.append((key, titolo, None, grp))
            panes.append(pane(key, titolo, lede, md, "../", FIGS.get(f"{slug}/{key}")))
        body = guide_body(meta["badge"], meta["nome"],
                          f"{meta['fonte']} — {meta['occhiello']}. Testo integrale, nelle parole dell'autore.",
                          tab_buttons(tabs, "../"), "".join(panes))
        (ROOT / "guide" / f"{slug}.html").write_text(
            page(f"{meta['nome']} — Green Mihawk OP17", "../", body,
                 f"Guida Green Mihawk OP17 di {meta['nome']}, trascrizione verbatim."),
            encoding="utf-8")
        print(f"  guide/{slug}.html")


# --------------------------------------------------- LawSopp vs HawkRona
# le righe della tabella del documento, raggruppate per tema (l'ordine interno resta quello della fonte)
TEMI = [
 ("identita", "🧭", "Identità e filosofia",
  ["Primary deck identity", "Central philosophy", "Main source of advantage", "Main failure mode",
   "Skill test", "Best player profile", "Best metagame profile", "Most transferable lesson"]),
 ("pacchetto", "🃏", "Il pacchetto da 5 e 6 costi",
  ["Preferred 5/6-cost package", "Why play 6c Mihawk?", "Why play Law?", "Why play Yasopp?",
   "Yasopp's self-restand", "Perona's role (1c/5c)", "Perona + Law interaction"]),
 ("motore", "⚙️", "Motore, consistenza e difesa",
  ["Brick management", "View of raw card draw", "Opener dependence", "Small-body vulnerability",
   "Samurai interaction", "Coffin Boat", "2K counter philosophy", "Defensive events"]),
 ("piano", "🗺️", "Piano di gioco turno per turno",
  ["Early-game objective", "Midgame objective", "Use of extra DON", "Attacking philosophy",
   "Preferred board state", "Board protection", "Role of freezes", "View of long control games"]),
 ("shanks", "🗡️", "Shanks e i boss",
  ["Shanks evaluation", "Shanks timing", "Shanks + Luna", "Shanks + Vander Decken", "Law & Bepo",
   "View of 7c/9c Shanks lines"]),
 ("mirror", "🪞", "Il mirror",
  ["Mirror priority", "Mirror going second", "Mirror life management", "Mirror attack thresholds",
   "Mirror tech: Stun Bonney"]),
 ("matchup", "⚔️", "Gli altri matchup",
  ["Sabo matchup", "Sabo plan", "Sabo and Yasopp", "Kaido matchup", "Kaido attack sequencing",
   "Robin matchup", "Rocks matchup", "Enel matchup"]),
]


def _table_rows(md, header_start):
    """Righe della prima tabella markdown la cui intestazione inizia con header_start."""
    lines = md.split("\n")
    for i, ln in enumerate(lines):
        if ln.strip().startswith("| " + header_start):
            rows = []
            for r in lines[i + 2:]:
                if not r.strip().startswith("|"):
                    break
                rows.append([c.strip() for c in r.strip().strip("|").split("|")])
            return rows
    return []


def build_confronto():
    f = TRASC / "lawsopp-vs-hawkrona.md"
    if not f.exists():
        return
    md = f.read_text(encoding="utf-8")
    rows = _table_rows(md, "Topic")
    fast = _table_rows(md, "If this sounds like you")
    by_topic = {r[0]: r for r in rows}
    placed = set()

    def card(r):
        placed.add(r[0])
        return (f'<article class="cmp"><h4>{esc(r[0])}</h4><div class="cmp-2">'
                f'<div class="cmp-s"><span class="badge b-sam">Sam · HawkRona</span><p>{esc(r[1])}</p></div>'
                f'<div class="cmp-i"><span class="badge b-impact">Impact · LawSopp</span><p>{esc(r[2])}</p></div>'
                f'</div><div class="cmp-p"><b>What it means in practice</b><p>{esc(r[3])}</p></div></article>')

    groups, chips = [], []
    for gid, ico, titolo, topics in TEMI:
        cards = [card(by_topic[t]) for t in topics if t in by_topic]
        if not cards:
            continue
        chips.append(f'<a class="cm-t" href="#{gid}" data-jump="{gid}"><span class="cm-ico">{ico}</span>'
                     f'<span>{titolo}<small>{len(cards)} voci</small></span></a>')
        groups.append(f'<section class="gs" ><div class="gs-h"><h2 id="{gid}">{ico} {titolo}</h2></div>'
                      f'<div class="gs-b cmp-list">{"".join(cards)}</div></section>')
    resto = [r for r in rows if r[0] not in placed]
    if resto:
        groups.append('<section class="gs"><div class="gs-h"><h2 id="altro">Altro</h2></div>'
                      f'<div class="gs-b cmp-list">{"".join(card(r) for r in resto)}</div></section>')

    sam = [r for r in fast if r[1].startswith("Sam's HawkRona") and "Impact" not in r[1]]
    imp = [r for r in fast if r[1].startswith("Impact's LawSopp")]
    other = [r for r in fast if r not in sam and r not in imp]
    li = lambda rs: "".join(f"<li>{esc(r[0])}</li>" for r in rs)
    fast_html = f"""<section class="gs"><div class="gs-h"><h2 id="fast">🎯 Fast Decision Table</h2></div><div class="gs-b">
<div class="fdt"><div class="fdt-c fdt-s"><div class="fdt-h"><span class="badge b-sam">Start with</span> Sam's HawkRona</div>
<p class="fdt-q">If this sounds like you…</p><ul>{li(sam)}</ul></div>
<div class="fdt-c fdt-i"><div class="fdt-h"><span class="badge b-impact">Start with</span> Impact's LawSopp</div>
<p class="fdt-q">If this sounds like you…</p><ul>{li(imp)}</ul></div></div>
{''.join(f'<div class="key">{esc(r[0])} → {esc(r[1])}</div>' for r in other)}
<p style="margin-top:14px"><a class="btn" href="quiz-deck.html">Fai il quiz sulla lista →</a></p>
</div></section>"""

    body = f"""<div class="hero hero-s"><div class="wrap">
<span class="badge b-sint">Documento comparativo</span>
<h1 style="margin-top:12px">LawSopp vs <em>HawkRona</em></h1>
<p class="sub">Le due versioni del mazzo messe a confronto argomento per argomento —
Law + Yasopp (Impact) contro Mihawk 6c + Perona 5c (samsansOP). Le {len(rows)} righe del documento sono
raggruppate per tema: per ognuna la posizione di Sam, quella di Impact e cosa significa in pratica.</p>
</div></div>
<section class="gpage"><div class="wrap">
<div class="agg" style="margin:0 0 16px"><b class="agg-h">🆕 Aggiornamento 17/09</b>
<p>Il documento confronta le liste di fine agosto. Nel Q&amp;A del 17/09 Impact indica tre build: la <b>tempo/Perona</b>
(la più vicina a HawkRona, 1ª al regionale, «best in the mirror»), la <b>rest-spell build</b> con 4 «Faces of Trash» e 4 Coffin Boat
(2ª al regionale, la sua scelta per il weekend) e l'<b>ibrida</b> 3 Law / 2 Hawk. La LawSopp di questa pagina è quindi la base da cui è
partita la sua build attuale, non la build attuale.
<a href="guide/impact.html#qa1709">Le tre build nel Q&amp;A →</a></p></div>
<div class="cmp-legend"><span><i class="sw" style="background:var(--sam)"></i><b>Sam · HawkRona</b> — 6c Mihawk + Perona</span>
<span><i class="sw" style="background:var(--impact)"></i><b>Impact · LawSopp</b> — Law + Yasopp</span></div>
<div class="cmap"><div class="cmap-h">Salta a un tema</div><div class="cmap-g">{''.join(chips)}
<a class="cm-t" href="#fast" data-jump="fast"><span class="cm-ico">🎯</span><span>Fast Decision Table<small>quale scegliere</small></span></a></div></div>
<div class="verb">{''.join(groups)}{fast_html}</div>
<p class="fn" style="margin-top:24px">✎ Trascrizione fedele del documento «LawSopp vs HawkRona.docx»: il testo delle celle è verbatim
(inglese); nel sito le righe della tabella sono state solo raggruppate per tema.</p>
</div></section>"""
    (ROOT / "confronto.html").write_text(
        page("LawSopp vs HawkRona — Green Mihawk OP17", "", body,
             "Le due versioni di Green Mihawk OP17 a confronto argomento per argomento."),
        encoding="utf-8")
    print(f"  confronto.html ({len(rows)} righe, {len(resto)} fuori tema)")


if __name__ == "__main__":
    build_video()
    build_carte()
    build_flat()
    build_confronto()

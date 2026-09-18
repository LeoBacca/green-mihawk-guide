# -*- coding: utf-8 -*-
"""Markdown verbatim -> HTML impaginato.

Il testo delle guide resta parola per parola: qui cambia solo COME viene mostrato,
per dare gerarchia a quello che nelle fonti sembra un unico muro di testo.

  riga tutta in grassetto, breve        -> sottotitolo (h5.ph)
  frase tutta in grassetto / MAIUSCOLO  -> punto chiave (.key)
  "**Etichetta:** testo lungo"          -> schede etichettate (.concepts)
  "**Chiave:** valore breve", "Chiave: valore" in fila -> fatti (.facts)
  lista Difficulty / Turn Order / ...   -> scheda matchup (.sheet)
  A -> B -> C                           -> schema a flusso (.flow)
  "Cost: 1 -> 25 · 2 -> 3 ..."          -> mini grafico a barre (.bars2)
  [Card: ... (ID)] con testo            -> scheda carta con immagine (.cprof)
  [Hand image: ...]                     -> mano di carte (.hand)
  **Question** | Multiple Choice        -> quiz visivo (.mq)
  **[hh:mm:ss](url)** testo             -> timeline (.tl)
  > ⚠️ Nota: ... (note del trascrittore)  -> nota discreta (.fn)
  h2 -> fascia di sezione, h3 -> pannello
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
CARTE = ROOT / "carte"
ON_DISK = {p.stem for p in CARTE.glob("*.png")} if CARTE.exists() else set()
CARD_IDS = set()

ID_RE = r"(?:OP|ST|EB|PRB)\d{2}-\d{3}"

# nome carta -> ID, solo dove il nome non e' ambiguo (o lo diventa con il costo)
_NAMES = [
    ("otama", "OP07-022"), ("kin'emon", "ST32-001"), ("kinemon", "ST32-001"),
    ("vander decken", "OP06-033"), ("kawamatsu", "OP12-023"), ("yasopp", "OP17-031"),
    ("kouzuki oden", "ST32-002"), ("kozuki oden", "ST32-002"), ("trafalgar law", "OP13-031"),
    ("law & bepo", "ST24-004"), ("electrical luna", "OP08-036"),
    ("you can be my samurai", "OP01-055"), ("billion-fold", "OP06-038"), ("billion fold", "OP06-038"),
    ("coffin boat", "OP14-039"), ("i never bother", "OP14-038"), ("for fun", "OP14-037"),
    ("kikunojo", "OP14-023"), ("jewelry bonney", "OP07-026"), ("hody jones", "OP06-035"),
    ("smoker", "OP10-030"), ("i know you're strong", "OP13-040"), ("strive to surpass", "OP14-036"),
]


def guess_id(name, cost=None):
    n = name.lower().replace("’", "'").strip()
    n = re.sub(r"\s*×\d+$", "", n)
    if n.startswith("perona"):
        return {1: "OP12-034", 5: "OP14-033"}.get(cost)
    if n.startswith("shanks"):
        return "OP17-022" if cost == 10 else None
    if n.startswith("dracule mihawk"):
        return {6: "ST32-003"}.get(cost)
    for key, cid in _NAMES:
        if n.startswith(key):
            return cid
    return None


# ------------------------------------------------------------------ inline

def card_chip(nome, cid, rel):
    cid = (cid or "").strip()
    base = re.sub(r"_p\d+$", "", cid)
    if base not in ON_DISK:
        base = guess_id(nome) or base
    if base in ON_DISK:
        CARD_IDS.add(base)
        return (f'<span class="cardchip"><img src="{rel}carte/{base}.png" alt="" loading="lazy">'
                f'{html.escape(nome)} <code>{base}</code></span>')
    code = f' <code>{html.escape(cid)}</code>' if cid and cid != "ID?" else ""
    return f'<span class="cardchip nocard">{html.escape(nome)}{code}</span>'


def inline(t, rel=""):
    """grassetto, corsivo, codice, link, carte e curve — su testo gia' escapato."""
    t = re.sub(r"\[Cards?:\s*([^\[\]]+?)\s*\(([^()\[\]]*)\)\s*\]",
               lambda m: card_chip(m.group(1), m.group(2), rel), t)
    t = re.sub(r"\[Cards?:\s*([^\[\]()]+?)\s*\]",
               lambda m: card_chip(m.group(1), "", rel), t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)",
               lambda m: f'<a href="{m.group(2).replace("_", "&#95;")}" target="_blank" '
                         f'rel="noopener">{m.group(1)}</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*([^*\n]+?)\*(?![*\w])", r"<em>\1</em>", t)
    t = re.sub(r"(?:(?<=\s)|(?<=^)|(?<=>)|(?<=\())_([^_\n/=]+?)_(?![\w])", r"<em>\1</em>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"&lt;u&gt;(.+?)&lt;/u&gt;", r"<u>\1</u>", t)
    # curve di DON: 1->3->7->10->10  -> gradini
    t = re.sub(r"(?<![\w>])(\d{1,2}(?:-&gt;\d{1,2}){2,})(?![\w-])",
               lambda m: '<span class="curve">' + "".join(
                   f"<b>{x}</b>" for x in m.group(1).split("-&gt;")) + "</span>", t)
    return t


def esc(t, rel=""):
    # &nbsp; letterali dei sottotitoli YouTube ("[&nbsp;__&nbsp;]" = parola censurata)
    return inline(html.escape(t, quote=False).replace("&amp;nbsp;", "&nbsp;"), rel)


def strip_bold(t):
    return re.sub(r"\*\*", "", t).strip()


def slug(t):
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"[^\w\s-]", "", t.lower(), flags=re.U)
    return re.sub(r"[\s_-]+", "-", t).strip("-")[:48] or "s"


# ------------------------------------------------------------ classificazione

PHASES = [
    (r"mulligan", "mull", "Mulligan"),
    (r"going (1st|first|2nd|second)|go (first|second)|first or second|die roll|turn order|dado", "turn", "Turno"),
    (r"early|1/2/3/4 don|1 to 4 don|turn 1|t1\b", "early", "Early"),
    (r"late|10 don|endgame|end game|lethal|closing|finish", "late", "Late"),
    (r"mid[ -]?game|5 to 9 don|[5-9] don|midgame", "mid", "Mid"),
]


def phase_of(text):
    t = text.lower()
    for rx, cls, lbl in PHASES:
        if re.search(rx, t):
            return cls, lbl
    return None


LEADERS = [
    (r"luffy ?(and|&|-) ?ace|ace luffy", "ST30-001"), (r"mirror|mihawk", "OP14-020"), (r"robin", "OP09-062"),
    (r"linlin|big mom|big mama", "OP17-099"), (r"boa", "OP14-041"), (r"pudding", "OP08-058"),
    (r"black luffy|bluffy|b luffy", "OP17-079"), (r"sabo|elbo", "OP13-004"), (r"\bace\b", "OP16-001"),
    (r"kaido", "OP17-058"), (r"rocks", "OP17-039"), (r"enel", "OP15-058"),
]


def leader_of(text):
    t = re.sub(r"\(as mihawk\)", "", text.lower())
    m = re.search(r"\b(?:vs\.?|versus)\s+(.*)", t)
    before = ""
    if m:
        before, t = t[:m.start()], m.group(1)
    elif re.search(r"\bmirror\b", t):
        t = "mirror"
    else:
        return None

    def find(x):
        for rx, cid in LEADERS:
            if re.search(rx, x):
                return cid
        return None
    cid = find(t)
    # "ELBAF SABO VS MIHAWK": la partita e' vista dall'altro lato, conta l'altro leader
    if cid == "OP14-020" and before and find(before) not in (None, "OP14-020"):
        cid = find(before)
    return cid if cid in ON_DISK else None


SHEET_KEYS = {"difficulty", "turn order", "mulligan", "win condition", "cards to watch out for",
              "tech cards", "macro gameplan"}

VERDICT_RX = [
    (r"very favou?red", "vf"), (r"slightly unfavou?red", "su"), (r"slightly favou?red", "sf"),
    (r"unfavou?red", "uf"), (r"favou?red", "fv"), (r"\beven\b|50-50|close to even", "ev"),
    (r"\bgood\b|chill|dies from", "fv"),
]


def verdict_cls(v):
    t = v.lower()
    for rx, c in VERDICT_RX:
        if re.search(rx, t):
            return "v-" + c
    if re.search(r"\b(second|2nd)\b", t):
        return "v-2nd"
    if re.search(r"\b(first|1st)\b", t):
        return "v-1st"
    return ""


def is_fn_note(txt):
    return txt.startswith("⚠") and "TRONCAMENTO" not in txt.upper()


def sentence_count(t):
    return len(re.findall(r"[.!?](?:\s+[A-Z\"“]|$)", t.strip()))


def is_caps(t):
    letters = re.sub(r"[^A-Za-z]", "", strip_bold(t))
    return len(letters) >= 30 and sum(c.isupper() for c in letters) / len(letters) > .85


# ---------------------------------------------------------------- 1. parsing

VIS_RX = r"^\[(Cards?|Card text|Board diagram|Decklist image|Video embed|Banner|Table|Hand image|Immagine|Flow|Tree|Columns|ILLEGGIBILE)"


def parse(md):
    """markdown -> lista di blocchi grezzi."""
    lines = md.split("\n")
    n, i, out = len(lines), 0, []
    while i < n:
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        # tabella
        if s.startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:\-|]+\|\s*$", lines[i + 1]):
            head = [c.strip() for c in s.strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append({"t": "table", "head": head, "rows": rows})
            continue
        m = re.match(r"^(#{1,5})\s+(.*)$", s)
        if m:
            out.append({"t": "h", "lvl": len(m.group(1)), "txt": m.group(2).strip()})
            i += 1
            continue
        if s.startswith(">"):
            blk = []
            while i < n and lines[i].strip().startswith(">"):
                blk.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append({"t": "quote", "lines": [x for x in blk if x], "paras": blk})
            continue
        if s == "[/Columns]":
            out.append({"t": "colend"})
            i += 1
            continue
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", s):
            out.append({"t": "hr"})
            i += 1
            continue
        # marcatore visivo (anche su piu' righe, fino alla ] di chiusura)
        s2 = re.sub(r"^\*\*(\[.*\])\*\*$", r"\1", s)
        if re.match(VIS_RX, s2):
            blk, j = [s2], i
            depth = s2.count("[") - s2.count("]")
            while depth > 0 and j + 1 < n and (lines[j + 1].strip() or depth > 0):
                j += 1
                ln = lines[j].strip()
                if not ln and j + 1 < n and not lines[j + 1].strip():
                    break
                blk.append(ln)
                depth += ln.count("[") - ln.count("]")
            m = re.match(r"^\[(?:(ILLEGGIBILE)\]|([A-Za-z ]+?):\s*(.*)\])\s*$", "\n".join(blk), re.S)
            if m:
                out.append({"t": "vis", "kind": (m.group(1) or m.group(2)).strip(),
                            "body": (m.group(3) or "").strip()})
                i = j + 1
                continue
        # lista
        if re.match(r"^([-*+]|\d+[.)])\s+", s):
            ordered = bool(re.match(r"^\d+[.)]\s+", s))
            items, lv = [], []
            while i < n and re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[i]):
                ind = len(lines[i]) - len(lines[i].lstrip())
                lv.append(0 if ind < 2 else (1 if ind < 5 else 2))
                items.append(re.sub(r"^\s*([-*+]|\d+[.)])\s+", "", lines[i]).strip())
                i += 1
                while i < n and lines[i].startswith("   ") and lines[i].strip() \
                        and not re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[i]):
                    items[-1] += " " + lines[i].strip()
                    i += 1
            out.append({"t": "ol" if ordered else "ul", "items": items, "lv": lv})
            continue
        # paragrafo
        para = [s]
        i += 1
        while i < n and lines[i].strip() and not re.match(
                r"^\s*(#{1,5}\s|[-*+]\s|\d+[.)]\s|>|\||\[(Card|Cards|Board|Video|Banner|Table|Decklist|Hand|Immagine)|-{3,}|\*\*\[\d)",
                lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append({"t": "p", "txt": " ".join(para)})
    return out


# ---------------------------------------------------------- 2. arricchimento

FACT_BOLD = re.compile(r"\*\*([^*]{2,40}?):\*\*\s*([^*]*?)(?=\s*\*\*[^*]{2,40}?:\*\*|$)")
FACT_PLAIN = re.compile(r"^([A-Za-z0-9][\w .'/&-]{0,22}):\s+(\S.{0,70})$")
CONCEPT = re.compile(r"^\*\*([^*]{2,70}?)([:;]?)\*\*([:;]?)\s+(.+)$", re.S)
LABELED = re.compile(r"^\*\*([^*]{2,60}?)(?:[:;]\*\*|\*\*[:;]|\*\*(?=\s+—))\s*(.+)$", re.S)
TS = re.compile(r"^\*\*\[(\d\d:\d\d:\d\d)\]\((https?://[^)]+)\)\*\*\s*(.*)$", re.S)
STATS = re.compile(r"^\*\*([A-Za-z ]{2,14}):\*\*\s*((?:[\w]+ → \d+(?: · )?){2,})$")


def classify_p(txt):
    s = txt.strip()
    m = TS.match(s)
    if m:
        return {"t": "ts", "time": m.group(1), "url": m.group(2), "txt": m.group(3)}
    m = re.match(r"^\*\*([QA])\*\*\s+(.+)$", s, re.S)
    if m:
        return {"t": "qa_" + m.group(1).lower(), "txt": m.group(2)}
    m = STATS.match(s)
    if m:
        pairs = [tuple(x.split(" → ")) for x in m.group(2).split(" · ") if " → " in x]
        return {"t": "stats", "lbl": m.group(1), "pairs": pairs}
    if re.match(r"^\*\*Question\*\*\s*\|", s):
        return {"t": "qhead", "txt": s}
    if s in ("Reset", "Check answer"):
        return {"t": "qbtn", "txt": s}
    if (re.match(r"^—\s", s) and len(s) < 60) or re.match(r"^\*[^*]{2,40}\*$", s) \
            or re.match(r"^Continue to next page", s) or s in ("Main Section", "To Follow"):
        return {"t": "crumb", "txt": s}
    # catena A -> B -> C  (anche piu' catene separate dai "****" letterali della fonte)
    all_bold = bool(re.match(r"^\*\*.*\*\*$", s))
    if s.count("→") >= 1 and len(strip_bold(s)) < 260 and (all_bold or s.count("→") >= 2):
        segs = [strip_bold(x).rstrip(".") for x in s.split("****") if strip_bold(x)]
        flows, pend = [], ""
        for sg in segs:
            if "→" not in sg:
                pend = sg.rstrip(":")
                continue
            lm = re.match(r"^([^→:]{2,30}):\s*(.+)$", sg)
            lab, chain = (lm.group(1), lm.group(2)) if lm else (pend, sg)
            steps = [x.strip() for x in chain.split("→")]
            if not (len(steps) >= (2 if all_bold else 3) and all(0 < len(x) <= 60 for x in steps)):
                flows = None
                break
            flows.append({"lbl": lab, "steps": steps})
            pend = ""
        if flows and not pend:
            return {"t": "flow", "flows": flows, "raw": s}
    # riga tutta in grassetto
    m = re.match(r"^\*\*([^*]+)\*\*$", s)
    if m:
        inner = m.group(1).strip()
        if len(inner) <= 64 and not inner.startswith(("\"", "“", "«")) and not inner.endswith("?\""):
            return {"t": "ph", "txt": inner}
        return {"t": "key", "txt": inner}
    if is_caps(s) and len(s) > 40:
        return {"t": "key", "txt": s}
    # fatti in grassetto: "**Die roll:** Second **Default game plan:** Value / Control"
    if s.startswith("**"):
        facts = FACT_BOLD.findall(s)
        if facts and "".join(f"**{k}:** {v}" for k, v in facts).replace(" ", "") == s.replace(" ", "") \
                and all(len(v) <= 90 for _, v in facts):
            return {"t": "facts", "items": [(k.strip(), v.strip().rstrip("·").strip()) for k, v in facts]}
        m = CONCEPT.match(s)
        if m and (m.group(2) or m.group(3)) and "**" not in m.group(4)[:3]:
            return {"t": "concept", "lbl": m.group(1).strip(), "txt": m.group(4).strip()}
    m = FACT_PLAIN.match(s)
    if m and len(m.group(1).split()) <= 4 and not re.search(r"[.!?]$", m.group(1)):
        return {"t": "pfact", "k": m.group(1), "v": m.group(2), "raw": s}
    return {"t": "p", "txt": s}


def enrich(blocks):
    # 1) paragrafi spezzati da un cambio pagina della cattura: si riuniscono
    merged = []
    for b in blocks:
        if b["t"] == "p" and merged and merged[-1]["t"] == "p":
            prev = merged[-1]["txt"]
            if not re.search(r"[.!?:\"”)\]*…]$", prev) and re.match(r"^[a-z(]", b["txt"]):
                merged[-1] = {"t": "p", "txt": prev + " " + b["txt"]}
                continue
        merged.append(b)

    # 2) classificazione dei paragrafi
    out = [classify_p(b["txt"]) if b["t"] == "p" else b for b in merged]

    # 3) "Chiave: valore" isolati non sono fatti: tornano paragrafi
    res = []
    i = 0
    while i < len(out):
        b = out[i]
        if b["t"] == "pfact":
            j = i
            while j < len(out) and out[j]["t"] == "pfact":
                j += 1
            if j - i >= 2:
                res.append({"t": "facts", "items": [(x["k"], x["v"]) for x in out[i:j]]})
            else:
                res.append({"t": "p", "txt": b["raw"]})
            i = j
            continue
        res.append(b)
        i += 1
    out = res

    # 4) raggruppamenti
    def is_caption(x):
        return x["t"] in ("p", "crumb") and re.match(r"^\*[^*].*\*$", x["txt"].strip(), re.S)

    def box_tail(j, box):
        if j < len(out) and is_caption(out[j]):
            box["cap"] = out[j]["txt"].strip()[1:-1]
            j += 1
        return j

    res = []
    i = 0
    while i < len(out):
        b = out[i]
        t = b["t"]
        # riquadri dei PDF: schema a passi, albero di decisione, colonne a confronto
        if t == "vis" and b["kind"] == "Flow" and i + 1 < len(out) and out[i + 1]["t"] in ("ol", "ul"):
            box = {"t": "flowbox", "title": b["body"], "steps": out[i + 1]["items"], "cap": None}
            i = box_tail(i + 2, box)
            res.append(box)
            continue
        if t == "vis" and b["kind"] == "Tree":
            box = {"t": "treebox", "title": b["body"], "root": "", "branches": [], "cap": None}
            j = i + 1
            if j < len(out) and out[j]["t"] in ("p", "ph", "key"):
                box["root"] = out[j]["txt"] if out[j]["t"] == "p" else f"**{out[j]['txt']}**"
                j += 1
            if j < len(out) and out[j]["t"] in ("ul", "ol"):
                box["branches"] = out[j]["items"]
                j += 1
            i = box_tail(j, box)
            res.append(box)
            continue
        if t == "vis" and b["kind"] == "Columns":
            cols, j = [], i + 1
            while j < len(out) and out[j]["t"] != "colend":
                x = out[j]
                if x["t"] == "h":
                    cols.append({"h": x["txt"], "items": []})
                elif x["t"] in ("ul", "ol") and cols:
                    cols[-1]["items"] += x["items"]
                j += 1
            res.append({"t": "colbox", "title": b["body"], "cols": cols})
            i = j + 1
            continue
        # domande e risposte
        if t in ("qa_q", "qa_a"):
            if not (res and res[-1]["t"] == "qa"):
                res.append({"t": "qa", "items": []})
            if t == "qa_q" or not res[-1]["items"] or res[-1]["items"][-1][1] is not None:
                res[-1]["items"].append([b["txt"] if t == "qa_q" else "", None])
            if t == "qa_a":
                res[-1]["items"][-1][1] = b["txt"]
            i += 1
            continue
        # fatti consecutivi -> una sola striscia
        if t == "facts" and res and res[-1]["t"] == "facts":
            res[-1]["items"] += b["items"]
        # concetti consecutivi -> un blocco di schede
        elif t == "concept":
            if res and res[-1]["t"] == "concepts":
                res[-1]["items"].append(b)
            else:
                res.append({"t": "concepts", "items": [b]})
        # timeline
        elif t == "ts":
            if res and res[-1]["t"] == "tl":
                res[-1]["items"].append(b)
            else:
                res.append({"t": "tl", "items": [b]})
        # quiz di mulligan
        elif t == "qhead":
            q = {"t": "quiz", "kind": strip_bold(b["txt"]).replace("|", "·"), "hand": None,
                 "q": "", "opts": [], "notes": []}
            if res and res[-1]["t"] == "vis" and res[-1]["kind"] == "Hand image":
                q["hand"] = res.pop()["body"]
            j = i + 1
            if j < len(out) and out[j]["t"] in ("ph", "key", "p"):
                q["q"] = out[j]["txt"]
                j += 1
            if j < len(out) and out[j]["t"] in ("ul", "ol"):
                q["opts"] = out[j]["items"]
                j += 1
            while j < len(out) and (out[j]["t"] == "qbtn" or (
                    out[j]["t"] == "quote" and "risposta" in " ".join(out[j]["lines"]))):
                if out[j]["t"] == "quote":
                    q["notes"].append(" ".join(out[j]["lines"]))
                j += 1
            res.append(q)
            i = j
            continue
        elif t == "qbtn":
            pass
        # frase che termina con ":" seguita da frasi brevi -> elenco
        elif t == "p" and b["txt"].endswith(":") and len(b["txt"]) < 220:
            j = i + 1
            items = []
            while j < len(out) and out[j]["t"] == "p" and len(out[j]["txt"]) <= 170 \
                    and sentence_count(out[j]["txt"]) <= 1 and not out[j]["txt"].endswith(":"):
                items.append(out[j]["txt"])
                j += 1
            if len(items) >= 2:
                res.append({"t": "lead", "txt": b["txt"]})
                res.append({"t": "ul", "items": items, "soft": True})
                i = j
                continue
            res.append(b)
        # scheda matchup (lista Difficulty / Turn Order / ...)
        elif t == "ul" and sum(1 for x in b["items"] if (m := LABELED.match(x))
                               and m.group(1).strip().lower() in SHEET_KEYS) >= 3:
            res.append({"t": "sheet", "items": b["items"]})
        # carta semplice seguita dal suo testo -> scheda carta
        elif t in ("quote", "vis") and res and res[-1]["t"] == "vis" and res[-1]["kind"] in ("Card", "Cards") \
                and not res[-1].get("eff") and len(re.findall(ID_RE, res[-1]["body"])) == 1 and (
                    (t == "quote" and not b["lines"][0].startswith("⚠")) or (t == "vis" and b["kind"] == "Card text")):
            res[-1]["eff"] = b["lines"] if t == "quote" else [b["body"]]
        else:
            res.append(b)
        i += 1
    return res


# -------------------------------------------------------------- 3. rendering

def r_card(body, rel, eff=None):
    ids = re.findall(ID_RE, body)
    desc_len = len(re.sub(r"\(" + ID_RE + r"\)", "", body))
    # una sola carta con descrizione / effetto -> scheda
    if len(ids) == 1 and (eff or desc_len > 48):
        cid = ids[0]
        name = re.split(r"\s+—\s+|\s*\(", body, 1)[0].strip()
        rest = body[len(name):]
        rest = re.sub(r"\s*\(" + cid + r"\)(\.?)\s*",
                      lambda m: " · " if m.end() < len(rest) else "", rest, 1).strip()
        rest = re.sub(r"^[\s·—]+", "", rest)
        img = ""
        if cid in ON_DISK:
            CARD_IDS.add(cid)
            img = (f'<a class="cp-img" href="{rel}carte/{cid}.png" target="_blank" rel="noopener">'
                   f'<img src="{rel}carte/{cid}.png" alt="{html.escape(name)}" loading="lazy"></a>')
        effs = "".join(f'<div class="cp-eff">{esc(e, rel)}</div>' for e in (eff or []))
        return (f'<div class="cprof">{img}<div class="cp-body"><div class="cp-name">{esc(name, rel)} '
                f'<code>{cid}</code></div>{f"<div class=cp-meta>{esc(rest, rel)}</div>" if rest else ""}'
                f'{effs}</div></div>')
    chips = []
    for piece in re.split(r"\s*(?:,|·)\s*(?![^()]*\))", body):
        cm = re.match(r"(.+?)\s*\(([^)]*)\)\s*$", piece.strip())
        if cm:
            chips.append(card_chip(cm.group(1), cm.group(2), rel))
        elif piece.strip():
            chips.append(card_chip(piece.strip(), "", rel))
    return '<div class="cardrow">' + "".join(chips) + "</div>"


def r_hand(body, rel):
    m = re.match(r"^(\d+)\s*cards?\s*—\s*(.*)$", body, re.S)
    count, items = (m.group(1), m.group(2)) if m else ("", body)
    cards = []
    for piece in items.split(" · "):
        pm = re.match(r"^(.+?)(?:\s*×(\d+))?\s*\((.*)\)\s*$", piece.strip())
        if not pm:
            continue
        name, mult, info = pm.group(1), pm.group(2), pm.group(3)
        cm = re.search(r"cost (\d+)", info)
        cost = int(cm.group(1)) if cm else None
        cid = guess_id(name, cost)
        img = (f'<img src="{rel}carte/{cid}.png" alt="" loading="lazy">' if cid in ON_DISK
               else f'<span class="hc-ph">{html.escape(name)}</span>')
        if cid in ON_DISK:
            CARD_IDS.add(cid)
        badge = f'<i class="hc-x">×{mult}</i>' if mult else ""
        cards.append(f'<figure class="hc">{img}{badge}<figcaption>{html.escape(name)}'
                     f'{f" <small>{cost}c</small>" if cost is not None else ""}</figcaption></figure>')
    lbl = f"Mano di {count} carte" if count else "Carte in mano"
    return f'<div class="hand" title="{html.escape(body, quote=True)}"><div class="hand-l">✋ {lbl}</div><div class="hand-c">{"".join(cards)}</div></div>'


def r_quiz(b, rel):
    hand = r_hand(b["hand"], rel) if b["hand"] else ""
    opts = []
    for o in b["opts"]:
        ok = "✅" in o
        o = re.sub(r"✅\s*", "", o)
        o = re.sub(r"\s*\*\(risposta evidenziata[^)]*\)\*", "", o)
        opts.append(f'<button type="button" class="mq-o{" ok" if ok else ""}">'
                    f'{"<i>✓ </i>" if ok else ""}{esc(o, rel)}</button>')
    clean = [re.sub(r"^⚠️?\s*", "", x) for x in b["notes"]]
    notes = "".join(f'<div class="fn">✎ {esc(x, rel)}</div>' for x in clean)
    has_ok = any("✅" in o for o in b["opts"])
    hint = ('<span class="mq-h">Scegli la tua risposta, poi confrontala con quella dell\'autore</span>'
            if has_ok else "")
    return (f'<div class="mq{" play" if has_ok else ""}"><div class="mq-k">🎯 {html.escape(b["kind"])}</div>{hand}'
            f'<div class="mq-q">{esc(strip_bold(b["q"]), rel)}</div>'
            f'<div class="mq-opts">{"".join(opts)}</div>{hint}{notes}</div>')


def r_sheet(items, rel):
    top, rows = [], []
    for it in items:
        m = LABELED.match(it)
        if not m:
            rows.append(f'<div class="sh-row"><div class="sh-v">{esc(it, rel)}</div></div>')
            continue
        k, v = m.group(1).strip(), m.group(2).strip()
        if k.lower() in ("difficulty", "turn order"):
            first = re.split(r"[,.;]", v, 1)[0]
            top.append(f'<div class="sh-tile {verdict_cls(first)}"><span class="sh-k">{html.escape(k)}</span>'
                       f'<b>{esc(first, rel)}</b><span class="sh-rest">{esc(v[len(first):].lstrip(",.; "), rel)}</span></div>')
        else:
            rows.append(f'<div class="sh-row"><div class="sh-k">{html.escape(k)}</div><div class="sh-v">{esc(v, rel)}</div></div>')
    return (f'<div class="sheet"><div class="sheet-h">Scheda del matchup</div>'
            f'<div class="sh-top">{"".join(top)}</div>{"".join(rows)}</div>')


def r_facts(items, rel):
    cells = "".join(
        f'<div class="fact {verdict_cls(v)}"><span class="fk">{esc(k, rel)}</span><span class="fv">{esc(v, rel)}</span></div>'
        for k, v in items)
    return f'<div class="facts">{cells}</div>'


def r_list(b, rel):
    tag = "ol" if b["t"] == "ol" else "ul"
    lv = b.get("lv") or [0] * len(b["items"])
    cls = ' class="soft"' if b.get("soft") else ""
    out, depth = [f"<{tag}{cls}>"], 0
    for k, (it, level) in enumerate(zip(b["items"], lv)):
        level = min(level, depth + 1)
        if k and level > depth:              # sotto-elenco dentro la voce precedente
            out.append('<ul class="sub">')
            depth = level
        elif k:
            out.append("</li>")
            while depth > level:
                out.append("</ul></li>")
                depth -= 1
        m = LABELED.match(it)
        if m and len(m.group(2)) > 25:
            out.append(f'<li class="lab"><span class="lbl">{esc(m.group(1).strip(), rel)}</span>{esc(m.group(2), rel)}')
        else:
            out.append(f"<li>{esc(it, rel)}")
    if b["items"]:
        out.append("</li>")
    while depth > 0:
        out.append("</ul></li>")
        depth -= 1
    return "".join(out) + f"</{tag}>"


def _title_sub(it):
    """«**Titolo** — sottotitolo» -> (titolo, sottotitolo)"""
    m = re.match(r"^\*\*(.+?)\*\*\s*(?:—\s*(.*))?$", it.strip(), re.S)
    if m:
        return m.group(1), (m.group(2) or "")
    return it, ""


def r_flowbox(b, rel):
    steps = []
    for it in b["steps"]:
        tt, sub = _title_sub(it)
        steps.append(f'<li><b>{esc(tt, rel)}</b>{f"<span>{esc(sub, rel)}</span>" if sub else ""}</li>')
    cap = f'<p class="bx-cap">{esc(b["cap"], rel)}</p>' if b.get("cap") else ""
    return (f'<div class="bx"><div class="bx-h">{esc(b["title"], rel)}</div>'
            f'<ol class="fsteps">{"".join(steps)}</ol>{cap}</div>')


def r_treebox(b, rel):
    rt, rsub = _title_sub(b["root"]) if b["root"] else ("", "")
    br = []
    for it in b["branches"]:
        tt, sub = _title_sub(it)
        # «condizione → esito»: l'esito e' la risposta, va in evidenza
        cond, _, esito = tt.rpartition(" → ")
        head = (f'{esc(cond, rel)} <i class="tr-ar">→</i> <em class="tr-out">{esc(esito, rel)}</em>'
                if cond else f'<em class="tr-out">{esc(tt, rel)}</em>')
        br.append(f'<li><div class="tr-b">{head}</div>{f"<span>{esc(sub, rel)}</span>" if sub else ""}</li>')
    root = (f'<div class="tr-root"><b>{esc(rt, rel)}</b>{f"<span>{esc(rsub, rel)}</span>" if rsub else ""}</div>'
            if rt else "")
    cap = f'<p class="bx-cap">{esc(b["cap"], rel)}</p>' if b.get("cap") else ""
    return (f'<div class="bx"><div class="bx-h">{esc(b["title"], rel)}</div>{root}'
            f'<ul class="tr">{"".join(br)}</ul>{cap}</div>')


def r_colbox(b, rel):
    cols = "".join(
        f'<div class="bx-col"><h5>{esc(c["h"], rel)}</h5><ul>'
        + "".join(f"<li>{esc(x, rel)}</li>" for x in c["items"]) + "</ul></div>"
        for c in b["cols"])
    return (f'<div class="bx"><div class="bx-h">{esc(b["title"], rel)}</div>'
            f'<div class="bx-cols n{len(b["cols"])}">{cols}</div></div>')


def r_qa(b, rel):
    rows = "".join(
        f'<div class="qa-i"><div class="qa-q"><i>Q</i><span>{esc(q, rel)}</span></div>'
        + (f'<div class="qa-a"><i>A</i><span>{esc(a, rel)}</span></div>' if a else "") + "</div>"
        for q, a in b["items"])
    return f'<div class="qa">{rows}</div>'


def r_table(b, rel):
    th = "".join(f"<th>{esc(c, rel)}</th>" for c in b["head"])
    tb = "".join("<tr>" + "".join(f"<td>{esc(c, rel).replace('&lt;br&gt;', '<br>')}</td>" for c in r) + "</tr>"
                 for r in b["rows"])
    return f'<div class="tscroll"><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>'


def r_stats(b):
    mx = max(int(v) for _, v in b["pairs"]) or 1
    bars = "".join(f'<div class="b2"><span class="b2k">{html.escape(k)}</span><span class="b2t">'
                   f'<i style="width:{int(v) / mx * 100:.0f}%"></i></span><span class="b2v">{v}</span></div>'
                   for k, v in b["pairs"])
    return f'<div class="bars2"><div class="b2l">{html.escape(b["lbl"])}</div>{bars}</div>'


def r_figure(path, rel, caption, desc_html=""):
    fig = (f'<figure class="gfig"><a href="{rel}{path}" target="_blank" rel="noopener">'
           f'<img src="{rel}{path}" alt="{html.escape(caption)}" loading="lazy"></a>'
           f'<figcaption>{html.escape(caption)}</figcaption></figure>')
    if desc_html:
        fig += f'<details class="imgdesc"><summary>Trascrizione dell\'immagine</summary>{desc_html}</details>'
    return fig


def r_visual(b, rel, figs):
    kind, body = b["kind"], b["body"]
    fig = None
    for rx, paths in figs:
        if paths and re.search(rx, body):
            fig = paths.pop(0)
            break
    desc = None
    if kind in ("Card", "Cards"):
        return r_card(body, rel, b.get("eff"))
    if kind == "Card text":
        return f'<div class="cp-eff solo">{esc(body, rel)}</div>'
    if kind == "Hand image":
        return r_hand(body, rel)
    if kind == "Video embed":
        return (f'<div class="vid"><span class="ic">▶</span><span>Video nella guida: '
                f'<b>{esc(body, rel)}</b></span></div>')
    if kind == "ILLEGGIBILE":
        return '<p class="fn">✎ [porzione illeggibile nello screenshot della fonte]</p>'
    if kind == "Banner":
        desc = f'<p class="banner">🖼 {esc(body, rel)}</p>'
        if fig:
            return r_figure(fig, rel, "Immagine originale dalla guida", desc)
        return desc
    if kind == "Table":
        lab = f'<p class="tlabel">▦ {esc(body, rel)}</p>'
        return (r_figure(fig, rel, "L'immagine originale dalla guida") + lab) if fig else lab
    # Board diagram / Decklist image / Immagine
    lbl = {"Board diagram": "Board", "Decklist image": "Decklist", "Immagine": "Immagine"}.get(kind, kind)
    txt = body.replace("\n", " \n")
    parts = [x for x in txt.split("\n")]
    inner = esc(parts[0], rel) + ("".join(
        f"<br>{esc(x.strip(), rel)}" for x in parts[1:] if x.strip()) if len(parts) > 1 else "")
    boxed = f'<div class="board"><b>{lbl}</b>{inner}</div>'
    if fig:
        return r_figure(fig, rel, f"{lbl} — immagine originale dalla guida", boxed)
    return boxed


def r_quote(lines, rel, paras=None):
    txt = " ".join(lines)
    if "TRONCAMENTO" in txt.upper():
        return f'<div class="note trunc">{esc(txt, rel)}</div>'
    if is_fn_note(txt):
        body = re.sub(r"^⚠️?\s*(\*\*)?Nota(\*\*)?:?\s*", "", txt)
        return f'<div class="fn" title="Nota del trascrittore">✎ <span>{esc(body, rel)}</span></div>'
    if paras and "" in paras:
        ps, cur = [], []
        for x in paras + [""]:
            if x:
                cur.append(x)
            elif cur:
                ps.append(" ".join(cur))
                cur = []
        return '<div class="note multi">' + "".join(f"<p>{esc(x, rel)}</p>" for x in ps) + "</div>"
    return f'<div class="note">{esc(txt, rel)}</div>'


def render(md, rel="", figs=None, wrap=True):
    """-> (html, headings[(lvl, id, testo, leader)])"""
    figs = [(rx, list(p)) for rx, p in (figs or [])]
    blocks = enrich(parse(md))
    # le tabelle "CARTE CITATE" sono un indice del trascrittore: finivano in mezzo a un
    # matchup (cucitura delle strisce) -> in appendice richiudibile a fine capitolo
    appendix, k = [], 0
    while k < len(blocks):
        b = blocks[k]
        if b["t"] == "h" and strip_bold(b["txt"]).upper() == "CARTE CITATE":
            j = k + 1
            while j < len(blocks) and blocks[j]["t"] in ("table", "quote"):
                appendix.append(blocks[j])
                j += 1
            del blocks[k:j]
            continue
        k += 1
    out, heads, used = [], [], {}
    state = {"sec": False, "pan": False}

    def uid(t):
        s = slug(t)
        used[s] = used.get(s, 0) + 1
        return s if used[s] == 1 else f"{s}-{used[s]}"

    def close_pan():
        if state["pan"]:
            out.append("</div>")
            state["pan"] = False

    def close_sec():
        close_pan()
        if state["sec"]:
            out.append("</div></section>")
            state["sec"] = False

    tl_last = [None]
    for b in blocks:
        t = b["t"]
        if t == "h":
            txt = b["txt"]
            lvl = b["lvl"]
            ph = phase_of(txt)
            tag = f'<span class="phase ph-{ph[0]}">{ph[1]}</span>' if ph else ""
            if lvl == 1:
                out.append(f'<div class="doc-t">{esc(txt, rel)}</div>')
                continue
            if lvl == 2 and wrap:
                close_sec()
                hid = uid(txt)
                ld = leader_of(txt)
                heads.append((2, hid, re.sub(r"\*", "", txt), ld))
                img = f'<img src="{rel}carte/{ld}.png" alt="" loading="lazy">' if ld else ""
                out.append(f'<section class="gs{" mu" if ld else ""}"><div class="gs-h">{img}'
                           f'<h2 id="{hid}" data-t="{html.escape(strip_bold(txt))}">{esc(txt, rel)}</h2></div><div class="gs-b">')
                state["sec"] = True
                continue
            if lvl == 3 and wrap:
                close_pan()
                hid = uid(txt)
                heads.append((3, hid, re.sub(r"\*", "", txt), None))
                ld = leader_of(txt) if re.match(r"^\s*vs\b", txt, re.I) else None
                img = f'<img class="h3-ld" src="{rel}carte/{ld}.png" alt="" loading="lazy">' if ld else ""
                out.append(f'<div class="pan{" mu" if ld else ""}"><h3 id="{hid}" data-t="{html.escape(strip_bold(txt))}">'
                           f'{img}{tag}{esc(txt, rel)}</h3>')
                state["pan"] = True
                continue
            hl = min(lvl, 5)
            out.append(f'<h{hl}>{tag}{esc(txt, rel)}</h{hl}>')
        elif t == "p":
            out.append(f"<p>{esc(b['txt'], rel)}</p>")
        elif t == "ph":
            ph = phase_of(b["txt"])
            tag = f'<span class="phase ph-{ph[0]}">{ph[1]}</span>' if ph else ""
            cm = re.search(ID_RE, b["txt"])
            img = ""
            if cm and cm.group(0) in ON_DISK:
                CARD_IDS.add(cm.group(0))
                img = f'<img src="{rel}carte/{cm.group(0)}.png" alt="" loading="lazy">'
            out.append(f'<h5 class="ph{" withcard" if img else ""}">{img}{tag}<span>{esc(b["txt"], rel)}</span></h5>')
        elif t == "key":
            out.append(f'<div class="key">{esc(b["txt"], rel)}</div>')
        elif t == "lead":
            out.append(f'<p class="leadin">{esc(b["txt"], rel)}</p>')
        elif t == "crumb":
            out.append(f'<div class="crumb">{esc(b["txt"], rel)}</div>')
        elif t == "flow":
            for f in b["flows"]:
                lab = f'<span class="fl-l">{esc(f["lbl"], rel)}</span>' if f["lbl"] else ""
                steps = "".join(f"<li>{esc(x, rel)}</li>" for x in f["steps"])
                out.append(f'<div class="flow">{lab}<ol>{steps}</ol></div>')
        elif t == "facts":
            out.append(r_facts(b["items"], rel))
        elif t == "sheet":
            out.append(r_sheet(b["items"], rel))
        elif t == "concepts":
            cc = "".join(f'<div class="cc"><div class="cc-l">{esc(x["lbl"], rel)}</div>'
                         f'<div class="cc-t">{esc(x["txt"], rel)}</div></div>' for x in b["items"])
            out.append(f'<div class="concepts">{cc}</div>')
        elif t == "flowbox":
            out.append(r_flowbox(b, rel))
        elif t == "treebox":
            out.append(r_treebox(b, rel))
        elif t == "colbox":
            out.append(r_colbox(b, rel))
        elif t == "qa":
            out.append(r_qa(b, rel))
        elif t == "colend":
            pass
        elif t == "stats":
            out.append(r_stats(b))
        elif t == "quiz":
            out.append(r_quiz(b, rel))
        elif t == "tl":
            rows = []
            for x in b["items"]:
                h, mnt = int(x["time"][:2]), int(x["time"][3:5])
                bucket = (h * 60 + mnt) // 10
                if bucket != tl_last[0]:
                    tl_last[0] = bucket
                    rows.append(f'<div class="tl-mark" id="t{bucket * 10}" data-m="{bucket * 10}">'
                                f'{bucket * 10 // 60}h{bucket * 10 % 60:02d}′</div>')
                rows.append(f'<div class="tl-r"><a class="tl-t" href="{x["url"]}" target="_blank" rel="noopener">'
                            f'▶ {x["time"]}</a><div class="tl-x">{esc(x["txt"], rel)}</div></div>')
            out.append(f'<div class="tl">{"".join(rows)}</div>')
        elif t in ("ul", "ol"):
            out.append(r_list(b, rel))
        elif t == "quote":
            out.append(r_quote(b["lines"], rel, b.get("paras")))
        elif t == "table":
            out.append(r_table(b, rel))
        elif t == "hr":
            out.append('<hr class="div">')
        elif t == "vis":
            out.append(r_visual(b, rel, figs))
        elif t == "qbtn":
            pass
    close_sec()
    if appendix:
        inner = "".join(r_table(x, rel) if x["t"] == "table" else r_quote(x["lines"], rel) for x in appendix)
        out.append(f'<details class="appx"><summary>🗂 Carte citate nel capitolo '
                   f'<span>indice del trascrittore</span></summary>{inner}</details>')
    return "\n".join(out), heads


def md2html(md, rel="", figs=None):
    return render(md, rel, figs)[0]


def chapter_map(heads, rel):
    """Griglia-indice in testa ai capitoli con molte sezioni."""
    h2 = [h for h in heads if h[0] == 2]
    if len(h2) < 3:
        return ""
    tiles = []
    for _, hid, txt, ld in h2:
        img = f'<img src="{rel}carte/{ld}.png" alt="" loading="lazy">' if ld else '<span class="cm-n"></span>'
        tiles.append(f'<a class="cm-t" href="#{hid}" data-jump="{hid}">{img}<span>{html.escape(txt)}</span></a>')
    return (f'<div class="cmap"><div class="cmap-h">In questo capitolo · {len(h2)} sezioni</div>'
            f'<div class="cmap-g">{"".join(tiles)}</div></div>')

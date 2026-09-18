# -*- coding: utf-8 -*-
"""Controlla che ogni frase di '## _hl' in sintesi/<autore>/*.md esista identica nella trascrizione."""
import glob, os, re, sys
from render import load_sintesi
bad = 0
for f in sorted(glob.glob("sintesi/*/*.md")):
    autore, slug = f.replace("\\", "/").split("/")[1], os.path.basename(f)[:-3]
    md = re.sub(r"\s+", " ", open(f"trascrizioni/{autore}/{slug}.md", encoding="utf-8").read())
    hl = load_sintesi(f).get("_hl", [])
    for ph in hl:
        if ph not in md or ph.count("**") % 2:
            bad += 1
            print(f"[NON TROVATA] {slug}: {ph[:90]}")
    print(f"{slug}: {len(hl)} frasi")
sys.exit(1 if bad else 0)

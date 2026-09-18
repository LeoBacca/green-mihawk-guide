# Green Mihawk OP17 — hub delle guide

Sito che raccoglie **cinque guide a Green Mihawk in OP17** in un posto solo: il testo integrale di ognuna,
più le sezioni che una guida singola non può darti — i matchup incrociati fra tutte le fonti, una sezione
dedicata al mirror e due quiz.

🔗 **[Apri il sito](https://leobacca.github.io/green-mihawk-guide/)**

## Le fonti

| Autore | Cosa contiene | Versione del mazzo |
|---|---|---|
| **Raphterra** — *OP17 Mihawk Ultimate Guide* (Metafy) | 6 capitoli: intro, deck core e deckbuilding, fondamentali, meta OP17, matchup vs meta e vs field. 4 sample build, 4 cheat sheet, 23 video | 6c Law / ibrida |
| **Rondino** (Metafy) | 5 capitoli, di cui la «matchups bible» è il cuore: è la fonte della **strategia di starving** | 6c Law |
| **NebulusTCG** (Metafy) | 16 capitoli: tech card, probabilità di pesca, gestione del loop, MU spread e **guide dedicate ai mazzi gialli** | 6c Law, 4 Coffin Boat |
| **Impact** — *Why is 10c Shanks So Broken? Srsly* | PowerPoint da 34 slide + video-lezione da 2h08 con appunti e confronto video↔note | **Law + Yasopp** |
| **samsansOP** — *OP17 Mihawk Deep Dive* | Video da 2h + note ordinate + confronto video↔note | **Mihawk 6c + Perona 5c** |
| **Rondino** — masterclass 16/09 (Dog of Wisdom) | Session notes (PDF, 6 pagine): game tree, lista senza Bonney e Perona 5c, starve vs race, 6 matchup | 3 rest spell |
| **Impact** — Deep Dive Q&A 17/09 (The Dojo) | Session notes (PDF, 20 pagine) + note ufficiali del Dojo: le tre build, 7 matchup, 27 Q&A | **rest spell** (4 Faces of Trash) |
| **The Dojo** — «The Codex» | Sessioni della Training Library: VOD review vs Robin (9/09), ladder di Elijah (3/09), VOD review con Equinby (27/08) | Law+Yasopp / Mihawk+Perona |

> Nota sulle fonti Dojo: `fonti/Dojo/Qand and A Pre-FINALS !.txt` coincide (98%) con la sessione 1 del Codex ed è
> integrato una volta sola; le sessioni 4 e 5 del Codex coincidono con gli appunti del video di Impact e con le note di
> samsansOP, già nel sito.

## Struttura del sito

```
index.html              home
quiz-player.html        quiz «che tipo di giocatore sei» → a quale autore assomigli
quiz-deck.html          quiz «come buildare il tuo mazzo» → quale lista reale fa per te,
                        con la domanda a scelta multipla sui matchup che soffri tu (→ tech consigliate)
matchup.html            aggregatore: 12 matchup, verdetto di ogni fonte, accordi e conflitti
mirror.html             il mirror match fase per fase, 4 fonti a confronto
confronto.html          LawSopp vs HawkRona (le due versioni del mazzo)
video.html              25 video divisi per argomento e matchup
carte.html              67 carte ufficiali Bandai raggruppate per ruolo
guide/<autore>.html     il testo integrale di ogni guida, in tab per capitolo
guide/dojo.html         le sessioni del Dojo (Codex) non coperte dalle altre pagine
versione-precedente.html  il vecchio sito a pagina singola (Impact + samsansOP)
```

## Convenzioni

- Il contenuto strategico è **verbatim in inglese**, refusi delle fonti compresi. Dove una guida dice
  qualcosa di sbagliato o incoerente, il testo resta com'è e una nota `⚠️` lo segnala.
- Le sintesi, i confronti e le note di conflitto sono **in italiano**.
- **Impaginato, non riassunto.** `render.py` non cambia una parola: riconosce la struttura che le fonti
  hanno già (titoletti in grassetto, frasi in grassetto, «Etichetta: testo», catene A → B → C, schede
  Difficulty/Turn Order, mani di mulligan, blocchi di domande) e la mostra con una gerarchia visiva.
  Le note del trascrittore sui refusi diventano note discrete (✎); solo i troncamenti restano in rosso.
  Le tabelle «CARTE CITATE» del trascrittore finiscono in un'appendice richiudibile a fine capitolo.
- Ogni fonte ha un colore: Raphterra verde, Rondino azzurro, NebulusTCG viola, Impact arancione, samsansOP rosa.

### Priorità editoriali applicate

- **Mazzi gialli → pesa NebulusTCG.** Robin, Linlin, Boa e Pudding hanno da lui rating separato per
  primo/secondo, mulligan dichiarato e piano spiegato.
- **Black Luffy, Red Ace, RB Sabo → la linea di starving di Rondino** è riportata per intera e in evidenza,
  con le controparti dove qualcuno la contraddice (NebulusTCG su Black Luffy dice l'opposto).

### ⚠️ Due fonti sono troncate

Le catture PDF di due capitoli si interrompono per un limite dello screenshot (FireShot si ferma a 32 tile):

- **Raphterra — «Matchup Strategies vs The Meta»**: si interrompe sul titolo *Vs. Red Black Sabo*.
  Quel matchup non c'è nel testo; restano i due video su Sabo.
- **Rondino — «5. The matchups bible»**: si interrompe a metà frase nel *Vs Red Ace*.

Per recuperarli serve una nuova cattura di quelle due pagine Metafy.

## Come è costruito

```
render.py        markdown verbatim -> HTML impaginato (sottotitoli, punti chiave, schede,
                 schemi a flusso, mani di carte, quiz, timeline dei video, note discrete)
build.py         genera le pagine delle guide e riallinea il menu delle pagine scritte a mano
                 (con --stitch ricuce prima i capitoli dalle strisce)
build_pages.py   genera video.html, carte.html, le guide "piatte" e confronto.html
assets/          style.css e app.js (tab, indice, filtri, motore quiz)
data/            matchup.js (l'aggregatore), aggiornamenti.js (le fonti di settembre incrociate
                 matchup per matchup) e video.js
trascrizioni/    il markdown verbatim, un file per capitolo
carte/           immagini ufficiali Bandai (EN)
img/guide/       decklist, cheat sheet e tier list ritagliate dalle guide
fonti/           PDF e sorgenti originali — NON versionati (contenuti a pagamento)
```

Per rigenerare il sito dopo una modifica alle trascrizioni:

```bash
python build.py && python build_pages.py
```

Le trascrizioni sono state prodotte dai PDF (screenshot senza layer di testo) affettandoli con tagli che
cadono solo su righe di sfondo uniforme, così nessuna immagine di carta e nessuna riga di testo viene
spezzata a metà.

---

Immagini carte © Bandai / Shueisha. Le guide Metafy appartengono ai rispettivi autori: i PDF sorgente non
sono ridistribuiti in questo repository. Progetto personale di studio.

/* ===========================================================================
   Aggiornamento settembre — le fonti nuove incrociate matchup per matchup.
   rond16   = masterclass di Rondino, 16/09 (Dog of Wisdom, session notes)
   impact17 = Deep Dive Q&A di Impact sul Dojo, 17/09 (session notes)
   dojo     = sessioni della Training Library del Dojo (Codex): 9/09 VOD review
              vs Robin, 3/09 ladder di Elijah, 27/08 VOD review con Equinby
   Le citazioni fra virgolette sono verbatim dalle fonti (inglese).
   =========================================================================== */

const FONTI_AGG = {
  rond16:   {nome:'Rondino · 16/09',  badge:'b-rond',   link:'guide/rondino.html#06-masterclass-16-09'},
  impact17: {nome:'Impact · 17/09',   badge:'b-impact', link:'guide/impact.html#qa1709'},
  dojo2:    {nome:'Dojo · 9/09',      badge:'b-dojo',   link:'guide/dojo.html#s2'},
  dojo3:    {nome:'Elijah · 3/09',    badge:'b-dojo',   link:'guide/dojo.html#s3'},
  dojo6:    {nome:'Elijah · 27/08',   badge:'b-dojo',   link:'guide/dojo.html#s6'},
};

/* La novità che attraversa tutti i matchup */
const NOVITA = {
  titolo:'Il «rest spell» cambia il mazzo',
  testo:'Fra il 16 e il 17 settembre Rondino e Impact convergono sulla stessa carta: <b>I Never Bother to Remember the Faces of Trash</b> (OP14-038), il «trash event» / «rest spell». Rondino lo gioca a 3 al posto di Bonney e Perona 5c; Impact a 4, con 4 Coffin Boat, e lo chiama «a whole game plan», non una tech. Il risultato: i matchup con i mazzi da early game (Sabo, Enel) si girano, e lo starve diventa il piano di default contro metà del campo.',
  citazioni:[
    {f:'impact17', txt:'"Sabo has gotten a lot worse this week" — the rest spell makes the deck "a board-control deck first, aggro second".'},
    {f:'rond16', txt:'With 3 events + 4 Yasopp "their early game is non-existent": you always have something to attack into, so starving becomes the default.'},
  ],
};

const AGGIORNAMENTI = {
 'mirror':{
   pill:'resta pari · si va secondi',
   voci:[
     {f:'rond16', txt:'Verdict: <b>even; whoever reads the game tree first</b>. Turn order: <b>second is stronger</b> (you see his searchers first); first must high-roll. E soprattutto: «Starving in the mirror is wrong».'},
     {f:'impact17', txt:'Life plan: <b>take the first two life, defend the third</b>. La build Perona/tempo è «best in the mirror»; ma la build col rest spell non è un sacrificio: «you\'re not making sacrifices to play it»: tappandogli le 1-drop gli neghi il Law al turno da 6 DON!!.'},
     {f:'dojo3', txt:'Law/Bepo «underwhelming in the mirror»; il mirror si gioca a colpi da 7k per «2k-check» l\'avversario; Perona «is better than it looks».'},
   ],
   conflitti:[
     {t:'Law & Bepo nel mirror: seconda bomba o carta debole?', pos:[
       {f:'dojo3', txt:'«What does Law/Bepo actually do that Shanks plus Vander Decken plus Luna does not already do better?» — nel mirror la vede sottotono.'},
       {f:'impact17', txt:'4 Shanks meglio di 3 Shanks + 1 Bepo, ma Bepo resta giusto quando devi «stretch your Lunas one more turn»: «I\'m still not convinced it\'s better than the 4th Shanks. It certainly can be».'},
     ], nota:'Nelle guide di agosto samsansOP dava a Law & Bepo molto più peso nel mirror (vedi il confronto LawSopp vs HawkRona).'},
   ]},
 'py-robin':{
   pill:'Impact ora lo dà 45-55',
   voci:[
     {f:'impact17', txt:'Verdict: <b>slightly unfavored, ~45-55</b> ("Robin is still Robin"). Non è una corsa: controlli la board finché Big Mom diventa «just a 10-mana heal + draw». Law è «the best card in the matchup»; le prime due vite si prendono «most of the time».'},
     {f:'rond16', txt:'Contro Robin <b>non si affama</b>: «they heal and trigger too many pieces». Il rest spell fa il lavoro che prima faceva Bonney.'},
     {f:'dojo2', txt:'VOD review dedicata: il matchup si decide sul tempo prima del primo Big Mom da 10. ⚠️ Sul turno la fonte si contraddice (prima «going first», poi «Take Second»).'},
     {f:'dojo3', txt:'Elijah preferisce <b>andare primo</b> con Law + Yasopp: rende più difficile la partenza migliore di Robin (secondo, doppio ramp, Teach, Big Mom).'},
   ],
   conflitti:[]},
 'black-luffy':{
   pill:'Rondino ora affama anche da primo',
   voci:[
     {f:'rond16', txt:'Con il nuovo evento Black Luffy è <b>full-starved going first and second</b> — prima dell\'evento Rondino correva quando andava primo.'},
     {f:'impact17', txt:'Visto dal lato di Black Luffy: «decent, not fully tested»; il punto forte è il 6-5 al turno da 7 DON!! — «Impact would still just play Mihawk».'},
   ],
   conflitti:[]},
 'red-ace':{
   pill:'Rondino ora lo dà ~80%',
   voci:[
     {f:'rond16', txt:'Verdict: <b>favored (~80% first, easier second)</b>. <b>Full starve</b>: poke 8s into Marco, Oden on top; «First Shanks established = everything he plays is nuked». Lo starve spegne il buff a 8k del leader.'},
   ],
   conflitti:[]},
 'rb-sabo':{
   pill:'girato a favore col rest spell',
   voci:[
     {f:'impact17', txt:'Verdict: <b>went from bad to really good with the rest spell</b>. «Starve, especially if you\'re playing the spell»; si passa alla faccia solo quando loro vanno double 6-cost.'},
     {f:'rond16', txt:'Verdict: <b>favored</b>. Turn order: <b>starve first and second</b>. «Decken first, then kill the Luffy (they need it for the 12-cost)».'},
     {f:'dojo6', txt:'Dal lato di Sabo (27/08, prima del rest spell): «Sabo wants the game to be short. Mihawk wants the game to go long» — Sabo sceglie secondo.'},
   ],
   conflitti:[]},
 'p-kaido':{
   pill:'confermato: si va primi',
   voci:[
     {f:'impact17', txt:'Verdict: <b>super good</b> — «it\'s hard for them to win». Turn order: <b>first almost always</b>. Primi corpi: Yasopp; Odens + stun sul King; «Shanks + Decken one, blast the other».'},
   ],
   conflitti:[]},
 'rocks':{
   pill:'~95% per Rondino',
   voci:[
     {f:'rond16', txt:'Verdict: <b>favored, ~95% in his words</b>. Turn order: second. Clear Kyo before turn 10, Shanks + Decken the Xebec.'},
     {f:'impact17', txt:'Verdict: <b>favored</b> ("free" only if you board control) — Luna makes it unlosable. Turn order: second preferred, first is still fine. Regola: <b>Oden the John</b>.'},
   ],
   conflitti:[
     {t:'Starve o controllo della board?', pos:[
       {f:'rond16', txt:'«Starve = default vs Sabo, Ace, Black Luffy, Rocks».'},
       {f:'impact17', txt:'«Plan — board control, not starve»: Shanks, Decken e Yasopp come rimozione; la vita solo quando conviene. «Rocks cannot win without Newgate, Shiki and Linlin in play.»'},
     ], nota:'In pratica le due linee si toccano: entrambi tolgono la board prima di andare in faccia; la differenza è quanto a lungo si rinuncia a prendere vita.'},
   ]},
 'p-enel':{
   pill:'Impact: da brutto a molto buono',
   voci:[
     {f:'impact17', txt:'Verdict: <b>went from bad to really good with the rest spell</b> — «fighting Enel is miserable if you don\'t have it, especially if you lose the roll». Full starve + board control: finiscono prima loro le rimozioni.'},
     {f:'rond16', txt:'Dipende dalla sua partenza: «Starts with Holy → full value control… Starts Hom Hom → you cannot win the value war… so race him».'},
     {f:'dojo3', txt:'Elijah (3/09, prima del rest spell): Enel «harder now than in OP16.5» con Law + Yasopp; non regalare Mamaragan su attacchi da 5k.'},
     {f:'dojo6', txt:'Elijah (27/08): «Take early life liberally», sviluppa Mihawk + Oden, rispetta gli Ohm multipli.'},
   ],
   conflitti:[
     {t:'Affamare Enel o prendere vita presto?', pos:[
       {f:'impact17', txt:'«Full starve + board control… don\'t give life cards».'},
       {f:'dojo6', txt:'«Take early 5k and 6k attacks liberally».'},
       {f:'rond16', txt:'Dipende dall\'apertura: Holy → value control; Hom Hom → corsa.'},
     ], nota:'La posizione di Impact è l\'unica scritta dopo l\'arrivo del rest spell; quella di Elijah è di fine agosto.'},
   ]},
 'uy-boa':{
   pill:'favorevole anche per Rondino e Impact',
   voci:[
     {f:'rond16', txt:'Verdict: <b>favored but matchup with little reps</b>. Linea di letale fissa <b>7-7-9</b> contro i Blocker in vita.'},
     {f:'impact17', txt:'Verdict: <b>a lot chiller than you think</b>. Rimuovi la roba non-Kuja, «double clear» due Kuja Pirates nello stesso turno.'},
   ],
   conflitti:[
     {t:'Attaccare subito o costruire prima?', pos:[
       {f:'rond16', txt:'«Do not starve: attack, take all lives fast, then contest the whole board in one turn».'},
       {f:'impact17', txt:'«Don\'t give them triggers early… Not really attack them until you build up a board, then attack all at once».'},
     ], nota:'Concordano su una cosa: il turno decisivo è quello in cui si contesta tutta la loro board in una volta.'},
   ]},
 'luffy-ace':{
   pill:'corsa: attacchi da 7k in faccia',
   voci:[
     {f:'impact17', txt:'Verdict: <b>"you win the game the last turn before you die"</b>. Turn order: second is good. Non si affama un leader che dà Rush: stun + corsa, vita dispari (3 → 1), <b>Oden is the most important 5</b>.'},
     {f:'dojo6', txt:'«Attack Ace Luffy with repeated 7k swings and it dies»: il mazzo non ha counter; «Why Board Control Is Usually Wrong».'},
   ],
   conflitti:[]},
};

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
     {f:'impact17', txt:'Verdict: <b>went from bad to really good with the rest spell</b> — «fighting Enel is miserable if you don\'t have it, especially if you lose the roll». E il cambio di opinione è dichiarato: «Impact has changed his opinion on Mihawk versus Enel. He now believes Mihawk should often <b>starve Enel</b>, control board, and make Enel run out of removal.»'},
     {f:'impact17', txt:'<b>Il piano in otto passi, verbatim:</b> 1) «Do not feed Enel easy life cards»; 2) «Use rest spell, Yasopp, Perona, Oden, and Vander Decken to control Enel\'s board»; 3) «Force Enel to spend removal spells»; 4) «Do not give Enel more cards while it is trying to clear your board»; 5) «Eventually stick one or two meaningful bodies»; 6) «Play Shanks and remove Enel\'s big threat»; 7) «Force Enel to take life in one large board turn»; 8) «Kill over the next one or two turns».<br><b>Perché funziona:</b> «Enel\'s removal spells do not replace themselves… Enel must find both removal and a character repeatedly» — mentre «your things draw when removed, so you keep playing more». «Mihawk may go low in life while starving Enel, but that is acceptable if Enel is also running out of cards.»'},
     {f:'impact17', txt:'<b>Dettagli operativi della linea starve.</b> Pre-gioca al turno 1 (unit + stage, o due unit) «so you can bomb the thing». Ogni attacco chiede due carte alla loro mano e «they have few 2ks (two Sanji, a Mama 1k)». Quando qualcosa sticka: «play two more, remove their guy: eventually 3 things stick, then Shanks, then 4 — you win». Quando arriva Shanks: «play Shanks and bomb their Enel: with no life cards they have nothing to defend with». Poi «force all their life in one turn — they get 1-2 turns max to use those cards».'},
     {f:'impact17', txt:'<b>Il rest spell è il motivo per cui la lista è quella.</b> Sequenza vs Enel: «rest spell + Yasopp + Law + Yasopp again, every turn, until you have won the board. You are <b>full-starving Enel and Sabo</b> until the board is won». Il bersaglio giusto sono i loro 1-costo, che <b>nega anche il Law</b> al turno da 6 DON!!. È la ragione dichiarata per preferire la build col rest spell a quella Perona/tempo: «rest is good into all the random decks (Enel, Sabo, Robin, Rocks, Luffy-Ace, Kaido)… you never play against the same deck five times in a tournament». La lista arrivata 2ª (rest spell + 4 Coffin Boat) «makes all of Enel\'s random stuff not as good».'},
     {f:'impact17', txt:'<b>Enel nel meta del weekend:</b> è uno dei «three or four decks you can really consider» (Mihawk, Robin, Enel, RG Luffy-Ace). Nella mappa del meta: buono contro Robin con 4 Enel, perde contro Boa («cooked») e contro il Mihawk col rest spell. Al grande regionale della settimana prima: 11 Mihawk in top cut contro 6 Robin e <b>5 Enel</b>.'},
     {f:'rond16', txt:'<b>Q: «How do you play Enel?»</b> — «Depends on his start and your hand. <b>Starts with Holy → full value control</b> (Shanks tanks stabilize). <b>Starts Hom Hom → you cannot win the value war</b> (Franky, 4-cost Law follow up), <b>so race him</b>.»<br>È l\'unica fonte che fa dipendere il piano dalla <b>loro prima carta</b> invece che dalla propria lista. Rondino gioca 3 copie del trash event e annuncia «an Enel chapter with more videos to come»: il capitolo è poi uscito (nella guida il trigger per la corsa diventa <b>Ohm → Ohm</b>) — <a href="guide/rondino.html#05b-enel">leggilo qui</a>.'},
     {f:'dojo3', txt:'<b>Elijah, ladder 3/09 (prima del rest spell): il matchup si è indurito.</b> «Enel is meaningfully harder for Mihawk now than it was in OP16.5, especially if Enel is built to target Mihawk» — con la build Law + Yasopp. Motivi: X-Drake e Law, hand-rip, tanti 1-costo (soprattutto <b>Ohm</b>), <b>Mamaragan</b> per guadagnare vita senza spendere mano. «This is no longer a matchup Mihawk can treat as routine.»<br>Priorità: «control Enel\'s one-drops where possible; remove midrange bodies before they snowball; <b>do not expect your board to remain untouched</b>; use Shanks and Luna to create a final turn where Enel\'s one-drops no longer attack».<br>Perona: «excellent against Enel because it is hard to cleanly remove» — in una partita «remained in play and attacked several times… if Perona had been any other 5-cost body, it would have been removed immediately».'},
     {f:'dojo6', txt:'<b>Elijah, VOD review 27/08: la gestione della vita e degli attacchi.</b> Piano: «take early life liberally; develop Mihawk plus Oden; preserve enough board to create wide future turns; use Perona, Oden, and Law/Bepo to control Enel\'s relevant attackers; <b>avoid giving Enel efficient Mamaragan targets</b>; convert the board into large life pressure once Enel can no longer afford to use its events freely».<br>La regola secca: «<b>Do not give Enel a clean Mamaragan if you could have attacked for a real number instead.</b>» Un 5k viene Mamaragan\'ato: loro tengono la mano, guadagnano una vita, e quella vita assorbe un 7k dopo.<br>Contro triplo Ohm: Samurai anche i corpi grossi, «because those bodies are doomed anyway».<br>La chiave del matchup: «the Enel player can remove one body. <b>The Mihawk player wins by forcing Enel to answer several bodies over multiple turns.</b>»'},
   ],
   conflitti:[
     {t:'Affamare Enel o prendere vita presto?', pos:[
       {f:'impact17', txt:'<b>Starve.</b> «Full starve + board control… do not feed Enel easy life cards.» Accetta di andare basso di vita: finiscono prima loro le rimozioni.'},
       {f:'dojo6', txt:'<b>Prendi vita.</b> «Take early 5k and 6k attacks liberally» — le carte pescate dalla vita migliorano la mano.'},
       {f:'impact', txt:'<b>Tieni il cuscinetto.</b> La guida Law+Yasopp dice l\'opposto di entrambi: «counter at least 1 of their swings per turn so that you don\'t lose more than 1 life a turn. You\'ll need a life buffer to resolve back to back Shanks.»'},
       {f:'rond16', txt:'<b>Dipende dalla loro apertura</b>: Holy → value control; Hom Hom → corsa.'},
     ], nota:'Tre posizioni diverse su tre momenti diversi del matchup, non tre errori. Impact (guida) parla della <b>vita tua</b> e conta all\'indietro dal doppio Shanks; Impact (17/09) parla della <b>vita loro</b> e del non regalargli carte; Elijah parla del <b>valore in carte</b> dei primi colpi presi. Ordine di lettura: se giochi il rest spell, starve; dentro lo starve, la vita che prendi presto va comunque contata contro i due Shanks finali.'},
     {t:'Prima o dopo il rest spell: due matchup diversi con lo stesso nome', pos:[
       {f:'dojo3', txt:'<b>3/09 — «harder now than in OP16.5»</b>, con la build Law + Yasopp. Enel costruito apposta contro Mihawk.'},
       {f:'dojo6', txt:'<b>27/08 — matchup di misura</b>, giocato sulla gestione della vita e sulla taglia degli attacchi, senza rimozione a costo zero.'},
       {f:'impact17', txt:'<b>17/09 — «from bad to really good»</b> grazie a 4 copie del trash event.'},
       {f:'neb', txt:'<b>1/09 — «Slightly Favored / Even»</b>, con l\'avvertenza che «the yellow decks &amp; Enel are in the midst of evolving to counter Mihawk so this could be different soon». Aveva ragione.'},
     ], nota:'Il verdetto di una fonte su Enel dice soprattutto <b>che lista aveva in mano quel giorno</b>. Prima del 16/09 nessuno gioca il trash event: le sessioni del Dojo di agosto e inizio settembre descrivono un matchup che, se tu giochi 3-4 copie dell\'evento, non è più quello.'},
     {t:'La variante hand-rip: quanto conta', pos:[
       {f:'neb', txt:'<b>Hand Rip PEnel</b> è elencata fra i «MU\'s that I need to test more that are losing».'},
       {f:'dojo3', txt:'Fra i motivi per cui il matchup si è indurito: «Enel can hand-rip key pieces». Countera presto se la tua mano ha una vulnerabilità critica.'},
       {f:'impact', txt:'Non la tratta come matchup separato: «try and play around hand rip Law if you can. If you can\'t, then just deal with it» — Decken e Kawamatsu si pitchano come counter, non si tengono.'},
       {f:'impact17', txt:'Nella Q&amp;A non compare affatto: il rest spell che uccide i loro 1-costo presto riduce il problema alla radice.'},
     ], nota:'Nessuno la smentisce, semplicemente due fonti l\'hanno testata e due no. La linea difensiva su cui concordano tutti è una sola: counterare presto con le carte che nel matchup sono morte, per non farsi svuotare la mano due turni di fila.'},
     {t:'Il cane sì o no (letto dal loro lato)', pos:[
       {f:'impact17', txt:'<b>No dog.</b> «It just dies to the rest spell» — «a pretty stuff card if everyone\'s playing the rest spell».'},
     ], nota:'Per te è un indicatore: se l\'Enel di fronte gioca il cane, sta giocando una lista tarata su un meta senza trash event, e il tuo piano di starve sui loro 1-costo funziona meglio del previsto.'},
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

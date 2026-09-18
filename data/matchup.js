/* ===========================================================================
   Aggregatore matchup — Green Mihawk OP17
   Ogni matchup raccoglie il verdetto di OGNI fonte, i punti in cui concordano
   e i punti in cui si contraddicono apertamente.
   Le citazioni tra virgolette sono verbatim dalle guide originali (inglese).
   =========================================================================== */

const FONTI = {
  raph:   {nome:'Raphterra',  badge:'b-raph',   link:'guide/raphterra.html'},
  rond:   {nome:'Rondino',    badge:'b-rond',   link:'guide/rondino.html'},
  neb:    {nome:'NebulusTCG', badge:'b-neb',    link:'guide/nebulus.html'},
  impact: {nome:'Impact',     badge:'b-impact', link:'guide/impact.html'},
  sam:    {nome:'samsansOP',  badge:'b-sam',    link:'guide/samsans.html'},
};

const MATCHUP = [
{
  id:'mirror', nome:'Green Mihawk — Mirror', carta:'OP14-020', colore:'Verde',
  tier:'even', sintesi:'Battaglia di risorse che diventa battaglia di combo pieces. Tutte e quattro le fonti dicono la stessa cosa sul turno: si va secondi.',
  extra:'<a href="mirror.html" class="btn" style="display:inline-block;margin-top:6px">Apri la sezione Mirror dedicata →</a>',
  verdetti:[
    {f:'raph', v:'even', txt:'<b>Even</b>, "but it can come down to who has more combo pieces in the late game". Turn order: <b>Go Second</b>, per essere il primo ad avere l\'opzione 10C Shanks.'},
    {f:'rond', v:'even', txt:'<b>Die roll: Second</b>. Default game plan: <b>Value / Control</b>. Alternative game plan: "Aggro when the value game becomes unfavorable".'},
    {f:'impact', v:'even', txt:'<b>Go 2nd</b>. "This matchup is about damage. Understanding how to deal damage and how to map damage across multiple turns is going to be the key to victory."'},
    {f:'sam', v:'even', txt:'Sezione dedicata al mirror con il problema del "nuovo mirror", gestione vita e Stun Bonney come piano del giocatore che va primo.'},
  ],
  accordo:[
    'Si va <b>secondi</b>: è l\'unico punto su cui tutte e quattro le fonti sono esplicitamente d\'accordo.',
    '<b>5C Yasopp è il 5-costo più importante</b>: si ristanda da solo, uccide i 6k riposati e — se sopravvive — ristanda 10C Shanks nel late game. Raphterra: "Always Kill Yasopp". Rondino e samsansOP dicono lo stesso.',
    '<b>Electrical Luna decide le partite</b>. Impact: "Games are won or lost by how many turns you can stall the game with Luna". Raphterra costruisce l\'intero late game sul conteggio delle Luna.',
    '<b>Conserva 2C Vander Decken + una carta Fishman</b> per rispondere al 10C Shanks avversario. Raphterra lo chiama "The Always Rule"; è anche l\'avvertimento di Rondino sul counterare con i Fishman.',
    'Il <b>10C Law & Bepo</b> è l\'alternativa quando la combo non è completa: corpo + freeze + leader a 8k in una carta sola.',
  ],
  conflitti:[
    {t:'Controllo board o corsa al danno?', pos:[
      {f:'raph', txt:'"My Default Is Board Control" — logorare le risorse prima di provare a chiudere. La corsa è il piano B.'},
      {f:'impact', txt:'Piano centrato sul <b>danno</b>: "We play less overall stuns than before. Less Peronas means attacks will go through... size the attacks with the goal of dealing damage, not extracting cards."'},
      {f:'rond', txt:'Via di mezzo dichiarata: "You need to identify as early as possible what kind of game you\'re playing" — value di default, aggro appena il gioco di valore gira male.'},
    ]},
    {t:'Quanto andare larghi prima del turno da 10', pos:[
      {f:'raph', txt:'"The 3-Attacker Cap": massimo tre attaccanti. Andare a 4-5 corpi ti fa congelare da Electrical Luna appena arriva il turno da 10 DON!!.'},
      {f:'impact', txt:'Non pone un tetto esplicito: il focus è arrivare a mettere l\'avversario a 1 vita, poi Shanks porta a 0 e Luna congela gli attaccanti.'},
    ]},
  ],
  carte:['OP17-022','OP08-036','OP06-033','OP17-031','ST24-004','OP07-026'],
},
{
  id:'py-robin', nome:'Purple Yellow Robin', carta:'OP09-062', colore:'Viola/Giallo',
  tier:'fav', sintesi:'Il matchup giallo per eccellenza. Yasopp è la carta che lo definisce — e qui le fonti litigano sul turno.',
  nautilus:true,
  verdetti:[
    {f:'neb', v:'fav', txt:'<b>Go Second</b> — "1st: Favored / 2nd: Very Favored". Mulligan: <b>"HARD MULLIGAN for YASOPP"</b>. Dichiara il matchup nettamente a favore di Mihawk.'},
    {f:'raph', v:'even', txt:'<b>Even</b>, "the matchup is easy for us assuming we draw well, but a bad opener can be punished with her Banish attacks". Turn order: <b>Go Second</b>.'},
    {f:'rond', v:'even', txt:'<b>Die roll: Second</b>. Game plan: <b>Full Value / Aggro</b>. Matchup: <b>"Close to even"</b>.'},
    {f:'impact', v:'fav', txt:'<b>Go 1st</b>. "The matchup is not good for Robin with Yasopp controlling them in the early game and Shanks removing all their attackers."'},
  ],
  accordo:[
    '<b>Yasopp è LA carta del matchup</b>: si ristanda quindi è immune alla riduzione di potenza dei 3 Sweet Generals, e uccide i corpi da 4k prima che Big Mom li porti a 8k. Nebulus arriva a chiedere un hard mulligan per trovarlo.',
    '<b>Shanks + Vander Decken + Luna è la win condition.</b> Impact: "Shanks + Vander Decken and Luna the 4K Bodies is the win condition."',
    '<b>Vanno pressati</b>: Robin non gioca praticamente KO trigger, quindi i corpi restano in campo e fanno da clock.',
    '<b>Gum Gum Giant non va temuto troppo</b>: Impact dice di attaccare per 7 e forzarlo; Nebulus suggerisce di appiattire gli swing o stackarli a 9k.',
  ],
  conflitti:[
    {t:'Primo o secondo? — il disaccordo più netto del meta', pos:[
      {f:'impact', txt:'<b>Go 1st.</b> Prendersi i primi colpi del leader e concentrarsi sul pescare tanto con Samurai per aggirare lo starve del leader Robin.'},
      {f:'neb', txt:'<b>Go Second.</b> Li costringe al triplo ramp per la 10c Linlin, la tua curva è più liscia e peschi una carta in più.'},
      {f:'raph', txt:'<b>Go Second.</b>'},
      {f:'rond', txt:'<b>Go Second.</b>'},
    ], nota:'Tre fonti su quattro dicono secondo. Sui mazzi gialli conviene pesare NebulusTCG, che è anche la più esplicita sul perché: il triplo ramp.'},
    {t:'Quanto è favorevole davvero', pos:[
      {f:'neb', txt:'Favored andando primi, <b>Very Favored</b> andando secondi.'},
      {f:'raph', txt:'<b>Even</b> — un\'apertura scarsa viene punita dagli attacchi Banish.'},
      {f:'rond', txt:'<b>"Close to even"</b>.'},
    ], nota:'Nebulus è molto più ottimista degli altri due. La differenza sta nel piano: Nebulus vince il matchup col controllo board via Yasopp, non con la linea Mihawk "standard".'},
    {t:'La linea standard di Mihawk funziona?', pos:[
      {f:'neb', txt:'<b>No.</b> Ripetere Law+Oden picchiando in faccia è "la linea che affossa le statistiche da simulatore": appena parte la catena di Big Mom devi switchare al controllo del board.'},
      {f:'rond', txt:'Game plan dichiarato <b>Full Value / Aggro</b> — più vicino alla linea standard.'},
    ]},
  ],
  carte:['OP17-031','OP17-022','OP06-033','OP08-036','OP17-099'],
},
{
  id:'black-luffy', nome:'Black Luffy (Elbaph)', carta:'OP17-079', colore:'Nero',
  tier:'even', sintesi:'Qui la strategia di starving di Rondino è il contributo più utile: cambia completamente il piano a seconda del tiro del dado.',
  starve:true,
  verdetti:[
    {f:'raph', v:'even', txt:'<b>Even</b> — "It can go either way depending on draws and the dice roll, but it\'s slightly favored for Mihawk on average". Turn order: <b>Go Second</b>, "to give them 1 less hand card and to steal their ideal curve".'},
    {f:'rond', v:'even', txt:'<b>Die roll: Second.</b> Going First: <b>Full Race / Aggro</b>. Going Second: <b>Starve / Control</b>. Due partite completamente diverse.'},
    {f:'neb', v:'even', txt:'<b>Go Second</b> — "Going 1st: Unfavored / Going 2nd: Favored". Mulligan: "Many Odens to lock up Saul / Docking / Loki". ⚠️ Nella tabella riassuntiva però lo elenca anche fra i <b>"MU\'s that I need to test more that are losing?"</b>: le sue due valutazioni non coincidono.'},
  ],
  accordo:[
    '<b>Si va secondi</b>: unanime fra le tre fonti.',
    '<b>Andando primi il matchup peggiora</b> per tutti.',
    '<b>Non provare a uccidere i corpi piccoli</b>: si congelano e si ignorano. Rondino: "Freeze them → ignore them → pressure Leader → eventually punish the accumulated board with Electrical Luna."',
    '<b>Decken e gli swing grossi vanno sui corpi grandi</b>, non sulle weenie. Nebulus: tutti gli attacchi grossi sui giganti da 12+ costo, perché sono loro ad abilitare il resto del kit.',
    '<b>6c Loki</b> è un problema riconosciuto da tutte le guide che lo trattano, con una sezione dedicata ciascuna.',
    '<b>Oden è la carta da cercare</b> per bloccare Saul, Pirate Docking 6 e Loki.',
  ],
  conflitti:[
    {t:'Affamare o no? — le due guide si contraddicono apertamente', pos:[
      {f:'rond', txt:'<b>Andando secondi si affama.</b> "We\'re trying to starve, control the board, and reach our stabilization turn." Schema: Starve → Control board → Preserve resources → 10c Shanks → Stabilize.'},
      {f:'neb', txt:'<b>NON starvare.</b> Leader e weenie restano fissi a 5k tutta la partita, quindi affamando perdi troppi swing gratis, e oltre gli 8 DON!! loro rushano un 8k ogni turno. Propone invece uno <b>pseudo-starve da entrambe le parti</b>, puntando a uccidere il grosso della board al primo turno da 10c Shanks.'},
    ], nota:'È il conflitto più secco fra due guide su uno stesso matchup. Le due linee condividono però l\'obiettivo (arrivare forti al primo 10c Shanks): la differenza sta nel se prendersi o no le vite per strada.'},
    {t:'Quando prendere vita', pos:[
      {f:'neb', txt:'<b>Presto.</b> Incassa i primi 3 life prima di iniziare a contrare — peschi meglio combo e motore di pesca — poi stabilizza a 1 vita e arriva al turno da 10 DON!! con il 6c Law già in piedi.'},
      {f:'rond', txt:'Andando secondi preserva le risorse e la vita; andando primi invece accetta la corsa piena.'},
    ]},
  ],
  starveBox:{
    titolo:'La linea di starving di Rondino (going second)',
    txt:'"We\'re trying to <b>starve</b>, control the board, and reach our stabilization turn." Lo schema dichiarato è <b>Starve → Control board → Preserve resources → 10c Shanks → Stabilize</b>, con la domanda guida: "How do I deny him enough resources that his engine never gets the chance to overwhelm me?"<br><br>Andando <b>primi</b> invece il piano si ribalta: "we can\'t realistically starve Black Luffy" → <b>Setup → Develop Tempo → Freeze → Race</b>. "We\'re not building our hand for a prolonged control game."',
  },
  carte:['OP17-079','OP08-036','OP06-033','OP17-022','OP14-037'],
},
{
  id:'red-ace', nome:'Red Ace', carta:'OP16-001', colore:'Rosso',
  tier:'unf', sintesi:'Il disaccordo più importante di tutto il sito: Raphterra vuole correre, Rondino dice espressamente di non correre.',
  starve:true,
  verdetti:[
    {f:'raph', v:'unf', txt:'<b>Slightly Unfavored</b> — "If they win the dice and have a god draw, there is not much we can do, but they can be pretty inconsistent". Turn order: <b>Go Second</b>, per impedire la curva 6C Marco → Newgate consecutivi. Macro gameplan della cheat sheet: <b>"RACE TO LETHAL"</b>.'},
    {f:'rond', v:'unf', txt:'<b>Die roll: Second.</b> Matchup plan: <b>Starve / Stabilize</b>. Mulligan: "Yasopp + searcher / 2+ searchers / Yasopp + law".'},
    {f:'neb', v:'even', txt:'<b>Go Second</b> — "1st: Unfavored / 2nd: Slightly Favored". Mulligan: Draw Engine.'},
  ],
  accordo:[
    '<b>Si va secondi</b>: unanime fra le tre fonti.',
    '<b>Andando primi il matchup è brutto</b> per tutti (Raphterra: dice + god draw = poco da fare; Nebulus: "1st: Unfavored").',
    '<b>Il vero pericolo è il Newgate da 10</b> e la curva 6C Marco → Newgate.',
  ],
  conflitti:[
    {t:'Correre o affamare? — la domanda centrale del matchup', pos:[
      {f:'raph', txt:'<b>RACE TO LETHAL.</b> "Play aggressive and race with a wide mid-game board, then close out with 10C Shanks."'},
      {f:'rond', txt:'<b>Non correre affatto.</b> "Don\'t even start the race." Il perno è il 10c Whitebeard che rende il loro leader 8k base: in una corsa quel numero ti seppellisce.'},
    ], nota:'Priorità alla linea di Rondino: è quella costruita apposta contro il Whitebeard da 10 e ha una spiegazione meccanica del perché la corsa perde.'},
  ],
  starveBox:{
    titolo:'Perché si affama Ace — Rondino, verbatim',
    txt:'<b>Why do we starve Ace?</b> Il perno è il <b>10c Whitebeard</b>, che porta il loro leader a 8k base. "Don\'t even start the race."<br><br><b>Change the structure of the game:</b> "We don\'t need to slowly chip Ace down. We can starve them, build an overwhelming position, and then kill them very quickly once we\'re ready." Con 2-3 copie di 10c Shanks si uccide in due turni.<br><br><b>How to punish the starvation game:</b> "Use <b>Yasopp</b> and <b>Oden</b> to interact with their pieces. Control their board. Defend the life attacks that you can defend efficiently." E soprattutto: <b>"Don\'t attack Leader just because you have spare attacks."</b> — "We\'re deliberately delaying the point at which Ace receives those resources."<br><br><b>The first 10c Shanks:</b> "The objective isn\'t to immediately convert 10c Shanks into damage. The objective is to create a board state where Ace progressively loses the ability to threaten us. Then we do it again."<br><br><b>The second 10c Shanks:</b> "And from there? <b>GG.</b> This is true even if we\'re sitting at 1 life—or sometimes even 0."',
  },
  carte:['OP16-001','OP17-031','ST32-002','OP17-022','OP07-026'],
},
{
  id:'rb-sabo', nome:'Red Black Sabo (Elbaph)', carta:'OP13-004', colore:'Rosso/Nero',
  tier:'unf', sintesi:'Considerato da tutti uno dei matchup peggiori. Anche qui Rondino propone lo starve totale.',
  starve:true, troncato:'La sezione di Raphterra su questo matchup NON è recuperabile: la cattura PDF della sua guida si interrompe esattamente sul titolo «Vs. Red Black Sabo».',
  verdetti:[
    {f:'rond', v:'unf', txt:'<b>Die roll: Second.</b> Game plan: <b>Starve and stabilize</b> — "Starve them, progressively remove their board, and stabilize on 10c shanks turn".'},
    {f:'neb', v:'unf', txt:'<b>Go Second</b> — nella tabella riassuntiva "1st: Unfavored / 2nd: 50-50"; nel capitolo dedicato è più preciso: <b>"1st — Unfavored — ATTACK / 2nd — Slightly Favored — STARVE"</b>. Mulligan: Draw Engine + Oden. ⚠️ Il capitolo è dichiarato "IN PROGRESS" e la sezione "What makes Elbo unique?" è vuota nella fonte.'},
    {f:'impact', v:'unf', txt:'<b>Go 2nd</b>. "This is one of our worst matchups (still 45-55 btw, and with the techs I think it\'s at worst 50-50)".'},
    {f:'sam', v:'unf', txt:'Sezione "Mihawk vs Sabo" con il confronto esplicito <b>Attack Versus Starve</b> e quando attaccare la board di Sabo.'},
    {f:'raph', v:'na', txt:'⚠️ Non disponibile — la cattura della guida si interrompe sul titolo del matchup.'},
  ],
  accordo:[
    '<b>Si va secondi</b>: unanime.',
    '<b>È fra i matchup peggiori</b>, ma nessuno lo dà per perso: Impact lo quota 45-55, Nebulus 50-50 andando secondi.',
    '<b>Yasopp serve presto</b>, per gestire i corpi da 2000 prima che arrivino i Giant. Impact: "Yasopp was one of the cards put into the deck originally to help deal with the early characters from Sabo while not losing value."',
    '<b>Se togli l\'unico Giant, tutte le loro weenie crollano</b> (Impact).',
    '<b>Occhio a Otama</b>: Impact consiglia di non metterla in campo se puoi evitarlo, perché fanno 2K check spesso con le weenie da 6000.',
    '<b>Andando secondi si affama</b>: Rondino e NebulusTCG arrivano alla stessa conclusione per vie diverse — Nebulus scrive letteralmente "2nd — Slightly Favored — <b>STARVE</b>" contro "1st — Unfavored — <b>ATTACK</b>".',
    '<b>Contra sempre gli swing da 5k</b>, anche il primo della partita e anche mentre stai affamando: dopo i primi uno-due 5k ogni attacco successivo arriva a 6k (NebulusTCG).',
  ],
  conflitti:[
    {t:'Affamare o contrattaccare?', pos:[
      {f:'rond', txt:'<b>Starve totale:</b> "Full starve them at 5 life until their board is cleared. Only then do we start attacking Leader."'},
      {f:'neb', txt:'<b>Dipende dal dado:</b> andando secondi starve, andando primi attacco. È l\'unica fonte che lega esplicitamente il piano al tiro del dado.'},
      {f:'impact', txt:'<b>Contropiede programmato:</b> "You won\'t be able to fully stabilize but their defenses are weak so you are often able to 2 turn with Shanks back to back if you can get them to 2."'},
      {f:'sam', txt:'Tratta il bivio come una scelta di lettura, con una sezione "When to Attack Sabo\'s Board".'},
    ], nota:'Rondino e Nebulus concordano sul piano going second. Impact è l\'unico che punta sul doppio Shanks consecutivo come chiusura.'},
  ],
  boxes:[
    {t:'⚠️ Rispetta Ain (OP07-002)', txt:'Avvertimento di NebulusTCG, e vale la partita: <b>se hai Yasopp e 10c Shanks insieme, ristanda Shanks, non Yasopp</b>, altrimenti perdi sul colpo. Ain è un 7 costo rosso che con l\'On Play porta a 0 la potenza di un tuo personaggio; Shanks ti serve poi per ripulire i loro corpi da 7k in su.'},
    {t:'Non bruciare i 2k', txt:'Kawamatsu va tenuto come munizione per Decken, e a volte conviene proprio giocare Otama. Raccogli gli Otama col 6 Law quando non devi rimbalzare Perona per trovare il Law successivo.'},
  ],
  starveBox:{
    titolo:'Lo starve di Rondino contro Sabo',
    txt:'Schema completo dichiarato a fine matchup: <b>Starve → Trade into Board → Preserve Life → 10c Shanks → Stabilize → Attack Face</b> — con l\'avvertimento finale: <b>"Don\'t rush the last step."</b><br><br>Il cuore è: "We want to play for maximum value and deny them life cards for as long as possible" e <b>"Full starve them at 5 life until their board is cleared. Only then do we start attacking Leader."</b> La sequenza di attacco consigliata per ripulire la board è <b>6k → 6k → 9k</b>.<br><br>Sulla difesa: counterare ogni attacco che costa una sola carta, anche il primo della partita — "We want to preserve our life total because we\'re deliberately starving our opponent".',
  },
  carte:['OP13-004','OP17-031','OP14-037','OP08-036'],
},
{
  id:'p-kaido', nome:'Purple Kaido', carta:'OP17-058', colore:'Viola',
  tier:'fav', sintesi:'Il matchup più favorevole del formato secondo tutte le fonti che lo trattano. Ed è l\'unico in cui si va primi con convinzione.',
  verdetti:[
    {f:'neb', v:'fav', txt:'<b>Go First</b> — "1st: Very Favored / 2nd: Very Favored". Mulligan: Draw engine + 2-3x Oden.'},
    {f:'raph', v:'fav', txt:'Nella tier list della guida è l\'unico leader in fascia <b>Favored</b>.'},
    {f:'impact', v:'fav', txt:'<b>Go 1st</b>. "Take their first so you can develop an extra attacker and slow down their ramp. Ramp decks typically want to go first as they want more turns to use their extra DON."'},
    {f:'sam', v:'fav', txt:'Sezione dedicata con priorità di gioco e il perché Oden conta così tanto.'},
  ],
  accordo:[
    '<b>Si va primi</b>: è il matchup che rovescia la regola generale del mazzo. La ragione è la stessa in tutte le fonti: rubare un turno di ramp.',
    '<b>Attacca per 7000 con i corpi da 6000</b> per giocare attorno all\'effetto leader di Kaido (-2000). Impact: meglio investire i DON!! sui personaggi che sul leader quando cerchi carte; il contrario quando spingi per il letale.',
    '<b>Shanks + Vander Decken rimuove l\'investimento del ramp</b> generando tempo: è il motivo per cui il matchup è girato rispetto ai set precedenti.',
    '<b>Yasopp permette di spingere senza paura del contrattacco</b> e più avanti ristanda Shanks per giocare attorno alla 10-Mom.',
    '<b>Oden è prioritario in mulligan</b> (Nebulus chiede 2-3 copie).',
  ],
  conflitti:[],
  boxes:[
    {t:'Tieni King "in galera"', txt:'NebulusTCG: blocca il King con Oden finché non cominci a calare i 10c Shanks. Se invece non pescano King, piazza gli Yasopp così non possono attaccare nei tuoi corpi riposati.'},
    {t:'Numeri di swing — mai 6/6', txt:'Con un attacco da personaggio e uno da leader: <b>5 dal leader e 7 dal personaggio</b>. Mai 6/6, perché regala valore all\'abilità del leader Kaido. Con due personaggi: 7 / 6 (leader) / 7.'},
    {t:'Massimizza le combo Decken', txt:'È il piano di vittoria primario, perché Kaido non ha modo di proteggere i corpi grossi. Senza Decken in mano, lascia passare lo swing e poi fai Decken + Law per rimbalzare il Decken e rigiocare Oden: il Law resta in piedi come blocker.'},
    {t:'Forzali a -1 DON!!', txt:'Spingili in posizioni scomode (swing da 6 al leader, poi al King per 6, poi 5) per impedire i 10-drop nei turni in cui non hai risposta — cioè quando ti mancano Decken + Shanks o lo Yasopp per ristandare Shanks.'},
  ],
  carte:['OP17-058','ST32-002','OP17-031','OP17-022','OP06-033'],
},
{
  id:'rocks', nome:'Blue Rocks', carta:'OP17-039', colore:'Blu',
  tier:'fav', sintesi:'Molto favorevole per una ragione strutturale: tutti i loro attaccanti costano 7 o meno, quindi Luna li spegne.',
  verdetti:[
    {f:'neb', v:'fav', txt:'<b>Go Second</b> — "1st: Very Favored / 2nd: Very Favored". Mulligan: Draw Engine.'},
    {f:'impact', v:'fav', txt:'<b>Go 2nd</b>. "Rocks major weakness is that all of its primary attackers are 7 cost or less, so it is extremely weak to Luna. If Luna + Shanks combo didn\'t exist, this matchup wouldn\'t be so lopsided."'},
    {f:'raph', v:'fav', txt:'Tier list: <b>Slightly Favored</b>. Nel capitolo "vs The Field" c\'è la sezione con video di gameplay.'},
    {f:'sam', v:'fav', txt:'Sezione dedicata con la debolezza principale di Rocks e cosa rispettare.'},
  ],
  accordo:[
    '<b>Matchup molto favorevole</b> — è la valutazione più alta insieme a Kaido.',
    '<b>Rocks è un leader Slash</b>: il leader Mihawk va a 6000 gratis, quindi estrae più counter a ogni scambio.',
    '<b>Luna è il blowout</b>: nessuno dei loro attaccanti principali esce dal range.',
    '<b>Captain John compra turni extra</b>: non andare all-in con Luna troppo presto. Impact: "Even just a single Captain John can buy them an extra turn."',
    '<b>Gioca attorno a Shiki</b> non attaccando con un solo corpo da 6000 alla volta; rimuovi gli Shiki a vista con Decken se non sono protetti da Kyo.',
  ],
  conflitti:[
    {t:'Si va primi o secondi?', pos:[
      {f:'impact', txt:'<b>Go 2nd.</b>'},
      {f:'neb', txt:'<b>Go Second</b> — ma segnala il matchup come Very Favored da entrambe le parti, quindi la scelta pesa poco.'},
    ], nota:'Non è un vero conflitto: concordano. Riportato perché è uno dei pochi matchup in cui il tiro del dado non cambia il piano.'},
    {t:'Chi si uccide per primo', pos:[
      {f:'neb', txt:'<b>Newgate prima di Shiki</b>, perché Newgate li aiuta sia in attacco sia in difesa mentre Shiki solo in difesa. Se tappano Newgate per spingere danno, puniscili con Decken.'},
      {f:'impact', txt:'<b>Shiki a vista</b> con Vander Decken se non è protetto da Kyo; e togliere i Kyo con Yasopp nell\'early game vale spesso la pena per fermare lo snowball.'},
    ], nota:'Priorità diverse, ma non incompatibili: dipende da quale dei due è sceso per primo e da cosa hai in mano.'},
  ],
  boxes:[
    {t:'Non saltare le Luna', txt:'NebulusTCG: pescane il più possibile per il late game. Tre Luna che congelano l\'intera board per tre turni battono anche il setup Captain John + evento Usopp.'},
    {t:'Se è l\'avversario ad affamare te', txt:'Accumula 10c Shanks — sono durissimi da uccidere, e più vita hai più valore ti danno i corpi grossi. Spendi il DON!! extra a cercare Luna e spingi la faccia con 12 su 5. Nel late game Yasopp o Oden più Luna per 12/12/12. Di norma bastano due Decken risolti.'},
    {t:'Numeri contro i counter da 3k', txt:'7k su 5k è quasi sempre bait: Shiki da 7 e Newgate da 6 danno +3k. Se hanno solo Shiki, swinga piccolo col leader e almeno 8k col board per chiedere due carte. Se hanno entrambi, rendi scomodo il counter: 11 su 5, 14 su 8.'},
  ],
  carte:['OP17-039','OP08-036','OP17-022','OP17-044','OP17-048','OP06-033'],
},
{
  id:'p-enel', nome:'Purple Enel', carta:'OP15-058', colore:'Viola',
  tier:'even', sintesi:'Favorevole ma scomodo: Enel pressa in modo efficiente e serve un cuscinetto di vita per risolvere due Shanks di fila.',
  verdetti:[
    {f:'neb', v:'even', txt:'<b>Go First</b> — "1st: Slightly Favored / 2nd: Even". Mulligan: Oden, Weenies. Segnala però la variante <b>Hand Rip P Enel</b> fra i matchup "che sto perdendo".'},
    {f:'impact', v:'fav', txt:'<b>Go 1st</b>. "Getting Enel to 0 is basically game over as Shanks send 5 17 is basically always game since they have no +3-4k Event counters."'},
    {f:'raph', v:'fav', txt:'Tier list: <b>Slightly Favored</b>. Fra le tech card consigliate contro Enel indica 6C Mihawk e 5C Perona.'},
  ],
  accordo:[
    '<b>Si va primi.</b>',
    '<b>Oden è il freno ai grossi Enel</b>: va conservato per quello.',
    '<b>Yasopp rimuove i corpi da 4</b> e impedisce lo snowball.',
    '<b>Non prendere troppi danni</b>: serve counterare almeno uno swing a turno per tenere il cuscinetto di vita necessario a due Shanks consecutivi.',
    '<b>Le weenie servono</b> per togliere i loro corpi da 1 costo senza investirci niente.',
  ],
  conflitti:[
    {t:'La versione hand-rip', pos:[
      {f:'neb', txt:'Elenca <b>Hand Rip P Enel</b> fra i matchup che sta perdendo e su cui gli serve più testing.'},
      {f:'impact', txt:'Tratta Enel come un matchup vincente senza distinguere la variante hand-rip.'},
    ], nota:'La distinzione è recente: se all\'evento ti aspetti la versione hand-rip, il verdetto ottimista di Impact non si applica direttamente.'},
  ],
  carte:['OP15-058','ST32-002','OP17-031','OP17-022'],
},
{
  id:'y-linlin', nome:'Yellow Linlin', carta:'OP17-099', colore:'Giallo',
  tier:'fav', sintesi:'NebulusTCG dichiara oltre l\'80% di vittorie anche andando primi — a patto di non fare l\'errore più comune: correre.',
  nautilus:true,
  verdetti:[
    {f:'neb', v:'fav', txt:'<b>Go Second</b> — "1st: Favored (even w/ Zeus + Y Grav Blade) / 2nd: Very Favored". Mulligan: Hard Mulligan for Yasopp. Claim esplicito: <b>"my gameplan allows Mihawk to win over 80% of the time even going first"</b>.'},
    {f:'sam', v:'fav', txt:'Trattato dentro "Mihawk vs Yellow Big Mom decks": identità del matchup, piano principale, ruolo di Stun Bonney e perché Mihawk vince.'},
  ],
  accordo:[
    '<b>Yasopp è di nuovo il mulligan obbligatorio</b>: si ristanda (immune ai 3 Sweet Generals), il 6k uccide i loro 4k riposati e il mazzo Linlin <b>non gioca counter event</b>.',
    '<b>Luna è la carta chiave</b>: il loro mazzo è oltre il 50% trigger, quindi riempiono la board se attacchi in vita.',
  ],
  conflitti:[],
  boxes:[
    {t:'La regola numero uno: NON rushare', txt:'"DONT DO THE FOLLOWING STRATEGY" è un titolo letterale della guida. Rushare fa finire loro con la mano piena e tanti 8k gratis dalla vita, e te a mani vuote. Perché funzioni servirebbe che l\'avversario sia sfortunato sui trigger, manchi la 10 Mom e tu topdecki: troppo inconsistente — ed è la ragione per cui i simulatori danno questo matchup come pessimo.'},
    {t:'10C Shanks è una risposta, non uno sviluppo', txt:'Rispondi ai corpi da 8 e 10 costi appena scendono. A differenza dei mazzi PY col pacchetto Big Mom, qui rispondi <b>sempre</b> alla 10 Mom nel turno in cui la giocano: se la calano senza almeno due corpi da 8k dietro, hanno speso 10 DON!! per curarsi una sola vita e vengono puniti da Shanks + Decken.'},
    {t:'La formula del letale garantito', txt:'<code>a</code> = numero di Luna · <code>b</code> = numero di Shanks in campo · <b>X</b> (danno garantito da Shanks) = <code>(a²+a)/2 + a·b</code> · <code>c</code> = vita avversaria in questo momento · <code>d</code> (cura di Linlin) = <code>a−1</code>.<br>Se <b>c + d &lt; X</b>, parti col letale usando Luna + Shanks.'},
    {t:'Effetto del leader avversario', txt:'Scegli quasi sempre di fargli scartare la seconda carta e curare una vita, per svuotargli la mano — finché non entri in modalità letale. Da lì in poi passa allo scarto random per cappare la cura a 1 per turno.'},
    {t:'Black Rope Dragon Twister (Y Gravity Blade)', txt:'Richiede più corpi sulla tua board che sulla loro <b>e</b> una vita coperta: minimizza i corpi inutili, per esempio non calare la Perona appena rimbalzata. I loro bersagli prioritari sono Yasopp e il 6c Law.'},
  ],
  carte:['OP17-099','OP17-031','OP08-036','OP17-022','OP06-033'],
},
{
  id:'uy-boa', nome:'Blue Yellow Boa Hancock', carta:'OP14-041', colore:'Blu/Giallo',
  tier:'fav', sintesi:'Si vince portando la PROPRIA vita a zero in fretta e stabilizzando dietro al 6c Law.',
  nautilus:true,
  verdetti:[
    {f:'neb', v:'fav', txt:'<b>Go Second</b> — "1st/2nd: Very Favored but can flip if they hit 2 good triggers out of first 2 life (gorgon sisters + ran)". Mulligan: Yasopp e card draw per Shanks/Luna più avanti.'},
    {f:'raph', v:'fav', txt:'Tier list: <b>Slightly Favored</b> (Boa Hancock). Nel capitolo "vs The Field" c\'è una sezione dedicata.'},
  ],
  accordo:[
    '<b>Si va secondi.</b>',
    '<b>Yasopp resta la carta da cercare</b> anche qui.',
  ],
  conflitti:[],
  boxes:[
    {t:'Vai a 0 vita apposta', txt:'Porta la tua vita a 0 in fretta e stabilizza dietro almeno un 6c Law. Ogni vita presa è un counter risparmiato, e a 0 vita l\'effetto burn del leader Boa diventa carta morta. Aspettati di esserci entro il turno 5-6: non sprecare carte per evitarlo.'},
    {t:'Il 6c Law è la guerra d\'attrito', txt:'Boa cappa a 2 copie l\'evento unblockable, quindi con un Law in piedi deve trovarne una copia <b>e</b> dedicarci tutto il turno. Tieni sempre un Law blocker in piedi a 0 vita (due se ha corpi che possono attaccare — Boa non gioca rush), e tieni sempre counter o DON!! attivo per sopravvivere allo swing unblockable da 15-17k.'},
    {t:'Uccidi subito le Gorgon Sisters', txt:'Valgono fino a 5 DON!! extra per copia: vale la pena scambiare una vita pur di ammazzarle (swing da 8k, oppure 7k+7k early-mid). Spesso le stackano come prima vita, quindi riposale e rimuovile con Yasopp sui 7-8 DON!!.'},
    {t:'Il 9c Boa va ucciso appena scende', txt:'Con Shanks 10c + Decken, oppure con lo swing da 17k di Shanks: il vero pericolo è il letale da 22k. Se non hanno modo di attaccare DON!! al turno da 9, puoi ucciderlo gratis e restare a una vita un turno in più.'},
    {t:'Luna solo per necessità', txt:'Boa può triggerare corpi per schivare Luna, quindi giocala a fine turno; e giocarla consuma il DON!! che ti serve per i counter event da 4k contro l\'unblockable. Prima di andare per il letale conta le carte in mano avversarie, non la vita: possono curare 1 + 2 blocker + 2 heal trigger = cinque vite in un turno.'},
  ],
  carte:['OP14-041','OP13-031','OP17-031','OP17-022','OP08-036'],
},
{
  id:'py-pudding', nome:'Purple Yellow Pudding', carta:'OP08-058', colore:'Viola/Giallo',
  tier:'fav', sintesi:'Il più fragile fra i mazzi gialli: il suo strumento difensivo principale è invalidato da 10c Shanks.',
  nautilus:true,
  verdetti:[
    {f:'neb', v:'fav', txt:'<b>Go First</b> — "1st: Very Favored / 2nd: Very Favored". Mulligan: Hard Mulligan for Yasopp.'},
  ],
  accordo:[
    '<b>Si va primi</b> pur essendo Very Favored da entrambe le parti.',
    '<b>Hard mulligan per Yasopp</b>, che è lo strumento di controllo board del matchup.',
  ],
  conflitti:[],
  boxes:[
    {t:'Perché è il giallo più fragile', txt:'Il suo strumento difensivo principale è completamente invalidato da 10c Shanks: non ha il counter del Gum Gum Giant per proteggere i pezzi riposati.'},
    {t:'L\'ordine del turno è tutto', txt:'<b>Attacca con le tue unità PRIMA di usare i DON!! per minacciare il KO di Decken sull\'8c Katakuri.</b> Con i fishmen, Katakuri si neutralizza semplicemente ordinando bene il turno.'},
    {t:'Sequenza di rimozione', txt:'Prima uccidi i 10c Big Mom, poi l\'8c Katakuri, così non può bloccare gratis i tuoi swing in eccesso prima che tu giochi il 10c Shanks. Se blocca avidamente con Katakuri presto nel tuo turno, poppalo con Decken e poi rimbalzalo in mano con 6 Law per la 10 Mom successiva.'},
    {t:'It\'s to Die For', txt:'Non ci si gioca attorno: devi comunque sviluppare board per interagire. Consideralo solo se il doppio ramp le farebbe raggiungere 10 DON!! un turno prima.'},
  ],
  carte:['OP08-058','OP17-031','OP17-022','OP06-033'],
},
{
  id:'luffy-ace', nome:'Red Green Luffy & Ace', carta:'ST30-001', colore:'Rosso/Verde',
  tier:'fav', sintesi:'Favorevole, con una differenza di mezzo gradino fra andare primi e secondi.',
  verdetti:[
    {f:'neb', v:'fav', txt:'<b>Go Second</b> — "1st: Slightly Favored / 2nd: Favored". Mulligan: Luna, Oden.'},
    {f:'raph', v:'fav', txt:'Tier list: <b>Slightly Favored</b> (Luffy & Ace). Nel capitolo "vs The Field" c\'è la sezione col video di gameplay.'},
    {f:'sam', v:'fav', txt:'Sezione "Mihawk vs Ace Luffy" con identità del matchup e play pattern.'},
  ],
  accordo:[
    '<b>Si va secondi.</b>',
    '<b>Luna e Oden sono le carte da cercare</b> (mulligan dichiarato da Nebulus).',
  ],
  conflitti:[],
  carte:['ST30-001','OP08-036','ST32-002','OP17-022'],
},
];

/* matchup citati dalle fonti ma senza contenuto sufficiente per una scheda */
const MATCHUP_APERTI = [
  {nome:'Red Newgate', nota:'Raphterra lo elenca nel capitolo "vs The Field" ma il contenuto è letteralmente "To Follow".'},
  {nome:'Red Green Luffy', nota:'Stessa cosa: sezione presente, contenuto "To Follow".'},
  {nome:'UP Luffy', nota:'NebulusTCG lo mette fra i matchup "che sto perdendo" e che deve testare di più.'},
  {nome:'Shanks · UG Zonji · PY Rosinante · B Imu · RG Luffy', nota:'NebulusTCG: "MU\'s that should be free which I haven\'t tested".'},
];

/* Tutti i video delle guide, con categoria e matchup di riferimento. */
const VIDEO = [
 /* ---- Impact / samsansOP: le due lezioni lunghe ---- */
 {src:'Impact', cat:'Lezioni complete', t:'Hawk Guide Law/Yasopp Version — video-lezione della guida',
  u:'https://www.youtube.com/watch?v=EkvbqZMAk5w', note:'2h08 · versione Law + Yasopp. La lezione integrale che accompagna il PowerPoint.', mu:'generale'},
 {src:'samsansOP', cat:'Lezioni complete', t:'OP17 Mihawk Deep Dive',
  u:'https://www.youtube.com/watch?v=MB2ejUdFAkY', note:'2h00 · versione Mihawk 6c + Perona 5c. Analisi carta per carta e matchup.', mu:'generale'},

 /* ---- Raphterra · Deckbuilding ---- */
 {src:'Raphterra', cat:'Deckbuilding', t:'10C Shanks — Mihawk vs Green Shanks',
  u:'https://www.youtube.com/watch?v=ziYvNYx2oPo', note:'Perché 10C Shanks ridisegna il mazzo.', mu:'shanks'},
 {src:'Raphterra', cat:'Deckbuilding', t:'Pacchetto Slash e Wano — Mihawk vs Kaido',
  u:'https://www.youtube.com/watch?v=H35-mI-o2RM', note:'Il core di consistenza in partita.', mu:'kaido'},
 {src:'Raphterra', cat:'Deckbuilding', t:'Mid game — Mihawk Mirror #1',
  u:'https://www.youtube.com/watch?v=jNf7esBF3k8', note:'Mirror: come si costruisce il mid game.', mu:'mirror'},
 {src:'Raphterra', cat:'Deckbuilding', t:'Boss alternativi — Mihawk Mirror #2',
  u:'https://www.youtube.com/watch?v=wcwswJAbqH0', note:'Mirror: Law &amp; Bepo e gli altri boss.', mu:'mirror'},

 /* ---- Raphterra · Gameplay ---- */
 {src:'Raphterra', cat:'Gameplay', t:'La forza dei turni consecutivi 6+5',
  u:'https://www.youtube.com/watch?v=lbDV-kyqFFE', note:'Il pattern di gioco centrale del mazzo.', mu:'generale'},
 {src:'Raphterra', cat:'Gameplay', t:'Il piano di gioco di Mihawk',
  u:'https://www.youtube.com/watch?v=DbUYJYF0VIo', note:'Gameplan completo dall\'early al lethal.', mu:'generale'},
 {src:'Raphterra', cat:'Gameplay', t:'Lethal e gestione DON!! — vs Purple Kaido',
  u:'https://www.youtube.com/watch?v=Kax-5VWfyNo', note:'Come si conta il letale gestendo i DON!!.', mu:'kaido'},
 {src:'Raphterra', cat:'Gameplay', t:'Recuperare una partita difficile — vs Black Luffy',
  u:'https://www.youtube.com/watch?v=oz2kaM0RwLQ', note:'Rimonta da una posizione compromessa.', mu:'black luffy'},

 /* ---- Raphterra · Matchup meta ---- */
 {src:'Raphterra', cat:'Matchup — Meta', t:'Green Mihawk Mirror — pezzi chiave del mid game',
  u:'https://www.youtube.com/watch?v=ltsztajAkow', note:'Mirror.', mu:'mirror'},
 {src:'Raphterra', cat:'Matchup — Meta', t:'Green Mihawk Mirror — rispondere a 10C Shanks (1)',
  u:'https://www.youtube.com/watch?v=JbJ5hnCK_KQ', note:'Mirror: come si risponde al boss avversario.', mu:'mirror'},
 {src:'Raphterra', cat:'Matchup — Meta', t:'Green Mihawk Mirror — rispondere a 10C Shanks (2)',
  u:'https://www.youtube.com/watch?v=i-IYSktDic8', note:'Mirror: seconda linea di risposta.', mu:'mirror'},
 {src:'Raphterra', cat:'Matchup — Meta', t:'Green Mihawk Mirror — valutare il lethal',
  u:'https://www.youtube.com/watch?v=7pN-9eYMTmA', note:'Mirror: leggere la distanza dal letale.', mu:'mirror'},
 {src:'Raphterra', cat:'Matchup — Meta', t:'Purple Yellow Robin — turno di 10C Linlin',
  u:'https://www.youtube.com/watch?v=XxhhCYF5AE8', note:'Il turno che decide il matchup giallo.', mu:'py robin'},
 {src:'Raphterra', cat:'Matchup — Meta', t:'Purple Yellow Robin — quando il piano va storto',
  u:'https://www.youtube.com/watch?v=OOOljBLILkI', note:'Recupero contro Robin.', mu:'py robin'},
 {src:'Raphterra', cat:'Matchup — Meta', t:'Black Luffy — counter e rimozioni',
  u:'https://www.youtube.com/watch?v=K4ULh4SpmyU', note:'Gestione delle rimozioni contro Elbaph.', mu:'black luffy'},
 {src:'Raphterra', cat:'Matchup — Meta', t:'Black Luffy — esempio aggiuntivo',
  u:'https://www.youtube.com/watch?v=G-ZkmpkNbuU', note:'Seconda partita commentata.', mu:'black luffy'},
 {src:'Raphterra', cat:'Matchup — Meta', t:'Red Black Sabo — dopo il primo turno d\'attacco',
  u:'https://www.youtube.com/watch?v=w5PaRMl7JBU', note:'⚠️ Il capitolo scritto su Sabo è troncato nella fonte: questo video è la parte recuperabile.', mu:'rb sabo'},
 {src:'Raphterra', cat:'Matchup — Meta', t:'Red Black Sabo — piano di gioco',
  u:'https://www.youtube.com/watch?v=RXMHl4c54UU', note:'⚠️ Vedi sopra: qui c\'è il gameplan che manca nel testo.', mu:'rb sabo'},
 {src:'Raphterra', cat:'Matchup — Meta', t:'Purple Enel — arrivare al turno di Shanks',
  u:'https://www.youtube.com/watch?v=gpRh_nFnocA', note:'Sopravvivere fino al turno bomba.', mu:'enel'},
 {src:'Raphterra', cat:'Matchup — Meta', t:'Purple Enel — nuova versione',
  u:'https://www.youtube.com/watch?v=9ATwHjfoo40', note:'Contro la lista Enel aggiornata.', mu:'enel'},

 /* ---- Raphterra · Matchup field ---- */
 {src:'Raphterra', cat:'Matchup — Field', t:'Blue Rocks',
  u:'https://www.youtube.com/watch?v=10Oy3KJZWfQ', note:'Il matchup più favorevole insieme a Kaido.', mu:'rocks'},
 {src:'Raphterra', cat:'Matchup — Field', t:'Red Green Luffy & Ace',
  u:'https://www.youtube.com/watch?v=33c_ALHCmsg', note:'', mu:'luffy ace'},
 {src:'Raphterra', cat:'Matchup — Field', t:'Purple Kaido',
  u:'https://www.youtube.com/watch?v=26mU1XokeuM', note:'', mu:'kaido'},
];

# WORK-IN-PROGRESS 👷

### Studente proponente
s323600 Cavallo Gabriele

### Titolo della proposta
Simulatore degli effetti sul bilancio di decisioni di investimento aziendale - BusinessScenarioLab

### Descrizione del problema proposto
Le aziende private utilizzano sempre di più software gestionali per effettuare valutazioni ex-post della situazione aziendale e prendere decisioni. Funzionalità come la gestione delle fatture elettroniche e la redazione automatica dei bilanci sono ormai diffuse. 
Poche aziende invece utilizzano **strumenti di simulazione** per provare ad ipotizzare gli **effetti futuri** delle loro decisioni di investimento sugli indici aziendali. 
Lo strumento ha l'obiettivo di permettere, a partire da uno o più bilanci storici aziendali presenti in un dataset, di **simulare l'effetto di decisioni di investimento** tramite l'osservazione della variazione degli indici di bilancio, la presentazione di grafici calcolati in automatico e la produzione dei tipici documenti riassuntivi (conto economico, stato patrimoniale, prospetto dei flussi di cassa). Inoltre, fornirà la possibilità di valutare **progetti di investimento strutturati** e composti da più micro-investimenti, unendo i diversi effetti. 

### Descrizione della rilevanza gestionale del problema
Lo strumento proposto impatta direttamente la gestione aziendale, permettendo a chi lo usa di simulare in modo semplice gli effetti di decisioni future sulla struttura aziendale e di confrontare scenari diversi. 
Il problema è rilevante perchè permette a chi utilizza lo strumento di non dover conoscere gli algoritmi di calcolo e i meccanismi economico/finanziari alla base dell'impresa per avere una prima valutazione degli impatti futuri di decisioni prese. 

### Descrizione dei data-set per la valutazione	
Lo strumento utilizzerà dati reali di aziende (PMI non quotate) italiane, scaricati da questo dataset:
* AIDA - Orbis for Italy - Moody's https://www.polito.it/impatto-sociale/biblioteche-di-ateneo/risorse-elettroniche/banche-dati-in-abbonamento
Il dataset contiene informazioni delle aziende italiane, tra cui quelle finanziarie e di bilancio. In base a quanto indicato sul sito del Politecnico, è già disponibile una licenza in libreria. Tutte le informazioni possono essere scaricate selezionando una specifica azienda in diversi formati. Siccome le API (che sarebbero comode per non dover scaricare il dataset in locale) non sono tipicamente incluse nella licenza universitaria, si procederà scaricando manualmente un dataset rappresentativo di aziende italiane e il software si occuperà del caricamento dei dati a partire dall'excel/CSV prodotto dalla base dati AIDA. 

### Descrizione preliminare degli algoritmi coinvolti
L'applicativo si basa sull'utilizzo di una **simulazione DES** (Discrete Event Simulation) dell'andamento aziendale. Il bilancio e gli indici aziendali vengono caricati nello stato della simulazione e i progetti di investimento de-strutturati in eventi discreti che impattano il bilancio. La simulazione è eseguita su un orizzonte temporale definito e utilizza i dati presenti nel dataset, producendo degli snapshot di potenziali situazioni finali. 
Nella simulazione verranno inserite **distribuzioni statistiche**, come ad esempio la possibilità di specificare una **distribuzione di probabilità per la domanda** o per il **fatturato**. Inoltre, se presenti dati storici (ad esempio di fatturato o di vendite unitarie) verranno forniti algoritmi di **previsione con Time Series** per integrare nella simulazione una previsione sensata dei ricavi.
In questo modo le diverse esecuzioni forniranno **output più realistici** utilizzando input diversi ad ogni esecuzione. 
L'applicativo, sfruttando la simulazione DES, farà anche una **valutazione del Valore Attuale Netto** del progetto di investimento e del **TIR** (Tasso Interno di Rendimento + Tempo di rientro). I **flussi di cassa** per la valutazione sono direttamente generati dagli eventi della simulazione, il cui spawn avverrà in base agli **effetti previsti** dal **tipo di investimento** e alle logiche interne di funzionamento dell'impresa. 

#### Tech stack
Il tech stack proposto è: Python, SimPy (per implementazione simulazione DES), per la UI Flet oppure PyQt (porting Python della libreria Qt), per i grafici MatplotLib, per la statistica NumPy/Pandas/SciPy

### Descrizione preliminare delle funzionalità previste per l’applicazione software	
1) L'utente **seleziona un'impresa** su cui lavorare (tra quelle disponibili nel dataset AIDA). Inizialmente **visualizza i dati disponibili** per quell'impresa (bilanci depositati, informazioni generali) e gli **indici iniziali** calcolati dal software (situazione iniziale). Eventualmente, fornisce informazioni aggiuntive se necessarie
2) L'utente inserisce un **progetto di investimento**, composto da una serie di **sotto-moduli** da aggiungere in un **apposito pannello** (ad esempio: "Miglioramento infrastruttura macchine" con costo di 200.000 € e i cui effetti previsti sono la riduzione dei costi operativi del 20% in 3 anni). Per ogni modulo si utilizzerà un ragionamento costo-effetto (quanto costa e quali effetti produce). 
3) L'utente specifica **l'orizzonte temporale di simulazione**, eventuali distribuzioni da utilizzare, il numero di run da eseguire
4) L'applicativo **esegue la simulazione DES**, calcola la **situazione finale (snapshot di bilancio)** e i **grafici** di confronto iniziale-finale, mostrandoli all'utente
5) L'utente **visualizza il confronto** tra la situazione iniziale e quella finale dell'impresa
6) L'utente **salva lo scenario finale prodotto**, eventualmente per confrontarlo con un altro progetto di investimento
7) L'utente **crea un nuovo progetto di investimento**, ottiene una nuova simulazione e fa un confronto tra le situazioni finali con i due progetti di investimento per scegliere quale sia migliore

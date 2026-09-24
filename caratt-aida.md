
## Caratteristiche utili di AIDA
Permette di filtrare per dimensioni delle aziende (piccole, medie e grandi)

Ci sono quasi 3 milioni di società con bilancio su AIDA
Fornisce ricerca per indici. 
Ci sono sia SPA che SRL
Esporta un Excel e posso personalizzare le sezioni
Calcola già gli indici di bilancio
A seconda dell'azienda ho annualità disponibile diverse --> COME GESTIRLE, sono le colonne dell'excel
Esponenti/Manager non servono, neanche gli azionisti
Contiene anche informazioni di contesto sull'impresa (dipendenti, dimensioni) Gruppo dei Pari, classificazione merceologica

Strutturare un database relazionale a partire dalle informazioni dell'excel.
* Perchè dovrò poter salvare gli snapshot della situazione
* Valutare se è meglio crearne uno non relazionale perchè la normativa civilistica impone livelli di dettaglio diversi per i bilanci nelle imprese, quindi spesso potrebbero esserci
campi non esistenti e non è possibile prevederlo a priori. La libreria da utilizzare sarebbe PyMongo

## Dataset di test e produzione
Per il test e lo sviluppo viene utilizzato un dataset contenente i dati di 50 società così ricercate:
* Forma giuridica --> Società di capitali (SRL, SPA, ...)
* Almeno 2 bilanci disponibili
* Numero di dipendenti da 50 a 500 (dimensioni medie dell'impresa)
La zona geografica viene presa in Italia
Per effettuare questa ricerca è stato impostato su Aida una strategia di ricerca con questi 3 criteri. Il dataset generato da AIDA effettuando l'export contiene:
* Lista delle società nel dataset con principali indicatori di filtro (file `dataset-test-companies-listv2.xlsx`)
* Bilanci di tutte le società nel dataset (CE, SP, Indici finanziari e informazioni di mercato) nel file `dataset-test.xlsx`. Ogni società è un foglio diverso dello stesso file. 

### Dataset produzione
Per il dataset in produzione viene utilizzata la stessa struttura ma i dati sono divisi in chunk da 50 società, caricati uno per volta. Il dataset contiene 10 chunk, ossia
500 società con tutti i dati. 
La presenza di questi chunk è dovuta al fatto che AIDA permette di esportare solo 50 report per volta. 

# Architettura generale
Modulo data-import --> Prende l'excel generato con la struttura specifica e lo importa nel DB MongoDB aggiungendo documenti (così può essere utilizzato più volte)
Il programma ragiona e scrive sul db Mongo

## Importazione dei dati
I dati contenuti in un chunk vengono elaborati utilizzando uno script python di importazione per strutturare un database che li renda utilizzabili dall'applicazione. 
Il database è non relazionale (MongoDB) ed ha la seguente struttura:
* Ogni società è un documento con una struttura diversa, perchè a seconda del tipo di società i dati possono variare
* Ogni documento ha una serie di sezioni, ognuna con un titolo (ad esempio Anagrafica, Informazioni commerciali, Profilo Finanziario, etc...), memorizzate come oggetti
* Ogni sezione ha una serie di voci (attributi i cui valori sono sempre vettori per gestire le diverse annualità)
* Ogni sezione può avere delle sotto-sezioni (ad esempio la sezione Stato Patrimoniale ha la sotto-sezione Attivo)

I nomi delle voci sono generati in automatico partendo dal nome della cella e applicando questa trasformazione: 
* Tutto il testo è trasformato in minuscolo
* Gli spazi e altri simboli sono sostituiti con underscore
Per lo stato patrimoniale e il conto economico viene mantenuta la numerazione originale, sostituendo i punti con underscore.

Alcune sezioni scrivono il contenuto mettendo due coppie chiave-valore per riga. Il parser è in grado di accorgersene e gestirlo. Per questo modulo
vengono anche scritti degli unit-test per assicurare il funzionamento anche in edge-cases, basandosi sul dataset di test

# UI Con PyQt
Pacchetto python per utilizzare Qt
Qt Design Studio per generare il Qt-Quick
Posso usarlo sia in modo imperativo che con il qt-quick (vogliono che usi quello imperativo come con flet o posso usare la declarative UI con QML)
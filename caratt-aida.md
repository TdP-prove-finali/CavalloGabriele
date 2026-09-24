
# Caratteristiche utili di AIDA
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

# Architettura
Modulo data-import --> Prende l'excel generato con la struttura specifica e lo importa nel DB MongoDB aggiungendo documenti (così può essere utilizzato più volte)
Il programma ragiona e scrive sul db Mongo

# UI Con PyQt
Pacchetto python per utilizzare Qt
Qt Design Studio per generare il Qt-Quick
Posso usarlo sia in modo imperativo che con il qt-quick (vogliono che usi quello imperativo come con flet o posso usare la declarative UI con QML)
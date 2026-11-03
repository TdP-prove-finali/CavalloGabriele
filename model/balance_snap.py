from copy import deepcopy
from enum import IntEnum
from numbers import Number
from typing import Callable, Any

from model.raw_company_data import CompanyData

class BalanceLocation(IntEnum):
    SP_ATTIVO = 0,
    SP_PASSIVO_DEBITI = 1,
    SP_PASSIVO_PATRIM = 2,
    CE = 3

class BalanceSnaphot:
    def __init__(self,
                 stato_patrimoniale: dict[str, Any],
                 conto_economico: dict[str, Any],
                 indici: dict[str, Any],
                 timestamp: int,
                 sim_id: int,
                 available_years: int,
                 effect_pointer: str | None
                 ):
        self.stato_patrimoniale = stato_patrimoniale
        self.conto_economico = conto_economico
        self.indici = indici
        self.timestamp = timestamp
        self.sim_id = sim_id
        self.effect_pointer = effect_pointer
        self.available_columns = available_years
        self.__integrity__: bool | None = None
        self.__ce_edited_fields__ = []     # Lista con i nomi di tutti i campi i cui valori sono stati modificati a mano
        self.__sp_edited_fields__ = []     # Lista con i nomi di tutti i campi i cui valori sono stati modificati a mano
        # In automatico, i campi da ricalcolare vengono ricavati a partire dai campi che sono stati modificati, secondo la seguente logica:
        # modificato un campo che appartiene alla lettera A (ad esempio A.1) viene ricalcolato il totale alla lettera A
        # e' però necessario specificare anche dei campi che non appartengono a questa logica ma che devono lo stesso essere ricalcolati, come l'utile nel CE o i totali attivo e passivo in SP
        # inoltre alcuni campi per coerenza sono impostati come "no-copy", ossia nonostante nel bilancio storico sia presente un valore iniziale verrà sempre utilizzato 0. Questo è utile per campi
        # che specificano operazioni straordinarie che la simulazione non ripete
        self.__sp_need_recalc_fields = [
            "totale_passivo",
            "totale_attivo"
        ]
        self.__ce_need_recalc_fields = [
            "risultato_prima_delle_imposte"
        ]
        self.__sp_no_copy = [
            # Risultato dell'esercizio da chiudere e destinare
            "aix_utile_frac_perdita_di_esercizio",
            # Operazioni di distribuzione/copertura
            "acconto_dividendi",
            "copertura_parziale_perdita_di_esercizio",
        ]
        self.__ce_no_copy = [
            # Rettifiche di valore delle immobilizzazioni
            "b10c_altre_svalut_immob",

            # Rivalutazioni finanziarie
            "d18a_rivalut_di_partec",
            "d18b_rivalut_di_altre_imm_fin",
            "d18c_rivalut_di_titoli",
            "d18d_rivalut_di_strumenti_finanziari_derivati",
            "rivalut_di_attivita_finanziarie_per_la_gestione_accentrata_della_tesoreria",

            # Svalutazioni finanziarie
            "d19a_svalut_di_partec",
            "d19b_svalut_di_altre_imm_fin",
            "d19c_svalut_di_titoli",
            "d19d_svalut_di_strumenti_finanziari_derivati",
            "svalut_di_attivita_finanziarie_per_la_gestione_accentrata_della_tesoreria",

            # Proventi e oneri straordinari
            "proventi_straordinari",
            "di_cui_plusvalenze",
            "oneri_straordinari",
            "di_cui_minusvalenze",
            "di_cui_imposte_esercizio_precedente",
            "imposte_relative_a_esercizi_precedenti",
        ]

    def verify_integrity(self) -> bool:
        """Verifica l'integrità del bilancio e la quadratura"""
        def verify_row(_, values):
            assert len(values) == self.available_columns

        try:
            self.for_each_ce_field(verify_row)
            self.for_each_sp_field(verify_row)

            if self.sp_totale_attivo != self.sp_totale_passivo:
                print("Warning: Controllo quadratura patrimoniale non passato")

            return True
        except:
            return False

    @property
    def sp_totale_attivo(self):
        return self.stato_patrimoniale["subsections"]["attivo"]["totale_attivo"]

    @property
    def sp_totale_passivo(self):
        return self.stato_patrimoniale["subsections"]["passivo"]["subsections"]["debiti"]["totale_passivo"]

    def create_column(self, title):
        """Crea una nuova colonna nei dati (tipicamente per un nuovo mese della simulazione) e inizializza tutti i campi a 0, assicurando
        che tutti i vettori dei valori dei campi di tutti i documenti contengano lo stesso numero di elementi orizzontali"""
        def value_factory(key, value):
            if key == "data":
                value.append(title)
            elif len(value) > 0 and type(value[0]) is int:
                value.append(0)
            elif len(value) > 0 and type(value[0]) is float:
                value.append(0.0)
            elif len(value) > 0 and type(value[0]) is str:
                value.append("")
            elif len(value) > 0 and value[0] is None:
                value.append(None)
            else:
                print("WARNING: Impossibile capire il tipo da aggiungere per il campo " + key)
                value.append(None)

        self.for_each_ce_field(value_factory)
        self.for_each_sp_field(value_factory)
        self.available_columns += 1

    def first_non_null_val(self, s_index: int, field_name: str, location: BalanceLocation):
        f_data = self.get_field_data(location, field_name)
        for i in range(s_index, -1, -1):
            if f_data[i] is not None and f_data[i] > 0:
                return f_data[i]

        return None

    def __mark_edited(self, field_name, sp):
        if sp and field_name not in self.__sp_edited_fields__:
            self.__sp_edited_fields__.append(field_name)
        elif not sp and field_name not in self.__ce_edited_fields__:
            self.__ce_edited_fields__.append(field_name)

    def set_field_value(self, field_name: str, location: BalanceLocation, value: Any, month: int):
        """Imposta il valore del campo identificato da
        :param field_name alla colonna month """
        if location == BalanceLocation.SP_ATTIVO:
            self.stato_patrimoniale["subsections"]["attivo"][field_name][month] = value
            self.__mark_edited(field_name, True)
        elif location == BalanceLocation.SP_PASSIVO_DEBITI:
            self.stato_patrimoniale["subsections"]["passivo"]["subsections"]["debiti"][field_name][month] = value
            self.__mark_edited(field_name, True)
        elif location == BalanceLocation.SP_PASSIVO_PATRIM:
            self.stato_patrimoniale["subsections"]["passivo"]["subsections"]["patrimonio_netto"][field_name][month] = value
            self.__mark_edited(field_name, True)
        elif location == BalanceLocation.CE:
            self.conto_economico[field_name][month] = value
            self.__mark_edited(field_name, False)

    def get_field_value(self, where: BalanceLocation, field_name, month):
        """Restituisce il valore del campo alla colonna giusta"""
        if where == BalanceLocation.CE:
            return self.conto_economico.get(field_name)[month]
        elif where == BalanceLocation.SP_ATTIVO:
            return self.stato_patrimoniale["subsections"]["attivo"].get(field_name)[month]
        elif where == BalanceLocation.SP_PASSIVO_DEBITI:
            return self.stato_patrimoniale["subsections"]["passivo"]["subsections"]["debiti"].get(field_name)[month]
        elif where == BalanceLocation.SP_PASSIVO_PATRIM:
            return self.stato_patrimoniale["subsections"]["passivo"]["subsections"]["patrimonio_netto"].get(field_name)[month]

        raise ValueError("Non è stato possibile trovare il campo " + field_name + " nella posizione " + where)

    def get_field_data(self, where: BalanceLocation, field_name):
        """Restituisce il valore del campo oppure None se non esiste"""
        if where == BalanceLocation.CE:
            return self.conto_economico.get(field_name)
        elif where == BalanceLocation.SP_ATTIVO:
            return self.stato_patrimoniale["subsections"]["attivo"].get(field_name)
        elif where == BalanceLocation.SP_PASSIVO_DEBITI:
            return self.stato_patrimoniale["subsections"]["passivo"]["subsections"]["debiti"].get(field_name)
        elif where == BalanceLocation.SP_PASSIVO_PATRIM:
            return self.stato_patrimoniale["subsections"]["passivo"]["subsections"]["patrimonio_netto"].get(field_name)

        return None

    def calc_indicies(self):
        """Calcola gli indici di bilancio"""
        # TODO: Implement
        pass

    def calc_terminal_fields(self):
        """
        Calcola le voci finali del documento come la cassa e i totali
        :return:
        """
        # TODO: Implement
        pass

    def aggregate_by_year(self, number_of_years: int):
        """
        Restituisce un nuovo snapshot di bilancio in cui i dati non sono aggregati per mesi ma per anni
        Orizzontalmente, le colonne sono aggregate in ogni anno. Tutti i valori non modificati in un certo mese
        vengono lasciati a 0 per far sì che ricompaia il valore storico nella voce, senza perdita di dati o duplicazione.
        Tutti gli effetti indicano nella colonna corrispondente solo il nuovo valore, se presente.
        :return:
        """

        def aggr(key, values: list[Any]):
            histor_value = values[0]
            groups = [values[i:i + 12] for i in range(1, len(values), 12)]

            s = None
            new_cols = []

            for g in groups:
                if key in self.__sp_no_copy or key in self.__ce_no_copy or key in self.__sp_need_recalc_fields or key in self.__ce_need_recalc_fields:
                    s = 0       # Tutti i campi che non possono essere copiati o che necessitano esplicitamente di essere ricalcolati vengono inizializzati a 0 e poi gestiti successivamente

                for item in g:
                    if type(item) is int or type(item) is float:
                        if s is None:
                            s = item + histor_value
                        elif type(s) is int or type(s) is float:
                            s += item
                    elif item is None and s is None:
                        break       # Al primo elemento None viene aggiunta la colonna dell'anno come None e si passa al prossimo gruppo
                    elif type(item) is not int and type(item) is not float:
                        if item == "" or item is None:
                            s = histor_value
                        else:
                            s = item
                        break
                new_cols.append(s)
                s = None

            return [values[0]] + new_cols

        return self.advanced_copy(
            aggr, aggr, number_of_years + 1
        )

    def for_each_ce_field(self, function: Callable[[str, list[Any]], None | list[Any]],
                          substitute: bool = False):
        for key in list(self.conto_economico.keys()):
            if key != "subsections":
                if not substitute:
                    function(key, self.conto_economico[key])
                else:
                    self.conto_economico[key] = function(key, self.conto_economico[key])

    def for_each_sp_field(self,
                          function: Callable[[str, list[Any]], None | list[Any]],
                          substitute: bool = False
                          ):
        """
        Applica una trasformazione a tutti i campi dello stato patrimoniale, opzionalmente sostituendo i valori di tale campo
        :param function: Funzione da applicare. Se viene impostato substitute a True il valore di ritorno deve essere la lista dei nuovi valori del campo.
        :param substitute:
        :return:
        """
        def visit(section: dict[str, Any]) -> None:
            for key, value in section.items():

                if key == "subsections":
                    for subsection in value.values():
                        visit(subsection)
                else:
                    if not substitute:
                        function(key, value)
                    else:
                        section[key] = function(key, value)

        visit(self.stato_patrimoniale)

    @staticmethod
    def copy_last_balance(company_data):
        result = deepcopy(company_data)
        visited = set()

        def transform(value):
            if isinstance(value, list):
                if any(isinstance(item, dict) for item in value):
                    return [transform(item) for item in value]

                return value[0:1]

            if isinstance(value, dict):
                for key, item in value.items():
                    value[key] = transform(item)
                return value

            if isinstance(value, tuple):
                return tuple(transform(item) for item in value)

            if hasattr(value, "__dict__"):
                if id(value) in visited:
                    return value

                visited.add(id(value))

                for name, item in vars(value).items():
                    setattr(value, name, transform(item))

            return value

        return transform(result)

    def copy(self):
        """
        Restituisce una nuova copia identica dello snapshot di bilancio corrente
        Utile per svolgere ulteriori operazioni retro-compatibili
        :return:
        """
        return BalanceSnaphot(
            stato_patrimoniale=self.stato_patrimoniale.copy(),
            conto_economico=self.conto_economico.copy(),
            indici=self.indici.copy(),
            timestamp=self.timestamp,
            sim_id=self.sim_id,
            available_years=self.available_columns,
            effect_pointer=self.effect_pointer
        )

    def advanced_copy(self,
                      stato_patrimon_transformer: Callable[[str, list[Any]], list[Any]],
                      conto_economico_transformer: Callable[[str, list[Any]], list[Any]],
                      new_column_count: int
                      ):
        """
        Crea una copia dello snapshot di bilancio applicando prima una trasformazione su tutte le righe dei bilanci.
        Questa trasformazione può cambiare il numero di colonne, portandolo ad un valore a piacere che deve però coincidere
        per tutti i campi.
        :param stato_patrimon_transformer: Funzione che trasforma ogni campo dello stato patrimoniale
        :param conto_economico_transformer: Funzione che trasforma ogni campo del conto economico

        Entrambe le funzioni devono restituire la nuova lista di valori del campo e non modificar
        :return:
        """
        tot_cp = self.copy()
        tot_cp.for_each_sp_field(stato_patrimon_transformer, substitute=True)
        tot_cp.for_each_ce_field(conto_economico_transformer, substitute=True)
        tot_cp.calc_indicies()
        tot_cp.available_columns = new_column_count
        tot_cp.calc_terminal_fields()
        if not tot_cp.verify_integrity():
            raise Exception("Trasformazione non consistente sullo snapshot di bilancio. La trasformazione che hai specificato non porta ad avere un bilancio valido. ")

        tot_cp.timestamp = self.timestamp
        return tot_cp

    @staticmethod
    def from_company_data(data: CompanyData,
                          timestamp: int,
                          sim_id: int,
                          effect_pointer: str | None,
                          single_year: bool = True
                          ):
        """
        Crea uno snapshot dei dati a partire dal company data complessivo
        :param data:
        :param single_year: Permette di specificare opzionalmente un anno singolo da mantenere, altrimenti verranno mantenuti tutti
        :return:
        """
        if not single_year:
            return BalanceSnaphot(data.stato_patrimoniale.copy(), data.conto_economico.copy(), data.indici.copy(), timestamp, sim_id, data.available_years, effect_pointer)
        else:
            return BalanceSnaphot(
                stato_patrimoniale=BalanceSnaphot.copy_last_balance(data.stato_patrimoniale),
                conto_economico=BalanceSnaphot.copy_last_balance(data.conto_economico),
                indici=data.indici.copy(),
                timestamp=timestamp,
                sim_id=sim_id,
                available_years=1,
                effect_pointer=effect_pointer
            )
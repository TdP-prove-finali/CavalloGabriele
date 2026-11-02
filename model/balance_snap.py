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

    def verify_integrity(self) -> bool:
        """Verifica l'integrità del bilancio e la quadratura"""
        def verify_row(_, values):
            assert len(values) == self.available_columns

        try:
            self.for_each_ce_field(verify_row)
            self.for_each_sp_field(verify_row)
            return True
        except:
            return False

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

    def set_field_value(self, field_name: str, location: BalanceLocation, value: Any, month: int):
        """Imposta il valore del campo identificato da
        :param field_name alla colonna month """
        if location == BalanceLocation.SP_ATTIVO:
            self.stato_patrimoniale["subsections"]["attivo"][field_name][month] = value
        elif location == BalanceLocation.SP_PASSIVO_DEBITI:
            self.stato_patrimoniale["subsections"]["passivo"]["subsections"]["debiti"][field_name][month] = value
        elif location == BalanceLocation.SP_PASSIVO_PATRIM:
            self.stato_patrimoniale["subsections"]["passivo"]["subsections"]["patrimonio_netto"][field_name][month] = value
        elif location == BalanceLocation.CE:
            self.conto_economico[field_name][month] = value

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

    def aggregate_by_year(self):
        """
        Restituisce un nuovo snapshot di bilancio in cui i dati non sono aggregati per mesi ma per anni
        Orizzontalmente, le colonne sono aggregate in ogni anno. Tutti i valori non modificati in un certo mese
        vengono lasciati a 0 per far sì che ricompaia il valore storico nella voce, senza perdita di dati o duplicazione.
        Tutti gli effetti indicano nella colonna corrispondente solo il nuovo valore, se presente.
        :return:
        """
        # TODO: Implement
        return self

    def for_each_ce_field(self, function: Callable):
        for key in list(self.conto_economico.keys()):
            if key != "subsections":
                function(key, self.conto_economico[key])

    def for_each_sp_field(self, function: Callable):
        def visit(section: dict[str, Any]) -> None:
            for key, value in section.items():

                if key == "subsections":
                    for subsection in value.values():
                        visit(subsection)
                else:
                    function(key, value)

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
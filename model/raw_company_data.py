from dataclasses import dataclass, field
from enum import Enum, IntEnum
from functools import cached_property
from typing import Any, Callable

from model.section import Section

class BalanceLocation(IntEnum):
    SP_ATTIVO = 0,
    SP_PASSIVO_DEBITI = 1,
    SP_PASSIVO_PATRIM = 2,
    CE = 3

@dataclass
class RawCompanyData:
    """Rappresenta i dati di una company caricati da un file Excel, senza rielaborazioni. 
    Le sections sono memorizzate come vettore per poter gestire la possibilità in cui non siano messe nello stesso ordine all'interno del file. """
    sections: list[Section] = field(default_factory=list)

@dataclass(frozen=True)
class CompanyBrief:
    company_name: str
    fiscal_code: str

@dataclass
class CompanyData:
    """
    Classe che rappresenta una company con i dati completi dopo la fase di ri-elaborazione interna
    """
    company_name: str
    fiscal_code: str
    general_info: dict[str, Any] = field(default_factory=dict)
    anagrafica: dict[str, Any] = field(default_factory=dict)
    informazioni_commerciali_e_legali: dict[str, Any] = field(default_factory=dict)
    dimensioni_e_gruppo: dict[str, Any] = field(default_factory=dict)
    gruppo_dei_pari: dict[str, Any] = field(default_factory=dict)
    overview_completa: dict[str, Any] = field(default_factory=dict)
    profilo_finanziario: dict[str, Any] = field(default_factory=dict)
    stato_patrimoniale: dict[str, Any] = field(default_factory=dict)
    conto_economico: dict[str, Any] = field(default_factory=dict)
    indici: dict[str, Any] = field(default_factory=dict)

    @property
    def available_years(self) -> int:
        return self.informazioni_commerciali_e_legali["numero_di_anni_disponibili"]


class BalanceSnaphot:
    def __init__(self,
                 stato_patrimoniale: dict[str, Any],
                 conto_economico: dict[str, Any],
                 indici: dict[str, Any],
                 timestamp: tuple[int, int],
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

    def set_field_value(self, field_name: str, location: BalanceLocation, value: Any, month: int, year: int):
        """Imposta il valore del campo identificato da
        :param field_name alla colonna year*12 + month """
        if location == BalanceLocation.SP_ATTIVO:
            self.stato_patrimoniale["subsections"]["attivo"][field_name][year * 12 + month] = value
        elif location == BalanceLocation.SP_PASSIVO_DEBITI:
            self.stato_patrimoniale["subsections"]["passivo"]["subsections"]["debiti"][field_name][year * 12 + month] = value
        elif location == BalanceLocation.SP_PASSIVO_PATRIM:
            self.stato_patrimoniale["subsections"]["passivo"]["subsections"]["patrimonio_netto"][field_name][year * 12 + month] = value
        elif location == BalanceLocation.CE:
            self.conto_economico[field_name][year * 12 + month] = value

    def get_field_value(self, field_name, month, year):
        """Restituisce il valore del campo alla colonna giusta"""
        pass

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
    def from_company_data(data: CompanyData,
                          timestamp: tuple[int, int],
                          sim_id: int,
                          effect_pointer: str | None,
                          single_year: int | None = None
                          ):
        """
        Crea uno snapshot dei dati a partire dal company data complessivo
        :param data:
        :param single_year: Permette di specificare opzionalmente un anno singolo da mantenere, altrimenti verranno mantenuti tutti
        :return:
        """
        # TODO: Implement single_year
        return BalanceSnaphot(data.stato_patrimoniale.copy(), data.conto_economico.copy(), data.indici.copy(), timestamp, sim_id, data.available_years, effect_pointer)

from dataclasses import dataclass
from functools import cached_property
from typing import Any


def clear_section(section: dict[str, Any]):
    """Rimuove dai dati di una sezione le indicazioni di eventuali sotto-sezioni"""
    if section.get("subsections") is not None:
        section.pop("subsections")

    return section.copy()

def find_key_by_token(data: dict, token: str) -> str | None:
    return next((key for key in data if token in key), None)

# Rappresenta una sezione generica del file excel con tutti i dati della company
@dataclass
class Section:
    name: str
    data: dict
    __last__row__name = None        # Nome dell'ultima riga che ho aggiunto

    def append_row(self, rowName, values):
        self.data[rowName] = values
        self.__last__row__name = rowName

    @property
    def last_added_row_name(self):
        return self.__last__row__name

class SPSection:
    """
    Rappresenta lo stato patrimoniale con le sue sotto-sezioni
    """

    def __init__(self, context, attivo, debiti, patrimonio_netto):
        self.context: dict[str, Any] = clear_section(context)
        self.attivo: dict[str, Any] = clear_section(attivo)
        self.debiti: dict[str, Any] = clear_section(debiti)
        self.patrimonio_netto: dict[str, Any] = clear_section(patrimonio_netto)

    @cached_property
    def passivo(self):
        return {
            "debiti": self.debiti,
            "patrimonio_netto": self.patrimonio_netto
        }

    @cached_property
    def count_attivo_fields(self):
        return len(self.attivo.keys())

    @cached_property
    def count_passivo_fields(self):
        return len(self.passivo.keys())

    @cached_property
    def count_debiti_fields(self):
        return len(self.debiti.keys())

    @cached_property
    def count_patrimon_fields(self):
        return len(self.patrimonio_netto.keys())

    def get_attivo_key(self, index: int):
        return list(self.attivo.keys())[index]

    def get_passivo_key(self, index: int):
        return list(self.passivo.keys())[index]

    def get_debiti_key(self, index: int):
        return list(self.debiti.keys())[index]

    def get_patrimn_key(self, index: int):
        return list(self.patrimonio_netto.keys())[index]

    @staticmethod
    def fromSection(section: dict):
        return SPSection(
            context={"data": section["data"],
                     "moneta": section["moneta"],
                     "periodo": section["periodo"]},
            attivo=section["subsections"]["attivo"],
            debiti=section["subsections"]["passivo"]["subsections"]["debiti"],
            patrimonio_netto=section["subsections"]["passivo"]["subsections"]["patrimonio_netto"],
        )

class IndiciesSection:
    def __init__(self, context, financiary: dict[str, Any], current_period, revenue, productivity, signif_data):
        self.context: dict[str, Any] = clear_section(context)
        self.financiary: dict[str, Any] = clear_section(financiary)
        self.current_period: dict[str, Any] = clear_section(current_period)
        self.revenue: dict[str, Any] = clear_section(revenue)
        self.productivity: dict[str, Any] = clear_section(productivity)
        self.signif_data: dict[str, Any] = clear_section(signif_data)

    @staticmethod
    def fromSection(section: dict):
        return IndiciesSection(
            context={"data": section["data"],
                     "moneta": section["moneta"],
                     "periodo": section["periodo"]},
            financiary=section["subsections"][find_key_by_token(section["subsections"], "indicatori_finanziari")],
            current_period=section["subsections"][find_key_by_token(section["subsections"], "gestione_corrente")],
            revenue=section["subsections"][find_key_by_token(section["subsections"], "redditivita")],
            productivity=section["subsections"][find_key_by_token(section["subsections"], "produttivita")],
            signif_data=section["subsections"][find_key_by_token(section["subsections"], "dati_significativi")],
        )
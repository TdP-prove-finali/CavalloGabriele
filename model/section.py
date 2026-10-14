
from dataclasses import dataclass
from functools import cached_property
from typing import Any

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
        self.context: dict[str, Any] = self.__clear_section__(context)
        self.attivo: dict[str, Any] = self.__clear_section__(attivo)
        self.debiti: dict[str, Any] = self.__clear_section__(debiti)
        self.patrimonio_netto: dict[str, Any] = self.__clear_section__(patrimonio_netto)

    def __clear_section__(self, section: dict[str, Any]):
        if section.get("subsections") is not None:
            section.pop("subsections")

        return section.copy()

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
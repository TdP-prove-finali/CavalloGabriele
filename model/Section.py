
from dataclasses import dataclass

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


@dataclass
class GeneralInfoSection(Section):
    nome_azienda: str
    sede: str
    codice_fiscale: str
    numero_cciaa: str
    descrizione: str

from dataclasses import dataclass

# Rappresenta una sezione generica del file excel con tutti i dati della company
@dataclass
class Section:
    name: str
    data: dict

@dataclass
class GeneralInfoSection(Section):
    nome_azienda: str
    sede: str
    codice_fiscale: str
    numero_cciaa: str
    descrizione: str
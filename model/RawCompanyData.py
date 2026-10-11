from dataclasses import dataclass, field
from functools import cached_property
from typing import Any

from model.Section import Section

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

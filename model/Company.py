from dataclasses import dataclass, field
from functools import cached_property

from model.Section import Section

@dataclass
class Company:
    sections: list[Section] = field(default_factory=list)

@dataclass(frozen=True)
class CompanyBrief:
    nome: str
    codice_fiscale: str

class CompanyReader:
    """
    Classe per semplificare la lettura della struttura dati con le informazioni dell'azienda
    """
    def __init__(self, company):
        self.__company__ = company

    @cached_property
    def general_info(self) -> Section:
        if len(self.__company__.sections) > 0:
            return list(filter(lambda t: t.name == "general_info", self.__company__.sections))[0]

        raise Exception("Company non inizializzata")

    @cached_property
    def anagrafica(self) -> Section:
        if len(self.__company__.sections) > 0:
            return list(filter(lambda t: t.name == "anagrafica", self.__company__.sections))[0]

        raise Exception("Company non inizializzata")

    @cached_property
    def informazioni_comm(self) -> Section:
        if len(self.__company__.sections) > 0:
            return list(filter(lambda t: t.name == "informazioni_commerciali_e_legali", self.__company__.sections))[0]

        raise Exception("Company non inizializzata")

    @cached_property
    def dimensioni_e_gruppo(self) -> Section:
        if len(self.__company__.sections) > 0:
            return list(filter(lambda t: t.name == "dimensioni_e_gruppo", self.__company__.sections))[0]

        raise Exception("Company non inizializzata")

    @cached_property
    def gruppo_dei_pari(self) -> Section:
        if len(self.__company__.sections) > 0:
            return list(filter(lambda t: t.name == "gruppo_dei_pari", self.__company__.sections))[0]

        raise Exception("Company non inizializzata")

    @cached_property
    def overview_completa(self) -> str:
        if len(self.__company__.sections) > 0:
            return list(filter(lambda t: t.name == "overview_completa", self.__company__.sections))[0].data["overview"]

        raise Exception("Company non inizializzata")

    @cached_property
    def company_name(self):
        return self.general_info.data["company_name"]

    @cached_property
    def fiscal_code(self):
        return self.general_info.data["fiscal_code"]

    @cached_property
    def cciaa_code(self):
        return self.general_info.data["numero_cciaa"]
import dataclasses

from model.RawCompanyData import CompanyData


@dataclasses.dataclass
class MainModel:
    company_fiscal_code: str
    _company_data: CompanyData | None = None

    @property
    def company_data(self):
        if self._company_data is not None:
            return self._company_data

        raise Exception("Accesso a company_data prima dell'inizializzazione")
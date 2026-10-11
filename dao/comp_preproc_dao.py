from copy import deepcopy
from dataclasses import fields
from typing import Any

from model.RawCompanyData import RawCompanyData, CompanyData
from model.Section import Section


class CompanyPreprocessorDAO:
    @staticmethod
    def process_company_data(raw: RawCompanyData) -> CompanyData:
        """
        Effettua gli ultimi step di processamento dei dati importati dall'excel per realizzare una struttura
        più comoda, da memorizzare nel DB e utilizzare per i calcoli. Le sezioni vengono memorizzate utilizzando il loro nome in un dizionario,
        rendendo più semplice l'accesso ai dati. Le top-level section vengono memorizzate in attributi della classe, per facilitare ulteriormente l'accesso
        ai dati.
        :param raw: Dati crudi della company ottenuti da BalanceDAO.import_from_excel()
        :return: Dati rielaborati della company più utilizzabili
        """
        sections = CompanyPreprocessorDAO._convert_sections(raw.sections)

        general_info = sections.get("general_info", {})

        company_name = general_info.get("company_name")
        fiscal_code = general_info.get("codice_fiscale")

        if not company_name or not fiscal_code:
            raise ValueError(
                "Dati obbligatori mancanti: company_name o codice_fiscale"
            )

        # Gli identificativi diventano attributi di CompanyData,
        # quindi vengono rimossi dalla sezione general_info.
        general_info.pop("company_name", None)
        general_info.pop("codice_fiscale", None)

        sections["general_info"] = general_info

        # Individua le sezioni supportate da CompanyData.
        supported_sections = {
                                 f.name
                                 for f in fields(CompanyData)
                             } - {"company_name", "fiscal_code"}

        unknown_sections = set(sections) - supported_sections

        if unknown_sections:
            raise ValueError(
                f"Sezioni non riconosciute: {sorted(unknown_sections)}"
            )

        return CompanyData(
            company_name=company_name,
            fiscal_code=fiscal_code,
            **sections,
        )

    @staticmethod
    def _convert_sections(
            sections: list[Section],
    ) -> dict[str, dict[str, Any]]:

        result = {}

        for section in sections:
            if section.name in result:
                raise ValueError(
                    f"Sezione duplicata: {section.name}"
                )

            result[section.name] = (
                CompanyPreprocessorDAO._convert_data(section.data)
            )

        return result

    @staticmethod
    def _convert_data(data: dict[str, Any]) -> dict[str, Any]:
        result = {}

        for key, value in data.items():

            if key == "subsections":
                result[key] = (
                    CompanyPreprocessorDAO._convert_sections(value)
                )

            elif isinstance(value, dict):
                result[key] = CompanyPreprocessorDAO._convert_data(value)

            else:
                result[key] = deepcopy(value)

        return result
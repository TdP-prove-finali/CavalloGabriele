from pymongo.synchronous.collection import Collection

from dao.mongodb_connector import MongoDBConnector
from model.Company import Company

from datetime import datetime
from typing import Any

from model.Section import Section

class CompanyDAO:
    @staticmethod
    def _serialize(value: Any) -> Any:
        """Converte ricorsivamente i modelli in valori BSON compatibili."""

        if isinstance(value, Company):
            return {
                "sections": [
                    CompanyDAO._serialize(section)
                    for section in value.sections
                ]
            }

        if isinstance(value, Section):
            return {
                "name": value.name,
                "data": CompanyDAO._serialize(value.data),
            }

        if isinstance(value, dict):
            return {
                key: CompanyDAO._serialize(item)
                for key, item in value.items()
            }

        if isinstance(value, list):
            return [CompanyDAO._serialize(item) for item in value]

        if isinstance(value, tuple):
            raise TypeError(
                "Le tuple richiedono una codifica esplicita "
                "per garantire il round-trip 1:1."
            )

        if value is None or isinstance(
                value, (str, bool, int, float, datetime)
        ):
            return value

        raise TypeError(
            f"Tipo non supportato: {type(value).__name__}"
        )

    @staticmethod
    def _deserialize_section(document: dict) -> Section:
        """Ricostruisce una Section, comprese le sottosezioni."""

        data = dict(document["data"])

        if "subsections" in data:
            data["subsections"] = [
                CompanyDAO._deserialize_section(subsection)
                for subsection in data["subsections"]
            ]

        return Section(
            name=document["name"],
            data=data,
        )

    @staticmethod
    def company_to_document(company: Company) -> dict:
        """Converte Company in un documento MongoDB."""

        if not isinstance(company, Company):
            raise TypeError("È richiesta un'istanza Company")

        return CompanyDAO._serialize(company)

    @staticmethod
    def load_company(codice_fiscale: str) -> Company | None:
        client = MongoDBConnector.get_client()
        collection = client["business_scenario_lab"]["companies"]
        document = collection.find_one({"_id": codice_fiscale})

        if document is None:
            return None

        document.pop("_id", None)

        return CompanyDAO.document_to_company(document)

    @staticmethod
    def document_to_company(document: dict) -> Company:
        """Ricostruisce Company da un documento MongoDB."""

        return Company(
            sections=[
                CompanyDAO._deserialize_section(section)
                for section in document["sections"]
            ]
        )

    @staticmethod
    def save_company(company: Company) -> str:
        client = MongoDBConnector.get_client()
        collection = client["business_scenario_lab"]["companies"]

        document = CompanyDAO.company_to_document(company)

        codice_fiscale = next(
            section.data["codice_fiscale"]
            for section in company.sections
            if section.name == "general_info"
        )

        document["_id"] = codice_fiscale

        collection.replace_one(
            {"_id": codice_fiscale},
            document,
            upsert=True,
        )
        return codice_fiscale

    @staticmethod
    def deleteCompany(codice_fiscale: str) -> bool:
        collection = MongoDBConnector.get_database()["companies"]

        result = collection.delete_one({
            "_id": codice_fiscale
        })

        return result.deleted_count > 0

    @staticmethod
    def importCompany(company: Company):
        client = MongoDBConnector.get_client()
        database = client["business_scenario_lab"]
        collection: Collection[Company] = database["companies"]

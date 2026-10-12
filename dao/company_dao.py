from dataclasses import asdict

from pymongo.synchronous.collection import Collection

from dao.mongodb_connector import MongoDBConnector
from model.RawCompanyData import RawCompanyData, CompanyBrief, CompanyData

from datetime import datetime
from typing import Any

from model.Section import Section

class CompanyDAO:
    @staticmethod
    def _serialize(value: Any) -> Any:
        """Converte ricorsivamente i modelli in valori BSON compatibili."""

        if isinstance(value, CompanyData):
            return asdict(value)

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
    def company_to_document(company: CompanyData) -> dict:
        """Converte CompanyData in un documento MongoDB."""

        if not isinstance(company, CompanyData):
            raise TypeError("È richiesta un'istanza Company")

        return CompanyDAO._serialize(company)

    @staticmethod
    def load_company(codice_fiscale: str) -> CompanyData | None:
        database = MongoDBConnector.get_database()
        collection = database["companies"]
        document = collection.find_one({"_id": codice_fiscale})

        if document is None:
            return None

        document.pop("_id", None)

        return CompanyDAO.document_to_company(document)

    @staticmethod
    def document_to_company(document: dict) -> CompanyData:
        """Ricostruisce Company da un documento MongoDB."""
        data = {
            key: value
            for key, value in document.items()
            if key != "_id"
        }

        return CompanyData(**data)

    @staticmethod
    def save_company(company: CompanyData) -> str:
        client = MongoDBConnector.get_client()
        collection = client["business_scenario_lab"]["companies"]

        document = CompanyDAO.company_to_document(company)

        codice_fiscale = company.fiscal_code

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
    def find_all_companies() -> list[CompanyBrief]:
        database = MongoDBConnector.get_database()
        collection = database["companies"]

        # Query con projection per trovare i brief delle company presenti
        results = collection.find({},
                                  {
                                      "_id": 0,
                                      "company_name": 1,
                                      "fiscal_code": 1
                                  })

        return [
            CompanyBrief(
                company_name=doc["company_name"],
                fiscal_code=doc["fiscal_code"]
            )
            for doc in results
        ]
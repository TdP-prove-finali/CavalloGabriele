from dataclasses import fields

from pymongo import UpdateOne

from dao.mongodb_connector import MongoDBConnector
from model.raw_company_data import CompanyData


class TranslationDAO:
    """
    Classe per gestire l'accesso alle traduzioni dei nomi dei campi del bilancio,
    generate in automatico dalla fase di importazione e salvate sul database.

    Le traduzioni dei campi vengono gestite come una collection mongodb a parte. Questa collection utilizza come id il nome del campo
    (generato internamente e garantito python-safe) e come valore un oggetto che contiene la traduzione in Italiano. E' un approccio scalabile
    perchè rende possibile integrare anche la traduzione in altre lingue
    """


    @staticmethod
    def save_translations(data: dict):
        if not data:
            return
        database = MongoDBConnector.get_database()
        collection = database["translations"]

        operations = [
            UpdateOne(
                {"_id": field_name},
                {
                    "$set": {
                        "it": description
                    }
                },
                upsert=True
            )
            for field_name, description in data.items()
        ]

        collection.bulk_write(operations, ordered=False)

    @staticmethod
    def get_translation(field_name: str) -> str | None:
        """
        Restituisce la traduzione italiana di un campo.
        Ritorna None se non esiste.
        """
        database = MongoDBConnector.get_database()
        collection = database["field_translations"]

        document = collection.find_one(
            {"_id": field_name},
            {"_id": 0, "it": 1}
        )

        return document.get("it") if document else None

    @staticmethod
    def get_translations(field_names: list[str]) -> dict[str, str]:
        """
        Restituisce un dizionario campo -> traduzione italiana.
        I campi non trovati vengono esclusi.
        """
        if not field_names:
            return {}

        database = MongoDBConnector.get_database()
        collection = database["translations"]

        documents = collection.find(
            {"_id": {"$in": field_names}},
            {"_id": 1, "it": 1}
        )

        return {
            document["_id"]: document["it"]
            for document in documents
            if document.get("it") is not None
        }

    @staticmethod
    def count_translations() -> int:
        database = MongoDBConnector.get_database()
        coll = database["translations"]
        return coll.count_documents({})

    @staticmethod
    def get_translations_for_company(company_data: CompanyData) -> dict[str, str]:
        """
        Restituisce le traduzioni per tutti i campi di questa company, caricando dal database solo quelle utili
        :param company_data: Dati completi della company
        :return:
        """
        field_names: set[str] = set()

        def collect_keys(data: dict) -> None:
            for key, value in data.items():
                if key != "subsections":
                    field_names.add(key)

                if isinstance(value, dict):
                    collect_keys(value)

                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            collect_keys(item)

        for field_info in fields(company_data):
            if field_info.name in {"company_name", "fiscal_code"}:
                continue

            field_names.add(field_info.name)

            section_data = getattr(company_data, field_info.name)

            if isinstance(section_data, dict):
                collect_keys(section_data)

        return TranslationDAO.get_translations(list(field_names))

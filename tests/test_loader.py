import datetime

from dao.balance_dao import CompanyBalanceImporter
from dao.company_dao import CompanyDAO
from dao.mongodb_connector import MongoDBConnector
from model.Company import Company, CompanyReader
from model.Section import Section
from test_data import company, company2


def test_loader():
    c = CompanyBalanceImporter("../dataset/sample-aida-single.xlsx")
    c.import_from_excel()
    assert c.company == company

def test_loader2():
    c = CompanyBalanceImporter("../dataset/sample-aida-single2.xlsx")
    c.import_from_excel()
    assert c.company == company2

def test_serialization():
    document = CompanyDAO.company_to_document(company)
    company_ricostruita = CompanyDAO.document_to_company(document)

    assert company_ricostruita == company

def test_company_mongodb_roundtrip():
    """
    Verifica che una Company salvata e ricaricata
    da MongoDB mantenga esattamente tutti i dati.
    """
    codice_fiscale = next(
        section.data["codice_fiscale"]
        for section in company.sections
        if section.name == "general_info"
    )
    CompanyDAO.deleteCompany(codice_fiscale)
    CompanyDAO.save_company(company)
    loaded_company = CompanyDAO.load_company(codice_fiscale)

    # 5. Verifica che sia stata caricata
    assert loaded_company is not None, (
        f"Company {codice_fiscale} non trovata su MongoDB"
    )

    # 6. Verifica che il tipo sia identico
    assert type(loaded_company) is type(company), (
        "La classe dell'oggetto caricato è diversa"
    )

    # 7. Confronta tutti i dati ricorsivamente
    assert loaded_company == company, (
        "La Company caricata differisce da quella originale"
    )

def test_company_brief():
    database = MongoDBConnector.get_database()
    collection = database["companies"]
    collection.drop()
    CompanyDAO.save_company(company)
    assert collection.count_documents({}) == 1

    brief = CompanyDAO.find_all_companies()
    company_reader = CompanyReader(company)
    assert len(brief) == 1
    assert brief[0].codice_fiscale == company_reader.general_info.data["codice_fiscale"]
    assert brief[0].nome == company_reader.general_info.data["company_name"]
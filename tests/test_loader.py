from dao.data_import.CompanyImportDAO import CompanyImportDAO
from dao.data_import.balance_dao import RawCompanyBalanceImporter
from dao.data_import.comp_preproc_dao import CompanyPreprocessorDAO
from dao.company_dao import CompanyDAO
from dao.mongodb_connector import MongoDBConnector
from dao.translations.translation_dao import TranslationDAO
from test_data import raw_company_paramount, raw_company_eni, complete_company_1

def test_loader():
    RawCompanyBalanceImporter.clear_translations()
    c = RawCompanyBalanceImporter("../dataset/sample-aida-single.xlsx")
    translations = RawCompanyBalanceImporter.get_translations()
    c.import_from_excel()
    assert c.company == raw_company_paramount
    assert len(translations.keys()) > 0

def test_loader2():
    RawCompanyBalanceImporter.clear_translations()
    c = RawCompanyBalanceImporter("../dataset/sample-aida-single2.xlsx")
    c.import_from_excel()
    assert c.company == raw_company_eni
    RawCompanyBalanceImporter.clear_translations()

def test_loader_cross():
    RawCompanyBalanceImporter.clear_translations()
    assert len(RawCompanyBalanceImporter.get_translations().keys()) == 0
    c1 = RawCompanyBalanceImporter("../dataset/sample-aida-single.xlsx")
    translations = RawCompanyBalanceImporter.get_translations()
    c1.import_from_excel()

    assert c1.company == raw_company_paramount
    assert len(translations.keys()) > 0
    l1 = len(RawCompanyBalanceImporter.get_translations().keys())
    assert l1 > 0
    c = RawCompanyBalanceImporter("../dataset/sample-aida-single2.xlsx")
    c.import_from_excel()
    assert c.company == raw_company_eni
    assert len(RawCompanyBalanceImporter.get_translations().keys()) > l1
    RawCompanyBalanceImporter.clear_translations()

def test_company_mongodb_roundtrip():
    """
    Verifica che una Company salvata e ricaricata
    da MongoDB mantenga esattamente tutti i dati.
    """
    codice_fiscale = complete_company_1.fiscal_code
    CompanyDAO.deleteCompany(codice_fiscale)
    CompanyDAO.save_company(complete_company_1)
    loaded_company = CompanyDAO.load_company(codice_fiscale)

    # 5. Verifica che sia stata caricata
    assert loaded_company is not None, (
        f"Company {codice_fiscale} non trovata su MongoDB"
    )

    # 6. Verifica che il tipo sia identico
    assert type(loaded_company) is type(complete_company_1), (
        "La classe dell'oggetto caricato è diversa"
    )

    # 7. Confronta tutti i dati ricorsivamente
    assert loaded_company == complete_company_1, (
        "La Company caricata differisce da quella originale"
    )

def test_company_brief():
    RawCompanyBalanceImporter.clear_translations()
    database = MongoDBConnector.get_database()
    collection = database["companies"]
    collection.drop()
    CompanyDAO.save_company(complete_company_1)
    assert collection.count_documents({}) == 1

    brief = CompanyDAO.find_all_companies()
    assert len(brief) == 1
    assert brief[0].fiscal_code == complete_company_1.fiscal_code
    assert brief[0].company_name == complete_company_1.company_name
    RawCompanyBalanceImporter.clear_translations()

def test_preproc_company():
    RawCompanyBalanceImporter.clear_translations()
    c = RawCompanyBalanceImporter("../dataset/sample-aida-single.xlsx")
    translations = RawCompanyBalanceImporter.get_translations()
    c.import_from_excel()
    raw_company = c.company
    assert raw_company == raw_company
    complete_company = CompanyPreprocessorDAO.process_company_data(raw_company)
    assert complete_company.fiscal_code == "07237600965"
    assert complete_company == complete_company_1

    document = CompanyDAO.company_to_document(complete_company)
    company_ricostruita = CompanyDAO.document_to_company(document)

    assert company_ricostruita == complete_company
    RawCompanyBalanceImporter.clear_translations()

def test_complete():
    RawCompanyBalanceImporter.clear_translations()
    MongoDBConnector.get_database()["translations"].drop()

    imp = CompanyImportDAO("../dataset/sample-aida-single.xlsx")
    imp.import_company()

    assert imp.company == complete_company_1
    assert imp.translations is not None

    TranslationDAO.save_translations(imp.translations)
    assert TranslationDAO.count_translations() > 0

    translated = TranslationDAO.get_translations_for_company(imp.company)
    assert len(translated.keys()) > 0
    RawCompanyBalanceImporter.clear_translations()
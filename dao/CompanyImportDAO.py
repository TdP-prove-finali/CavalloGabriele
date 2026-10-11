from dao.balance_dao import RawCompanyBalanceImporter
from dao.comp_preproc_dao import CompanyPreprocessorDAO
from model.RawCompanyData import CompanyData

class CompanyImportDAO:
    def __init__(self, filePath):
        self.__filePath__ = filePath
        self.__company__: CompanyData | None = None
        self.__translations__: dict = None

    def import_company(self):
        """
        Importa una company a partire da un file Excel eseguendo tutti gli step, ossia:
        1 - Importazione della struttura Raw dal file excel
        2 - Pre processamento della struttura per rendela di facile manipolazione

        Successivamente utilizzare {self.company} e {self.translations} per accedere ai dati della company e alle traduzioni
        automatiche di tutti i campi con i rispettivi descrittori completi.
        :return:
        """
        dao = RawCompanyBalanceImporter(self.__filePath__)
        dao.import_from_excel()
        raw_company = dao.company

        self.__company__ = CompanyPreprocessorDAO.process_company_data(raw_company)
        self.__translations__ = dao.get_translations()

    @property
    def company(self) -> CompanyData:
        if self.__company__ is None:
            raise Exception("Importazione non ancora avviata")

        return self.__company__

    @property
    def translations(self) -> dict:
        if self.__translations__ is None:
            raise Exception("Importazione non ancora avviata")

        return self.__translations__
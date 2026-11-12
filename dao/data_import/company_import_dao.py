from PySide6.QtCore import QObject, Signal, Slot
from openpyxl import load_workbook

from dao.company_dao import CompanyDAO
from dao.data_import.balance_dao import RawCompanyBalanceImporter
from dao.data_import.comp_preproc_dao import CompanyPreprocessorDAO
from dao.translations.translation_dao import TranslationDAO
from model.raw_company_data import CompanyData, RawCompanyData


class CompanyImportDAO(QObject):
    """
    Thread da eseguire per l'importazione delle company a partire da un file excel.
    """
    finished = Signal(object)
    error = Signal(str)
    progress = Signal(float)

    def __init__(self, filePath):
        super().__init__()
        self.__filePath__ = filePath
        self.__company__: CompanyData | None = None
        self.__translations__: dict = None

    def import_single_company(self):
        """
        Importa una company a partire da un file Excel eseguendo tutti gli step, ossia:
        1 - Importazione della struttura Raw dal file excel
        2 - Pre processamento della struttura per rendela di facile manipolazione

        Successivamente utilizzare {self.company} e {self.translations} per accedere ai dati della company e alle traduzioni
        automatiche di tutti i campi con i rispettivi descrittori completi.
        :return:
        """
        self.progress.emit(0)
        wb = load_workbook(filename=self.__filePath__, read_only=False, data_only=True)

        if len(wb.sheetnames) == 0:
            raise Exception("Il file non ha fogli da cui caricare i dati")

        firstSheet = wb.worksheets[0]

        dao = RawCompanyBalanceImporter(firstSheet)
        dao.import_from_excel()
        raw_company = dao.company

        self.__company__ = CompanyPreprocessorDAO.process_company_data(raw_company)
        self.__translations__ = dao.get_translations()
        self.progress.emit(100)
        self.finished.emit(self.__company__)
        return self.__company__

    @Slot()
    def start(self):
        """
        Importa tutte le company presenti nel file excel, una per foglio di lavoro.
        Salva ogni company sul database e genera in automatico le traduzioni dei campi.
        Comunica al thread principale lo stato tramite il segnale "progress"
        :return:
        """
        print(f"Importazione iniziata dal file {self.__filePath__}")
        imported = []

        self.progress.emit(10)
        wb = load_workbook(filename=self.__filePath__, read_only=False, data_only=True)
        self.progress.emit(20)

        tot = len(wb.sheetnames)
        if tot == 0:
            raise Exception("Il file non ha fogli da cui caricare i dati")
        cur_sheet_name = ""
        try:
            i = 1
            for sheet in wb.worksheets:
                cur_sheet_name = sheet.title
                imp = RawCompanyBalanceImporter(sheet)
                raw_data = imp.import_from_excel()
                completed = CompanyPreprocessorDAO.process_company_data(raw_data)
                imported.append(completed)
                CompanyDAO.save_company(completed)
                self.progress.emit((80/tot) * i + 20)
                i += 1

            self.__translations__ = RawCompanyBalanceImporter.get_translations()
            TranslationDAO.save_translations(self.translations)
            wb.close()
            self.finished.emit(imported)
            return imported
        except Exception as e:
            print(f"ERRORE: Impossibile importare la company dallo sheet {cur_sheet_name}")
            print(e.with_traceback(None))
            print(e)
            self.error.emit(e.__str__())

    @property
    def translations(self) -> dict:
        if self.__translations__ is None:
            raise Exception("Importazione non ancora avviata")

        return self.__translations__
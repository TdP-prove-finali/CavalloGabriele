from openpyxl.cell import Cell
from openpyxl.utils import get_column_letter

from model.Company import Company
from openpyxl import load_workbook

from model.Section import GeneralInfoSection, Section


class CompanyBalanceImporter:

    def __init__(self, path):
        self.path = path
        self.cursor_column = 1
        self.cursor_row = 1
        self.data = {}
        self.worksheet = None
        self.max_col = None
        self.max_row = None
        self.company = None

    def __set_cursor(self, column: int, row: int):
        if column > self.max_col or row > self.max_row:
            raise ValueError("Colonna o riga fuori dalla dimensione del foglio")

        self.cursor_column = column
        self.cursor_row = row

    def __return_to_rstart(self):       # Riporta il cursore all'inizio della riga
        self.cursor_column = 1

    def __next_row(self):
        self.cursor_row += 1
        self.cursor_column = 1

    def __next_column(self):
        self.cursor_column += 1

    def __reset_cursor(self):
        self.cursor_row = 1
        self.cursor_column = 1

    def __get_cell(self) -> Cell:   # Restituisce la cella a cui sta puntando adesso il cursore
        return self.worksheet[get_column_letter(self.cursor_column) + str(self.cursor_row)]

    def __move_to_next_value(self) -> Cell: # Sposta il cursore a destra fino a quando non trova un valore in una cella
        self.__next_column()
        while self.__get_cell() is not None and self.__get_cell().value is None:
            self.__next_column()

        return self.__get_cell()

    def __move_to_next_sechead(self) -> Cell:   # Sposta orizzontalmente il cursore fino alla prossima intestazione di campo (valore in grassetto blu)
        self.__next_column()
        while self.__get_cell() is None or not self.__get_cell().font.bold:
            self.__next_column()

        return self.__get_cell()

    def __check_empty_row(self) -> bool:        # Controlla se la riga è vuota
        self.cursor_column = 1
        for i in range(self.max_col):
            if self.__get_cell().value is not None:
                return False
            self.__next_column()

        return True

    def __is_section_start(self) -> bool:       # Controlla se la cella corrente è un inizio di una nuova sezione
        content = self.__get_cell().value
        return (content is not None and self.__get_cell().font is not None
                and self.__get_cell().font.bold
                and self.__get_cell().font.color.value == 'FF003366'
                and self.__get_cell().fill is not None
                and self.__get_cell().fill.start_color.value == 'FFB2CBEA')

    def __has_av_rows(self) -> bool:
        return self.cursor_row < self.max_row

    # TODO: Sistema di cursori globali nella classe e metodi che li spostano in un certo modo
    # Spostamento in riga alla ricerca di coppia campo-valore
    # Spostamento in colonna alla ricerca di campo-tuplavalori

    def import_from_excel(self) -> Company:
        # aprire il file
        # parti dalla prima cella della prima riga
        # e' vuota? Passa alla successiva
        # Ha qualcosa? Il testo è in grassetto? Lo sfondo è blu? Crea una nuova sezione general info
        # Parsifica la sezione
        # Ripeti
        wb = load_workbook(filename=self.path, read_only=True, data_only=True)

        if len(wb.sheetnames) == 0:
            raise Exception("Il file non ha fogli da cui caricare i dati")

        firstSheet = wb.worksheets[0]
        self.worksheet = firstSheet
        self.max_row = firstSheet.max_row
        self.max_col = firstSheet.max_column
        self.__set_cursor(2, 1) # B1
        self.company = Company()

        v = self.__get_cell()
        bold = v.font.bold
        content = v.value
        if bold and content is not None and v.font.color.value == 'FF003366':
            self.data["company_name"] = content
            s = self.__load_general_info_sec()
            self.company.sections.append(s)
            self.data = {}

        print("Carico i dati dal foglio ")
        return self.company

    def __get_field_name(self, cellContent) -> str:
        return cellContent.lower().replace(" ", "_")

    def __load_general_info_sec(self) -> Section:
        content_rows = 0

        while self.__has_av_rows() and not self.__is_section_start():
            self.__next_row()
            if not self.__check_empty_row():
                content_rows += 1
                self.__return_to_rstart()

                if content_rows == 1:
                    self.data["sede"] = self.__get_cell().value
                    field_cell = self.__move_to_next_sechead().value
                    field_name = self.__get_field_name(field_cell)
                    field_value = self.__move_to_next_value().value

                    self.data[field_name] = field_value
                elif content_rows == 2:
                    field_cell = self.__move_to_next_sechead().value
                    field_name = self.__get_field_name(field_cell)
                    field_value = self.__move_to_next_value().value

                    self.data[field_name] = field_value

        return Section(
            name="general_info",
            data=self.data.copy()
        )
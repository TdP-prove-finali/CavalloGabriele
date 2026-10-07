from openpyxl.cell import Cell
from openpyxl.utils import get_column_letter

from dao.util import remove_accents
from model.Company import Company
from openpyxl import load_workbook

from model.Section import Section

# TODO: Gestione dei "di cui" in SP
# TODO: Gestione sotto-sezioni passivo
# TODO: Migliorare gestione valute (classe valuta, migliaia, operazioni)
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
        cell = self.__get_cell()
        while (cell is not None
               and cell.value is None):
            if not self.__has_av_cols():
                raise Exception("Non è stato possibile trovare un valore successivo sulla riga " + str(self.cursor_row))

            self.__next_column()
            cell = self.__get_cell()

        return cell

    def __has_av_cols(self):
        return self.cursor_column < self.max_col

    def __move_to_next_sechead(self) -> Cell:   # Sposta orizzontalmente il cursore fino alla prossima intestazione di campo (valore in grassetto blu)
        while self.__get_cell() is None or self.__get_cell().font is None or not self.__get_cell().font.bold:
            if not self.__has_av_cols():
                raise Exception("Ricerca di una sezione orizzontale non trovata sulla riga " + str(self.cursor_row))

            self.__next_column()

        return self.__get_cell()

    def __check_empty_row(self) -> bool:        # Controlla se la riga è vuota
        self.cursor_column = 1
        for i in range(int(self.max_col / 3)):
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

    def __is_vsec_start(self) -> bool:      # Controlla se è l'inizio di una sezione verticale
        content = self.__get_cell().value
        return (content is not None and self.__get_cell().font is not None
                and self.__get_cell().font.bold
                and self.__get_cell().font.color.value == 'FF333333'
                and self.__get_cell().fill is not None
                and self.__get_cell().fill.start_color.value == 'FFD1D6DC')

    def __is_company_head(self) -> bool:        # Restituisce true se la cella corrente è l'intestazione del foglio
        v = self.__get_cell()
        bold = v.font.bold
        content = v.value
        return bold and content is not None and v.font.color.value == 'FF003366'

    def __down_vertically(self):        # Non riporta il cursore a sinistra, va solo giù verticalmente
        self.cursor_row += 1

    def __prev_row(self):
        if self.cursor_row > 0:
            self.cursor_row -= 1
            self.cursor_column = 1

    def __has_av_rows(self) -> bool:
        return self.cursor_row < self.max_row

    def __snap_cursor(self) -> tuple[int, int]:
        return tuple([self.cursor_column, self.cursor_row])

    def __restore_snap(self, curs: tuple):
        self.cursor_column = curs[0]
        self.cursor_row = curs[1]

    def __load_all_hvalues(self) -> list:       # Restituisce una lista con tutti i valori presenti sulla riga corrente, a partire dalla cella attuale
        values = []

        while self.__has_av_cols() and self.__get_cell() is not None:
            self.__next_column()
            cell = self.__get_cell()
            if cell.value is not None:
                values.append(self.__get_field_value(cell.value))

        return values.copy()

    def import_from_excel(self) -> Company:
        # aprire il file
        # parti dalla prima cella della prima riga
        # e' vuota? Passa alla successiva
        # Ha qualcosa? Il testo è in grassetto? Lo sfondo è blu? Crea una nuova sezione general info
        # Parsifica la sezione
        # Ripeti
        wb = load_workbook(filename=self.path, read_only=False, data_only=True)

        if len(wb.sheetnames) == 0:
            raise Exception("Il file non ha fogli da cui caricare i dati")

        firstSheet = wb.worksheets[0]
        self.worksheet = firstSheet
        self.max_row = firstSheet.max_row
        self.max_col = firstSheet.max_column
        self.__set_cursor(2, 1) # B1
        self.company = Company()

        if self.__is_company_head():
            self.data["company_name"] = self.__get_cell().value
            s = self.__load_general_info_sec()
            self.company.sections.append(s)
            self.data = {}

        while self.__has_av_rows():
            if self.__is_section_start():
                sectionName = self.__get_field_name(self.__get_cell().value)
                secVal = None
                if sectionName == "anagrafica":
                    self.__next_row()
                    secVal = self.__load_anagrafica_section()
                    self.__prev_row()
                elif sectionName == "informazioni_commerciali_e_legali":
                    self.__next_row()
                    secVal = self.__load_infcomleg_section()
                    self.__prev_row()
                elif sectionName == "informazioni_su_dimensione_e_gruppo":
                    self.__next_row()
                    secVal = self.__load_dimgroup_section()
                    self.__prev_row()
                elif sectionName == "classificazione_merceologica":
                    pass
                elif sectionName == "gruppo_dei_pari":
                    self.__next_row()
                    secVal = self.__load_parigroup_section()
                    self.__prev_row()
                elif sectionName == "overview_completa":
                    self.__next_row()
                    secVal = self.__load_overview()
                    self.__prev_row()
                elif sectionName == "profilo_finanziario_e_dipendenti":
                    self.__next_row()
                    secVal = self.__load_finance_profile_section()
                    self.__prev_row()
                elif sectionName == "stato_patrimoniale":
                    self.__next_row()
                    secVal = self.__load_sp_section()
                    self.__prev_row()
                else:
                    print("Sezione non riconosciuta " + sectionName)

                if secVal is not None:
                    self.company.sections.append(secVal)
                self.data = {}

            self.__next_row()

        wb.close()
        return self.company

    def __load_sp_section(self) -> Section:
        content_rows = 0
        sub_sections = []

        while self.__has_av_rows() and not self.__is_vsec_start():
            if not self.__check_empty_row():
                content_rows += 1
                self.__return_to_rstart()

                if content_rows <= 3:  # Le prime 3 righe non hanno un'intestazione
                    if content_rows == 1:
                        row_name = "data"
                        self.__next_column()
                    elif content_rows == 2:
                        row_name = "moneta"
                    elif content_rows == 3:
                        row_name = "periodo"

                    row_values = self.__load_all_hvalues()
                    self.data[row_name] = row_values.copy()

            self.__next_row()

        while self.__has_av_rows() and not self.__is_section_start():
            secName = self.__get_cell().value
            self.__next_row()
            sub_sections.append(self.__load_sp_subsection(
                self.__get_field_name(secName)))

        self.data["subsections"] = sub_sections.copy()
        return Section(
            name="stato_patrimoniale",
            data=self.data.copy()
        )

    def __load_sp_subsection(self, name) -> Section:
        s = Section(name, {})
        while self.__has_av_rows() and not self.__is_section_start() and not self.__is_vsec_start():
            if not self.__check_empty_row():
                row_name = self.__get_field_name(self.__get_cell().value)
                row_values = self.__load_all_hvalues()
                s.data[row_name] = row_values.copy()

            self.__next_row()

        return s

    def __load_finance_profile_section(self):
        content_rows = 0

        while self.__has_av_rows() and not self.__is_section_start():
            if not self.__check_empty_row():
                content_rows += 1
                self.__return_to_rstart()

                if content_rows <= 3:       # Le prime 3 righe non hanno un'intestazione
                    if content_rows == 1:
                        row_name = "data"
                        self.__next_column()
                    elif content_rows == 2:
                        row_name = "moneta"
                    elif content_rows == 3:
                        row_name = "periodo"

                    row_values = self.__load_all_hvalues()
                    self.data[row_name] = row_values.copy()
                elif content_rows >= 6:
                    row_name = self.__get_field_name(self.__get_cell().value)
                    self.__next_column()
                    row_values = self.__load_all_hvalues()
                    self.data[row_name] = row_values.copy()

            self.__next_row()

        return Section(
            name="profilo_finanziario",
            data=self.data.copy()
        )

    def __load_overview(self):
        content_rows = 0
        content = ""

        while self.__has_av_rows() and not self.__is_section_start():
            if not self.__check_empty_row():
                content_rows += 1
                self.__return_to_rstart()
                content += self.__get_cell().value

            self.__next_row()

        return Section(
            name="overview_completa",
            data={
                "overview": content
            }
        )

    def __load_parigroup_section(self):
        content_rows = 0

        while self.__has_av_rows() and not self.__is_section_start():
            if not self.__check_empty_row():
                content_rows += 1
                self.__return_to_rstart()

                if 0 < content_rows <= 3:
                    self.__return_to_rstart()
                    sec = self.__load_hsection()
                    self.data[sec[0]] = sec[1]

            self.__next_row()

        return Section(
            name="gruppo_dei_pari",
            data=self.data.copy()
        )

    def __load_dimgroup_section(self):
        content_rows = 0

        while self.__has_av_rows() and not self.__is_section_start():
            if not self.__check_empty_row():
                content_rows += 1
                self.__return_to_rstart()

                if content_rows == 1:
                    self.__return_to_rstart()
                    f1 = self.__load_hsection()
                    self.__next_column()
                    f2 = self.__load_hsection()
                    self.data[f1[0]] = f1[1]
                    self.data[f2[0]] = f2[1]
                elif content_rows != 6 and content_rows > 0:
                    self.__return_to_rstart()
                    sec = self.__load_hsection()
                    self.data[sec[0]] = sec[1]

            self.__next_row()

        return Section(
            name="dimensioni_e_gruppo",
            data=self.data.copy()
        )

    def __get_field_name(self, cellContent) -> str:
        return remove_accents(cellContent.lower().lstrip().rstrip().replace(" ", "_")
                .replace("-", "_").replace(".", "")
                .replace("(%)", "_perc_")
                .replace("(", "_")
                .replace(")", "_").replace("/", "_frac_")
                              .replace("'", "")
                              .replace("°", "")
                              .replace(",", "")
                              .replace(":", "")
                              )

    def __get_field_value(self, cellcontent):
        if type(cellcontent) == str and cellcontent == "n.d.":
            return None

        return cellcontent


    def __concat_vertically(self) -> str:       # Concatena i valori delle celle scendendo in verticale fino a quando non trova una cella vuota, un'intestazione di sotto-sezione o di sezione
        cont = ""
        while (self.__get_cell() is not None and
                self.__get_cell().value is not None and
               not self.__is_vsec_start() and
               not self.__is_section_start() and self.__has_av_rows()):
            cont += " " + self.__get_cell().value
            self.__down_vertically()

        return cont

    def __load_hsection(self)->tuple[str, ...]:
        self.__move_to_next_sechead()
        sec_name = self.__get_field_name(self.__get_cell().value)
        sec_value = self.__move_to_next_value().value

        return (sec_name, sec_value)

    def __load_anagrafica_section(self) -> Section:
        content_rows = 0

        while self.__has_av_rows() and not self.__is_section_start():
            if not self.__check_empty_row():
                content_rows += 1
                self.__return_to_rstart()

                if content_rows == 1 and self.__is_vsec_start():
                    subSecName = self.__get_field_name(self.__get_cell().value)
                    curSnap = self.__snap_cursor()  # Salvo la posizione da cui parto, poi scendo verticalmente e concateno i valori
                    self.__down_vertically()
                    content = self.__concat_vertically()
                    self.data[subSecName] = content
                    self.__restore_snap(curSnap)    # Ripristino la posizione del cursore
                elif content_rows == 2:
                    self.__return_to_rstart()
                    self.__move_to_next_value()     # Ignoro il valore già letto
                    sec = self.__load_hsection()
                    self.data[sec[0]] = sec[1]
                elif content_rows == 3 or content_rows == 4:
                    pass        # Ignoro i valori già utilizzati
                elif content_rows == 5:
                    if self.__is_vsec_start():
                        subSecName = self.__get_field_name(self.__get_cell().value)
                        curSnap = self.__snap_cursor()
                        self.__down_vertically()
                        value = self.__concat_vertically()
                        self.data[subSecName] = value
                        self.__restore_snap(curSnap)
                elif content_rows == 6:
                    self.__return_to_rstart()
                    self.__move_to_next_value()
                    sec = self.__load_hsection()
                    self.data[sec[0]] = sec[1]

            self.__next_row()

        return Section(
            name="anagrafica",
            data=self.data.copy()
        )

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
                elif content_rows == 3:
                    self.data["tipo_societa"] = self.__get_cell().value
                elif content_rows == 4:
                    self.data["controllante"] = self.__get_cell().value

        return Section(
            name="general_info",
            data=self.data.copy()
        )

    def __load_infcomleg_section(self) -> Section:
        content_rows = 0

        while self.__has_av_rows() and not self.__is_section_start():

            if not self.__check_empty_row():
                content_rows += 1
                self.__return_to_rstart()

                if content_rows == 5:      # Entrambe le righe hanno due campi
                    f1 = self.__load_hsection()
                    self.__next_column()
                    f2 = self.__load_hsection()
                    self.data[f1[0]] = f1[1]
                    self.data[f2[0]] = f2[1]
                elif content_rows >= 6:
                    f1 = self.__load_hsection()
                    self.__next_column()
                    self.data[f1[0]] = f1[1]

            self.__next_row()

        return Section(
            name="informazioni_commerciali_e_legali",
            data=self.data.copy()
        )
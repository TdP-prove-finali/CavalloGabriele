import keyword

from openpyxl.cell import Cell
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

from dao.util import remove_accents

def get_field_name(cellContent) -> str:
    # TODO: I campi di cui non hanno traduzione
    """
    Restituisce un nome di campo valido per una voce dell'excel, verificando che possa essere utilizzato come identificatore
    python in un dizionario.
    Inoltre, salva la corrispondenza Descrizione - nomecampo per permettere la traduzione sull'interfaccia
    :param cellContent:
    :return:
    """
    field_name = remove_accents(cellContent.lower().lstrip().rstrip().replace(" ", "_")
                                .replace("-", "_").replace(".", "")
                                .replace("(%)", "_perc_")
                                .replace("(", "_")
                                .replace(")", "_").replace("/", "_frac_")
                                .replace("'", "")
                                .replace("°", "")
                                .replace(",", "")
                                .replace(":", "")
                                .replace("+", "plus")
                                .replace("-", "minus")
                                )
    # Evita identificatori che iniziano con una cifra
    if field_name and field_name[0].isdigit():
        field_name = f"_{field_name}"

    # Evita parole riservate di Python
    if keyword.iskeyword(field_name):
        field_name = f"{field_name}_"

    # Verifica finale
    if not field_name.isidentifier():
        raise ValueError(
            f"Nome campo non valido: {cellContent!r} -> {field_name!r}"
        )

    self.__translations__[field_name] = cellContent
    return field_name


def get_field_value(self, cellcontent):
    if type(cellcontent) == str and cellcontent == "n.d.":
        return None

    return cellcontent


class ExcelCursor:

    def __init__(self, worksheet: Worksheet):
        self.cursor_column = 1
        self.cursor_row = 1
        self.max_col = None
        self.max_row = None
        self.worksheet = worksheet

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

    def __move_to_next_value(self, suppressable = False) -> Cell | None: # Sposta il cursore a destra fino a quando non trova un valore in una cella
        self.__next_column()
        cell = self.__get_cell()
        while (cell is not None
               and cell.value is None):
            if not self.__has_av_cols() and not suppressable:
                raise Exception("Non è stato possibile trovare un valore successivo sulla riga " + str(self.cursor_row))
            elif not self.__has_av_cols():
                return None

            self.__next_column()
            cell = self.__get_cell()

        return cell

    def __has_av_cols(self):
        return self.cursor_column < self.max_col

    def __move_to_next_sechead(self, suppressable = False) -> Cell | None:
        f""" Sposta orizzontalmente il cursore fino alla prossima intestazione di campo (valore in grassetto blu). 
         Nel caso in cui non venga trovata, se il parametro {suppressable} non è specificato, lancia un'eccezione, altrimenti restituisce None. """
        while self.__get_cell() is None or self.__get_cell().font is None or not self.__get_cell().font.bold:
            if not self.__has_av_cols() and not suppressable:
                raise Exception("Ricerca di una sezione orizzontale non trovata sulla riga " + str(self.cursor_row))
            elif not self.__has_av_cols():
                return None

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

    def __is_vsubsec2_start(self):
        content = self.__get_cell().value
        return (content is not None and self.__get_cell().font is not None
                and self.__get_cell().font.bold
                and self.__get_cell().font.color.value == 'FF333333'
                and self.__get_cell().fill is not None
                and self.__get_cell().fill.start_color.value == 'FFE4ECF6')


    def __concat_vertically(self) -> str:       # Concatena i valori delle celle scendendo in verticale fino a quando non trova una cella vuota, un'intestazione di sotto-sezione o di sezione
        cont = ""
        while (self.__get_cell() is not None and
                self.__get_cell().value is not None and
               not self.__is_vsec_start() and
               not self.__is_section_start() and self.__has_av_rows()):
            cont += " " + self.__get_cell().value
            self.__down_vertically()

        return cont

    def __load_hsection(self, suppressable=False)-> tuple[str, ...] | None:
        """
        Carica una sezione orizzontale identificata da una cella di heading (nome del campo) e una di valore.
        :param suppressable: Indica se lanciare un'eccezione nel caso in cui la sezione non venga trovata o se semplicemente restituire None
        :return: Cella in cui inizia la sezione oppure None
        """
        res = self.__move_to_next_sechead(suppressable)
        if res is not None:
            sec_name = self.__get_field_name(self.__get_cell().value)
            sec_value = self.__move_to_next_value(suppressable)
            if sec_value is not None:
                return (sec_name, sec_value.value)
            else:
                return None
        else:
            return None

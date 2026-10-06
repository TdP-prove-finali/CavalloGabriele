from openpyxl.utils import get_column_letter

from model.Company import Company
from openpyxl import load_workbook

from model.Section import GeneralInfoSection

def is_section_start(cell) -> bool:
    content = cell.value
    return (content is not None and cell.font is not None and cell.font.bold and cell.font.color.value == 'FF003366'
            and cell.fill is not None
            and cell.fill.start_color.value == 'FFB2CBEA')

class BalanceDao:

    @staticmethod
    def import_from_excel(path) -> Company:
        # aprire il file
        # parti dalla prima cella della prima riga
        # e' vuota? Passa alla successiva
        # Ha qualcosa? Il testo è in grassetto? Lo sfondo è blu? Crea una nuova sezione general info
        # Parsifica la sezione
        # Ripeti
        wb = load_workbook(filename=path, read_only=True, data_only=True)

        if len(wb.sheetnames) == 0:
            raise Exception("Il file non ha fogli da cui caricare i dati")

        firstSheet = wb.worksheets[0]

        v = firstSheet["B1"]
        bold = v.font.bold
        content = v.value
        print(v)
        if bold and content is not None and v.font.color.value == 'FF003366':
            print("Ho trovato il nome della company")
            s = BalanceDao.__load_general_info_sec(v, firstSheet, content)

        print("Carico i dati dal foglio ")
        return Company()

    @staticmethod
    def __load_general_info_sec(start_cell, worksheet, companyName) -> GeneralInfoSection:
        start_row = start_cell.row + 1
        cur_col = 1
        max_row = worksheet.max_row
        max_col = 20
        available_rows = 0

        values = {}

        while not is_section_start(worksheet[get_column_letter(cur_col) + str(start_row)]) or start_row == max_row:
            # Non ho raggiunto la fine della sezione o del file
            # Ogni riga la leggo in orizzontale
            curCell = worksheet[get_column_letter(cur_col) + str(start_row)]

            if type(curCell) == tuple:
                print("Cella unita con " + str(len(curCell)))

            if curCell.value is not None:
                available_rows += 1

                if available_rows == 1:
                    values["sede"] = curCell.value
                    # vado alla prima cella successiva che contiene
                    cl = worksheet[get_column_letter(cur_col) + str(start_row)]
                    while cur_col <= max_col and not cl.font.bold:
                        cl = worksheet[get_column_letter(cur_col) + str(start_row)]
                        print(cl.value)
                        cur_col += 1

                    values[cl.value.lower().replace(" ", "_")] = worksheet[get_column_letter(cur_col) + str(start_row)].value
                    print()

            start_row += 1
            cur_col = 1

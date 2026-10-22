from dao.data_import.abstract_section_loader import AbstractSectionLoader
from model.section import Section


class AnagraficaSectionLoader(AbstractSectionLoader):
    section_name = "anagrafica"

    def __parse__(self) -> Section:
        ctx = self.context
        content_rows = 0

        while ctx.__has_av_rows() and not ctx.__is_section_start():
            if not ctx.__check_empty_row():
                content_rows += 1
                ctx.__return_to_rstart()

                if content_rows == 1 or content_rows == 5 and ctx.__is_vsec_start():
                    subSecName = ctx.__get_field_name(ctx.__get_cell().value)
                    curSnap = ctx.__snap_cursor()  # Salvo la posizione da cui parto, poi scendo verticalmente e concateno i valori
                    ctx.__down_vertically()
                    content = ctx.__concat_vertically()
                    ctx.data[subSecName] = content
                    ctx.__restore_snap(curSnap)  # Ripristino la posizione del cursore

                if ctx.__move_to_next_value(True) is not None:  # Ignoro il valore già letto
                    sec = ctx.__load_hsection(
                        True)  # Nel caso di società cessate, il sito web potrebbe non essere presente
                    if sec is not None:
                        ctx.data[sec[0]] = sec[1]

            ctx.__next_row()

        return Section(
            name="anagrafica",
            data=self.data.copy()
        )
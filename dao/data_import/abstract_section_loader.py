from dao.data_import.ImportException import ImportException
from dao.data_import.balance_dao import RawCompanyBalanceImporter
from model.section import Section


class AbstractSectionLoader:
    """Rappresenta un generico loader per una section della company"""
    section_name: str = "none"

    def __init__(self, context: RawCompanyBalanceImporter):
        self.context: RawCompanyBalanceImporter = context

    def __parse__(self) -> Section:
        raise NotImplementedError("Method not implemented")

    def load_content(self) -> Section:
        try:
            return self.__parse__()
        except ImportException as e:
            raise e
        except Exception as exc:
            raise ImportException(self.section_name, tuple([self.context.cursor_row, self.context.cursor_column]), exc.__str__())

    @classmethod
    def applies_to(cls, section_name: str):
        """Controlla se questo loader si applica a questa sezione"""
        return cls.section_name == section_name

    def __str__(self):
        return "Abstract Section Loader"
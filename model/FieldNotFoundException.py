from dao.util import BalanceLocation


class FieldNotFoundException(Exception):
    def __init__(self, field_name: str, where: BalanceLocation, msg: str = ""):
        self.field_name = field_name
        self.where = where
        self.msg = msg

    def __str__(self):
        return f"Il campo {self.field_name} non è stato trovato nella location {self.where}. {self.msg}"
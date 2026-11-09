
from dataclasses import dataclass
from enum import IntEnum
from typing import Any
from dao.util import extract_complete_numbering

class BalanceLocation(IntEnum):
    SP_ATTIVO = 0,
    SP_PASSIVO_DEBITI = 1,
    SP_PASSIVO_PATRIM = 2,
    CE = 3,
    SP_PASSIVO = 4,
    SP = 5

    @staticmethod
    def from_str(input: str):
        d = {
            "attivo": BalanceLocation.SP_ATTIVO,
            "passivo": BalanceLocation.SP_PASSIVO,
            "debiti": BalanceLocation.SP_PASSIVO_DEBITI,
            "patrimonio_netto": BalanceLocation.SP_PASSIVO_PATRIM,
            "conto_economico": BalanceLocation.CE
        }
        if d.get(input) is None:
            raise Exception("BalanceLocation non riconosciuta")

        return d.get(input)

class NodeType(IntEnum):
    VIRTUAL = 0,
    FIELD = 1

class Flag(IntEnum):
    NO_COPY = 0,
    NEED_RECALC = 1,
    UPDATED = 2

@dataclass
class Node:
    """
    Rappresenta un generico campo del bilancio
    """

    type: NodeType
    field_name: str
    flags: list[Flag]
    value: list[Any]
    where: BalanceLocation

    def get_column(self, col):
        return self.value[col]

    @property
    def numeration(self):
        return extract_complete_numbering(self.field_name) or ""

    @property
    def name(self):
        return self.field_name.removeprefix(self.numeration).removeprefix("_")

    def __hash__(self):
        return hash(self.field_name)

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.field_name == other.field_name

    def __str__(self):
        return f"Campo {self.field_name} di tipo {"virtual" if self.type == NodeType.VIRTUAL else "field"}"

    def has_data(self):
        return self.value != []

    def set_flag(self, value: Flag):
        if value not in self.flags:
            self.flags.append(value)

    @staticmethod
    def virtual(field_name, where):
        return Node(
            NodeType.VIRTUAL,
            field_name,
            [],
            [],
            where
        )
from dataclasses import dataclass
from enum import IntEnum
from typing import Any
from dao.util import extract_complete_numbering, BalanceLocation, is_specification_field


class NodeType(IntEnum):
    VIRTUAL = 0,
    FIELD = 1

class Flag(IntEnum):
    NO_COPY = 0,
    NEED_RECALC = 1,
    UPDATED = 2,
    NO_SUM_CHILDREN_NO_DC = 3,          # Indica che questo campo NON è dato dalla somma dei figli, escludendo i figli che sono dei "di cui". Normalmente è la regola di default per i campi che hanno figli.
    IGNORE_CHILDREN = 4,                 # Indica che per questo campo è necessario ignorare i figli che sono presenti e utilizzare il suo valore per il calcolo
    RECALCULATED = 5,
    USE_FIELD_NAME = 6                  # Indica che per identificarlo è necessario utilizzare il field name e non il name senza numerazione.

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

    def remove_flag(self, value: Flag):
        if value in self.flags:
            self.flags.remove(value)

    def is_dc_specification(self):
        return is_specification_field(self.field_name)

    @staticmethod
    def virtual(field_name, where):
        return Node(
            NodeType.VIRTUAL,
            field_name,
            [],
            [],
            where
        )

    @staticmethod
    def all_dc_dicui(nodes: list):
        for n in nodes:
            if not n.is_dc_specification():
                return False
        return True
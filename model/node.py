from dataclasses import dataclass
from enum import IntEnum
from typing import Any
from dao.util import extract_complete_numbering, BalanceLocation

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
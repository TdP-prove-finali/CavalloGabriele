from enum import Enum
from typing import Callable, Any

from model.raw_company_data import BalanceSnaphot

"""
Rappresenta il tipo di effetto che l'investimento avrà su un determinato campo del bilancio
"""
class EffectType(Enum):
    INCREASE = 0,
    DECREASE = 1

"""
Indica la modalità con cui calcolare il valore dell'effetto quando lo si applica"""
class ValueMode(Enum):
    CONSTANT = 0,
    FORMULA = 1

class EffectDestination(Enum):
    STATO_PATRIM = 0,
    CONTO_ECON = 1

class EffectFrequency(Enum):
    ANNUAL = 0,
    MONTHLY = 1,
    DAILY = 2,
    TRI_MONTHLY = 3,
    BI_MONTHLY = 4,
    ONCE = 5

class InvestmentEffect:
    def __init__(self, id: int, inv_type: EffectType, value_mode: ValueMode, field_name: str,
                 frequency: EffectFrequency,
                 where: EffectDestination,
                 value_constant: float | None = None,
                  value_func: Callable[[Any], float] | None = None):

        self.id = id
        self.type = inv_type
        self.value_mode = value_mode
        self.field_name = field_name
        self.where = where
        self.value_func = value_func
        self.value_constant = value_constant
        self.frequency = frequency

    def apply(self, state) -> BalanceSnaphot:
        """
        Applica l'effetto sullo snapshot corrente del bilancio
        :param state:
        :return:
        """
        pass        # TODO: Implement

    def __str__(self):
        return f"Investment Effect con id {self.id} sulla voce di bilancio {self.field_name}. Tipo di effetto: {self.type}"

    def __eq__(self, other):
        return self.id == other.id
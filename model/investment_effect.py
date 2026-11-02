from enum import Enum
from math import exp, sqrt
from typing import Callable, Any

from model.balance_snap import BalanceSnaphot, BalanceLocation
from model.sim_state import SimulationState
import numpy as np

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
    def __init__(self, title: str, inv_type: EffectType, value_mode: ValueMode, field_name: str,
                 frequency: EffectFrequency,
                 where: EffectDestination,
                 value_constant: float | None = None,
                 value_func: Callable[[Any], float] | None = None):

        self.title = title
        self.type = inv_type
        self.value_mode = value_mode
        self.field_name = field_name
        self.where = where
        self.value_func = value_func
        self.value_constant = value_constant
        self.frequency = frequency

    def apply(self, state: SimulationState) -> BalanceSnaphot:
        """
        Applica l'effetto sullo snapshot corrente del bilancio. Viene chiamata in automatico sulla base della frequenza dell'effetto.
        :param state: Stato della simulazione
        :return:
        """
        pass

    def __str__(self):
        return f"Investment Effect con id {self.title} sulla voce di bilancio {self.field_name}. Tipo di effetto: {self.type}"

    def __eq__(self, other):
        return self.title == other.title

class OrganicGrowthEffect(InvestmentEffect):
    def __init__(self, avg, var, title):
        self.average = avg
        self.variance = var
        super().__init__(title, EffectType.INCREASE, ValueMode.CONSTANT, "a1_ricavi_vendite_e_prestazioni",
                         EffectFrequency.ANNUAL,
                         EffectDestination.CONTO_ECON)

    def apply(self, state) -> BalanceSnaphot:
        current_month = state.current_month
        prev_value = state.working_snapshot.first_non_null_val(current_month, self.field_name, BalanceLocation.CE)
        if prev_value is None:
            raise Exception("Attenzione: non è disponibile un'informazione di fatturato storico")

        rng = np.random.default_rng(seed=42)
        Z_n = rng.normal(loc=0, scale=1)
        dt = current_month / 12
        X_tn1 = prev_value * exp(
            (self.average - self.variance / 2) * dt
            + sqrt(self.variance * dt) * Z_n
        )
        state.working_snapshot.set_field_value(self.field_name, BalanceLocation.CE, X_tn1, month=current_month + 1)
        return state.working_snapshot
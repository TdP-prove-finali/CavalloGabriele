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
    DECREASE = 1,
    VAL_FUNCT = 2,# Indica di ricalcolare il valore applicando la funzione di calcolo
    CONST = 3

class EffectFrequency(Enum):
    ANNUAL = 0,
    MONTHLY = 1,
    DAILY = 2,
    TRI_MONTHLY = 3,
    BI_MONTHLY = 4,
    ONCE = 5

class InvestmentEffect:
    def __init__(self, title: str, inv_type: EffectType, field_name: str,
                 frequency: EffectFrequency,
                 where: BalanceLocation,
                 value_constant: float | None = None,
                 value_func: Callable[[Any], float] | None = None):
        self.title = title
        self.type = inv_type
        self.field_name = field_name
        self.where = where
        self.value_func = value_func
        self.value_constant = value_constant
        self.frequency = frequency

    def apply(self, state: SimulationState) -> BalanceSnaphot:
        """
        Applica l'effetto sullo snapshot corrente del bilancio. Viene chiamata in automatico sulla base della frequenza dell'effetto.
        Il cambiamento è effettuato leggendo il campo alla colonna del mese corrente e scrivendo la colonna del mese successivo. Per ottenere un funzionamento diverso
        è necessario fare l'override di questo metodo
        :param state: Stato della simulazione
        :return:
        """
        data = state.working_snapshot.get_field_data(self.where, self.field_name)
        if data is None:
            raise Exception(f"Effetto {self.__str__()} non applicabile al campo perchè non esiste il campo. ")

        if self.type == EffectType.INCREASE:
            val = self.value_constant
            if val is None:
                raise Exception("Per un effetto di incremento è necessario specificare un importo di cui aumentare il campo attraverso value_constant")

            state.working_snapshot.set_field_value(
                field_name=self.field_name,
                location=self.where,
                value=state.working_snapshot.get_field_value(
                    field_name=self.field_name,
                    where=self.where,
                    month=state.current_month) + val,
                month=state.current_month + 1
            )
        elif self.type == EffectType.DECREASE:
            val = self.value_constant
            if val is None:
                raise Exception(
                    "Per un effetto di incremento è necessario specificare un importo di cui aumentare il campo attraverso value_constant")

            state.working_snapshot.set_field_value(
                field_name=self.field_name,
                location=self.where,
                value=state.working_snapshot.get_field_value(
                    field_name=self.field_name,
                    where=self.where,
                    month=state.current_month) - val,
                month=state.current_month + 1
            )
        elif self.type == EffectType.CONST:
            val = self.value_constant
            if val is None:
                raise Exception(
                    "Per un effetto di incremento è necessario specificare un importo di cui aumentare il campo attraverso value_constant")

            state.working_snapshot.set_field_value(
                field_name=self.field_name,
                location=self.where,
                value=val,
                month=state.current_month + 1
            )
        elif self.type == EffectType.VAL_FUNCT:
            func: Callable = self.value_func
            if func is None:
                raise Exception(f"Funzione di calcolo non specificata per l'effetto {self.__str__()}")

            newVal = func(state.working_snapshot.get_field_value(
                    field_name=self.field_name,
                    where=self.where,
                    month=state.current_month))
            state.working_snapshot.set_field_value(
                field_name=self.field_name,
                location=self.where,
                value=newVal,
                month=state.current_month + 1
            )

    def __str__(self):
        return f"Investment Effect con id {self.title} sulla voce di bilancio {self.field_name}. Tipo di effetto: {self.type}"

    def __eq__(self, other):
        return self.title == other.title

class OrganicGrowthEffect(InvestmentEffect):
    def __init__(self, avg, var, title):
        self.average = avg
        self.variance = var
        super().__init__(title, EffectType.INCREASE,"a1_ricavi_vendite_e_prestazioni",
                         EffectFrequency.ANNUAL,
                         BalanceLocation.CE)

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
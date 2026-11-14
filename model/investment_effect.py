import math
from enum import Enum
from math import exp, sqrt
from typing import Callable, Any

from dao.util import BalanceLocation
from model.balance_snap import BalanceSnaphot
from model.sim_state import SimulationState
import numpy as np

"""
Rappresenta il tipo di effetto che l'investimento avrà su un determinato campo del bilancio
"""
class EffectType(Enum):
    INCREASE = 0,
    DECREASE = 1,
    VAL_FUNCT = 2, # Indica di ricalcolare il valore applicando la funzione di calcolo
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

    def current_write_index(self, state):
        return 2 + (state.current_month % 12)

    def current_read_index(self, state):
        return 1

    def apply(self, state: SimulationState) -> BalanceSnaphot:
        """
        Applica l'effetto sullo snapshot corrente del bilancio. Viene chiamata in automatico sulla base della frequenza dell'effetto.
        Il cambiamento è effettuato leggendo il campo alla colonna del mese corrente e scrivendo la colonna del mese successivo. Per ottenere un funzionamento diverso
        è necessario fare l'override di questo metodo
        :param state: Stato della simulazione
        :return:
        """
        data = state.working_snapshot.get_field_data(self.field_name, self.where)
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
                    month=self.current_read_index(state)) + val,
                month=self.current_write_index(state)
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
                    month=self.current_read_index(state)) - val,
                month=self.current_write_index(state)
            )
        elif self.type == EffectType.CONST:
            val = self.value_constant
            if val is None:
                raise Exception(
                    "Per un effetto di incremento è necessario specificare un importo di cui aumentare il campo attraverso value_constant")

            prev_value = state.working_snapshot.get_field_value(
                field_name=self.field_name,
                where=self.where,
                month=self.current_write_index(state)
            )
            if prev_value is None or prev_value == '' or prev_value == 0:
                state.working_snapshot.set_field_value(
                    field_name=self.field_name,
                    location=self.where,
                    value=val,
                    month=self.current_write_index(state)
                )
            elif type(prev_value) is int or type(prev_value) is float:      # Se il campo contiene già un valore, significa che un altro effetto ci ha già lavorato. Sovrascrivendolo perderei quell'effetto, quindi viene sommato
                state.working_snapshot.set_field_value(
                    field_name=self.field_name,
                    location=self.where,
                    value=val + prev_value,
                    month=self.current_write_index(state)
                )
        elif self.type == EffectType.VAL_FUNCT:
            func: Callable = self.value_func
            if func is None:
                raise Exception(f"Funzione di calcolo non specificata per l'effetto {self.__str__()}")

            newVal = func(state.working_snapshot.get_field_value(
                    field_name=self.field_name,
                    where=self.where,
                    month=self.current_read_index(state)))
            state.working_snapshot.set_field_value(
                field_name=self.field_name,
                location=self.where,
                value=newVal,
                month=self.current_write_index(state)
            )

    def __str__(self):
        return f"Investment Effect con id {self.title} sulla voce di bilancio {self.field_name}. Tipo di effetto: {self.type}"

    def __eq__(self, other):
        return self.title == other.title

class TimeToProductivityEffect(InvestmentEffect):
    def __init__(self, average: float, variance: float):
        super().__init__(
            title="ttp-effect",
            inv_type=EffectType.CONST,
            field_name="ricavi_vendite_e_prestazioni",
            frequency=EffectFrequency.MONTHLY,
            where=BalanceLocation.CE,
        )
        self.average = average
        self.variance = variance

    def apply(self, state: SimulationState) -> BalanceSnaphot:
        # TODO: Implement
        pass

class HyperPerformerEffect(InvestmentEffect):
    def __init__(self, scale: float, shape: float):
        super().__init__(
            title="hp-effect",
            inv_type=EffectType.CONST,
            field_name="ricavi_vendite_e_prestazioni",
            frequency=EffectFrequency.MONTHLY,
            where=BalanceLocation.CE,
        )
        self.scale = scale
        self.shape = shape

    def apply(self, state: SimulationState) -> BalanceSnaphot:
        # TODO: Implement
        pass

# TODO: Gestione delle immobilizzazioni in corso "B.I.6 Immobilizzazioni in corso e acconti
# Valutare se copiarle semplicemente o se trasferirle come immobilizzazioni completate in SP Attivo

class OrganicGrowthEffect(InvestmentEffect):
    seed = None

    # TODO: Aspetti patrimoniali e gestione dei crediti
    def __init__(self, avg, var, title):
        self.average = avg
        self.variance = var
        super().__init__(title, EffectType.INCREASE,"ricavi_vendite_e_prestazioni",
                         EffectFrequency.MONTHLY,
                         BalanceLocation.CE)
        OrganicGrowthEffect.seed = np.random.default_rng(seed=42)

    def apply(self, state) -> BalanceSnaphot:
        current_month = state.current_month
        # Il valore della colonna year start è annuale, quindi viene diviso per 12 per renderlo mensile
        prev_value = state.working_snapshot.get_field_value(self.field_name,BalanceLocation.CE, 0) / 12
        if prev_value is None:
            raise Exception("Attenzione: non è disponibile un'informazione di fatturato storico")

        rng = OrganicGrowthEffect.seed
        Z_n = rng.normal(loc=0, scale=1)
        dt = (current_month / 12) + 1
        X_tn1 = prev_value * exp(
            (self.average - self.variance / 2) * dt
            + sqrt(self.variance * dt) * Z_n
        )
        state.working_snapshot.set_field_value(self.field_name, BalanceLocation.CE, X_tn1 - prev_value, month=self.current_write_index(state))
        return state.working_snapshot

class CostGrowthEffect(InvestmentEffect):
    seed = None     # Il seed è condiviso così non si resetta ad ogni applicazione

    """
    Effetto automatico di aumento dei costi per materie prime e consumo.
    """
    def __init__(self, avg, var, title):
        super().__init__(title, EffectType.INCREASE,"materie_prime_e_consumo",
                         EffectFrequency.MONTHLY,
                         BalanceLocation.CE)
        self.var = var
        self.avg = avg
        CostGrowthEffect.seed = np.random.default_rng(seed=42)

    def apply(self, state: SimulationState) -> BalanceSnaphot:
        annual_base = state.working_snapshot.get_field_value(
            self.field_name,
            BalanceLocation.CE,
            0
        )
        monthly_base = annual_base / 12.0
        growth_mean = self.avg
        growth_var = self.var
        factor_mean = 1.0 + growth_mean
        sigma2 = math.log1p(growth_var / (factor_mean ** 2))
        sigma = math.sqrt(sigma2)
        mu = math.log(factor_mean) - sigma2 / 2.0
        rng = CostGrowthEffect.seed
        growth_factor = rng.lognormal(mean=mu,sigma=sigma)
        growth_rate = growth_factor - 1
        marginal = monthly_base * growth_rate
        state.working_snapshot.set_field_value(
            self.field_name,
            BalanceLocation.CE,
            marginal,
            month=self.current_write_index(state)
        )

        return state.working_snapshot


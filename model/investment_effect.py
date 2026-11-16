import math
from enum import Enum, IntEnum
from math import exp, sqrt
from typing import Callable, Any
from scipy.stats import lomax
import numpy.random

from dao.util import BalanceLocation
from model.balance_snap import BalanceSnaphot
from model.node import Flag
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

class EffectExecFlags(IntEnum):
    YEAR_START = 1,
    YEAR_END = 2

class IdFactory:
    last = 0

    @staticmethod
    def new_id():
        IdFactory.last += 1
        return IdFactory.last

class InvestmentEffect:
    def __init__(self, title: str, inv_type: EffectType, field_name: str,
                 frequency: EffectFrequency,
                 where: BalanceLocation,
                 value_constant: float | None = None,
                 value_func: Callable[[Any], float] | None = None,
                 flags=None,
                 until: int | None = None,
                 starting_on: int | None = None
                 ):

        if flags is None:
            self.flags = []
        else:
            self.flags = flags

        self.title = title
        self.type = inv_type
        self.field_name = field_name
        self.where = where
        self.value_func = value_func
        self.value_constant = value_constant
        self.frequency = frequency
        self.exec_flags = flags
        self.until = until
        self.starting_on = starting_on

    def current_write_index(self, state):
        return 2 + (state.current_month % 12)

    def current_read_index(self, state):
        return 1

    def __check_applies__(self, state: SimulationState) -> bool:
        if state.current_month > (self.until or 0):
            print(f"Effetto {self} bloccato perchè ha superato la sua durata. ")
            return False

        if self.starting_on is not None and state.current_month < self.starting_on:
            print(f"Effetto {self} bloccato perchè deve partire al mese {self.starting_on}")
            return False

        return True

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

        if not self.__check_applies__(state):
            return state.working_snapshot

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

class MoveImportInvEffect(InvestmentEffect):
    """
    Effetto che permette di spostare un importo X da un campo ad un altro (sottraendolo dal primo e aggiungendolo al secondo)
    """
    def __init__(self,
                 source_field_name: str,
                dest_field_name: str,
                 title: str, inv_type: EffectType,
                 frequency: EffectFrequency,
                 where: BalanceLocation,
                 value_constant: float | None = None,
                 value_func: Callable[[Any], float] | None = None,
                 flags=None,
                 until: int | None = None,
                 starting_on: int | None = None
                 ):
        super().__init__(title, inv_type, source_field_name, frequency, where, value_constant, value_func, flags, until, starting_on)
        self.source_field_name = source_field_name
        self.dest_field_name = dest_field_name

    def apply(self, state: SimulationState) -> BalanceSnaphot:
        if not self.__check_applies__(state):
            return state.working_snapshot

        state.working_snapshot.sum_field_value(self.source_field_name, self.where, self.value_constant * (-1), self.current_write_index(state))
        state.working_snapshot.sum_field_value(self.dest_field_name, self.where, self.value_constant, self.current_write_index(state))

        return state.working_snapshot

class ProductivityIncreaseEffect(InvestmentEffect):
    seed: numpy.random.Generator | None = None

    def __init__(self, average: float, variance: float, hp_lomax_scale: float, hp_lomax_shape: float):
        super().__init__(
            title="ttp-effect",
            inv_type=EffectType.CONST,
            field_name="ricavi_vendite_e_prestazioni",
            frequency=EffectFrequency.MONTHLY,
            where=BalanceLocation.CE
        )
        self.average = average
        self.variance = variance
        ProductivityIncreaseEffect.seed = np.random.default_rng(55)
        self.ttp = ProductivityIncreaseEffect.seed.normal(self.average, math.sqrt(self.variance))
        self.hp_lomax_scale = hp_lomax_scale
        self.hp_lomax_shape = hp_lomax_shape
        self.r = None

    def apply(self, state: SimulationState) -> BalanceSnaphot:
        if self.r is None:
            self.r = state.working_snapshot.get_field_value(self.field_name, self.where, BalanceSnaphot.HISTORIC_COL) / state.working_snapshot.get_field_value("dipendenti", BalanceLocation.CE, BalanceSnaphot.HISTORIC_COL) / 12

        t = state.current_month + 1

        if t < self.ttp:
            alpha_t = math.pow(2, (t/self.ttp)) - 1
            hp = 0
        else:
            alpha_t = 1
            hp = lomax.rvs(c=self.hp_lomax_shape, scale=self.hp_lomax_scale)

        val = (self.r * alpha_t) + hp
        state.working_snapshot.sum_field_value(self.field_name, self.where, val, self.current_write_index(state))

        return state.working_snapshot

# TODO: Gestione delle immobilizzazioni in corso "B.I.6 Immobilizzazioni in corso e acconti
# Valutare se copiarle semplicemente o se trasferirle come immobilizzazioni completate in SP Attivo

class OrganicGrowthEffect(InvestmentEffect):
    seed = None
    field_target = "ricavi_vendite_e_prestazioni"

    def __init__(self, avg, var, title):
        self.average = avg / 12
        self.variance = var / 12
        super().__init__(title, EffectType.INCREASE,"ricavi_vendite_e_prestazioni",
                         EffectFrequency.MONTHLY,
                         BalanceLocation.CE)
        OrganicGrowthEffect.seed = np.random.default_rng(seed=42)

    def apply(self, state) -> BalanceSnaphot:
        current_month = state.current_month
        prev_value = 0
        if current_month == 0 or (current_month % 12) == 0:   # Primo mese dell'anno, prendo come valore iniziale lo storico
            # Il valore della colonna year start è annuale, quindi viene diviso per 12 per renderlo mensile
            prev_value = state.working_snapshot.get_field_value(self.field_name,BalanceLocation.CE, 0) / 12
            if prev_value is None:
                raise Exception("Attenzione: non è disponibile un'informazione di fatturato storico")
        else:
            # leggo il marginale precedente che è già diviso per 12
            prev_value = state.working_snapshot.get_field_value(self.field_name,BalanceLocation.CE, state.current_write_index() - 1)

        rng = OrganicGrowthEffect.seed
        Z_n = rng.normal(loc=0, scale=1)
        dt = 1 / 12
        X_tn1 = prev_value * exp(
            (self.average - self.variance / 2) * dt
            + sqrt(self.variance * dt) * Z_n
        )
        state.working_snapshot.sum_field_value(self.field_name, BalanceLocation.CE, X_tn1, column=self.current_write_index(state))
        return state.working_snapshot

class CostGrowthEffect(InvestmentEffect):
    field_target = "materie_prime_e_consumo"
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
        current_month = state.current_month
        prev_value = 0
        if current_month == 0 or (
                current_month % 12) == 0:
            prev_value = state.working_snapshot.get_field_value(self.field_name, BalanceLocation.CE, 0) / 12
            if prev_value is None:
                raise Exception("Attenzione: non è disponibile un'informazione di costo storico")
        else:
            # leggo il marginale precedente che è già diviso per 12
            prev_value = state.working_snapshot.get_field_value(self.field_name, BalanceLocation.CE,
                                                                state.current_write_index() - 1)

        growth_mean = self.avg / 12
        growth_var = self.var / 12
        factor_mean = 1.0 + growth_mean
        sigma2 = math.log1p(growth_var / (factor_mean ** 2))
        sigma = math.sqrt(sigma2)
        mu = math.log(factor_mean) - sigma2 / 2.0
        rng = CostGrowthEffect.seed
        growth_factor = rng.lognormal(mean=mu,sigma=sigma)
        state.working_snapshot.set_field_value(
            self.field_name,
            BalanceLocation.CE,
            prev_value * growth_factor,
            month=self.current_write_index(state)
        )

        return state.working_snapshot

class CreditCollectEffect(InvestmentEffect):
    seed: np.random.Generator | None = None  # Il seed è condiviso così non si resetta ad ogni applicazione

    """
    Effetto automatico di incasso dei crediti. 
    """
    def __init__(self, alpha: float, betha: float, cperc: float, title: str):
        super().__init__(title, EffectType.INCREASE, "",
                         EffectFrequency.ANNUAL,
                         BalanceLocation.SP_ATTIVO)
        self.alpha = alpha
        self.betha = betha
        self.cperc = cperc
        CreditCollectEffect.seed = np.random.default_rng(seed=42)

    def apply(self, state: SimulationState) -> BalanceSnaphot:
        # Sorteggiare una percentuale dalla distribuzione beta
        perc = CreditCollectEffect.seed.beta(self.alpha, self.betha)

        children = state.working_snapshot.get_children("totale_crediti", BalanceLocation.SP_ATTIVO, name_regex=r".*entro.*")
        for c in children:
            h = c.value[BalanceSnaphot.YEAR_START_COL]
            inc = h * perc      # Valore effettivamente incassato a fine anno
            # devo mettere un marginale che, sommato al valore storico diminuisca i crediti dell'importo incassato
            c.value[self.current_write_index(state)] = -1 * inc

        oltre = state.working_snapshot.get_children("totale_crediti", BalanceLocation.SP_ATTIVO, name_regex=r".*oltre.*")
        for o in oltre:
            h = o.value[BalanceSnaphot.YEAR_START_COL]
            trasf = h * self.cperc

            if trasf == 0:
                continue

            # devono essere sommati per non perdere gli incassi altrimenti i conti non tornano
            o.value[self.current_write_index(state)] = -1 * trasf
            n = None
            try:
                # provo a cercarlo con il nome, se lo trovo verifico che sia esattamente lui
                n = state.working_snapshot.get_node_by_name(o.name.replace("oltre", "entro").replace("_o1_", "_"), BalanceLocation.SP_ATTIVO)
                if n.field_name != o.field_name.replace("oltre", "entro").replace("_o1_", "_"):
                    raise Exception()
            except:
                n = state.working_snapshot.get_node_by_name(o.field_name.replace("oltre", "entro").replace("_o1_", "_"), BalanceLocation.SP_ATTIVO)

            n.value[self.current_write_index(state)] += trasf
            o.set_flag(Flag.UPDATED)

        return state.working_snapshot

class DebitPayEffect(InvestmentEffect):
    """
        Effetto automatico di pagamento dei debiti a entro e trasferimento debiti a oltre.
    """

    def __init__(self, years_ammort: float, title: str):
        super().__init__(title, EffectType.INCREASE, "",
                         EffectFrequency.ANNUAL,
                         BalanceLocation.SP_ATTIVO,
                         flags=[EffectExecFlags.YEAR_END])

        self.years_ammort = years_ammort
        self.ammort_quote: dict[str, float] = {}


    def apply(self, state: SimulationState) -> BalanceSnaphot:
        children = state.working_snapshot.get_children("totale_debiti", BalanceLocation.SP_PASSIVO_DEBITI,
                                                       name_regex=r".*entro.*")
        for c in children:
            h = c.value[BalanceSnaphot.YEAR_START_COL]

            # devo mettere un marginale che, sommato al valore storico diminuisca i debiti a entro e li porti a 0
            c.value[self.current_write_index(state)] = -1 * h

        oltre = state.working_snapshot.get_children("totale_debiti", BalanceLocation.SP_PASSIVO_DEBITI,
                                                    name_regex=r".*oltre.*")
        for o in oltre:
            if self.ammort_quote.get(o.name) is None:
                h = o.value[BalanceSnaphot.YEAR_START_COL]
                quote = h / self.years_ammort
                self.ammort_quote[o.name] = quote
            else:
                quote = self.ammort_quote.get(o.name)

            if quote == 0 or o.value[BalanceSnaphot.YEAR_START_COL] == 0:
                continue

            # devono essere sommati per non perdere gli incassi altrimenti i conti non tornano
            o.value[self.current_write_index(state)] -= quote
            n = None
            try:
                # provo a cercarlo con il nome, se lo trovo verifico che sia esattamente lui
                n = state.working_snapshot.get_node_by_name(o.name.replace("oltre", "entro").replace("_o1_", "_"),
                                                            BalanceLocation.SP_PASSIVO_DEBITI)
                if n.field_name != o.field_name.replace("oltre", "entro").replace("_o1_", "_"):
                    raise Exception()
            except:
                n = state.working_snapshot.get_node_by_name(o.field_name.replace("oltre", "entro").replace("_o1_", "_"),
                                                            BalanceLocation.SP_PASSIVO_DEBITI)


            n.value[self.current_write_index(state)] += quote
            o.set_flag(Flag.UPDATED)

        return state.working_snapshot
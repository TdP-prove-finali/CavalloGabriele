import simpy

from dao.util import BalanceLocation
from model.balance_snap import BalanceSnaphot


class SimulationStopEvent(simpy.events.Event):
    """
    Evento per richiedere il termine della simulazione
    """
    def __init__(self, env):
        super().__init__(env)
        self.motivation: simpy.events.Event | str | None = None

    def require_stop(self, motivation: simpy.events.Event | str):
        self.motivation = motivation
        self.succeed({
            "motivation": motivation.__str__()
        })

    def __str__(self):
        return f"Simulazione terminata per: {self.motivation.__str__()}"

class BankruptcyEvent(simpy.events.Event):
    """
    Rappresenta la bancarotta dell'impresa
    """

    def __init__(self, env, sim_stop: SimulationStopEvent):
        super().__init__(env)
        self.year = None
        self.liquidity = None
        self.sim_stop_evt = sim_stop
        self.callbacks.append(self.on_bankrupt)

    def declare_bankruptcy(self, year, liquidity):
        if self.triggered:
            return

        self.year = year
        self.liquidity = liquidity

        self.succeed({
            "year": year,
            "liquidity": liquidity
        })

    def on_bankrupt(self, event):
        print(self)
        self.sim_stop_evt.require_stop(self)

    def __str__(self):
        return f"Bancarotta all'anno {self.year} a causa di liquidità pari a {self.liquidity}"


class MoveCentralizedTreasury(simpy.events.Event):
    """
    Rappresenta la bancarotta dell'impresa
    """

    def __init__(self, env, amount, year, snapshot: BalanceSnaphot):
        super().__init__(env)
        self.amount = amount
        self.year = year
        self.snapshot = snapshot
        self.callbacks.append(self.handle_event)

    def require_move(self):
        if self.triggered:
            return

        self.succeed({
            "year": self.year,
            "amount": self.amount
        })

    def handle_event(self, event):
        print(self.__str__())
        # registro una diminuzione pari all'importo sul campo (eventualmente sommandolo a quantità già presenti)
        self.snapshot.sum_field_value("attivita_finanziarie_per_la_gestione_accentrata_della_tesoreria", BalanceLocation.SP_ATTIVO, self.amount * (-1) , BalanceSnaphot.YEAR_END_COL - 1)

    def __str__(self):
        return f"Prelevo liquidità dalla gestione accentrata verso l'azienda corrente per un importo di {self.amount} "


class DebitorInsolvencyEvent(simpy.events.Event):
    """
    Rappresenta la situazione di insolvenza parziale o totale dei debiti verso creditori
    """

    def __init__(self, env, sim_stop: SimulationStopEvent):
        super().__init__(env)
        self.year = None
        self.liquidity = None
        self.total_debt_entro = None
        self.sim_stop_evt = sim_stop
        self.callbacks.append(self.on_bankrupt)

    def declare_insolvency(self, year, liquidity, total_debt_entro):
        if self.triggered:
            return

        self.year = year
        self.liquidity = liquidity
        self.total_debt_entro = total_debt_entro

        self.succeed({
            "year": year,
            "liquidity": liquidity,
            "total_debt_entro": total_debt_entro
        })

    def on_bankrupt(self, event):
        print(self)
        self.sim_stop_evt.require_stop(self)

    def __str__(self):
        return f"Bancarotta all'anno {self.year} a causa di insolvenza verso i debitori. La liquidità è pari a {self.liquidity} ma i debiti sono di {self.total_debt_entro}"


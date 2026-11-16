import simpy

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


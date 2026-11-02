import simpy
from PySide6.QtCore import QObject, Signal, Slot

from dao.simulation.simulation_dao import SimulationDAO
from model.investment_effect import OrganicGrowthEffect, EffectFrequency
from model.sim_output import SimulationOutput
from model.sim_state import SimulationCompleteModel

class SimulationWorker(QObject):
    finished = Signal(object)
    error = Signal(str)
    progress = Signal(float)

    def __init__(self, model: SimulationCompleteModel):
        super().__init__()
        self.model = model

    def simulation_init(self):
        g = OrganicGrowthEffect(self.model.simulation_state.global_parameters.organic_growth_avg, self.model.simulation_state.global_parameters.organic_growth_var, "organic-growth")
        self.model.project.global_effects.append(g)

    @Slot()
    def start(self):
        m: SimulationCompleteModel = self.model
        total_step = m.simulation_state.global_parameters.number_of_years * 12
        self.simulation_init()

        def effect_spawner(env):
            id = m.simulation_state.global_parameters.sim_id
            print("Simulation id " + str(id))
            m.simulation_state.current_month = 0

            while True:
                print("===================")
                print("Mese " + str(m.simulation_state.current_month))
                self.model.simulation_state.working_snapshot.create_column("Mese "+ str(m.simulation_state.current_month))
                # Esecuzione effetti globali
                for effect in self.model.project.global_effects:
                    if effect.frequency == EffectFrequency.MONTHLY:
                        print("Eseguo l'effetto mensile " + effect.title)
                        effect.apply(self.model.simulation_state)
                    elif effect.frequency == EffectFrequency.ANNUAL and m.simulation_state.current_month % 12 == 0:
                        print("Eseguo l'effetto annuale " + effect.title)
                        effect.apply(self.model.simulation_state)

                yield env.timeout(1)
                m.simulation_state.current_month += 1
                print("===================")

        self.model.env = simpy.Environment()
        self.model.env.process(effect_spawner(self.model.env))
        # Aggiungere i process-generator
        self.model.env.run(until=m.simulation_state.global_parameters.number_of_years * 12)
        output = SimulationOutput(
            balance=self.model.simulation_state.working_snapshot,
            project=self.model.project,
            global_parameters=self.model.simulation_state.global_parameters
        )
        self.save_generated_data(output)
        self.finished.emit(output)

    def save_generated_data(self, output):
        try:
            SimulationDAO.save_simulation(output)
        except:
            print("Errore durante il salvataggio")
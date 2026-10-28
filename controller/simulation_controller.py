import simpy
from PySide6.QtCore import QObject, Signal, Slot

from dao.simulation.simulation_dao import SimulationDAO
from model.raw_company_data import BalanceSnaphot
from model.sim_output import SimulationOutput
from model.sim_state import SimulationCompleteModel

class SimulationWorker(QObject):
    finished = Signal(object)
    error = Signal(str)
    progress = Signal(float)

    def __init__(self, model: SimulationCompleteModel):
        super().__init__()
        self.model = model

    @Slot()
    def start(self):
        m: SimulationCompleteModel = self.model
        total_step = m.simulation_state.global_parameters.number_of_years * 12

        def effect_spawner(env):
            id = m.simulation_state.global_parameters.sim_id
            print("Simulation id " + str(id))

            while True:
                print('Start parking at %d' % env.now)
                self.progress.emit(env.now / total_step)
                parking_duration = 5
                self.model.simulation_state.working_snapshot.create_column("Colonna " + str(env.now))
                yield env.timeout(parking_duration)
                self.progress.emit(env.now / total_step)

                print('Start driving at %d' % env.now)
                trip_duration = 2
                self.model.simulation_state.working_snapshot.create_column("Colonna " + str(env.now))
                yield env.timeout(trip_duration)
                self.progress.emit(env.now / total_step)

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
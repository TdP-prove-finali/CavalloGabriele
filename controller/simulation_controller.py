import simpy
from PySide6.QtCore import QObject, Signal, Slot
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

        def effect_spawner(env):
            id = m.simulation_state.global_parameters.sim_id
            print("Simulation id " + str(id))

            while True:
                print('Start parking at %d' % env.now)
                self.progress.emit(env.now)
                parking_duration = 5
                yield env.timeout(parking_duration)
                self.progress.emit(env.now)

                print('Start driving at %d' % env.now)
                trip_duration = 2
                yield env.timeout(trip_duration)
                self.progress.emit(env.now)

        self.model.env = simpy.Environment()
        self.model.env.process(effect_spawner(self.model.env))
        # Aggiungere i process-generator
        self.model.env.run(until=m.simulation_state.global_parameters.number_of_years * 12)
        self.finished.emit(self.model.simulation_state.working_snapshot)

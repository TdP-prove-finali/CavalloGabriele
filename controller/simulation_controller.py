from typing import Any

import simpy

from controller.abstract import AbstractController
from model.sim_state import SimulationCompleteModel

class SimulationController(AbstractController[Any, SimulationCompleteModel, Any]):

    def start(self):
        m: SimulationCompleteModel = self.model

        def effect_spawner(env):
            id = m.simulation_state.global_parameters.sim_id
            print("Simulation id " + str(id))

            while True:
                print('Start parking at %d' % env.now)
                parking_duration = 5
                yield env.timeout(parking_duration)

                print('Start driving at %d' % env.now)
                trip_duration = 2
                yield env.timeout(trip_duration)

        self.model.env = simpy.Environment()
        self.model.env.process(effect_spawner(self.model.env))
        # Aggiungere i process-generator
        self.model.env.run(until=m.simulation_state.global_parameters.number_of_years * 12)

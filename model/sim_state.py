import simpy

from model.balance_snap import BalanceSnaphot

from model.sim_params import GlobalParameters

class SimulationState:
    def __init__(self, h_comp_data,
                 global_parameters: GlobalParameters):
        self.historical_company_data = h_comp_data
        self.global_parameters = global_parameters
        self.current_month: int = 0
        initial_snapshot = BalanceSnaphot.from_company_data(h_comp_data,
                                                            sim_id=global_parameters.sim_id,
                                                            timestamp=self.current_month,
                                                            effect_pointer="",
                                                            single_year=True,
                                                            global_config=self.global_parameters)
        self.working_snapshot: BalanceSnaphot = initial_snapshot

class SimulationCompleteModel:
    def __init__(self, simulation_state: SimulationState, project):
        self.sim_env = simpy.Environment()      # Il model contiene l'ambiente della simulazione e altre variabili
        self.simulation_state = simulation_state
        self.project = project
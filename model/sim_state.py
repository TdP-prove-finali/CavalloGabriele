import simpy

from model.investment_item import InvestmentProject
from model.raw_company_data import CompanyData, BalanceSnaphot
from dataclasses import dataclass

@dataclass
class GlobalParameters:
    selected_company: str
    number_of_years: int
    initial_year: int
    organic_growth: float
    last_available_years: int
    sim_id: int

class SimulationState:
    def __init__(self, h_comp_data: CompanyData, global_parameters: GlobalParameters):
        self.historical_company_data = h_comp_data
        self.global_parameters = global_parameters
        self.timestamp = (0, 0)
        initial_snapshot = BalanceSnaphot.from_company_data(h_comp_data, sim_id=global_parameters.sim_id, timestamp=self.timestamp, effect_pointer="")
        self.working_snapshot: BalanceSnaphot = initial_snapshot

class SimulationCompleteModel:
    def __init__(self, simulation_state: SimulationState, project: InvestmentProject):
        self.sim_env = simpy.Environment()      # Il model contiene l'ambiente della simulazione e altre variabili
        self.simulation_state = simulation_state
        self.project = project
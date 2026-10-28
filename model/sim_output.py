
from dataclasses import dataclass

from model.investment_item import InvestmentProject
from model.raw_company_data import BalanceSnaphot
from model.sim_state import GlobalParameters

@dataclass
class SimulationOutput:
    balance: BalanceSnaphot
    project: InvestmentProject
    global_parameters: GlobalParameters
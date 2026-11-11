
from dataclasses import dataclass

from model.balance_snap import BalanceSnaphot
from model.investment_item import InvestmentProject
from model.sim_params import GlobalParameters


@dataclass
class SimulationOutput:
    balance: BalanceSnaphot
    project: InvestmentProject
    global_parameters: GlobalParameters
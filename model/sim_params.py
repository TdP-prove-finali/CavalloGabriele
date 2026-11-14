from dataclasses import dataclass


@dataclass
class GlobalParameters:
    selected_company: str
    number_of_years: int
    organic_growth_avg: float
    organic_growth_var: float
    last_available_years: int
    sim_id: int
    tax_perc: float
    cost_gr_avg: float
    cost_gr_var: float

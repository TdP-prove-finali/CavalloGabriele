from dataclasses import dataclass, field

from model.investment_item import AbstractInvestmentItem


@dataclass
class InvestmentProjModel:
    proj_name: str | None
    proj_description: str | None
    components: list[AbstractInvestmentItem]
    selected_company: str
    number_of_years: int | None
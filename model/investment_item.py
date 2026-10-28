from enum import IntEnum

from model.investment_effect import (InvestmentEffect,
                                     EffectFrequency,
                                     EffectDestination,
                                     ValueMode, EffectType)


class AbstractInvestmentItem:
    def __init__(self, title: str, id: int, type: str, effects: list[InvestmentEffect]):
        self.title = title
        self.id = id
        self.type = type
        self.effects = effects

    def total_expenditure_first_month(self) -> float:
        """
        Restituisce la spesa totale per questo item nel primo mese
        :return:
        """
        return 0.0

    def total_funding_request_first_month(self) -> float:
        """
        Restituisce il totale dei finanziamenti richiesti da questa componente nel primo mese
        :return:
        """
        return 0.0

class EmployeeHireInvestment(AbstractInvestmentItem):
    def __init__(self,
                 title: str,
                 id: int,
                 total_monthly_cost: float,
                 onboarding_cost: float,
                 strumental_cost: float,
                 hp_lomax_scale: float,
                 hp_lomax_shape: float,
                 ttp_normal_average: float,
                 ttp_normal_variance:float,
                 stop_ratio: float,
                 role: str):

        effects = list()
        self.type = "employee-hire"
        self.tfr_quote = (total_monthly_cost * 12) / 13.5
        self.role = role
        self.onboarding_cost = onboarding_cost
        self.strumental_cost = strumental_cost
        self.hp_lomax_scale = hp_lomax_scale
        self.hp_lomax_shape = hp_lomax_shape
        self.ttp_normal_average = ttp_normal_average
        self.ttp_normal_variance = ttp_normal_variance
        self.stop_ratio = stop_ratio
        self.total_monthly_cost = total_monthly_cost

        # TODO: Raffinare gli effetti
        effects.append(InvestmentEffect(
            0, EffectType.INCREASE, ValueMode.CONSTANT, "costi_operativi", EffectFrequency.MONTHLY, EffectDestination.CONTO_ECON, value_constant=total_monthly_cost),
        )
        effects.append(InvestmentEffect(
            1, EffectType.INCREASE, ValueMode.CONSTANT, "costi_operativi", EffectFrequency.ANNUAL,
            EffectDestination.CONTO_ECON, value_constant=self.tfr_quote),
        )
        effects.append(InvestmentEffect(
            1, EffectType.INCREASE, ValueMode.CONSTANT, "costi_operativi", EffectFrequency.ONCE,
            EffectDestination.CONTO_ECON, value_constant=onboarding_cost),
        )

        super().__init__(title, id, self.type, effects)

    def total_expenditure_first_month(self):
        return self.total_monthly_cost + self.strumental_cost + self.onboarding_cost + self.tfr_quote / 12

class AssetType(IntEnum):
    MATERIAL = 0,
    IMMATERIAL = 1

class AssetInvestment(AbstractInvestmentItem):
    def __init__(self,
                 title: str,
                 id: int,
                 total_cost: float,
                 duration_years: int,
                 maintenance_cost: float,
                 asset_type: AssetType
                 ):
        self.type = "asset-investment"
        self.asset_type = asset_type

        if total_cost < 0:
            raise ValueError("Il costo del cespite non può essere negativo")

        self.total_cost = total_cost

        if duration_years <= 0:
            raise ValueError("La durata di un cespite non può essere negativa")

        self.duration_years = duration_years
        self.maintenance_cost = maintenance_cost
        self.amortization_quote = self.total_cost / self.duration_years
        effects = []            # TODO: Impostare effetti
        super().__init__(title, id, self.type, effects)

    def total_expenditure_first_month(self) -> float:
        return self.total_cost

class ProductivityImprovementInvestment(AbstractInvestmentItem):
    def __init__(self,
                 title: str,
                 id: int,
                 total_cost: float,
                 yearly_op_cost_reduction: float
                 ):
        self.type = "op-improvement-investment"

        if total_cost < 0:
            raise ValueError("Il costo del cespite non può essere negativo")

        self.yearly_op_cost_reduction = yearly_op_cost_reduction
        self.total_cost = total_cost
        effects = []            # TODO: Impostare effetti
        super().__init__(title, id, self.type, effects)

    def total_expenditure_first_month(self) -> float:
        return self.total_cost

class FundingType(IntEnum):
    BANK = 0,
    STOCK = 1

class FundingInvestment(AbstractInvestmentItem):
    def __init__(self, title: str,
                 id: int,
                 total_import: float,
                 type: FundingType,
                 interest_rate: float | None,
                 duration: int | None
                 ):
        self.total_import = total_import
        self.funding_type = type
        self.interest_rate = interest_rate
        self.duration = duration
        effects = []
        super().__init__(title, id, "funding-investment", effects)

    def total_funding_request_first_month(self) -> float:
        return self.total_import

class InvestmentProject:
    def __init__(self, title: str, description: str, global_effects: list, items: list[AbstractInvestmentItem] | None = None):
        self.title = title
        self.description = description
        self.items: list[AbstractInvestmentItem] = items or []
        self.global_effects = global_effects

    @staticmethod
    def total_expenditure(items: list[AbstractInvestmentItem]):
        f = 0
        for item in items:
            f += item.total_expenditure_first_month()

        return f

    @staticmethod
    def total_funding_request(items: list[AbstractInvestmentItem]):
        f = 0
        for item in items:
            f += item.total_funding_request_first_month()

        return f
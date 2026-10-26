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
        self.strumental_cost = strumental_cost
        self.hp_lomax_scale = hp_lomax_scale
        self.hp_lomax_shape = hp_lomax_shape
        self.ttp_normal_average = ttp_normal_average
        self.ttp_normal_variance = ttp_normal_variance
        self.stop_ratio = stop_ratio

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

class AssetInvestment(AbstractInvestmentItem):
    def __init__(self,
                 title: str,
                 id: int,
                 description: str,
                 total_cost: float,
                 duration_years: int,
                 maintenance_cost: float
                 ):
        self.type = "asset-investment"
        self.description = description

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

class ProductivityImprovementInvestment(AbstractInvestmentItem):
    def __init__(self,
                 title: str,
                 id: int,
                 description: str,
                 total_cost: float,
                 yearly_op_cost_reduction: float
                 ):
        self.type = "op-improvement-investment"
        self.description = description

        if total_cost < 0:
            raise ValueError("Il costo del cespite non può essere negativo")

        self.yearly_op_cost_reduction = yearly_op_cost_reduction
        self.total_cost = total_cost
        effects = []            # TODO: Impostare effetti
        super().__init__(title, id, self.type, effects)

class InvestmentProject:
    def __init__(self, title: str, description: str, global_effects: list):
        self.title = title
        self.description = description
        self.items: list[AbstractInvestmentItem] = []
        self.global_effects = global_effects
from model.investment_effect import InvestmentEffect, EffectType, ValueMode, EffectFrequency, EffectDestination


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

        super().__init__(title, id, type, effects)

class InvestmentProject:
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description
        self.items: list[AbstractInvestmentItem] = []
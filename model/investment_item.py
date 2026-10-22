from model.investment_effect import InvestmentEffect, EffectType, ValueMode, EffectFrequency, EffectDestination


class AbstractInvestmentItem:
    def __init__(self, title: str, id: int, type: str, effects: list[InvestmentEffect]):
        self.title = title
        self.id = id
        self.type = type
        self.effects = effects

class EmployeeHireInvestment(AbstractInvestmentItem):
    def __init__(self, title: str, id: int, type: str,
                 total_monthly_cost: float, onboarding_cost: float, role: str):
        effects = list()
        # TODO: Raffinare gli effetti
        self.tfr_quote = (total_monthly_cost * 12) / 13.5
        self.role = role
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
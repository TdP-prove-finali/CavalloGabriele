from enum import IntEnum

from model.investment_effect import (InvestmentEffect,
                                     EffectFrequency,
                                     EffectType, ProductivityIncreaseEffect, MoveImportInvEffect, IdFactory)
from model.node import BalanceLocation

# TODO: Gestire l'unità di misura del denaro in modo comodo (se i dati sono in migliaia mettere /1000 altrimenti i conti non tornano
class AbstractInvestmentItem:
    def __init__(self, title: str, type: str, effects: list[InvestmentEffect]):
        self.title = title
        self.id = IdFactory.new_id()
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
                 total_monthly_cost: float,
                 onboarding_cost: float,
                 strumental_cost: float,
                 hp_lomax_scale: float,
                 hp_lomax_shape: float,
                 ttp_normal_average: float,
                 ttp_normal_variance:float,
                 role: str):

        effects = list()
        self.type = "employee-hire"
        self.tfr_quote = (total_monthly_cost * 12) / 13.5
        self.role = role
        self.onboarding_cost = onboarding_cost
        self.strumental_cost = strumental_cost
        self.total_monthly_cost = total_monthly_cost

        effects.append(InvestmentEffect(
            title="stipendio-mensile",
            inv_type=EffectType.CONST,
            field_name="salari_e_stipendi",
            frequency=EffectFrequency.MONTHLY,
            where=BalanceLocation.CE,
            value_constant=total_monthly_cost),
        )
        effects.append(InvestmentEffect(
            title="accantonamento-tfr",
            inv_type=EffectType.CONST,
            field_name="tratt_fine_rapporto",
            frequency=EffectFrequency.ANNUAL,
            where=BalanceLocation.CE,
            value_constant=self.tfr_quote),
        )
        effects.append(InvestmentEffect(
            title="onboarding-cost",
            inv_type=EffectType.CONST,
            field_name="altri_costi",
            frequency=EffectFrequency.ONCE,
            where=BalanceLocation.CE,
            value_constant=onboarding_cost + strumental_cost),
        )
        effects.append(InvestmentEffect(
            title="employee-number",
            inv_type=EffectType.CONST,
            field_name="dipendenti",
            frequency=EffectFrequency.ANNUAL,
            value_constant=1,
            where=BalanceLocation.CE
        ))
        effects.append(ProductivityIncreaseEffect(
            average=ttp_normal_average,
            variance=ttp_normal_variance,
            hp_lomax_shape=hp_lomax_shape,
            hp_lomax_scale=hp_lomax_scale
        ))

        super().__init__(title, self.type, effects)

    def total_expenditure_first_month(self):
        return self.total_monthly_cost + self.strumental_cost + self.onboarding_cost + self.tfr_quote / 12

class AssetType(IntEnum):
    MATERIAL = 0,
    IMMATERIAL = 1

class AssetInvestment(AbstractInvestmentItem):
    def __init__(self,
                 title: str,
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
        effects = [
        ]
        if self.asset_type == AssetType.MATERIAL:
            field_amm = "amm_immob_mat"
            field_immob = "costi_ricerca_e_pubb"
        else:
            field_amm = "amm_immob_immat"
            field_immob = "impianti"

        effects.append(InvestmentEffect(
                title="ammortamento-cespite",
                inv_type=EffectType.CONST,
                field_name=field_amm,
                frequency=EffectFrequency.ANNUAL,
                where=BalanceLocation.CE,
                value_constant=self.amortization_quote,
            until=self.duration_years * 12
        ))
        effects.append(InvestmentEffect(
            field_name="servizi",
            where=BalanceLocation.CE,
            title="costo-manutenzione",
            frequency=EffectFrequency.ANNUAL,
            value_constant=self.maintenance_cost,
            inv_type=EffectType.CONST
        ))
        effects.append(InvestmentEffect(
            title="incremento-immobilizzazioni",
            inv_type=EffectType.CONST,
            field_name=field_immob,
            frequency=EffectFrequency.ONCE,
            value_constant=self.total_cost,
            where=BalanceLocation.SP_ATTIVO
        ))

        super().__init__(title, self.type, effects)

    def total_expenditure_first_month(self) -> float:
        return self.total_cost

class ProductivityImprovementInvestment(AbstractInvestmentItem):
    def __init__(self,
                 title: str,
                 total_cost: float,
                 yearly_op_red: float,
                 yearly_red_perc: float,
                 duration: int
                 ):
        self.type = "op-improvement-investment"
        self.duration = duration
        self.yearly_op_red_perc = yearly_red_perc
        if total_cost < 0:
            raise ValueError("Il costo del cespite non può essere negativo")

        self.yearly_op_cost_red = yearly_op_red
        self.total_cost = total_cost
        effects = [
            InvestmentEffect(
                title="cost-reduction",
                field_name="servizi",
                value_constant=self.yearly_op_cost_red * (-1),
                frequency=EffectFrequency.ANNUAL,
                where=BalanceLocation.CE,
                inv_type=EffectType.CONST,
                until=self.duration * 12
            ),
            InvestmentEffect(
                title="cost-amortization",
                field_name="amm_immob_immat",
                inv_type=EffectType.CONST,
                frequency=EffectFrequency.ANNUAL,
                value_constant=self.total_cost / self.duration,
                where=BalanceLocation.CE,
                until=self.duration * 12
            ),
            InvestmentEffect(
                title="incremento-immobilizzazioni",
                inv_type=EffectType.CONST,
                field_name="costi_impianto_e_ampl",
                frequency=EffectFrequency.ONCE,
                value_constant=self.total_cost,
                where=BalanceLocation.SP_ATTIVO
            )
        ]
        super().__init__(title, self.type, effects)

    def total_expenditure_first_month(self) -> float:
        return self.total_cost

class FundingType(IntEnum):
    BANK = 0,
    STOCK = 1



class FundingInvestment(AbstractInvestmentItem):
    def __init__(self, title: str,
                 total_import: float,
                 type: FundingType,
                 interest_rate: float | None,
                 duration: int | None
                 ):
        self.total_import = total_import
        self.funding_type = type
        self.interest_rate = interest_rate
        self.duration = duration
        self.capital_quote_y = self.total_import / self.duration
        effects = []
        if type == FundingType.BANK:
            # inizialmente registro l'importo totale del debito e poi l'effetto di spostamento (eseguito successivamente) ne sposterà una parte in quelli entro
            effects.append(InvestmentEffect(
                field_name="banche_oltre_lesercizio",
                where=BalanceLocation.SP_PASSIVO_DEBITI,
                value_constant=self.total_import,
                frequency=EffectFrequency.ONCE,
                inv_type=EffectType.CONST,
                title="banche_oltre"
            ))
            effects.append(
                InvestmentEffect(
                    field_name="totale_oneri_finanziari",
                    where=BalanceLocation.CE,
                    frequency=EffectFrequency.ANNUAL,
                    value_constant=self.interest_rate * self.total_import,
                    title="interessi-passivi",
                    inv_type=EffectType.CONST,
                    until=self.duration * 12
                )
            )
            effects.append(
                MoveImportInvEffect(
                    source_field_name="banche_oltre_lesercizio",
                    dest_field_name="banche_entro_lesercizio",
                    frequency=EffectFrequency.ANNUAL,
                    value_constant=self.capital_quote_y,
                    where=BalanceLocation.SP_PASSIVO_DEBITI,
                    title="riduzione-debito",
                    until=self.duration * 12,
                    inv_type=EffectType.CONST
                )
            )
            # In questo modo, ogni anno, il totale da rimborsare viene diminuito della quota capitale
        elif type == FundingType.STOCK:
            effects.append(
                InvestmentEffect(
                    field_name="capitale_sociale",
                    where=BalanceLocation.SP_PASSIVO_PATRIM,
                    value_constant=self.total_import,
                    frequency=EffectFrequency.ONCE,
                    inv_type=EffectType.CONST,
                    title="versamento-cap-sociale"
                )
            )
        super().__init__(title, "funding-investment", effects)

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

        return round(f)

    @staticmethod
    def total_funding_request(items: list[AbstractInvestmentItem]):
        f = 0
        for item in items:
            f += item.total_funding_request_first_month()

        return round(f)
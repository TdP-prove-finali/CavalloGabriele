import math

import simpy
from PySide6.QtCore import QObject, Signal, Slot
from dao.simulation.simulation_dao import SimulationDAO
from dao.util import BalanceLocation
from model.balance_snap import BalanceSnaphot
from model.event.custom_events import BankruptcyEvent, SimulationStopEvent, CreditorInsolvencyEvent, \
    MoveCentralizedTreasury
from model.investment_effect import OrganicGrowthEffect, EffectFrequency, CostGrowthEffect, CreditCollectEffect, \
    InvestmentEffect, EffectExecFlags, DebitPayEffect
from model.sim_output import SimulationOutput
from model.sim_state import SimulationCompleteModel, SimulationState

class SimulationWorker(QObject):
    finished = Signal(object)
    error = Signal(str)
    progress = Signal(float)

    def __init__(self, model: SimulationCompleteModel):
        super().__init__()
        self.model = model
        self.sim_finish_event: SimulationStopEvent | None = None
        self.bankrupt_event: BankruptcyEvent | None = None
        self.timeout_event = None
        self.insolvency_event: CreditorInsolvencyEvent | None = None

    def simulation_init(self):
        """
        Inizializza la simulazione aggiungendo gli effetti globali
        :return:
        """
        g_pars = self.model.simulation_state.global_parameters
        g = OrganicGrowthEffect(g_pars.organic_growth_avg, g_pars.organic_growth_var, "organic-growth")
        c = CostGrowthEffect(g_pars.cost_gr_avg, g_pars.cost_gr_var, "cost-growth")
        cc = CreditCollectEffect(g_pars.cred_alpha, g_pars.cred_betha, g_pars.cperc, "credit-collect")
        dbt = DebitPayEffect(2, "debit-pay")
        self.model.project.global_effects.append(g)
        self.model.project.global_effects.append(c)
        self.model.project.global_effects.append(cc)
        self.model.project.global_effects.append(dbt)
        self.__year_init__()

    def __year_init__(self):
        snap = self.model.simulation_state.working_snapshot
        snap.create_year_start()

        if snap.available_columns != 15:
            for m in range(1, 13):  # Creo i primi 12 mesi
                self.model.simulation_state.working_snapshot.create_column(f"Mese {m}")

            self.model.simulation_state.working_snapshot.create_column(
                f"Year end")  # Colonna in cui calcolare i risultati di fine anno

    def __is_year_end(self):
        return self.model.simulation_state.current_month != 0 and (self.model.simulation_state.current_month + 1) % 12 == 0

    def __current_year__(self):
        if self.model.simulation_state.current_month == 0:
            return 1

        return math.floor((self.model.simulation_state.current_month + 1) / 12)

    def __execute_effect__(self, effect: InvestmentEffect):
        """
        Esegue un effetto (se è arrivato il suo momento)
        :param effect:
        :return:
        """
        m: SimulationCompleteModel = self.model
        if effect.frequency == EffectFrequency.MONTHLY:
            self.model.log("Eseguo l'effetto mensile " + effect.title)
            effect.apply(self.model.simulation_state)
        elif effect.frequency == EffectFrequency.ANNUAL and self.__is_year_end():
            self.model.log("Eseguo l'effetto annuale " + effect.title)
            effect.apply(self.model.simulation_state)
        elif effect.frequency == EffectFrequency.BI_MONTHLY and m.simulation_state.current_month % 2 == 0:
            self.model.log("Eseguo l'effetto bimestrale " + effect.title)
            effect.apply(self.model.simulation_state)
        elif effect.frequency == EffectFrequency.TRI_MONTHLY and m.simulation_state.current_month % 3 == 0:
            self.model.log("Eseguo l'effetto trimestrale " + effect.title)
            effect.apply(self.model.simulation_state)
        elif effect.frequency == EffectFrequency.ONCE and m.simulation_state.current_month == 0:
            self.model.log("Eseguo effetto once " + effect.title)
            effect.apply(self.model.simulation_state)

    def __execute_global_effects__(self):
        """
        Esegue gli effetti globali, controllando se si applicano
        :return:
        """
        for effect in self.model.project.global_effects:
            if EffectExecFlags.YEAR_END not in effect.flags:
                self.__execute_effect__(effect)

    def __execute_global_effects_year_end_(self):
        """
        Esegue gli effetti globali, controllando se si applicano
        :return:
        """
        for effect in self.model.project.global_effects:
            if EffectExecFlags.YEAR_END in effect.flags:
                self.__execute_effect__(effect)

    def __execute_project_effects__(self):
        """
        Esegue gli effetti del progetto, se si applicano
        :return:
        """
        for item in self.model.project.items:  # Effetti legati alle componenti di investimento impostate
            self.model.log(f"Applicazione componente {item}")
            for effect in item.effects:
                self.__execute_effect__(effect)

    def __bankruptcy_check__(self, snapshot: BalanceSnaphot, column: int) -> simpy.events.Event | None:
        """
        Controlla le condizioni di bancarotta (liquidità negativa o impossibilità di pagamento debiti entro
        :param snapshot: Bilancio da leggere
        :return:
        """
        liq = snapshot.get_total_liquidity(column)
        acc = snapshot.get_field_value("attivita_finanziarie_per_la_gestione_accentrata_della_tesoreria", BalanceLocation.SP_ATTIVO, column)
        if liq + acc < 0:
            self.bankrupt_event.declare_bankruptcy(
                self.__current_year__(),
                self.model.simulation_state.working_snapshot.get_total_liquidity(
                    BalanceSnaphot.YEAR_END_COL))
            return self.bankrupt_event

        t_debt_entro = snapshot.get_total_debit_entro(column)
        if  t_debt_entro > liq + acc:

            self.insolvency_event.declare_insolvency(self.__current_year__(),
                self.model.simulation_state.working_snapshot.get_total_liquidity(
                    BalanceSnaphot.YEAR_END_COL),
                    self.model.simulation_state.working_snapshot.get_total_debit_entro(column))

            return self.insolvency_event

        diff = t_debt_entro - liq
        if diff > 0:
            mv = MoveCentralizedTreasury(self.model.env, diff, self.__current_year__(), self.model.simulation_state.working_snapshot)
            mv.require_move()
            return mv

        return None

    @Slot()
    def start(self):
        self.simulation_init()

        def effect_spawner(env):
            id = self.model.simulation_state.global_parameters.sim_id
            self.model.log("Simulation id " + str(id))
            self.model.simulation_state.current_month = 0

            while True:
                self.model.log("===================")
                self.model.log("Mese " + str(self.model.simulation_state.current_month))
                self.__execute_global_effects__()
                self.__execute_project_effects__()

                if self.__is_year_end():
                    self.model.log(f"Raggiunto termine anno {self.__current_year__()}")
                    # azioni da svolgere a fine anno sullo snapshot
                    self.model.simulation_state.working_snapshot.aggregate_by_year()
                    self.model.simulation_state.working_snapshot.recalculate_balance()
                    # logica di gestione del debito e fallimento
                    evt = self.__bankruptcy_check__(self.model.simulation_state.working_snapshot, BalanceSnaphot.YEAR_END_COL)
                    if evt is not None:
                        yield evt

                    self.model.log("Ricalcolo i debiti")
                    self.__execute_global_effects_year_end_()
                    # azzero solo lo stato patrimoniale
                    self.model.simulation_state.working_snapshot.reset_columns(BalanceSnaphot.YEAR_END_COL, BalanceSnaphot.YEAR_END_COL, 0, no_ce=True)
                    self.model.simulation_state.working_snapshot.aggregate_by_year(no_ce=True)
                    self.model.simulation_state.working_snapshot.recalculate_balance(only_sp=True)
                    self.model.simulation_state.working_snapshot.calc_indicies()
                    f_s = self.model.simulation_state.final_result_snapshot
                    f_s.create_column(f"Anno {self.__current_year__()}")
                    f_s.copy_column_from_snapshot(
                        snapshot=self.model.simulation_state.working_snapshot,
                        source_column=14,
                        dest_column=f_s.available_columns - 1,
                        column_title=f"Anno {self.__current_year__()}"
                    )

                    # pulizia e re-inizializzazione
                    self.model.simulation_state.working_snapshot.reset_columns(2, 15)   # resetto anche la colonna year start e year end
                    self.model.simulation_state.working_snapshot.reset_calc_flags()
                    # tra un anno e l'altro eredito solo lo stato patrimoniale
                    self.model.simulation_state.working_snapshot.copy_sp_fields_from_snapshot(f_s, self.__current_year__(), BalanceSnaphot.YEAR_START_COL)
                    # i campi del CE vengono mantenuti identici a quelli di inizializzazione, in modo tale che gli effetti economici non siano moltiplicativi tra di loro
                    # gli unici che vengono copiati sono i campi utilizzati dagli effetti globali
                    self.model.simulation_state.working_snapshot.copy_field_from_snapshot(OrganicGrowthEffect.field_target, BalanceLocation.CE, f_s, self.__current_year__(), BalanceSnaphot.HISTORIC_COL)
                    self.model.simulation_state.working_snapshot.copy_field_from_snapshot(CostGrowthEffect.field_target, BalanceLocation.CE, f_s, self.__current_year__(), BalanceSnaphot.HISTORIC_COL)

                yield env.timeout(1)
                self.model.simulation_state.current_month += 1
                self.model.log("===================")

        self.model.env = simpy.Environment()
        self.sim_finish_event = SimulationStopEvent(self.model.env)
        self.bankrupt_event = BankruptcyEvent(self.model.env, self.sim_finish_event)
        self.insolvency_event = CreditorInsolvencyEvent(self.model.env, self.sim_finish_event)
        self.timeout_event = self.model.env.timeout((self.model.simulation_state.global_parameters.number_of_years * 12) - 1)
        self.model.env.process(effect_spawner(self.model.env))
        result = self.model.env.run(until=self.sim_finish_event | self.timeout_event)

        r = ""
        if self.sim_finish_event in result:
            self.model.log(f"Simulazione interrotta per: { self.sim_finish_event.motivation}")
            r = self.sim_finish_event.motivation
        elif self.timeout_event in result:
            self.model.log("Simulazione completata per raggiungimento del tempo massimo")
            r = "Raggiungimento del tempo massimo"

        output = SimulationOutput(
            balance=self.model.simulation_state.final_result_snapshot,
            project=self.model.project,
            global_parameters=self.model.simulation_state.global_parameters,
            reason_exit=r.__str__(),
            logs=self.model.simulation_state.relevant_logs,
            id=self.model.simulation_state.global_parameters.sim_id
        )
        self.save_generated_data(output)
        self.finished.emit(output)
        return output   # utile se si chiama il worker senza creare un thread

    def save_generated_data(self, output):
        try:
            SimulationDAO.save_simulation(output)
        except Exception as e:
            self.model.log("Errore durante il salvataggio")
            self.model.log(e)
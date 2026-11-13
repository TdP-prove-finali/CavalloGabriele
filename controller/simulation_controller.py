import simpy
from PySide6.QtCore import QObject, Signal, Slot

from dao.simulation.simulation_dao import SimulationDAO
from model.investment_effect import OrganicGrowthEffect, EffectFrequency
from model.sim_output import SimulationOutput
from model.sim_state import SimulationCompleteModel

class SimulationWorker(QObject):
    finished = Signal(object)
    error = Signal(str)
    progress = Signal(float)

    def __init__(self, model: SimulationCompleteModel):
        super().__init__()
        self.model = model

    def simulation_init(self):
        """
        Inizializza la simulazione aggiungendo gli effetti globali
        :return:
        """
        g = OrganicGrowthEffect(self.model.simulation_state.global_parameters.organic_growth_avg, self.model.simulation_state.global_parameters.organic_growth_var, "organic-growth")
        self.model.project.global_effects.append(g)
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
        return self.model.simulation_state.current_month % 12

    @Slot()
    def start(self):
        m: SimulationCompleteModel = self.model
        self.simulation_init()

        def effect_spawner(env):
            # TODO: Cambiare struttura
            # al termine di ogni anno, eseguire:
            # 1. Aggregazione dei valori orizzontali
            # 2. Calcolo voci terminali tramite algoritmo ricorsivo
            # 3. Calcolo indici
            # tutto sulla colonna 14 che contiene lo year end
            # copiare la colonna 14 nello snapshot dei final results
            # rimuovere tutte le colonne tranne la 0
            # copiare lo year end nella colonna 0 del working snapshot
            # al termine dell'anno, verificare se la cassa è negativa:
            # se supera la soglia del fido (impostata da parametri simulazione) bloccare la simulazione e indicare che l'azienda è fallita
            # se non supera la soglia di fido, far nascere un debito e vedere come va successivamente

            id = m.simulation_state.global_parameters.sim_id
            print("Simulation id " + str(id))
            m.simulation_state.current_month = 0

            while True:
                print("===================")
                print("Mese " + str(m.simulation_state.current_month))
                # Esecuzione effetti globali
                for effect in self.model.project.global_effects:
                    if effect.frequency == EffectFrequency.MONTHLY:
                        print("Eseguo l'effetto mensile " + effect.title)
                        effect.apply(self.model.simulation_state)
                    elif effect.frequency == EffectFrequency.ANNUAL and self.__is_year_end():
                        print("Eseguo l'effetto annuale " + effect.title)
                        effect.apply(self.model.simulation_state)
                    elif effect.frequency == EffectFrequency.ONCE and m.simulation_state.current_month == 0:
                        print("Eseguo effetto once " + effect.title)
                        effect.apply(self.model.simulation_state)

                for item in self.model.project.items:   # Effetti legati alle componenti di investimento impostate
                    print(f"Applicazione componente {item}")
                    for effect in item.effects:
                        if effect.frequency == EffectFrequency.MONTHLY:
                            print("Eseguo l'effetto mensile " + effect.title)
                            effect.apply(self.model.simulation_state)
                        elif effect.frequency == EffectFrequency.ANNUAL and self.__is_year_end():
                            print("Eseguo l'effetto annuale " + effect.title)
                            effect.apply(self.model.simulation_state)
                        elif effect.frequency == EffectFrequency.BI_MONTHLY and m.simulation_state.current_month % 2 == 0:
                            print("Eseguo l'effetto bimestrale " + effect.title)
                            effect.apply(self.model.simulation_state)
                        elif effect.frequency == EffectFrequency.TRI_MONTHLY and m.simulation_state.current_month % 3 == 0:
                            print("Eseguo l'effetto trimestrale " + effect.title)
                            effect.apply(self.model.simulation_state)
                        elif effect.frequency == EffectFrequency.ONCE and m.simulation_state.current_month == 0:
                            print("Eseguo effetto once " + effect.title)
                            effect.apply(self.model.simulation_state)

                if self.__is_year_end():
                    print(f"Raggiunto termine anno {self.__current_year__()}")
                    # azioni da svolgere a fine anno sullo snapshot
                    self.model.simulation_state.working_snapshot.aggregate_by_year()
                    self.model.simulation_state.working_snapshot.recalculate_balance()
                    self.model.simulation_state.working_snapshot.calc_indicies()
                    f_s = m.simulation_state.final_result_snapshot
                    f_s.create_column(f"Anno {self.__current_year__()}")
                    f_s.copy_column_from_snapshot(
                        snapshot=self.model.simulation_state.working_snapshot,
                        source_column=14,
                        dest_column=f_s.available_columns - 1
                    )
                    self.model.simulation_state.working_snapshot.copy_column(14, 0)     # Il nuovo anno utilizzerà come bilancio storico quello generato dalla simulazione
                    if self.model.simulation_state.working_snapshot.get_total_liquidity(14) < 0:
                        print(f"WARNING: Al termine dell'anno {self.__current_year__()} la liquidità è diventata negativa. ")

                    # pulizia e re-inizializzazione
                    self.model.simulation_state.working_snapshot.reset_columns(2, 14)

                yield env.timeout(1)
                m.simulation_state.current_month += 1
                print("===================")

        self.model.env = simpy.Environment()
        self.model.env.process(effect_spawner(self.model.env))
        self.model.env.run(until=m.simulation_state.global_parameters.number_of_years * 12)
        output = SimulationOutput(
            balance=self.model.simulation_state.final_result_snapshot,
            project=self.model.project,
            global_parameters=self.model.simulation_state.global_parameters
        )
        self.save_generated_data(output)
        self.finished.emit(output)

    def save_generated_data(self, output):
        try:
            SimulationDAO.save_simulation(output)
        except:
            print("Errore durante il salvataggio")
import simpy


class Model:
    def __init__(self):
        self.sim_env = simpy.Environment()      # Il model contiene l'ambiente della simulazione e altre variabili
from copy import deepcopy
from typing import Callable, Any
import networkx as nx
from networkx.classes import DiGraph
from dao.util import step_up_field, extract_field_identif, SECTION_HEAD, BalanceLocation, sum_vectors
from model.FieldNotFoundException import FieldNotFoundException
from model.node import Node, NodeType, Flag
from model.raw_company_data import CompanyData
from model.sim_params import GlobalParameters

PRIVATE_FIELDS = ["data", "moneta", "periodo", "subsections"]

def get_matching_node(numeration: str, graph: DiGraph, where: BalanceLocation) -> Node | None:
    """Restituisce il nodo che ha esattamente la stessa numerazione di quella indicata e che si trova esattamente nella stessa sezione
    del documento. Il parametro where serve per distinguere campi che hanno la stessa numerazione ma si trovano in sezioni diverse del bilancio. . """
    c_num = numeration + "_" if not numeration.endswith("_") else numeration
    results = []
    for node in graph.nodes:
        if extract_field_identif(node.field_name) == c_num and where == node.where:
            results.append(node)

    if len(results) > 1:
        print(f"WARNING: Ci sono più nodi che fanno match con la numerazione {numeration} nella sezione {where.__str__()}")
        print(results)

        for r in results:
            if r.field_name.find("totale") >= 0:
                return r        # Di default viene restituito il campo che contiene un totale
    else:
        return results[0]

    return None

def get_matching_field_name(numeration: str, field_names: list[str]) -> str | None:
    """Restituisce il field_name che ha esattamente la numerazione indicata. """
    c_num = numeration + "_" if not numeration.endswith("_") else numeration

    for field_name in field_names:
        if extract_field_identif(field_name) == c_num:
            return field_name

    return None

def serialize_id_map(id_map: dict[str, Node], where: BalanceLocation)->dict[str, Any]:
    d = {}
    for name, node in id_map.items():
        if node.type != NodeType.VIRTUAL and not node.name in PRIVATE_FIELDS:
            d[node.field_name] = node.value

    if where != BalanceLocation.CE:
        d["subsections"] = {}
    return d

class BalanceSnaphot:
    CE_FIELD_FLAGS: dict[str, Flag] = {
        "ricavi_vendite_e_prestazioni": Flag.NO_COPY,
        "risultato_operativo": Flag.NO_COPY,
        "valore_aggiunto": Flag.NO_COPY,
        "totale_proventi_frac_oneri_straordinari": Flag.NO_COPY,
        "proventi_straordinari": Flag.NO_COPY,
        "oneri_straordinari": Flag.NO_COPY,
        "risultato_prima_delle_imposte": Flag.NO_COPY,
        "_20_totale_imposte_sul_reddito_correnti_differite_e_anticipate": Flag.NO_COPY,
        "imposte_correnti": Flag.NO_COPY,
        "imposte_relative_a_esercizi_precedenti": Flag.NO_COPY,
        '_21_utile_frac_perdita_di_esercizio': Flag.NO_COPY,
        "altri_ricavi": Flag.NO_COPY,
        "altre_svalut_immob": Flag.NO_COPY,
        "svalut_crediti": Flag.NO_COPY
    }

    SP_FIELD_FLAGS: dict[str, Flag] = {
    }

    YEAR_START_COL = 1
    HISTORIC_COL = 0
    YEAR_END_COL = 14

    def __init__(self,
                 stato_patrimoniale: DiGraph,
                 conto_economico: DiGraph,
                 sp_attivo_id_map: dict[str, Node],
                 sp_debiti_id_map: dict[str, Node],
                 sp_patrim_id_map: dict[str, Node],
                 ce_id_map: dict[str, Node],
                 indici: dict[str, Any],
                 timestamp: int,
                 sim_id: int,
                 available_years: int,
                 effect_pointer: str | None,
                 global_config: GlobalParameters
                 ):
        self.sp_attivo_id_map: dict[str, Node] = sp_attivo_id_map
        self.sp_debiti_id_map: dict[str, Node] = sp_debiti_id_map
        self.sp_patrim_id_map: dict[str, Node] = sp_patrim_id_map
        self.ce_id_map: dict[str, Node] = ce_id_map
        self.stato_patrimoniale: DiGraph = stato_patrimoniale
        self.conto_economico: DiGraph = conto_economico
        self.indici = indici
        self.timestamp = timestamp
        self.sim_id = sim_id
        self.effect_pointer = effect_pointer
        self.available_columns = available_years
        self.__integrity__: bool | None = None
        self.global_config = global_config

        self.CE_SPEC_CALC_RULES: dict[str, Callable[[Node, DiGraph], float]] = {
            'totale_proventi_e_oneri_finanziari': self.__calc_prov_fin,
            "totale_rettifiche_att_finanz": self.tot_rettif
        }
        # TODO: Formula di calcolo per le svalutazioni/rivalutazioni D totale rettifiche att finanz
        self.SP_SPEC_CALC_RULES: dict[str, Callable[[Node, DiGraph], float]] = {
            "totale_immob_immateriali": self.tot_immob,
            "totale_immob_materiali": self.tot_immob
        }

    def tot_rettif(self, node: Node, graph: DiGraph):
        s = 0
        children: list[Node] = list(graph.successors(node))
        for c in children:
            if "rivalutazioni" in c.name:
                s += self.__calc_from_node(c, graph)
            elif "svalutazioni" in c.name:
                s -= self.__calc_from_node(c, graph)

        return s

    def tot_immob(self, node: Node, graph: DiGraph):
        """
        Regola speciale di calcolo per il totale immobilizzazioni:
        veiene utilizzato l'ammortamento indiretto quindi i fondi devono essere sottratti
        :param node:
        :param graph:
        :param column:
        :return:
        """
        children = graph.successors(node)
        r = 0
        for c in children:
            if "fondo" in c.name:
                r -= self.__calc_from_node(c, graph)
            else:
                r += self.__calc_from_node(c, graph)
        return r

    def __calc_prov_fin(self, node: Node, graph: DiGraph):
        """
        Regola di calcolo per i proventi e oneri finanziari (gli oneri vanno sottratti alla somma di tutti gli altri)
        :param node: Nodo da cui partire
        :param graph: Grafo su cui lavorare
        :param read_col: Colonna da cui leggere il valore
        :param write_col: Colonna su cui scrivere il valore
        :return:
        """
        children = graph.successors(node)
        r = 0
        for c in children:
            if "oneri" in c.name:
                r -= self.__calc_from_node(c, graph)
            else:
                r += self.__calc_from_node(c, graph)
        return r

    @staticmethod
    def create_sp_graph(stato_patrimoniale: dict[str, Any]) -> tuple[DiGraph, dict, dict, dict]:
        """
        Crea il grafo dello stato patrimoniale e lo restituisce, insieme alle 3 id-map delle sezioni attivo, debiti, patrimonio netto
        :param stato_patrimoniale:
        :return:
        """
        id_map = {}
        graph = nx.DiGraph()
        sp = Node.virtual("stato_patrimoniale", BalanceLocation.SP)
        att = Node.virtual("attivo", BalanceLocation.SP_ATTIVO)
        pss = Node.virtual("passivo", BalanceLocation.SP_PASSIVO)
        dbt = Node.virtual("debiti", BalanceLocation.SP_PASSIVO_DEBITI)
        ptrm = Node.virtual("patrimonio_netto", BalanceLocation.SP_PASSIVO_PATRIM)
        id_map["stato_patrimoniale"] = sp
        id_map["attivo"] = att
        id_map["passivo"] = pss

        att_id_map = id_map.copy()
        pss_dbt_id_map = id_map.copy()
        pss_ptrm_id_map = id_map.copy()

        pss_dbt_id_map["debiti"] = dbt
        pss_ptrm_id_map["patrimonio_netto"] = ptrm

        graph.add_node(sp)
        graph.add_node(att)
        graph.add_edge(sp, att)
        graph.add_node(pss)
        graph.add_edge(sp, pss)
        graph.add_node(dbt)
        graph.add_edge(pss, dbt)
        graph.add_node(ptrm)
        graph.add_edge(pss, ptrm)

        BalanceSnaphot.__create_section_graph(att, stato_patrimoniale["subsections"]["attivo"], graph, att_id_map, BalanceLocation.SP_ATTIVO, BalanceSnaphot.SP_FIELD_FLAGS)
        BalanceSnaphot.__create_section_graph(dbt, stato_patrimoniale["subsections"]["passivo"]["subsections"]["debiti"], graph, pss_dbt_id_map, BalanceLocation.SP_PASSIVO_DEBITI, BalanceSnaphot.SP_FIELD_FLAGS)
        BalanceSnaphot.__create_section_graph(ptrm, stato_patrimoniale["subsections"]["passivo"]["subsections"]["patrimonio_netto"], graph, pss_ptrm_id_map, BalanceLocation.SP_PASSIVO_PATRIM, BalanceSnaphot.SP_FIELD_FLAGS)

        return (graph, att_id_map, pss_dbt_id_map, pss_ptrm_id_map)

    @staticmethod
    def create_ce_graph(conto_economico: dict[str, Any]) -> tuple[DiGraph, dict]:
        graph = DiGraph()
        ce = Node.virtual("conto_economico", BalanceLocation.CE)
        graph.add_node(ce)
        id_map = {"conto_economico": ce}
        BalanceSnaphot.__create_section_graph(ce, conto_economico, graph, id_map, BalanceLocation.CE, BalanceSnaphot.CE_FIELD_FLAGS)
        return (graph, id_map)

    @staticmethod
    def __create_section_graph(section_node: Node,
                               section: dict[str, Any],
                               graph: DiGraph,
                               id_map: dict[str, Any],
                               where: BalanceLocation,
                               default_flags: dict[str, Flag]
                               ):

        # prima creo tutti i nodi e poi li collego tutti
        for field_name, values in section.items():
            if field_name == "subsections":
                continue

            node = Node(
                type=NodeType.FIELD,
                field_name=field_name,
                value=values.copy(),
                flags=[],
                where=where
            )
            if default_flags.get(node.name) is not None:
                node.flags = [default_flags.get(node.name)]
                print(f"Applico flag di default a {node.field_name} -- {default_flags.get(node.name)}")
            graph.add_node(node)

            if id_map.get(node.name) is not None:
                print(f"WARNING: Il campo {node.name} non è univoco ed è già stato trovato in {node.where}. Attualmente la sezione è {where}. I valori sono: {node.value}. Verrà utilizzato il suo field_name completo {node.field_name}")
                id_map[node.field_name] = node
                node.set_flag(Flag.USE_FIELD_NAME)
            else:
                id_map[node.name] = node

        for name, node in id_map.items():
            if name in SECTION_HEAD:
                continue

            prev_ident = step_up_field(node.field_name, where)
            if prev_ident != "":
                parent_node = get_matching_node(prev_ident, graph, where)
                if node.field_name == parent_node.field_name:     # Evita la creazione di cicli
                    print("Ciclo")
                    continue

                if parent_node is None:
                    raise Exception("Impossibile trovare il nodo parent di questo nodo")

                # collego il nuovo nodo a quello padre per creare l'albero
                graph.add_edge(parent_node, node)
                print(f"- {node} è figlio di {parent_node} -")
            elif prev_ident == "":
                print(f"- {node} è figlio di {section_node} - ")
                graph.add_edge(section_node, node)

    def verify_integrity(self) -> bool:
        """Verifica l'integrità del bilancio e la quadratura"""
        def verify_row(_, values, node, __):
            assert len(values) == self.available_columns

        try:
            self.for_each_ce_field(verify_row)
            self.for_each_sp_field(verify_row)

            return True
        except:
            return False

    def get_node_by_name(self, name: str, where: BalanceLocation) -> Node:
        id_map = self.__get_id_map(where)
        return id_map[name]

    def create_column(self, title):
        def value_factory(key, value, node, _):
            if key == "data":
                value.append(title)
            elif len(value) > 0 and type(value[0]) is int:
                value.append(0)
            elif len(value) > 0 and type(value[0]) is float:
                value.append(0.0)
            elif len(value) > 0 and type(value[0]) is str:
                value.append("")
            elif len(value) > 0 and value[0] is None:
                value.append(0)
            else:
                print("WARNING: Impossibile capire il tipo da aggiungere per il campo " + key)
                value.append(0)
        """Crea una nuova colonna nei dati (tipicamente per un nuovo mese della simulazione) e inizializza tutti i campi a 0, assicurando
        che tutti i vettori dei valori dei campi di tutti i documenti contengano lo stesso numero di elementi orizzontali"""

        self.for_each_ce_field(value_factory)
        self.for_each_sp_field(value_factory)
        self.available_columns += 1

    def __leaf_value_factory(self, node: Node, read_column: int = 0, write_column: int = 1):
        """
        Imposta il nuovo valore della foglia (campo atomico) applicando la regola corretta
        :param node: Nodo su cui lavorare
        :return:
        """
        if Flag.UPDATED in node.flags:
            raise Exception(f"Impossibile inizializzare il bilancio. Alcuni campi sono stati modificati {node}")

        if Flag.NO_COPY in node.flags and isinstance(node.value[read_column], (int, float)):
            node.value[write_column] = 0.0
        elif isinstance(node.value[read_column], (int, float)):
            # Di default tutti i None vengono trasformati in 0 per la simulazione
            node.value[write_column] = node.value[read_column] or 0

        node.set_flag(Flag.UPDATED)     # Solo dopo la modifica imposto il campo come updated, così l'algoritmo di calcolo lo utilizzerà per il calcolo delle voci aggregate

    def __init_from_node__(self, node: Node, graph: DiGraph, read_column: int = 0, write_column: int = 1):
        """
        Processo di inizializzazione a partire da un nodo dell'albero. Scorre tutti i figli fino ad arrivare alle foglie,
        imposta le foglie seguendo la regola di COPY/NO-COPY e inizializza tutti gli aggregati o derivati a 0
        :param node: Nodo da cui partire
        :param graph: Grafo su cui lavorare
        :param read_column: Colonna da cui leggere i dati (tipicamente la 0 che contiene il bilancio storico disponibile)
        :param write_column: Colonna su cui scrivere
        :return:
        """
        if node.name in PRIVATE_FIELDS:
            return

        successors: list[Node] = list(graph.successors(node))

        if len(successors) == 0 or Node.all_dc_dicui(successors):
            # il nodo non ha figli oppure i figli sono tutti campi di_cui
            if Node.all_dc_dicui(successors):
                node.set_flag(Flag.IGNORE_CHILDREN)     # Così la prossima volta non devo controllarlo
                # copia tutti i dc
                for c in successors:
                    c.value[write_column] = c.value[read_column] or 0

            self.__leaf_value_factory(node, read_column, write_column)
        else:
            # scorro i figli e li inizializzo (anche se sono dei "di cui", tanto l'algoritmo di calcolo poi non li sommerà ma almeno non perdo l'informazione)
            for child in graph.successors(node):
                    self.__init_from_node__(child, graph, read_column=read_column, write_column=write_column)

            if node.type != NodeType.VIRTUAL:
                node.value[write_column] = 0        # tutti i campi che hanno dei figli vengono inizializzati a 0
                node.set_flag(Flag.NEED_RECALC)     # Vengono marcati anche come need-recalc per indicare che dovranno essere ricalcolati

    def sum_field_value(self, field_name: str, where: BalanceLocation, tot: float, column: int):
        """
        Imposta il valore del campo sommando un importo
        :param field_name:
        :param where:
        :param tot:
        :param column:
        :return:
        """
        self.set_field_value(field_name, where, value=self.get_field_value(field_name, where, column) + tot,
                             month=column)

    def __destinazione_utili__(self):
        # utile e perdita di esercizio (si suppone che sia riportato tutto a nuovo)
        # di default viene sommato (con segno) e portato a nuovo subito, all'inizio dell'anno (ipotesi semplificativa)
        ut = self.get_field_value('_21_utile_frac_perdita_di_esercizio', BalanceLocation.CE, self.YEAR_END_COL)
        self.set_field_value("utile_frac_perdita_di_esercizio", BalanceLocation.SP_PASSIVO_PATRIM, 0, self.YEAR_END_COL)
        self.set_field_value('utile_frac_perdita_a_nuovo',
                             BalanceLocation.SP_PASSIVO_PATRIM,
                             (self.get_field_value('utile_frac_perdita_a_nuovo', BalanceLocation.SP_PASSIVO_PATRIM, month=self.YEAR_START_COL))+ut,
                                month=self.YEAR_END_COL)

    def __ammortamenti_sp__(self):
        # gestione ammortamenti da CE a SP (vengono sommati ai rispettivi fondi)
        amm_immat = self.get_field_value("amm_immob_immat", BalanceLocation.CE, self.YEAR_END_COL)
        amm_mat = self.get_field_value("amm_immob_mat", BalanceLocation.CE, self.YEAR_END_COL)
        self.sum_field_value('fondo_ammto_immob_immateriali', BalanceLocation.SP_ATTIVO, amm_immat, self.YEAR_END_COL)
        self.sum_field_value('fondo_ammto_immob_materiali', BalanceLocation.SP_ATTIVO, amm_mat, self.YEAR_END_COL)

        # per l'anno successivo, controllo se i fondi non hanno superato il valore delle immobilizzazioni. In tal caso le azzero di qui in poi
        fdo_immat = self.get_field_value('fondo_ammto_immob_immateriali', BalanceLocation.SP_ATTIVO, self.YEAR_END_COL)
        fdo_mat = self.get_field_value('fondo_ammto_immob_materiali', BalanceLocation.SP_ATTIVO, self.YEAR_END_COL)
        tot_immat_net = self.sum_children_values("totale_immob_immateriali", BalanceLocation.SP_ATTIVO, self.YEAR_END_COL, exclude_fields=["fondo_ammto_immob_immateriali"])
        tot_mat_net = self.sum_children_values("totale_immob_materiali", BalanceLocation.SP_ATTIVO, self.YEAR_END_COL, exclude_fields=["fondo_ammto_immob_materiali"])

        diff = tot_immat_net - fdo_immat
        if diff == 0 or amm_immat > diff:
            # Il fondo ha raggiunto il valore delle immobilizzazioni da ammortare oppure lo supererà con il prossimo pagamento degli ammortamenti
            self.set_field_value("amm_immob_immat", BalanceLocation.CE, diff, self.YEAR_START_COL)
            print(f"EVENTO: Il valore degli ammortamenti per immob. immateriali è stato impostato a {diff} per completare il fondo. ")
        elif diff < 0:
            raise Exception(f"Il fondo di ammortamento delle immob. immateriali parte da un valore superiore a quello delle immobilizzazioni che deve ammortizzare. {fdo_immat}€")

        diff2 = tot_mat_net - fdo_mat
        if diff2 == 0 or amm_mat > diff2:
            # Il fondo ha raggiunto il valore delle immobilizzazioni da ammortare oppure lo supererà con il prossimo pagamento degli ammortamenti
            self.set_field_value("amm_immob_mat", BalanceLocation.CE, diff2, self.YEAR_START_COL)
            print(
                f"EVENTO: Il valore degli ammortamenti per immob. materiali è stato impostato a {diff} per completare il fondo nell'anno successivo. ")
        elif diff2 < 0:
            raise Exception(f"Il fondo di ammortamento delle immob. materiali parte da un valore superiore a quello delle immobilizzazioni che deve ammortizzare. {fdo_mat}€")

    def __tfr_fondo_sp__(self):
        # destinazione tfr a fondo
        tfr = self.get_field_value("tratt_fine_rapporto", BalanceLocation.CE, self.YEAR_END_COL)
        self.set_field_value("trattamento_di_fine_rapporto",
                             BalanceLocation.SP_PASSIVO_PATRIM,
                             value=tfr+self.get_field_value("trattamento_di_fine_rapporto", BalanceLocation.SP_PASSIVO_PATRIM, self.YEAR_START_COL),
                                month=self.YEAR_END_COL)
        quiesc = self.get_field_value("tratt_di_quiescenza", BalanceLocation.CE, self.YEAR_END_COL)
        self.set_field_value("fondo_di_quiescenza",
                             BalanceLocation.SP_PASSIVO_PATRIM,
                             value=quiesc + self.get_field_value("fondo_di_quiescenza",
                                                              BalanceLocation.SP_PASSIVO_PATRIM, self.YEAR_START_COL),
                             month=self.YEAR_END_COL)

    def __accantonamenti_sp__(self):
        rischi = self.get_field_value("accantonamenti_per_rischi", BalanceLocation.CE, self.YEAR_END_COL)
        self.sum_field_value("altri_fondi", BalanceLocation.SP_PASSIVO_PATRIM, rischi, self.YEAR_END_COL)
        altri = self.get_field_value("altri_accantonamenti", BalanceLocation.CE, self.YEAR_END_COL)
        self.sum_field_value("altri_fondi", BalanceLocation.SP_PASSIVO_PATRIM, altri, self.YEAR_END_COL)

    def calc_terminal_fields(self):
        self.calc_ce_terminal_fields(column=self.YEAR_END_COL)
        self.__ammortamenti_sp__()
        self.__destinazione_utili__()

        # debiti
        # l'anno si inizia con gli stessi debiti della chiusura dell'anno precedente
        # ogni hanno viene eseguito l'effetto di pagamento dei debiti che può essere configurato tramite i parametri globali della simulazione
        self.__tfr_fondo_sp__()
        self.__accantonamenti_sp__()
        # ricalcolo gli aggregati dello stato patrimoniale perchè alcuni li ho modificati a mano per trasportare i risultati dal CE
        self.__calc_from_node(self.sp_patrim_id_map["stato_patrimoniale"], self.stato_patrimoniale)
        self.calc_sp_terminal_fields(column=self.YEAR_END_COL)

    def create_year_start(self):
        """
        Inizializza la colonna di avvio dell'anno seguendo i flag e le regole
        :return:
        """
        if self.available_columns < 2:
            self.create_column("Init")

        def cp(key, values, node, where):
            node.value[1] = node.value[0] or 0       # copia diretta dal bilancio storico (converte i None in 0)
            # rimozione di tutti i flag di calcolo
            node.remove_flag(Flag.UPDATED)
            node.remove_flag(Flag.NEED_RECALC)
            # non vengono impostati flag perchè essendo una copia totale non necessita di ricalcolo

        # inizializzazione del conto economico
        self.__init_from_node__(self.ce_id_map["conto_economico"], self.conto_economico)
        # copia totale dello stato patrimoniale
        self.for_each_sp_field(cp, exclude_context_fields=True)

    def __get_id_map(self, location: BalanceLocation) -> dict[str, Node]:
        if location == BalanceLocation.CE:
            return self.ce_id_map
        elif location == BalanceLocation.SP_ATTIVO:
            return self.sp_attivo_id_map
        elif location == BalanceLocation.SP_PASSIVO_DEBITI:
            return self.sp_debiti_id_map
        elif location == BalanceLocation.SP_PASSIVO_PATRIM:
            return self.sp_patrim_id_map
        elif location == BalanceLocation.SP:    # Utilizzando in modo generico SP si fa una ricerca in tutto lo stato patrimoniale
            return self.sp_patrim_id_map | self.sp_attivo_id_map | self.sp_debiti_id_map

        raise Exception(f"Location {location} non associata ad una id map")

    def __mark_up_predecessors__(self, node, graph: DiGraph):
        """
        Marca in modo ricorsivo tutti i campi padre di questo campo come NEED_RECALC se la loro regola è di aggregare i figli
        :param node: Nodo di partenza
        :param graph: Grafo su cui lavorare
        :return:
        """
        for parent in graph.predecessors(node):
            if Flag.UPDATED in parent.flags:
                print(f"WARNING: Non posso marcare un campo come NEED_RECALC se è UPDATED {parent}")
                continue

            parent.set_flag(Flag.NEED_RECALC)
            self.__mark_up_predecessors__(parent, graph)

    def set_field_value(self, field_name: str, location: BalanceLocation, value: Any, month: int, set_flags: list[Flag] = []):
        """Imposta il valore del campo identificato da
        :param field_name alla colonna month nella sezione giusta del bilancio"""
        id_map = self.__get_id_map(location)
        node = id_map[field_name]
        id_map[field_name].value[month] = value
        if set_flags == []:
            id_map[field_name].set_flag(Flag.UPDATED)
        else:
            for f in set_flags:
                id_map[field_name].set_flag(f)

        # Imposto il need recalc a tutti i parenti fino al nodo di inizio
        if location.is_sp():
            self.__mark_up_predecessors__(node, self.stato_patrimoniale)
        else:
            self.__mark_up_predecessors__(node, self.conto_economico)

    def get_field_value(self, field_name, where: BalanceLocation, month):
        try:
            """Restituisce il valore del campo alla colonna giusta. Il field_name deve essere passato senza la numerazione. """
            id_map = self.__get_id_map(where)
            return id_map[field_name].value[month]
        except Exception:
            raise FieldNotFoundException(field_name, where)

    def get_field_data(self, field_name, where: BalanceLocation):
        """Restituisce il valore del campo oppure None se non esiste"""
        id_map = self.__get_id_map(where)
        return id_map[field_name].value

    def calc_indicies(self):
        """Calcola gli indici di bilancio"""
        # TODO: Implement
        pass

    def calc_ce_terminal_fields(self, column: int):
        """
        Calcola le voci finali del conto economico, come il valore aggiunto, risultato operativo, utile e imposte.
        :return:
        """
        self.set_field_value("risultato_operativo", BalanceLocation.CE,
                             value=self.get_field_value("tot_val_della_produzione", BalanceLocation.CE, column) -
                                   self.get_field_value("costi_della_produzione", BalanceLocation.CE, column),
                                    month=column
                             )

        self.set_field_value("valore_aggiunto", BalanceLocation.CE,
                             value=self.get_field_value("tot_val_della_produzione", BalanceLocation.CE, column) - self.sum_children_values("costi_della_produzione", BalanceLocation.CE, column, exclude_fields=["totale_costi_del_personale", "tot_ammortamenti_e_svalut"]),
                             month=column
                             )
        ebt = (self.get_field_value("risultato_operativo", BalanceLocation.CE, column) +
                            self.get_field_value("totale_proventi_e_oneri_finanziari", BalanceLocation.CE, column) +
                             self.get_field_value("totale_rettifiche_att_finanz", BalanceLocation.CE, column) +
                             self.get_field_value("totale_proventi_frac_oneri_straordinari", BalanceLocation.CE, column))

        self.set_field_value("risultato_prima_delle_imposte", BalanceLocation.CE,
                             value=ebt, month=column)

        tss = 0
        if ebt > 0:
            tss = ebt * self.global_config.tax_perc
        self.set_field_value('_20_totale_imposte_sul_reddito_correnti_differite_e_anticipate', BalanceLocation.CE, tss, column)

        utl = ebt - tss
        self.set_field_value('_21_utile_frac_perdita_di_esercizio', BalanceLocation.CE, utl, column)

    def aggregate_by_year(self):
        """
        Aggrega tutti i marginali delle variazioni (colonne da 2 a 13 incluse) in un unico valore per riga
        e lo scrive sulla colonna 14 (year end)
        I valori marginali non vengono cancellati (se ne occupa il motore di simulazione)
        :return:
        """
        def aggr(key, values: list[Any], node: Node, where: BalanceLocation):
            histor_value = values[self.HISTORIC_COL]
            year_start_value = values[self.YEAR_START_COL]
            vals_to_agg = values[2:14]
            s = sum(vals_to_agg)
            node.value[14] = s + year_start_value

        self.for_each_ce_field(aggr, exclude_context_fields=True)
        self.for_each_sp_field(aggr, exclude_context_fields=True)

    def for_each_ce_field(self, function: Callable[[str, list[Any], Node, BalanceLocation], None | list[Any]],
                          substitute: bool = False,
                          exclude_context_fields: bool = False
                          ):
        for node in self.conto_economico.nodes:
            if node.type == NodeType.VIRTUAL:
                continue

            if exclude_context_fields and node.name in PRIVATE_FIELDS:
                continue

            if not substitute:
                function(node.name if Flag.USE_FIELD_NAME not in node.flags else node.field_name, node.value, node, BalanceLocation.CE)
            else:
                node.value = function(node.name if Flag.USE_FIELD_NAME not in node.flags else node.field_name, node.value, node, BalanceLocation.CE)

    def for_each_sp_field(self,
                          function: Callable[[str, list[Any], Node, BalanceLocation], None | list[Any]],
                          substitute: bool = False,
                          exclude_context_fields: bool = False
                          ):
        """
        Applica una trasformazione a tutti i campi dello stato patrimoniale, opzionalmente sostituendo i valori di tale campo
        :param function: Funzione da applicare. Se viene impostato substitute a True il valore di ritorno deve essere la lista dei nuovi valori del campo.
        :param substitute:
        :return:
        """
        for node in self.stato_patrimoniale.nodes:
            if node.type == NodeType.VIRTUAL:
                continue

            if exclude_context_fields and node.name in PRIVATE_FIELDS:
                continue

            if not substitute:
                function(node.name if Flag.USE_FIELD_NAME not in node.flags else node.field_name, node.value, node, BalanceLocation.SP)
            else:
                node.value = function(node.name if Flag.USE_FIELD_NAME not in node.flags else node.field_name, node.value, node, BalanceLocation.SP)

    @staticmethod
    def copy_last_balance(company_data):
        result = deepcopy(company_data)
        visited = set()

        def transform(value):
            if isinstance(value, list):
                if any(isinstance(item, dict) for item in value):
                    return [transform(item) for item in value]

                return value[0:1]

            if isinstance(value, dict):
                for key, item in value.items():
                    value[key] = transform(item)
                return value

            if isinstance(value, tuple):
                return tuple(transform(item) for item in value)

            if hasattr(value, "__dict__"):
                if id(value) in visited:
                    return value

                visited.add(id(value))

                for name, item in vars(value).items():
                    setattr(value, name, transform(item))

            return value

        return transform(result)

    def copy(self):
        """
        Restituisce una nuova copia identica dello snapshot di bilancio corrente
        Utile per svolgere ulteriori operazioni retro-compatibili
        :return:
        """
        return BalanceSnaphot(
            stato_patrimoniale=self.stato_patrimoniale.copy(),
            conto_economico=self.conto_economico.copy(),
            ce_id_map=self.ce_id_map.copy(),
            sp_attivo_id_map=self.sp_attivo_id_map.copy(),
            sp_debiti_id_map=self.sp_debiti_id_map.copy(),
            sp_patrim_id_map=self.sp_patrim_id_map.copy(),
            indici=self.indici.copy(),
            timestamp=self.timestamp,
            sim_id=self.sim_id,
            available_years=self.available_columns,
            effect_pointer=self.effect_pointer,
            global_config=self.global_config
        )

    def get_children(self, field_name: str, where: BalanceLocation) -> list[Node]:
        """
        Restituisce tutti i campi che sono figli di primo livello del campo field_name
        :param field_name: Nome (senza numerazione) del campo da cui partire
        :param where: Posizione del campo
        :return:
        """
        source: Node = self.__get_id_map(where)[field_name]
        graph: DiGraph = self.conto_economico if where == BalanceLocation.CE else self.stato_patrimoniale
        l = []
        for s, d in list(graph.out_edges(source)):
            l.append(d)

        return l

    def for_each_child(self,
                       field_name: str,
                       where: BalanceLocation,
                       function: Callable[[str, list[Any], Node], list[Any] | None],
                       overwrite: bool = False):
        """
        Esegue una funzione su tutti i figli di un nodo. Questa funzione può opzionalmente calcolare qualcosa e sostituire il vecchio valore del campo.
        :param field_name:
        :param where:
        :param function:
        :param overwrite:
        :return:
        """
        child_fields: list[Node] = self.get_children(field_name, where)
        for node in child_fields:
            res = function(node.name, self.get_field_data(node.name, where), node)
            if overwrite:
                self.set_field_data(
                    field_name, where, res
                )

    def sum_children_values(self, field_name: str, where: BalanceLocation, column: int, exclude_fields: list[str] = []) -> float:
        """
        Calcola la somma di tutti i campi figli di field_name
        Restituisce il vettore con la somma di tutti i campi, con tanti elementi quante sono le colonne presenti
        nello snapshot
        :param field_name:
        :param where:
        :return:
        """
        children = self.get_children(field_name, where)
        res = 0
        for child in children:
            if not exclude_fields:
                res += child.value[column]
            elif child.name not in exclude_fields and child.field_name not in exclude_fields:
                res += child.value[column]

        return res

    def set_field_data(self, field_name: str, where: BalanceLocation, data: list[Any]):
        """
        Imposta tutti i valori del campo direttamente
        :param field_name:
        :param where:
        :param data:
        :return:
        """
        if len(data) != self.available_columns:
            raise Exception("Non è possibile impostare i valori di un campo con un numero di colonne diverse da quelle degli altri campi. Prima creare una nuova colonna con create_column()")

        id_map = self.__get_id_map(where)
        id_map[field_name].value = data
        id_map[field_name].set_flag(Flag.UPDATED)
        node = id_map[field_name]
        # Imposto il need recalc a tutti i parenti fino al nodo di inizio
        if where.is_sp():
            self.__mark_up_predecessors__(node, self.stato_patrimoniale)
        else:
            self.__mark_up_predecessors__(node, self.conto_economico)

    def __calc_from_node(self, node: Node, graph: DiGraph, write: bool = True):
        """
        Calcola il valore di un nodo ricorsivamente
        :param node: Nodo da cui partire
        :param graph: Grafo su cui lavorare
        :return:
        """
        if node.name in PRIVATE_FIELDS:
            return 0

        successors: list[Node] = list(graph.successors(node))

        if len(successors) == 0 or Flag.IGNORE_CHILDREN in node.flags or Node.all_dc_dicui(successors):
            # Il nodo è una foglia oppure è stato marcato per essere trattato come una foglia
            # restituisco il suo valore alla colonna year end
            return node.value[self.YEAR_END_COL]
        else:
            s = 0
            if self.CE_SPEC_CALC_RULES.get(node.name) is not None:
                # Applico la regola speciale
                s = self.CE_SPEC_CALC_RULES.get(node.name)(node, graph)
            elif self.SP_SPEC_CALC_RULES.get(node.name) is not None:
                # Applico la regola speciale
                s = self.SP_SPEC_CALC_RULES.get(node.name)(node, graph)
            elif Flag.NO_SUM_CHILDREN_NO_DC not in node.flags:
                # Regola di default che somma tutti i figli
                for child in successors:
                    if not child.is_dc_specification():     # I campi di cui non li sommo mai
                        s += self.__calc_from_node(child, graph)
            elif Flag.NO_SUM_CHILDREN_NO_DC in node.flags:  # Ignorare i figli e non sommarli
                s = node.value[self.YEAR_END_COL]           # Uso il valore del nodo

            if node.type != NodeType.VIRTUAL and write:
                # Applico il risultato solo se il campo non è virtuale
                node.value[self.YEAR_END_COL] = s

            return s

    def reset_calc_flags(self):
        def rst(key, values, node, where):
            node.remove_flag(Flag.NEED_RECALC)
            node.remove_flag(Flag.UPDATED)

        self.for_each_ce_field(rst, exclude_context_fields=True)
        self.for_each_sp_field(rst, exclude_context_fields=True)

    def recalculate_balance(self):
        """
        Ricalcola tutti gli aggregati del bilancio (prima il CE, poi trasporta i valori patrimoniali e poi SP)
        :return:
        """
        self.__calc_from_node(self.ce_id_map["conto_economico"], self.conto_economico)
        self.calc_terminal_fields()

    def serialize(self) -> tuple[dict, dict]:
        """
        Serializza lo snapshot di bilancio (che è un grafo) in una tupla contenente due dizionari che possono essere salvati su MongoDB.
        Restituisce, nell'ordine, SP - CE
        :return:
        """
        return ({
            "data": self.get_field_data("data", BalanceLocation.CE),
            "moneta": self.get_field_data("moneta", BalanceLocation.CE),
            "periodo": self.get_field_data("periodo", BalanceLocation.CE),
            "subsections":
                    {"attivo": serialize_id_map(self.sp_attivo_id_map, BalanceLocation.SP_ATTIVO),
                  "passivo": {
                      "subsections":
                          {"debiti": serialize_id_map(self.sp_debiti_id_map, BalanceLocation.SP_PASSIVO_DEBITI),
                           "patrimonio_netto": serialize_id_map(self.sp_patrim_id_map, BalanceLocation.SP_PASSIVO_PATRIM)},
                  }
                  }}, {"data": self.get_field_data("data", BalanceLocation.CE),
            "moneta": self.get_field_data("moneta", BalanceLocation.CE),
            "periodo": self.get_field_data("periodo", BalanceLocation.CE),} | serialize_id_map(self.ce_id_map, BalanceLocation.CE))

    def copy_column(self, source_column: int, dest_column: int):
        """
        Copia il contenuto di una colonna dentro un'altra, sovrascrivendola
        :param source_column:
        :param dest_column:
        :return:
        """
        assert dest_column < self.available_columns
        assert source_column < self.available_columns

        def cp(key, values, node: Node, where: BalanceLocation):
            v = values[source_column]
            node.value[dest_column] = v

        self.for_each_ce_field(cp, exclude_context_fields=True)
        self.for_each_sp_field(cp, exclude_context_fields=True)

    def copy_column_from_snapshot(self, snapshot, source_column: int, dest_column: int, column_title: str | None = None):
        """
        Copia il contenuto di una colonna da un altro snapshot
        :param snapshot: Snap da cui prendere i dati
        :param source_column: Colonna da cui leggere i dati
        :param dest_column: Colonna dello snapshot corrente su cui scrivere i dati
        (non vengono effettuati calcoli)
        :param column_title Titolo opzionale per la colonna
        :return:
        """
        assert dest_column < self.available_columns
        assert snapshot.available_columns > source_column

        def cp(key, values, node: Node, where: BalanceLocation):
            try:
                v = snapshot.get_field_value(key, where, month=source_column)

                if Flag.USE_FIELD_NAME in node.flags:
                    corr_node = self.get_node_by_name(key, where)
                    if corr_node.field_name != key:
                        raise Exception(f"Errore durante la copia. Non è stato possibile trovare la corrispondenza tra il campo {key} e un nodo del grafo. {node}")

                node.value[dest_column] = v
            except FieldNotFoundException:
                print(f"WARNING: Il campo {key} non è stato trovato nello snapshot da cui copiare. Verrà utilizzato il valore di default 0")
                node.value[dest_column] = 0

        self.for_each_ce_field(cp)
        self.for_each_sp_field(cp)

        if column_title is not None:
            self.set_column_title(dest_column, column_title)

    def set_column_title(self, index: int, title: str):
        self.ce_id_map["data"].value[index] = title

    def copy_sp_fields_from_snapshot(self, snapshot, source_column: int, dest_column: int):
        """
        Copia tutti i campi dello stato patrimoniale nello stato patrimoniale dello snapshot corrente
        alla colonna dest_col. Legge i dati dalla colonna source_col
        :param snapshot:
        :param source_col:
        :param dest_col:
        :return:
        """
        assert dest_column < self.available_columns
        assert snapshot.available_columns > source_column

        def cp(key, values, node: Node, where: BalanceLocation):
            try:
                v = snapshot.get_field_value(key, where, month=source_column)
                node.value[dest_column] = v
            except FieldNotFoundException:
                print(
                    f"WARNING: Il campo {key} non è stato trovato nello snapshot da cui copiare. Verrà utilizzato il valore di default 0")
                node.value[dest_column] = 0

        self.for_each_sp_field(cp)

    @staticmethod
    def from_company_data(data: CompanyData,
                          timestamp: int,
                          sim_id: int,
                          global_config: GlobalParameters,
                        effect_pointer: str | None,
                          single_year: bool = True
                          ):
        """
        Crea uno snapshot dei dati a partire dal company data complessivo. Crea in automatico il grafo
        :param data: Dati completi della company
        :param timestamp: Mese corrente della simulazione
        :param effect_pointer Nome dell'effetto che ha richiesto la modifica
        :param sim_id: Id della simulazione
        :param single_year: Permette di specificare opzionalmente un anno singolo da mantenere, altrimenti verranno mantenuti tutti
        :return: Una nuova istanza di BalanceSnapshot
        """
        if not single_year:
            sp_dict = data.stato_patrimoniale.copy()
            ce_dict = data.conto_economico.copy()
            l = data.available_years
        else:
            sp_dict = BalanceSnaphot.copy_last_balance(data.stato_patrimoniale)
            ce_dict = BalanceSnaphot.copy_last_balance(data.conto_economico)
            l = 1

        sp_graph, att, dbt, ptrm = BalanceSnaphot.create_sp_graph(sp_dict)
        ce_graph, ce_id_map = BalanceSnaphot.create_ce_graph(ce_dict)
        return BalanceSnaphot(
            stato_patrimoniale=sp_graph,
            conto_economico=ce_graph,
            sp_attivo_id_map=att,
            sp_debiti_id_map=dbt,
            sp_patrim_id_map=ptrm,
            ce_id_map=ce_id_map,
            timestamp=timestamp,
            sim_id=sim_id,
            effect_pointer=effect_pointer,
            available_years=l,
            indici=data.indici.copy(),
            global_config=global_config
        )

    def calc_sp_terminal_fields(self, column):
        """
        Calcola gli ultimi campi dello stato patrimoniale, tra cui il valore dei depositi bancari per differenza.
        :param column:
        :return:
        """
        tot_patrim_netto = self.sum_children_values(
            "patrimonio_netto",
            BalanceLocation.SP_PASSIVO_PATRIM,
            column=column,
        )

        tot_debiti = self.sum_children_values(
            "debiti",
            BalanceLocation.SP_PASSIVO_DEBITI,
            column=column,
            exclude_fields=[
                "totale_passivo",
                "totale_conti_dordine",
                "garanzie_prestate",
            ],
        )

        tot_passivo = tot_patrim_netto + tot_debiti
        self.set_field_value(
            "totale_passivo",
            BalanceLocation.SP_PASSIVO_DEBITI,
            tot_passivo,
            column,
        )
        self.set_field_value(
            "depositi_bancari",
            BalanceLocation.SP_ATTIVO,
            0,
            column,
        )
        self.__calc_from_node(
            self.sp_attivo_id_map["attivo"],
            self.stato_patrimoniale,
        )
        tot_att_senza_depositi = self.sum_children_values(
            "attivo",
            BalanceLocation.SP_ATTIVO,
            column=column,
            exclude_fields=["totale_attivo"],
        )
        liq = tot_passivo - tot_att_senza_depositi
        self.set_field_value(
            "depositi_bancari",
            BalanceLocation.SP_ATTIVO,
            liq,
            column,
        )
        self.__calc_from_node(
            self.sp_attivo_id_map["attivo"],
            self.stato_patrimoniale,
        )
        tot_attivo = self.sum_children_values(
            "attivo",
            BalanceLocation.SP_ATTIVO,
            column=column,
            exclude_fields=["totale_attivo"],
        )
        self.set_field_value(
            "totale_attivo",
            BalanceLocation.SP_ATTIVO,
            tot_attivo,
            column,
        )

    def get_total_liquidity(self, column: int):
        return self.get_field_value("tot_dispon_liquide", BalanceLocation.SP_ATTIVO, column)


    def reset_columns(self, col_start: int, col_end: int, default_value = 0):
        """
        Resetta un blocco di colonne
        :param col_start:
        :param col_end:
        :param default_value:
        :return:
        """
        def rst(key, values, node, where):
            if col_start == col_end:
                node.value[col_start] = default_value

            else:
                for i in range(col_start, col_end):
                    node.value[i] = default_value

        self.for_each_ce_field(rst, exclude_context_fields=True)
        self.for_each_sp_field(rst, exclude_context_fields=True)
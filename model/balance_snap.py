from copy import deepcopy
from enum import IntEnum
from typing import Callable, Any
import networkx as nx
import re
from networkx.classes import Graph, DiGraph
from dao.util import step_up_field, extract_field_identif, SECTION_HEAD, BalanceLocation
from model.node import Node, NodeType, Flag
from model.raw_company_data import CompanyData

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
                 effect_pointer: str | None
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
        # In automatico, i campi da ricalcolare vengono ricavati a partire dai campi che sono stati modificati, secondo la seguente logica:
        # modificato un campo che appartiene alla lettera A (ad esempio A.1) viene ricalcolato il totale alla lettera A
        # e' però necessario specificare anche dei campi che non appartengono a questa logica ma che devono lo stesso essere ricalcolati, come l'utile nel CE o i totali attivo e passivo in SP
        # inoltre alcuni campi per coerenza sono impostati come "no-copy", ossia nonostante nel bilancio storico sia presente un valore iniziale verrà sempre utilizzato 0. Questo è utile per campi
        # che specificano operazioni straordinarie che la simulazione non ripete
        self.__ce_need_recalc_fields = [
            "risultato_prima_delle_imposte"
        ]
        self.__sp_no_copy = [
            # Risultato dell'esercizio da chiudere e destinare
            "aix_utile_frac_perdita_di_esercizio",
            # Operazioni di distribuzione/copertura
            "acconto_dividendi",
            "copertura_parziale_perdita_di_esercizio",
        ]
        self.__ce_no_copy = [
            # Rettifiche di valore delle immobilizzazioni
            "b10c_altre_svalut_immob",

            # Rivalutazioni finanziarie
            "d18a_rivalut_di_partec",
            "d18b_rivalut_di_altre_imm_fin",
            "d18c_rivalut_di_titoli",
            "d18d_rivalut_di_strumenti_finanziari_derivati",
            "rivalut_di_attivita_finanziarie_per_la_gestione_accentrata_della_tesoreria",

            # Svalutazioni finanziarie
            "d19a_svalut_di_partec",
            "d19b_svalut_di_altre_imm_fin",
            "d19c_svalut_di_titoli",
            "d19d_svalut_di_strumenti_finanziari_derivati",
            "svalut_di_attivita_finanziarie_per_la_gestione_accentrata_della_tesoreria",

            # Proventi e oneri straordinari
            "proventi_straordinari",
            "di_cui_plusvalenze",
            "oneri_straordinari",
            "di_cui_minusvalenze",
            "di_cui_imposte_esercizio_precedente",
            "imposte_relative_a_esercizi_precedenti",
        ]

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

        BalanceSnaphot.__create_section_graph(att, stato_patrimoniale["subsections"]["attivo"], graph, att_id_map, BalanceLocation.SP_ATTIVO)
        BalanceSnaphot.__create_section_graph(dbt, stato_patrimoniale["subsections"]["passivo"]["subsections"]["debiti"], graph, pss_dbt_id_map, BalanceLocation.SP_PASSIVO_DEBITI)
        BalanceSnaphot.__create_section_graph(ptrm, stato_patrimoniale["subsections"]["passivo"]["subsections"]["patrimonio_netto"], graph, pss_ptrm_id_map, BalanceLocation.SP_PASSIVO_PATRIM)

        return (graph, att_id_map, pss_dbt_id_map, pss_ptrm_id_map)

    @staticmethod
    def create_ce_graph(conto_economico: dict[str, Any]) -> tuple[DiGraph, dict]:
        graph = DiGraph()
        ce = Node.virtual("conto_economico", BalanceLocation.CE)
        graph.add_node(ce)
        id_map = {"conto_economico": ce}
        BalanceSnaphot.__create_section_graph(ce, conto_economico, graph, id_map, BalanceLocation.CE)
        return (graph, id_map)

    @staticmethod
    def __create_section_graph(section_node: Node,
                               section: dict[str, Any],
                               graph: DiGraph,
                               id_map: dict[str, Any],
                               where: BalanceLocation
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
            graph.add_node(node)
            if id_map.get(node.name) is not None:
                print(f"WARNING: Il campo {node} non è univoco. Verrà utilizzato il suo field_name completo {field_name}")
                id_map[node.field_name] = node
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
        def verify_row(_, values, node):
            assert len(values) == self.available_columns

        try:
            self.for_each_ce_field(verify_row)
            self.for_each_sp_field(verify_row)

            return True
        except:
            return False

    @property
    def sp_totale_attivo(self):
        # TODO
        #return self.stato_patrimoniale["subsections"]["attivo"]["totale_attivo"]
        return 0

    @property
    def sp_totale_passivo(self):
        # TODO
        #return self.stato_patrimoniale["subsections"]["passivo"]["subsections"]["debiti"]["totale_passivo"]
        return 0

    def create_column(self, title):
        """Crea una nuova colonna nei dati (tipicamente per un nuovo mese della simulazione) e inizializza tutti i campi a 0, assicurando
        che tutti i vettori dei valori dei campi di tutti i documenti contengano lo stesso numero di elementi orizzontali"""
        def value_factory(key, value, node):
            if key == "data":
                value.append(title)
            elif len(value) > 0 and type(value[0]) is int:
                value.append(0)
            elif len(value) > 0 and type(value[0]) is float:
                value.append(0.0)
            elif len(value) > 0 and type(value[0]) is str:
                value.append("")
            elif len(value) > 0 and value[0] is None:
                value.append(None)
            else:
                print("WARNING: Impossibile capire il tipo da aggiungere per il campo " + key)
                value.append(None)

        self.for_each_ce_field(value_factory)
        self.for_each_sp_field(value_factory)
        self.available_columns += 1

    def first_non_null_val(self, s_index: int, field_name: str, location: BalanceLocation):
        f_data = self.get_field_data(field_name, location)
        for i in range(s_index, -1, -1):
            if f_data[i] is not None and f_data[i] > 0:
                return f_data[i]

        return None

    def __get_id_map(self, location: BalanceLocation) -> dict[str, Node]:
        if location == BalanceLocation.CE:
            return self.ce_id_map
        elif location == BalanceLocation.SP_ATTIVO:
            return self.sp_attivo_id_map
        elif location == BalanceLocation.SP_PASSIVO_DEBITI:
            return self.sp_debiti_id_map
        elif location == BalanceLocation.SP_PASSIVO_PATRIM:
            return self.sp_patrim_id_map

        raise Exception(f"Location {location} non associata ad una id map")

    def set_field_value(self, field_name: str, location: BalanceLocation, value: Any, month: int):
        """Imposta il valore del campo identificato da
        :param field_name alla colonna month nella sezione giusta del bilancio"""
        id_map = self.__get_id_map(location)

        id_map[field_name].value[month] = value
        id_map[field_name].set_flag(Flag.UPDATED)

    def get_field_value(self, field_name, where: BalanceLocation, month):
        """Restituisce il valore del campo alla colonna giusta. Il field_name deve essere passato senza la numerazione. """
        id_map = self.__get_id_map(where)
        return id_map[field_name].value[month]

    def get_field_data(self, field_name, where: BalanceLocation):
        """Restituisce il valore del campo oppure None se non esiste"""
        id_map = self.__get_id_map(where)
        return id_map[field_name].value

    def calc_indicies(self):
        """Calcola gli indici di bilancio"""
        # TODO: Implement
        pass

    def calc_terminal_fields(self):
        """
        Calcola le voci finali del documento come la cassa e i totali.
        Partendo dai field_name dei campi che sono stati modificati, risale al parent di ognuno di loro e lo ricalcola.
        Metodo 1:
        * Prendere tutti i campi figli del punto, sommarli, impostarli al primo parent, prendere tutti i parent dello stesso livello e risommarli.

        :return:
        """
        # TODO: Implement
        pass

    def aggregate_by_year(self, number_of_years: int):
        """
        Restituisce un nuovo snapshot di bilancio in cui i dati non sono aggregati per mesi ma per anni
        Orizzontalmente, le colonne sono aggregate in ogni anno. Tutti i valori non modificati in un certo mese
        vengono lasciati a 0 per far sì che ricompaia il valore storico nella voce, senza perdita di dati o duplicazione.
        Tutti gli effetti indicano nella colonna corrispondente solo il nuovo valore, se presente.
        :return:
        """

        def aggr(key, values: list[Any], node: Node):
            histor_value = values[0]
            groups = [values[i:i + 12] for i in range(1, len(values), 12)]

            s = None
            new_cols = []

            for g in groups:
                if key in self.__sp_no_copy or key in self.__ce_no_copy or key in self.__ce_need_recalc_fields:
                    s = 0       # Tutti i campi che non possono essere copiati o che necessitano esplicitamente di essere ricalcolati vengono inizializzati a 0 e poi gestiti successivamente

                for item in g:
                    if type(item) is int or type(item) is float:
                        if s is None:
                            s = item + histor_value
                        elif type(s) is int or type(s) is float:
                            s += item
                    elif item is None and s is None:
                        break       # Al primo elemento None viene aggiunta la colonna dell'anno come None e si passa al prossimo gruppo
                    elif type(item) is not int and type(item) is not float:
                        if item == "" or item is None:
                            s = histor_value
                        else:
                            s = item
                        break
                new_cols.append(s)
                s = None

            return [values[0]] + new_cols

        return self.advanced_copy(
            aggr, aggr, number_of_years + 1
        )

    def for_each_ce_field(self, function: Callable[[str, list[Any], Node], None | list[Any]],
                          substitute: bool = False):
        for node in self.conto_economico.nodes:
            if node.type == NodeType.VIRTUAL:
                continue

            if not substitute:
                function(node.name, node.value, node)
            else:
                node.value = function(node.name, node.value, node)

    def for_each_sp_field(self,
                          function: Callable[[str, list[Any], Node], None | list[Any]],
                          substitute: bool = False
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

            if not substitute:
                function(node.name, node.value, node)
            else:
                node.value = function(node.name, node.value, node)

    def for_each_debiti_field(self,
                          function: Callable[[str, list[Any]], None | list[Any]],
                          substitute: bool = False
                          ):
        """
        Applica una trasformazione a tutti i campi dei debiti dello stato patrimoniale, opzionalmente sostituendo i valori di tale campo.
        Può essere utilizzata anche per effettuare ricerche di campi
        :param function: Funzione da applicare. Se viene impostato substitute a True il valore di ritorno deve essere la lista dei nuovi valori del campo.
        :param substitute:
        :return:
        """
        def visit(section: dict[str, Any]) -> None:
            for key, value in section.items():
                if not substitute:
                    function(key, value)
                else:
                    section[key] = function(key, value)

        visit(self.stato_patrimoniale["subsections"]["passivo"]["subsections"]["debiti"])

    def for_each_patrim_field(self,
                          function: Callable[[str, list[Any]], None | list[Any]],
                          substitute: bool = False
                          ):
        """
        Applica una trasformazione a tutti i campi del patrimonio netto dello stato patrimoniale, opzionalmente sostituendo i valori di tale campo.
        Può essere utilizzata anche per effettuare ricerche di campi
        :param function: Funzione da applicare. Se viene impostato substitute a True il valore di ritorno deve essere la lista dei nuovi valori del campo.
        :param substitute:
        :return:
        """
        def visit(section: dict[str, Any]) -> None:
            for key, value in section.items():
                if not substitute:
                    function(key, value)
                else:
                    section[key] = function(key, value)

        visit(self.stato_patrimoniale["subsections"]["passivo"]["subsections"]["patrimonio_netto"])

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
            effect_pointer=self.effect_pointer
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

    def sum_children_values(self, field_name: str, where: BalanceLocation) -> list[float]:
        """
        Calcola la somma di tutti i campi figli di field_name
        Restituisce il vettore con la somma di tutti i campi, con tanti elementi quante sono le colonne presenti
        nello snapshot
        :param field_name:
        :param where:
        :return:
        """
        children = self.get_children(field_name, where)
        results = []
        for column_index in range(0, self.available_columns):
            s_c = 0
            for child_key in children:
                val = self.get_field_value(where=where, field_name=child_key, month=column_index)
                s_c += val
            results.append(s_c)

        return results

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

    def advanced_copy(self,
                      stato_patrimon_transformer: Callable[[str, list[Any], Node], list[Any]],
                      conto_economico_transformer: Callable[[str, list[Any], Node], list[Any]],
                      new_column_count: int
                      ):
        """
        Crea una copia dello snapshot di bilancio applicando prima una trasformazione su tutte le righe dei bilanci.
        Questa trasformazione può cambiare il numero di colonne, portandolo ad un valore a piacere che deve però coincidere
        per tutti i campi.
        :param stato_patrimon_transformer: Funzione che trasforma ogni campo dello stato patrimoniale
        :param conto_economico_transformer: Funzione che trasforma ogni campo del conto economico

        Entrambe le funzioni devono restituire la nuova lista di valori del campo e non modificar
        :return:
        """
        tot_cp = self.copy()
        tot_cp.for_each_sp_field(stato_patrimon_transformer, substitute=True)
        tot_cp.for_each_ce_field(conto_economico_transformer, substitute=True)
        tot_cp.calc_indicies()
        tot_cp.available_columns = new_column_count
        tot_cp.calc_terminal_fields()
        if not tot_cp.verify_integrity():
            raise Exception("Trasformazione non consistente sullo snapshot di bilancio. La trasformazione che hai specificato non porta ad avere un bilancio valido. ")

        tot_cp.timestamp = self.timestamp
        return tot_cp

    def serialize(self) -> tuple[dict, dict]:
        """
        Serializza lo snapshot di bilancio (che è un grafo) in una tupla contenente due dizionari che possono essere salvati su MongoDB.
        Restituisce, nell'ordine,
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

    @staticmethod
    def from_company_data(data: CompanyData,
                          timestamp: int,
                          sim_id: int,
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
            indici=data.indici.copy()
        )
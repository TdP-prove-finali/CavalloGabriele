from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any, Literal

import pytest

from controller.simulation_controller import SimulationWorker
from dao.simulation.simulation_dao import SimulationDAO
from dao.util import step_up_numbering, step_up_field, extract_complete_numbering, BalanceLocation
from model.balance_snap import BalanceSnaphot
from model.investment_item import InvestmentProject, EmployeeHireInvestment
from model.node import NodeType, Flag
from model.sim_output import SimulationOutput
from model.sim_state import SimulationCompleteModel, SimulationState
from test_data import complete_company_1, GLOBAL_CONFIG_MUL, GLOBAL_CONFIG_SINGLE

COLUMN = 1
TOLERANCE = Decimal("0.01")
Section = Literal["ce", "sp"]

def test_balance():
    b = complete_company_1
    snapshot = BalanceSnaphot.from_company_data(b, 0, 1, effect_pointer="", global_config=GLOBAL_CONFIG_SINGLE)
    assert snapshot.verify_integrity() == True
    snapshot.create_column("test")

    assert snapshot.verify_integrity() == True
    snapshot.set_field_value("crediti_verso_soci", BalanceLocation.SP_ATTIVO, 200, 0)
    snapshot.set_field_value("totale_patrimonio_netto", BalanceLocation.SP_PASSIVO_PATRIM, 300, 0)
    snapshot.set_field_value("soci_per_finanziamenti_entro", BalanceLocation.SP_PASSIVO_DEBITI, 30000000, 0)
    snapshot.set_field_value("diritti_brevetto_ind", BalanceLocation.SP_ATTIVO, 500, 0)
    assert Flag.NEED_RECALC in snapshot.get_node_by_name("totale_immob_immateriali", BalanceLocation.SP_ATTIVO).flags
    assert Flag.NEED_RECALC in snapshot.get_node_by_name("totale_immobilizzazioni_sepind_di_quelle_conc_in_loc_finanz", BalanceLocation.SP_ATTIVO).flags
    assert snapshot.get_field_value("crediti_verso_soci", BalanceLocation.SP_ATTIVO, month=0) == 200
    assert snapshot.get_field_value("totale_patrimonio_netto", BalanceLocation.SP_PASSIVO_PATRIM, month=0) == 300
    assert snapshot.get_field_value("soci_per_finanziamenti_entro", BalanceLocation.SP_PASSIVO_DEBITI, month=0) == 30000000
    assert snapshot.get_node_by_name("totale_attivo", BalanceLocation.SP) is not None
    # verifico manualmente che il nodo corrispondente nel grafo sia stato aggiornato
    for node in list(snapshot.stato_patrimoniale.nodes):
        if node.name == "soci_per_finanziamenti_entro":
            assert node.value[0] == 30000000
        elif node.name == "totale_patrimonio_netto":
            assert node.value[0] == 300

    # verifico che accedendo alla id-map manualmente e modificando un'informazione sul nodo come il valore si aggiorni il grafo
    snapshot.sp_debiti_id_map["soci_per_finanziamenti_entro"].value[0] = 42
    for node in list(snapshot.stato_patrimoniale.nodes):
        if node.name == "soci_per_finanziamenti_entro":
            assert node.value[0] == 42
        elif node.name == "totale_patrimonio_netto":
            assert node.value[0] == 300

    node1 = snapshot.sp_debiti_id_map["soci_per_finanziamenti_entro"]
    node2 = None
    for node in list(snapshot.stato_patrimoniale.nodes):
        if node.name == "soci_per_finanziamenti_entro":
            node2 = node

    # verifico che prendendo il nodo dalla id-map si ottenga un puntatore al nodo del grafo
    assert node2 is not None
    assert node1.field_name == node2.field_name
    assert node1.value == node2.value

    snapshot.set_field_data("soci_per_finanziamenti_entro", BalanceLocation.SP_PASSIVO_DEBITI, [42, 42])
    assert node2.value == [42, 42]

    # verifico che i flag vengano correttamente impostati
    def search_node_flag(name, flag):
        for node in list(snapshot.conto_economico.nodes()):
            if node.name == name or node.field_name == name:
                assert flag in node.flags
                return True
        return False

    for name, flag in BalanceSnaphot.CE_FIELD_FLAGS.items():
        assert search_node_flag(name, flag)

def test_sim():
    b = complete_company_1
    ctrl = SimulationOutput(
            global_parameters=GLOBAL_CONFIG_SINGLE,
            balance=BalanceSnaphot.from_company_data(b, 0, 1, effect_pointer="", global_config=GLOBAL_CONFIG_SINGLE),
            project=InvestmentProject(
                "test",
                "test",
                []
            )
        )

    SimulationDAO.save_simulation(ctrl)
    assert True

def test_stepup():
    assert step_up_numbering("d12_debiti_tributari_entro") == "d"
    assert step_up_numbering("d1_obbligni_entro") == "d"
    assert step_up_numbering("d11bis_debiti_vs_imprese_sottoposte_al_controllo_delle_controllanti_oltre") == "d11"
    assert step_up_numbering("d_o1_total_debiti_entro_lesercizio") == ""
    assert step_up_numbering("a2_plus_a3_totale_variazioni") == "a"
    assert step_up_numbering("b10a_amm_immob_immat") == "b10"
    assert step_up_numbering("c15_dc_di_cui_da_imprese_controllanti") == "c"
    assert step_up_numbering("c17bis_utili_e_perdite_su_cambi") == "c17"
    assert step_up_numbering("cii3_cred_vs_collegate_oltre") == "cii"
    assert step_up_numbering("ci_totale_rimanenze") == "c"
    assert step_up_numbering("c_attivo_circolante") == ""
    assert step_up_numbering("cii5bis_cred_tributari_entro") == "cii"
    assert step_up_numbering("cii5quater_cred_verso_altri_entro") == "cii"
    assert step_up_numbering("civ1_depositi_bancari") == "civ"
    assert step_up_numbering("aiv_riserva_legale") == "a"
    assert step_up_field("biii2dbis_o1_cred_vs_altri_oltre", BalanceLocation.SP_ATTIVO) == "biii2"

    assert step_up_field("d11bis_debiti_vs_imprese_sottoposte_al_controllo_delle_controllanti_entro", BalanceLocation.SP_PASSIVO_DEBITI) == "d"
    assert step_up_field("ci5_acconti", BalanceLocation.SP_ATTIVO) == "ci"
    assert step_up_field("ci5_o1_immobilizzazioni_materiali_destinate_alla_vendita", BalanceLocation.SP_ATTIVO) == "ci"
    assert step_up_field("_o1_totale_passivo") == ""
    assert step_up_field("d_o1_total_debiti_entro_lesercizio") == "d"
    assert step_up_field("d9_o1_imprese_controllate_oltre") == "d"
    assert step_up_field("e_o1_aggio_sui_prestiti") == "e"
    assert step_up_field("ai_dc_di_cui_versamenti_in_c_frac_futuro_aumento_di_capitale") == "ai"
    assert step_up_field("aix_o1_acconto_dividendi") == "a"
    assert step_up_field("aix_utile_frac_perdita_di_esercizio") == "a"
    assert step_up_field("av_o1_riserva_azioni_proprie") == "a"
    assert step_up_field("ax_riserva_negativa_per_azioni_proprie_in_portafoglio__plus_frac___") == "a"
    assert step_up_field("b1_fondo_di_quiescenza") == "b"
    assert step_up_field("c_trattamento_di_fine_rapporto") == ""
    assert step_up_field("_o1_totale_attivo") == ""
    assert step_up_field("bii_dc_di_cui_beni_materiali_concessi_in_locazione_finanziaria") == "bii"
    assert step_up_field("ax_o2_dc_di_cui_per_imposte_differite") == "ax_o2_"
    assert step_up_field("b10c_o1_b10aplusbplusc_amm_e_svalut_delle_immob", BalanceLocation.CE) == "b10"


    assert extract_complete_numbering("cii_o1_crediti_per_imposte_anticipate") == "cii_o1"


def test_debiti():
    b = complete_company_1
    snapshot = BalanceSnaphot.from_company_data(b, 0, 1, effect_pointer="", global_config=GLOBAL_CONFIG_SINGLE)
    children = snapshot.get_children("totale_debiti", BalanceLocation.SP_PASSIVO_DEBITI)
    assert list(map(lambda it: it.field_name, children)) == ['d10_imprese_collegate_entro',
 'd10_o1_imprese_collegate_oltre',
 'd11_controllanti_entro',
 'd11_o1_controllanti_oltre',
 'd11bis_debiti_vs_imprese_sottoposte_al_controllo_delle_controllanti_entro',
 'd11bis_o1_debiti_vs_imprese_sottoposte_al_controllo_delle_controllanti_oltre',
 'd12_debiti_tributari_entro',
 'd12_o1_debiti_tributari_oltre',
 'd13_istituti_previdenza_entro',
 'd13_o1_istituti_previdenza_oltre',
 'd14_altri_debiti_entro',
 'd14_o1_altri_debiti_oltre',
 'd1_o1_obbligni_oltre',
 'd1_obbligni_entro',
 'd2_o1_obbligni_convert_oltre',
 'd2_obbligni_convert_entro',
 'd3_o1_soci_per_finanziamenti_oltre',
 'd3_soci_per_finanziamenti_entro',
 'd4_banche_entro_lesercizio',
 'd4_o1_banche_oltre_lesercizio',
 'd5_altri_finanziatori_entro',
 'd5_o1_altri_finanziatori_oltre',
 'd6_acconti_entro',
 'd6_o1_acconti_oltre',
 'd7_fornitori_entro',
 'd7_o1_fornitori_oltre',
 'd8_o1_titoli_di_credito_oltre',
 'd8_titoli_di_credito_entro',
 'd9_imprese_controllate_entro',
 'd9_o1_imprese_controllate_oltre']

    r = sum(map(lambda it: it.value[0], children))
    assert snapshot.get_field_value("totale_debiti", BalanceLocation.SP_PASSIVO_DEBITI, 0) == r

    # Verifico che siano tutte foglie
    for child in children:
        assert len(snapshot.get_children(child.name, BalanceLocation.SP_PASSIVO_DEBITI)) == 0


def test_patrimonio_netto():
    b = complete_company_1
    snapshot = BalanceSnaphot.from_company_data(b, 0, 1, effect_pointer="", global_config=GLOBAL_CONFIG_SINGLE)
    children = snapshot.get_children("patrimonio_netto", BalanceLocation.SP_PASSIVO_PATRIM)

    assert list(map(lambda it: it.field_name, children)) == [
        "a_totale_patrimonio_netto",
        "b_totale_fondi_rischi",
        "c_trattamento_di_fine_rapporto"
    ]

    for child in children:
        c2 = snapshot.get_children(child.name, BalanceLocation.SP_PASSIVO_PATRIM)
        if len(c2) > 0:
            s = sum(map(lambda it: it.value[0] or 0, c2))
            assert s == child.value[0]

            for c in c2:
                if c.field_name == "ai_capitale_sociale":
                    # questi campi di cui non sono addittivi ma rappresentano un dettaglio, quindi è corretto che la loro somma non coincida con il valore del padre.
                    assert len(snapshot.get_children(c.name, BalanceLocation.SP_PASSIVO_PATRIM)) == 4
                else:
                    assert True
        else:
            assert True

def test_stato_patrimoniale_passivo():
    b = complete_company_1
    snapshot = BalanceSnaphot.from_company_data(b, 0, 1, effect_pointer="", global_config=GLOBAL_CONFIG_SINGLE)
    children_dbt = snapshot.get_children("debiti", BalanceLocation.SP_PASSIVO_DEBITI)
    children_ptrm = snapshot.get_children("patrimonio_netto", BalanceLocation.SP_PASSIVO_PATRIM)

    assert list(map(lambda it: it.field_name, children_dbt)) == [
        "_o2_totale_passivo",
        "_o3_totale_conti_dordine",
        "_o4_garanzie_prestate",
        "d_totale_debiti",
        "e_ratei_e_risconti"
    ]
    assert list(map(lambda it: it.field_name, children_ptrm)) == [
        'a_totale_patrimonio_netto',
        'b_totale_fondi_rischi',
        'c_trattamento_di_fine_rapporto'
    ]
    r = 0
    for c1 in children_dbt:
        if c1.name not in ["totale_passivo", "totale_conti_dordine", "garanzie_prestate"]:
            r += c1.value[0]

    for c2 in children_ptrm:
        r += c2.value[0]

    assert snapshot.get_field_value("totale_passivo", BalanceLocation.SP_PASSIVO_DEBITI, 0) == r

def test_attivo():
    b = complete_company_1
    snapshot = BalanceSnaphot.from_company_data(b, 0, 1, effect_pointer="", global_config=GLOBAL_CONFIG_SINGLE)
    children = snapshot.get_children("attivo", BalanceLocation.SP_ATTIVO)

    assert list(map(lambda it: it.field_name, children)) == ['_o1_totale_attivo',
         'a_crediti_verso_soci',
         'b_totale_immobilizzazioni_sepind_di_quelle_conc_in_loc_finanz',
         'c_attivo_circolante',
         'd_ratei_e_risconti']
    r = 0
    for c1 in children:
        if c1.name != "totale_attivo":
            r += c1.value[0]

    assert snapshot.get_field_value("totale_attivo", BalanceLocation.SP_ATTIVO, 0) == r

    c2 = snapshot.get_children("attivo_circolante", BalanceLocation.SP_ATTIVO)

    assert list(map(lambda it: it.field_name, c2)) == ['ci_totale_rimanenze',
 'cii_totale_crediti',
 'ciii_totale_attivita_finanziarie',
 'civ_tot_dispon_liquide']
    r = 0
    for c1 in c2:
        r += c1.value[0]

    assert snapshot.get_field_value("attivo_circolante", BalanceLocation.SP_ATTIVO, 0) == r

    c3 = snapshot.get_children("totale_attivita_finanziarie", BalanceLocation.SP_ATTIVO)

    assert list(map(lambda it: it.field_name, c3)) == ['ciii1_partecni_in_controllate',
 'ciii2_partecni_in_collegate',
 'ciii3_partecni_in_controllanti',
 'ciii3bis_partecni_in_imprese_sottoposte_al_controllo_delle_controllanti',
 'ciii4_altre_partecni',
 'ciii4bis_azioni_proprie',
 'ciii5_strumenti_finanziari_derivati_attivi',
 'ciii6_altri_titoli',
 'ciii7_attivita_finanziarie_per_la_gestione_accentrata_della_tesoreria']
    r = 0
    for c1 in c3:
        r += c1.value[0]

    assert snapshot.get_field_value("totale_attivita_finanziarie", BalanceLocation.SP_ATTIVO, 0) == r

    c4 = snapshot.get_children("totale_rimanenze", BalanceLocation.SP_ATTIVO)

    assert list(map(lambda it: it.field_name, c4)) == ['ci1_materie_prime',
 'ci2_prodotti_semilav_frac_in_corso',
 'ci3_lavori_in_corso',
 'ci4_prodotti_finiti',
 'ci5_acconti',
 'ci5_o1_immobilizzazioni_materiali_destinate_alla_vendita']
    r = 0
    for c1 in c4:
        r += c1.value[0]

    assert snapshot.get_field_value("totale_rimanenze", BalanceLocation.SP_ATTIVO, 0) == r

    c5 = snapshot.get_children("totale_immobilizzazioni_sepind_di_quelle_conc_in_loc_finanz", BalanceLocation.SP_ATTIVO)
    assert list(map(lambda it: it.field_name, c5)) == ['bi_totale_immob_immateriali',
 'bii_totale_immob_materiali',
 'biii_totale_immob_finanziarie']
    r = 0
    for c1 in c5:
        r += c1.value[0]

    assert snapshot.get_field_value("totale_immobilizzazioni_sepind_di_quelle_conc_in_loc_finanz", BalanceLocation.SP_ATTIVO, 0) == r

    c6 = snapshot.get_children("totale_immob_immateriali", BalanceLocation.SP_ATTIVO)
    assert list(map(lambda it: it.field_name, c6)) == ['bi1_costi_impianto_e_ampl',
 'bi2_costi_ricerca_e_pubb',
 'bi3_diritti_brevetto_ind',
 'bi4_concessioni_licenze',
 'bi5_avviamento_frac_differenza_di_consolidamento',
 'bi6_imm_in_corso',
 'bi7_altre_immobiliz_immateriali',
 'bi7_o1_fondo_ammto_immob_immateriali']
    r = 0
    for c1 in c6:
        r += c1.value[0] or 0

    assert snapshot.get_field_value("totale_immob_immateriali",
                                    BalanceLocation.SP_ATTIVO, 0) == r

    c7 = snapshot.get_children("totale_crediti", BalanceLocation.SP_ATTIVO)
    assert list(map(lambda it: it.field_name, c7)) == [
        'cii1_cred_vs_clienti_entro',
 'cii1_o1_cred_vs_clienti_oltre',
 'cii2_cred_vs_controllate_entro',
 'cii2_o1_cred_vs_controllate_oltre',
 'cii3_cred_vs_collegate_entro',
 'cii3_o1_cred_vs_collegate_oltre',
 'cii4_cred_vs_controllanti_entro',
 'cii4_o1_cred_vs_controllanti_oltre',
 'cii5_cred_vs_imprese_sottoposte_al_controllo_delle_controllanti_entro',
 'cii5_o1_cred_vs_imprese_sottoposte_al_controllo_delle_controllanti_oltre',
 'cii5bis_cred_tributari_entro',
 'cii5bis_o1_cred_tributari_oltre',
 'cii5quater_cred_verso_altri_entro',
 'cii5quater_o1_cred_verso_altri_oltre',
 'cii5ter_cred_per_imposte_anticipate_entro',
 'cii5ter_o1_cred_per_imposte_anticipate_oltre']
    r = 0
    for c1 in c7:
        r += c1.value[0] or 0

    assert snapshot.get_field_value("totale_crediti",
                                    BalanceLocation.SP_ATTIVO, 0) == r

    c8 = snapshot.get_children("totale_immob_finanziarie", BalanceLocation.SP_ATTIVO)
    assert list(map(lambda it: it.field_name, c8)) == ['biii1_tot_partecipazioni',
 'biii2_tot_crediti_imm_fin',
 'biii3_altri_titoli',
 'biii3bis_azioni_proprie',
 'biii4_strumenti_finanziari_derivati_attivi',
 'biii_dc_di_cui_esigibili_entro_lesercizio_successivo']
    r = 0
    for c1 in c8:
        r += c1.value[0] or 0

    assert snapshot.get_field_value("totale_immob_finanziarie",
                                    BalanceLocation.SP_ATTIVO, 0) == r

    c9 = snapshot.get_children("tot_crediti_imm_fin", BalanceLocation.SP_ATTIVO)
    assert list(map(lambda it: it.field_name, c9)) == ['biii2a_cred_vs_controllate_entro',
 'biii2a_o1_cred_vs_controllate_oltre',
 'biii2b_cred_vs_collegate_entro',
 'biii2b_o1_cred_vs_collegate_oltre',
 'biii2c_cred_vs_controllanti_entro',
 'biii2c_o1_cred_vs_controllanti_oltre',
 'biii2d_cred_vs_imprese_sottoposte_al_controllo_delle_controllanti_entro',
 'biii2d_o1_cred_vs_imprese_sottoposte_al_controllo_delle_controllanti_oltre',
 'biii2dbis_cred_vs_altri_entro',
 'biii2dbis_o1_cred_vs_altri_oltre']
    r = 0
    for c1 in c9:
        r += c1.value[0] or 0

    assert snapshot.get_field_value("tot_crediti_imm_fin",
                                    BalanceLocation.SP_ATTIVO, 0) == r


def test_conto_economico():
    b = complete_company_1
    snapshot = BalanceSnaphot.from_company_data(b, 0, 1, effect_pointer="", global_config=GLOBAL_CONFIG_SINGLE)
    children = snapshot.get_children("conto_economico", BalanceLocation.CE)

    assert list(map(lambda it: it.field_name, children)) == ['_o10__21_utile_frac_perdita_di_esercizio',
 '_o11_dipendenti',
 '_o1_risultato_operativo',
 '_o2_valore_aggiunto',
 '_o3_totale_proventi_frac_oneri_straordinari',
 '_o4_proventi_straordinari',
 '_o5_oneri_straordinari',
 '_o6_risultato_prima_delle_imposte',
 '_o7__20_totale_imposte_sul_reddito_correnti_differite_e_anticipate',
 '_o8_imposte_correnti',
 '_o9_imposte_relative_a_esercizi_precedenti',
 'a_tot_val_della_produzione',
 'b_costi_della_produzione',
 'c_totale_proventi_e_oneri_finanziari',
 'd_totale_rettifiche_att_finanz',
 'data',
 'moneta',
 'periodo']

    assert snapshot.get_field_value("risultato_operativo", BalanceLocation.CE, 0) == snapshot.get_field_value("tot_val_della_produzione", BalanceLocation.CE, 0) - snapshot.get_field_value("costi_della_produzione", BalanceLocation.CE, 0)

    c2 = snapshot.get_children("costi_della_produzione", BalanceLocation.CE)

    assert list(map(lambda it: it.field_name, c2)) == ['b10_tot_ammortamenti_e_svalut',
 'b11_variazione_materie',
 'b12_accantonamenti_per_rischi',
 'b13_altri_accantonamenti',
 'b14_oneri_diversi_di_gestione',
 'b6_materie_prime_e_consumo',
 'b7_servizi',
 'b8_godimento_beni_di_terzi',
 'b9_totale_costi_del_personale']

    r = 0
    for c1 in c2:
        r += c1.value[0]

    assert snapshot.get_field_value("costi_della_produzione",
                                    BalanceLocation.CE, 0) == r

    c3 = snapshot.get_children("tot_val_della_produzione", BalanceLocation.CE)

    assert list(map(lambda it: it.field_name, c3)) == ['a1_ricavi_vendite_e_prestazioni',
 'a2_var_rimanenze_prodotti',
 'a3_variazione_lavori',
 'a4_incrementi_di_immob',
 'a5_altri_ricavi',
 'a5_o1_contributi_in_conto_esercizio']

    r = 0
    for c1 in c3:
        r += c1.value[0]

    assert snapshot.get_field_value("tot_val_della_produzione",
                                    BalanceLocation.CE, 0) == r

    c4 = snapshot.get_children("totale_proventi_e_oneri_finanziari", BalanceLocation.CE)

    assert list(map(lambda it: it.field_name, c4)) == ['c15_tot_proventi_da_partecip',
 'c16_tot_altri_proventi',
 'c17_totale_oneri_finanziari',
 'c17bis_utili_e_perdite_su_cambi']

    r = 0
    for c1 in c4:
        if "oneri" in c1.field_name:
            r -= c1.value[0]
        else:
            r += c1.value[0]

    assert snapshot.get_field_value("totale_proventi_e_oneri_finanziari",
                                    BalanceLocation.CE, 0) == r

    c5 = snapshot.get_children("totale_rettifiche_att_finanz", BalanceLocation.CE)
    assert list(map(lambda it: it.field_name, c5)) == ['d18_tot_rivalutazioni', 'd19_tot_svalutazioni']

    r = 0
    for c1 in c5:
        if "svalutazioni" in c1.field_name:
            r -= c1.value[0]
        else:
            r += c1.value[0]

    assert snapshot.get_field_value("totale_rettifiche_att_finanz",
                                    BalanceLocation.CE, 0) == r

    c6 = snapshot.get_children("totale_costi_del_personale", BalanceLocation.CE)
    assert list(map(lambda it: it.field_name, c6)) == ['b9a_salari_e_stipendi',
 'b9b_oneri_sociali',
 'b9c_tratt_fine_rapporto',
 'b9d_tratt_di_quiescenza',
 'b9e_altri_costi']

    r = 0
    for c1 in c6:
        r += c1.value[0]

    assert snapshot.get_field_value("totale_costi_del_personale",
                                    BalanceLocation.CE, 0) == r





def test_serialize():
    b = complete_company_1
    snapshot = BalanceSnaphot.from_company_data(b, 0, 1, effect_pointer="", global_config=GLOBAL_CONFIG_SINGLE, single_year=False)
    assert snapshot.get_field_value("cred_vs_controllate_entro", BalanceLocation.SP_ATTIVO, 0) is not None
    sp, ce = snapshot.serialize()

    for node in list(snapshot.stato_patrimoniale.nodes()):
        if node.type != NodeType.VIRTUAL:
            assert (sp.get(node.field_name) is not None or
                    sp["subsections"]["attivo"].get(node.field_name) is not None or
                    sp["subsections"]["passivo"]["subsections"]["debiti"].get(node.field_name) is not None or
                    sp["subsections"]["passivo"]["subsections"]["patrimonio_netto"].get(node.field_name) is not None)

    for node in list(snapshot.conto_economico.nodes()):
        if node.type != NodeType.VIRTUAL:
            assert ce.get(node.field_name) is not None

    # verifico la compatibilità con la raw company iniziale (voglio che abbiano la stessa struttura in memoria)
    assert complete_company_1.stato_patrimoniale == sp
    assert complete_company_1.conto_economico == ce

def test_init():
    b = complete_company_1
    snapshot = BalanceSnaphot.from_company_data(b, 0, 1, effect_pointer="", global_config=GLOBAL_CONFIG_SINGLE)
    snapshot.create_year_start()

    assert snapshot.available_columns == 2

    def check(key, values, node, where):
        if Flag.NO_COPY in node.flags:
            assert node.value[1] == 0.0
        elif Flag.NEED_RECALC in node.flags:
            assert node.value[1] == 0.0
        elif Flag.NO_COPY not in node.flags and Flag.NEED_RECALC not in node.flags:
            assert (node.value[0] or 0) == node.value[1]

    snapshot.for_each_ce_field(check, exclude_context_fields=True)
    def check_shallow_copy(key, values, node, where):
        assert (node.value[0] or 0) == node.value[1]
        assert Flag.UPDATED not in node.flags
        assert Flag.NEED_RECALC not in node.flags

    snapshot.for_each_sp_field(check_shallow_copy, exclude_context_fields=True)

def test_simulation_single_year():
    worker = SimulationWorker(SimulationCompleteModel(
        SimulationState(
            complete_company_1,
            GLOBAL_CONFIG_SINGLE
        ),
        InvestmentProject(
            "Progetto test",
            "Progetto simulazione di test",
            [],
            items=[
                EmployeeHireInvestment(
                    "Assunzione dipendente",
                    1,
                    4000,
                    100,
                    0,
                    0.1,
                    0.1,
                    6,
                    0.24,
                    0.5,
                    "Ruolo"
                )
            ]
        )
    ), )

    result = worker.start()
    return result.balance.serialize()

@pytest.fixture(scope="module")
def balance_data() -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Esegue la simulazione una sola volta per modulo di test.

    La funzione restituisce (sp, ce), in quest'ordine.
    """
    sp, ce = test_simulation_single_year()
    return sp, ce


@pytest.fixture(scope="module")
def sp(balance_data: tuple[dict[str, Any], dict[str, Any]]) -> dict[str, Any]:
    return balance_data[0]


@pytest.fixture(scope="module")
def ce(balance_data: tuple[dict[str, Any], dict[str, Any]]) -> dict[str, Any]:
    return balance_data[1]

@dataclass(frozen=True)
class Term:
    section: Section
    key: str
    sign: int = 1


@dataclass(frozen=True)
class Identity:
    name: str
    target: Term
    terms: tuple[Term, ...]


def C(key: str, sign: int = 1) -> Term:
    return Term("ce", key, sign)


def S(key: str, sign: int = 1) -> Term:
    return Term("sp", key, sign)


def check(name: str, target: Term, *terms: Term) -> Identity:
    return Identity(name, target, terms)


IDENTITIES = [
    check("CE | A valore produzione", C("a_tot_val_della_produzione"),
          C("a1_ricavi_vendite_e_prestazioni"), C("a2_var_rimanenze_prodotti"),
          C("a3_variazione_lavori"), C("a4_incrementi_di_immob"), C("a5_altri_ricavi")),
    check("CE | B9 personale", C("b9_totale_costi_del_personale"),
          C("b9a_salari_e_stipendi"), C("b9b_oneri_sociali"),
          C("b9c_tratt_fine_rapporto"), C("b9d_tratt_di_quiescenza"),
          C("b9e_altri_costi")),
    check("CE | B10 ammortamenti e svalutazioni", C("b10_tot_ammortamenti_e_svalut"),
          C("b10a_amm_immob_immat"), C("b10b_amm_immob_mat"),
          C("b10c_altre_svalut_immob"), C("b10d_svalut_crediti")),
    check("CE | B costi produzione", C("b_costi_della_produzione"),
          C("b6_materie_prime_e_consumo"), C("b7_servizi"),
          C("b8_godimento_beni_di_terzi"), C("b9_totale_costi_del_personale"),
          C("b10_tot_ammortamenti_e_svalut"), C("b11_variazione_materie"),
          C("b12_accantonamenti_per_rischi"), C("b13_altri_accantonamenti"),
          C("b14_oneri_diversi_di_gestione")),
    check("CE | valore aggiunto", C("_o2_valore_aggiunto"),
          C("a_tot_val_della_produzione"), C("b6_materie_prime_e_consumo", -1),
          C("b7_servizi", -1), C("b8_godimento_beni_di_terzi", -1),
          C("b11_variazione_materie", -1), C("b14_oneri_diversi_di_gestione", -1)),
    check("CE | risultato operativo", C("_o1_risultato_operativo"),
          C("a_tot_val_della_produzione"), C("b_costi_della_produzione", -1)),
    check("CE | C16 altri proventi", C("c16_tot_altri_proventi"),
          C("c16a_da_crediti"), C("c16b_da_titoli_iscr_imm"),
          C("c16c_da_titoli_iscr_attcircol"), C("c16d_proventi_fin_diversi")),
    check("CE | C gestione finanziaria", C("c_totale_proventi_e_oneri_finanziari"),
          C("c15_tot_proventi_da_partecip"), C("c16_tot_altri_proventi"),
          C("c17_totale_oneri_finanziari", -1), C("c17bis_utili_e_perdite_su_cambi")),
    check("CE | D18 rivalutazioni", C("d18_tot_rivalutazioni"),
          C("d18a_rivalut_di_partec"), C("d18b_rivalut_di_altre_imm_fin"),
          C("d18c_rivalut_di_titoli"),
          C("d18d_rivalut_di_strumenti_finanziari_derivati"),
          C("d18d_o1_rivalut_di_attivita_finanziarie_per_la_gestione_accentrata_della_tesoreria")),
    check("CE | D19 svalutazioni", C("d19_tot_svalutazioni"),
          C("d19a_svalut_di_partec"), C("d19b_svalut_di_altre_imm_fin"),
          C("d19c_svalut_di_titoli"),
          C("d19d_svalut_di_strumenti_finanziari_derivati"),
          C("d19d_o1_svalut_di_attivita_finanziarie_per_la_gestione_accentrata_della_tesoreria")),
    check("CE | D rettifiche finanziarie", C("d_totale_rettifiche_att_finanz"),
          C("d18_tot_rivalutazioni"), C("d19_tot_svalutazioni", -1)),
    check("CE | risultato ante imposte", C("_o6_risultato_prima_delle_imposte"),
          C("_o1_risultato_operativo"), C("c_totale_proventi_e_oneri_finanziari"),
          C("d_totale_rettifiche_att_finanz")),
    check("CE | utile netto", C("_o10__21_utile_frac_perdita_di_esercizio"),
          C("_o6_risultato_prima_delle_imposte"),
          C("_o7__20_totale_imposte_sul_reddito_correnti_differite_e_anticipate", -1)),
    check("SP | BI immateriali", S("bi_totale_immob_immateriali"),
          S("bi1_costi_impianto_e_ampl"), S("bi2_costi_ricerca_e_pubb"),
          S("bi3_diritti_brevetto_ind"), S("bi4_concessioni_licenze"),
          S("bi5_avviamento_frac_differenza_di_consolidamento"),
          S("bi6_imm_in_corso"), S("bi7_altre_immobiliz_immateriali"),
          S("bi7_o1_fondo_ammto_immob_immateriali", -1)),
    check("SP | BII materiali", S("bii_totale_immob_materiali"),
          S("bii1_terreni_e_fabbricati"), S("bii2_impianti"),
          S("bii3_attrez_industriali"), S("bii4_altri_beni"),
          S("bii5_imm_in_corso_frac_acconti"),
          S("bii5_o1_fondo_ammto_immob_materiali", -1)),
    check("SP | BIII1 partecipazioni", S("biii1_tot_partecipazioni"),
          S("biii1a_imprese_controllate"), S("biii1b_imprese_collegate"),
          S("biii1c_imprese_controllanti"),
          S("biii1d_in_imprese_sottoposte_al_controllo_delle_controllanti"),
          S("biii1dbis_altre_imprese")),
    check("SP | BIII2 crediti finanziari", S("biii2_tot_crediti_imm_fin"),
          S("biii2a_cred_vs_controllate_entro"), S("biii2a_o1_cred_vs_controllate_oltre"),
          S("biii2b_cred_vs_collegate_entro"), S("biii2b_o1_cred_vs_collegate_oltre"),
          S("biii2c_cred_vs_controllanti_entro"), S("biii2c_o1_cred_vs_controllanti_oltre"),
          S("biii2d_cred_vs_imprese_sottoposte_al_controllo_delle_controllanti_entro"),
          S("biii2d_o1_cred_vs_imprese_sottoposte_al_controllo_delle_controllanti_oltre"),
          S("biii2dbis_cred_vs_altri_entro"), S("biii2dbis_o1_cred_vs_altri_oltre")),
    check("SP | BIII immobilizzazioni finanziarie", S("biii_totale_immob_finanziarie"),
          S("biii1_tot_partecipazioni"), S("biii2_tot_crediti_imm_fin"),
          S("biii3_altri_titoli"), S("biii3bis_azioni_proprie"),
          S("biii4_strumenti_finanziari_derivati_attivi")),
    check("SP | B immobilizzazioni", S("b_totale_immobilizzazioni_sepind_di_quelle_conc_in_loc_finanz"),
          S("bi_totale_immob_immateriali"), S("bii_totale_immob_materiali"),
          S("biii_totale_immob_finanziarie")),
    check("SP | CI rimanenze", S("ci_totale_rimanenze"),
          S("ci1_materie_prime"), S("ci2_prodotti_semilav_frac_in_corso"),
          S("ci3_lavori_in_corso"), S("ci4_prodotti_finiti"), S("ci5_acconti"),
          S("ci5_o1_immobilizzazioni_materiali_destinate_alla_vendita")),
    check("SP | CII crediti", S("cii_totale_crediti"),
          S("cii1_cred_vs_clienti_entro"), S("cii1_o1_cred_vs_clienti_oltre"),
          S("cii2_cred_vs_controllate_entro"), S("cii2_o1_cred_vs_controllate_oltre"),
          S("cii3_cred_vs_collegate_entro"), S("cii3_o1_cred_vs_collegate_oltre"),
          S("cii4_cred_vs_controllanti_entro"), S("cii4_o1_cred_vs_controllanti_oltre"),
          S("cii5_cred_vs_imprese_sottoposte_al_controllo_delle_controllanti_entro"),
          S("cii5_o1_cred_vs_imprese_sottoposte_al_controllo_delle_controllanti_oltre"),
          S("cii5bis_cred_tributari_entro"), S("cii5bis_o1_cred_tributari_oltre"),
          S("cii5ter_cred_per_imposte_anticipate_entro"),
          S("cii5ter_o1_cred_per_imposte_anticipate_oltre"),
          S("cii5quater_cred_verso_altri_entro"), S("cii5quater_o1_cred_verso_altri_oltre")),
    check("SP | CIII attività finanziarie", S("ciii_totale_attivita_finanziarie"),
          S("ciii1_partecni_in_controllate"), S("ciii2_partecni_in_collegate"),
          S("ciii3_partecni_in_controllanti"),
          S("ciii3bis_partecni_in_imprese_sottoposte_al_controllo_delle_controllanti"),
          S("ciii4_altre_partecni"), S("ciii4bis_azioni_proprie"),
          S("ciii5_strumenti_finanziari_derivati_attivi"), S("ciii6_altri_titoli"),
          S("ciii7_attivita_finanziarie_per_la_gestione_accentrata_della_tesoreria")),
    check("SP | CIV liquidità", S("civ_tot_dispon_liquide"),
          S("civ1_depositi_bancari"), S("civ2_assegni"), S("civ3_denaro_in_cassa")),
    check("SP | C attivo circolante", S("c_attivo_circolante"),
          S("ci_totale_rimanenze"), S("cii_totale_crediti"),
          S("ciii_totale_attivita_finanziarie"), S("civ_tot_dispon_liquide")),
    check("SP | totale attivo", S("_o1_totale_attivo"),
          S("a_crediti_verso_soci"),
          S("b_totale_immobilizzazioni_sepind_di_quelle_conc_in_loc_finanz"),
          S("c_attivo_circolante"), S("d_ratei_e_risconti")),

    # STATO PATRIMONIALE: PASSIVO
    check("SP | fondi rischi", S("b_totale_fondi_rischi"),
          S("b1_fondo_di_quiescenza"), S("b2_fondo_imposte_anche_differite"),
          S("b3_strumenti_finanziari_derivati_passivi"), S("b4_altri_fondi")),
    check("SP | debiti", S("d_totale_debiti"),
          S("d1_obbligni_entro"), S("d1_o1_obbligni_oltre"),
          S("d2_obbligni_convert_entro"), S("d2_o1_obbligni_convert_oltre"),
          S("d3_soci_per_finanziamenti_entro"), S("d3_o1_soci_per_finanziamenti_oltre"),
          S("d4_banche_entro_lesercizio"), S("d4_o1_banche_oltre_lesercizio"),
          S("d5_altri_finanziatori_entro"), S("d5_o1_altri_finanziatori_oltre"),
          S("d6_acconti_entro"), S("d6_o1_acconti_oltre"),
          S("d7_fornitori_entro"), S("d7_o1_fornitori_oltre"),
          S("d8_titoli_di_credito_entro"), S("d8_o1_titoli_di_credito_oltre"),
          S("d9_imprese_controllate_entro"), S("d9_o1_imprese_controllate_oltre"),
          S("d10_imprese_collegate_entro"), S("d10_o1_imprese_collegate_oltre"),
          S("d11_controllanti_entro"), S("d11_o1_controllanti_oltre"),
          S("d11bis_debiti_vs_imprese_sottoposte_al_controllo_delle_controllanti_entro"),
          S("d11bis_o1_debiti_vs_imprese_sottoposte_al_controllo_delle_controllanti_oltre"),
          S("d12_debiti_tributari_entro"), S("d12_o1_debiti_tributari_oltre"),
          S("d13_istituti_previdenza_entro"), S("d13_o1_istituti_previdenza_oltre"),
          S("d14_altri_debiti_entro"), S("d14_o1_altri_debiti_oltre")),
    check("SP | patrimonio netto", S("a_totale_patrimonio_netto"),
          S("ai_capitale_sociale"), S("aii_riserva_da_sovrapprezzo"),
          S("aiii_riserva_di_rivalutazione"), S("aiv_riserva_legale"),
          S("av_riserva_statutaria"), S("avi_altre_riserve"),
          S("avii_riserva_per_operazioni_di_copertura_dei_flussi_finanziari_attesi"),
          S("aviii_utile_frac_perdita_a_nuovo"),
          S("aix_utile_frac_perdita_di_esercizio"),
          S("ax_riserva_negativa_per_azioni_proprie_in_portafoglio__plus_frac___", -1)),
    check("SP | totale passivo", S("_o2_totale_passivo"),
          S("a_totale_patrimonio_netto"), S("b_totale_fondi_rischi"),
          S("c_trattamento_di_fine_rapporto"), S("d_totale_debiti"),
          S("e_ratei_e_risconti")),
    check("SP | attivo uguale passivo", S("_o1_totale_attivo"),
          S("_o2_totale_passivo")),
]


def read_value(
    sp: dict[str, Any],
    ce: dict[str, Any],
    term: Term,
) -> Decimal:
    """Legge il field_name completo nella colonna 1 dell'export originale.

    Il CE contiene direttamente le voci; lo SP contiene le sottosezioni
    attivo, passivo/debiti e passivo/patrimonio_netto. Non appiattisce nulla.
    """
    if term.section == "ce":
        data = ce
        section_name = "conto_economico"
    else:
        try:
            attivo = sp["subsections"]["attivo"]
            passivo = sp["subsections"]["passivo"]["subsections"]
            debiti = passivo["debiti"]
            patrimonio = passivo["patrimonio_netto"]
        except (KeyError, TypeError) as exc:
            pytest.fail(f"Struttura SP non conforme all'export: {exc}")

        matches = [
            (name, section)
            for name, section in (
                ("stato_patrimoniale/attivo", attivo),
                ("stato_patrimoniale/passivo/debiti", debiti),
                ("stato_patrimoniale/passivo/patrimonio_netto", patrimonio),
            )
            if term.key in section
        ]
        if not matches:
            pytest.fail(f"Chiave SP mancante: {term.key}")
        if len(matches) != 1:
            pytest.fail(
                f"Chiave SP ambigua, presente in più sottosezioni: {term.key}; "
                f"sezioni: {[name for name, _ in matches]}"
            )
        section_name, data = matches[0]

    if term.key not in data:
        pytest.fail(f"Chiave mancante in {section_name}: {term.key}")

    columns = data[term.key]
    if not isinstance(columns, (list, tuple)) or len(columns) <= COLUMN:
        pytest.fail(
            f"Colonna {COLUMN} assente per {section_name}.{term.key}: "
            f"{columns!r}"
        )

    raw = columns[COLUMN]
    if raw is None or isinstance(raw, bool):
        pytest.fail(
            f"Valore non numerico in {section_name}.{term.key}[{COLUMN}]: "
            f"{raw!r}"
        )
    try:
        result = Decimal(str(raw))
    except (InvalidOperation, ValueError):
        pytest.fail(
            f"Valore non numerico in {section_name}.{term.key}[{COLUMN}]: "
            f"{raw!r}"
        )
    if not result.is_finite():
        pytest.fail(f"Valore non finito in {section_name}.{term.key}[{COLUMN}]")
    return result

@pytest.mark.parametrize("rule", IDENTITIES, ids=lambda rule: rule.name)
def test_balance_identity(
    sp: dict[str, Any],
    ce: dict[str, Any],
    rule: Identity,
) -> None:
    """Controlla una quadratura del bilancio simulato (colonna 1)."""
    actual = read_value(sp, ce, rule.target)
    expected = sum(
        (term.sign * read_value(sp, ce, term) for term in rule.terms),
        Decimal("0"),
    )
    difference = actual - expected

    assert abs(difference) <= TOLERANCE, (
        f"\nIdentità: {rule.name}"
        f"\nCampo: {rule.target.section.upper()}.{rule.target.key}[{COLUMN}]"
        f"\nAtteso: {expected:,.2f}"
        f"\nEffettivo: {actual:,.2f}"
        f"\nScarto: {difference:,.2f}"
    )


def test_simulation_multiple_year():
    worker = SimulationWorker(SimulationCompleteModel(
        SimulationState(
            complete_company_1,
            GLOBAL_CONFIG_MUL
        ),
        InvestmentProject(
            "Progetto test",
            "Progetto simulazione di test",
            [],
            items=[
                EmployeeHireInvestment(
                    "Assunzione dipendente",
                    1,
                    4000,
                    100,
                    0,
                    0.1,
                    0.1,
                    6,
                    0.24,
                    0.5,
                    "Ruolo"
                )
            ]
        )
    ), )

    worker.start()

def test_copy_snap():
    s1 = BalanceSnaphot.from_company_data(complete_company_1, 0, 0, GLOBAL_CONFIG_SINGLE, single_year=True, effect_pointer="")
    s2 = BalanceSnaphot.from_company_data(complete_company_1, 1, 1, GLOBAL_CONFIG_SINGLE, single_year=False, effect_pointer="")

    s1.reset_columns(0, 0)

    def check0(key, values, node, __):
        assert node.value[0] == 0

    s1.for_each_sp_field(check0, exclude_context_fields=True)
    s1.for_each_ce_field(check0, exclude_context_fields=True)

    s2.copy_column_from_snapshot(s1, source_column=0, dest_column=2)

    def check(key, value, node, __):
        assert node.value[2] == 0

    s2.for_each_sp_field(check, exclude_context_fields=True)
    s2.for_each_ce_field(check, exclude_context_fields=True)



from dao.simulation.simulation_dao import SimulationDAO
from dao.util import step_up_numbering, step_up_field, extract_complete_numbering, BalanceLocation
from model.balance_snap import BalanceSnaphot
from model.investment_item import InvestmentProject
from model.node import Node, NodeType, Flag
from model.sim_output import SimulationOutput
from test_data import complete_company_1, GLOBAL_CONFIG


def test_balance():
    b = complete_company_1
    snapshot = BalanceSnaphot.from_company_data(b, 0, 1, effect_pointer="", global_config=GLOBAL_CONFIG)
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
            global_parameters=GLOBAL_CONFIG,
            balance=BalanceSnaphot.from_company_data(b, 0, 1, effect_pointer="", global_config=GLOBAL_CONFIG),
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
    snapshot = BalanceSnaphot.from_company_data(b, 0, 1, effect_pointer="", global_config=GLOBAL_CONFIG)
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
    snapshot = BalanceSnaphot.from_company_data(b, 0, 1, effect_pointer="", global_config=GLOBAL_CONFIG)
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
    snapshot = BalanceSnaphot.from_company_data(b, 0, 1, effect_pointer="", global_config=GLOBAL_CONFIG)
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
    snapshot = BalanceSnaphot.from_company_data(b, 0, 1, effect_pointer="", global_config=GLOBAL_CONFIG)
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
    assert list(map(lambda it: it.field_name, c6)) == ['bi_totale_immob_immateriali',
                                                       'bii_totale_immob_materiali',
                                                       'biii_totale_immob_finanziarie']
    r = 0
    for c1 in c5:
        r += c1.value[0]

    assert snapshot.get_field_value("totale_immobilizzazioni_sepind_di_quelle_conc_in_loc_finanz",
                                    BalanceLocation.SP_ATTIVO, 0) == r


def test_conto_economico():
    b = complete_company_1
    snapshot = BalanceSnaphot.from_company_data(b, 0, 1, effect_pointer="", global_config=GLOBAL_CONFIG)
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
    snapshot = BalanceSnaphot.from_company_data(b, 0, 1, effect_pointer="", global_config=GLOBAL_CONFIG, single_year=False)
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
    snapshot = BalanceSnaphot.from_company_data(b, 0, 1, effect_pointer="", global_config=GLOBAL_CONFIG)
    snapshot.create_year_start()

    assert snapshot.available_columns == 2
    assert snapshot.serialize() == []






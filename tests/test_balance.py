from controller.simulation_controller import SimulationWorker
from dao.simulation.simulation_dao import SimulationDAO
from dao.util import step_up_numbering, step_up_field
from model.balance_snap import BalanceSnaphot, BalanceLocation
from model.investment_item import InvestmentProject
from model.sim_output import SimulationOutput
from model.sim_state import SimulationCompleteModel, SimulationState, GlobalParameters
from test_data import complete_company_1


def test_balance():
    b = complete_company_1
    snapshot = BalanceSnaphot.from_company_data(b, 0, 1, "")
    assert snapshot.verify_integrity() == True
    snapshot.create_column("test")

    assert snapshot.verify_integrity() == True
    snapshot.set_field_value("a_crediti_verso_soci", BalanceLocation.SP_ATTIVO, 200, 4, 0)
    snapshot.set_field_value("a_totale_patrimonio_netto", BalanceLocation.SP_PASSIVO_PATRIM, 300, 4, 0)
    snapshot.set_field_value("d3_soci_per_finanziamenti_entro", BalanceLocation.SP_PASSIVO_DEBITI, 30000000, 4, 0)

    try:
        snapshot.set_field_value("ciao", BalanceLocation.CE, 300, 4, 0)
        assert False
    except:
        assert True

def test_sim():
    b = complete_company_1
    ctrl = SimulationOutput(
            global_parameters=GlobalParameters(
                    b.fiscal_code,
                    2,
                    2026,
                    organic_growth_avg=0.5,
                    last_available_years=b.available_years,
                    sim_id=5,
                organic_growth_var=0.3,
                ),
            balance=BalanceSnaphot.from_company_data(complete_company_1, 0, 5, ""),
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
    assert step_up_numbering("cii5bis_cred_tributari_entro") == "cii5"
    assert step_up_numbering("cii5quater_cred_verso_altri_entro") == "cii5"
    assert step_up_numbering("civ1_depositi_bancari") == "civ"
    assert step_up_numbering("aiv_riserva_legale") == "a"

    assert step_up_field("d11bis_debiti_vs_imprese_sottoposte_al_controllo_delle_controllanti_entro") == "d11"
    assert step_up_field("_o1_totale_passivo") == ""
    assert step_up_field("d_o1_total_debiti_entro_lesercizio") == "d"
    assert step_up_field("e_o1_aggio_sui_prestiti") == "e"
    assert step_up_field("ai_dc_di_cui_versamenti_in_c_frac_futuro_aumento_di_capitale") == "ai"
    assert step_up_field("aix_o1_acconto_dividendi") == "aix"
    assert step_up_field("aix_utile_frac_perdita_di_esercizio") == "a"
    assert step_up_field("av_o1_riserva_azioni_proprie") == "av"
    assert step_up_field("ax_riserva_negativa_per_azioni_proprie_in_portafoglio__plus_frac___") == "a"
    assert step_up_field("b1_fondo_di_quiescenza") == "b"
    assert step_up_field("c_trattamento_di_fine_rapporto") == ""
    assert step_up_field("_o1_totale_attivo") == ""
    assert step_up_field("bii_dc_di_cui_beni_materiali_concessi_in_locazione_finanziaria") == "bii"
    assert step_up_field("ax_o2_dc_di_cui_per_imposte_differite") == "ax_o2_"


def test_parent():
    b = complete_company_1
    snapshot = BalanceSnaphot.from_company_data(b, 0, 1, "")
    assert snapshot.__get_uppermost_field_parent__("c15_tot_proventi_da_partecip", BalanceLocation.CE) == "c_totale_proventi_e_oneri_finanziari"
    assert snapshot.__get_uppermost_field_parent__("c_totale_proventi_e_oneri_finanziari", BalanceLocation.CE) == "c_totale_proventi_e_oneri_finanziari"
    assert snapshot.__get_uppermost_field_parent__("b9f_tfr_plus_quiescenza_plus_altri_costi", BalanceLocation.CE) == "b_costi_della_produzione"
    assert snapshot.__get_uppermost_field_parent__("valore_aggiunto", BalanceLocation.CE) is None
    assert snapshot.__get_uppermost_field_parent__("rivalut_di_attivita_finanziarie_per_la_gestione_accentrata_della_tesoreria", BalanceLocation.CE) is None
    assert snapshot.__get_uppermost_field_parent__("_20_totale_imposte_sul_reddito_correnti_differite_e_anticipate", BalanceLocation.CE) is None
    assert snapshot.__get_uppermost_field_parent__("a2_plus_a3_totale_variazioni", BalanceLocation.CE) == "a_tot_val_della_produzione"
    assert snapshot.__get_uppermost_field_parent__("e_ratei_e_risconti", BalanceLocation.SP_PASSIVO_DEBITI) == "e_ratei_e_risconti"
    assert snapshot.__get_uppermost_field_parent__("d6_acconti_entro", BalanceLocation.SP_PASSIVO_DEBITI) == "d_totale_debiti"
    assert snapshot.__get_uppermost_field_parent__("d3_soci_per_finanziamenti_entro", BalanceLocation.SP_PASSIVO_DEBITI) == "d_totale_debiti"
    assert snapshot.__get_uppermost_field_parent__("totale_passivo", BalanceLocation.SP_PASSIVO_DEBITI) is None
    assert snapshot.get_children("d_totale_debiti", BalanceLocation.SP_PASSIVO_DEBITI) == [
 'd1_obbligni_entro',
 'd1_obbligni_oltre',
 'd2_obbligni_convert_entro',
 'd2_obbligni_convert_oltre',
 'd3_soci_per_finanziamenti_entro',
 'd3_soci_per_finanziamenti_oltre',
 'd4_banche_entro_lesercizio',
 'd4_banche_oltre_lesercizio',
 'd5_altri_finanziatori_entro',
 'd5_altri_finanziatori_oltre',
 'd6_acconti_entro',
 'd6_acconti_oltre',
 'd7_fornitori_entro',
 'd7_fornitori_oltre',
 'd8_titoli_di_credito_entro',
 'd8_titoli_di_credito_oltre',
 'd9_imprese_controllate_entro',
 'd9_imprese_controllate_oltre',
 'd10_imprese_collegate_entro',
 'd10_imprese_collegate_oltre',
 'd11_controllanti_entro',
 'd11_controllanti_oltre',
 'd11bis_debiti_vs_imprese_sottoposte_al_controllo_delle_controllanti_entro',
 'd11bis_debiti_vs_imprese_sottoposte_al_controllo_delle_controllanti_oltre',
 'd12_debiti_tributari_entro',
 'd12_debiti_tributari_oltre',
 'd13_istituti_previdenza_entro',
 'd13_istituti_previdenza_oltre',
 'd14_altri_debiti_entro',
 'd14_altri_debiti_oltre']

    assert snapshot.get_children("d1_obbligni_entro", BalanceLocation.SP_PASSIVO_DEBITI) == []

    try:
         snapshot.__get_uppermost_field_parent__("d18a_rivalut_di_partec", True)    # La ricerca del parent di un campo che non esiste deve lanciare un'eccezione
         assert False
    except:
        assert True

    assert (snapshot.sum_children_values(field_name="d_totale_debiti",
                            where=BalanceLocation.SP_PASSIVO_DEBITI) ==
            snapshot.get_field_data(field_name="d_totale_debiti", where=BalanceLocation.SP_PASSIVO_DEBITI))

    assert (snapshot.sum_children_values(field_name="a_tot_val_della_produzione",
                            where=BalanceLocation.CE) ==
            snapshot.get_field_data(field_name="a_tot_val_della_produzione", where=BalanceLocation.CE))

    assert snapshot.get_children("b_costi_della_produzione", BalanceLocation.CE) == ['b6_materie_prime_e_consumo',
 'b7_servizi',
 'b8_godimento_beni_di_terzi',
 'b9_totale_costi_del_personale',
 'b9a_salari_e_stipendi',
 'b9b_oneri_sociali',
 'b9c_tratt_fine_rapporto',
 'b9d_tratt_di_quiescenza',
 'b9e_altri_costi',
 'b9f_tfr_plus_quiescenza_plus_altri_costi',
 'b10_tot_ammortamenti_e_svalut',
 'b10a_amm_immob_immat',
 'b10b_amm_immob_mat',
 'b10c_altre_svalut_immob',
 'b10d_svalut_crediti',
 'b11_variazione_materie',
 'b12_accantonamenti_per_rischi',
 'b13_altri_accantonamenti',
 'b14_oneri_diversi_di_gestione']

    assert (snapshot.sum_children_values(field_name="b_costi_della_produzione",
                            where=BalanceLocation.CE) ==
            snapshot.get_field_data(field_name="b_costi_della_produzione", where=BalanceLocation.CE))



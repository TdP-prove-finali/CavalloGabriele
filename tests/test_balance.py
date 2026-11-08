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
    snapshot.set_field_value("crediti_verso_soci", BalanceLocation.SP_ATTIVO, 200, 0)
    snapshot.set_field_value("totale_patrimonio_netto", BalanceLocation.SP_PASSIVO_PATRIM, 300, 0)
    snapshot.set_field_value("soci_per_finanziamenti_entro", BalanceLocation.SP_PASSIVO_DEBITI, 30000000, 0)
    assert snapshot.get_field_value("crediti_verso_soci", BalanceLocation.SP_ATTIVO, month=0) == 200
    assert snapshot.get_field_value("totale_patrimonio_netto", BalanceLocation.SP_PASSIVO_PATRIM, month=0) == 300
    assert snapshot.get_field_value("soci_per_finanziamenti_entro", BalanceLocation.SP_PASSIVO_DEBITI, month=0) == 30000000

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
    assert list(map(lambda it: it.field_name, snapshot.get_children("totale_debiti", BalanceLocation.SP_PASSIVO_DEBITI))) == [
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


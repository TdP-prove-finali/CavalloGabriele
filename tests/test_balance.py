from controller.simulation_controller import SimulationWorker
from model.investment_item import InvestmentProject
from model.raw_company_data import BalanceSnaphot, BalanceLocation
from model.sim_state import SimulationCompleteModel, SimulationState, GlobalParameters
from test_data import complete_company_1


def test_balance():
    b = complete_company_1
    snapshot = BalanceSnaphot.from_company_data(b, (0, 0), 1, "")
    assert snapshot.conto_economico == b.conto_economico
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
    ctrl = SimulationWorker(
        SimulationCompleteModel(
            SimulationState(
                b,
                GlobalParameters(
                    b.fiscal_code,
                    2,
                    2026,
                    organic_growth=0.5,
                    last_available_years=b.available_years,
                    sim_id=5
                )
            ),
            InvestmentProject(
                "test",
                "test",
                []
            )
        ),
        None,
        None
    )
    ctrl.start()


from dao.balance_dao import BalanceDao
from model.Company import Company
from model.Section import GeneralInfoSection

company = Company(
    sections=[
        GeneralInfoSection(
            name="General-info",
            nome_azienda="PARAMOUNT GLOBAL ITALIA S.R.L.",
            sede="20122 Milano",
            codice_fiscale="07237600965",
            numero_cciaa="MI1945654",
            descrizione=
                "The Global Ultimate Owner of this controlled subsidiary is DAVID ELLISON FAMILY"
        )
    ]
)

def test_loader():
    c = BalanceDao.import_from_excel("../dataset/sample-aida-single.xlsx")
    assert c == company
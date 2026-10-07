from dao.balance_dao import CompanyBalanceImporter
from model.Company import Company
from model.Section import GeneralInfoSection, Section

company = Company(
    sections=[
        Section(
            name="general_info",
            data={"company_name": "PARAMOUNT GLOBAL ITALIA S.R.L.",
                  "sede": "20122 Milano",
                "codice_fiscale": "07237600965",
                "numero_cciaa":"MI1945654"}
        )
    ]
)

def test_loader():
    c = CompanyBalanceImporter("../dataset/sample-aida-single.xlsx")
    c.import_from_excel()
    assert c.company == company
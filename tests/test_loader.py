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
                "numero_cciaa":"MI1945654",
'controllante': 'The Global Ultimate Owner of '
                                               'this controlled subsidiary is '
                                               'DAVID ELLISON FAMILY',
                'tipo_societa': 'Società privata'
                  }
        ),
        Section(
            name="anagrafica",
            data={
                "indirizzo_sede_legale": ' CSO EUROPA, 5 20122 Milano MILANO(LOMBARDIA)',
                "sito_web": 'www.paromountplus.com',
                "indirizzo_sede_operativa": ' CORSO EUROPA 5 20122 Milano MILANO(LOMBARDIA)',
                "numero_di_telefono": '02762117288'
            }
        )
    ]
)

def test_loader():
    c = CompanyBalanceImporter("../dataset/sample-aida-single.xlsx")
    c.import_from_excel()
    assert c.company == company
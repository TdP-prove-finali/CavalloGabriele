import datetime

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
        ),
        Section(
            name="informazioni_commerciali_e_legali",
            data={
                "stato_giuridico": "Attiva",
                'data_di_chiusura_ultimo_bilancio': '31/12/2024',
                "forma_giuridica": 'S.R.L.',
'numero_di_anni_disponibili':10,
"data_di_costituzione": datetime.datetime(2010, 12, 13, 0, 0),
                "bilanci_disponibili": 'Bilancio non consolidato',
                "ultimo_modello_di_contabilità___bilancio": 'Dettagliato'
            }
        ),
Section(name='dimensioni_e_gruppo',
                          data={'capitale_sociale__2024_': '1.010\xa0migl EUR',
                                'dipendenti__2024_': '122',
                                "indicatore_d'indipendenza_bvd": 'D',
                                'no_of_companies_in_corporate_group': 1081,
                                'n°_partecipate_registrate': 0,
                                'principale_borsa': 'Non quotata',
                                'ricavi_del_vendite__2024_': '51.425.537\xa0'
                                                             'EUR',
                                'totale_attività__2024_': '254.218.368\xa0EUR',
                                'utile_netto__2024_': '2.127.024\xa0EUR'}),
Section(name='gruppo_dei_pari',
                          data={'descrizione': 'Attività di produzione '
                                               'cinematografica, di video e di '
                                               'programmi televisivi',
                                'dimensione': '862 società',
                                'nome': '591 VL (Aziende Molto Grandi)'})
    ]
)

def test_loader():
    c = CompanyBalanceImporter("../dataset/sample-aida-single.xlsx")
    c.import_from_excel()
    assert c.company == company
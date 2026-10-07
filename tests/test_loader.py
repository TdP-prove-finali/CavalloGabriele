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
                "ultimo_modello_di_contabilita___bilancio": 'Dettagliato'
            }
        ),
Section(name='dimensioni_e_gruppo',
                          data={'capitale_sociale__2024_': '1.010\xa0migl EUR',
                                'dipendenti__2024_': '122',
                                "indicatore_dindipendenza_bvd": 'D',
                                'no_of_companies_in_corporate_group': 1081,
                                'n_partecipate_registrate': 0,
                                'principale_borsa': 'Non quotata',
                                'ricavi_del_vendite__2024_': '51.425.537\xa0'
                                                             'EUR',
                                'totale_attivita__2024_': '254.218.368\xa0EUR',
                                'utile_netto__2024_': '2.127.024\xa0EUR'}),
Section(name='gruppo_dei_pari',
                          data={'descrizione': 'Attività di produzione '
                                               'cinematografica, di video e di '
                                               'programmi televisivi',
                                'dimensione': '862 società',
                                'nome': '591 VL (Aziende Molto Grandi)'}),
Section(name='overview_completa',
                          data={'overview': 'This company, which is based in '
                                            'Italy, is engaged in the '
                                            'provision of television '
                                            'broadcasting services. It was '
                                            'incorporated in 2010 and has its '
                                            'registered business address '
                                            'located in Milano. It operates '
                                            'its business primarily in the '
                                            'domestic market.The company is '
                                            'involved in the operation of '
                                            'television broadcasting studios '
                                            'and facilities for the '
                                            'programming and transmission of '
                                            'programs to the public. It also '
                                            'produces and transmits visual '
                                            'programming to affiliated '
                                            'broadcast television stations, '
                                            'which in turn broadcast the '
                                            'programs to the public on a '
                                            'predetermined schedule. The '
                                            "company's programming may "
                                            'originate in their own studio, '
                                            'from an affiliated network, or '
                                            'from other external sources.'}),
Section(name='profilo_finanziario',
                          data={'data': ['31/12/2024',
                                         '31/12/2023',
                                         '31/12/2022',
                                         '31/12/2021',
                                         '31/12/2020',
                                         '31/12/2019',
                                         '30/09/2018',
                                         '30/09/2017',
                                         '30/09/2016',
                                         '30/09/2015'],
                                'debiti_v_frac_banche_su_fatt__perc_': [0,
                                                                        0,
                                                                        0,
                                                                        0,
                                                                        0,
                                                                        0,
                                                                        0,
                                                                        0,
                                                                        0,
                                                                        0.04],
                                'debt_frac_ebitda_ratio': [0,
                                                           0,
                                                           0,
                                                           0,
                                                           0,
                                                           0,
                                                           0,
                                                           0,
                                                           0,
                                                           0],
                                'debt_frac_equity_ratio': [0,
                                                           0,
                                                           0,
                                                           0,
                                                           0,
                                                           0,
                                                           0,
                                                           0,
                                                           0,
                                                           0],
                                'dipendenti': [122,
                                               125,
                                               114,
                                               113,
                                               115,
                                               115,
                                               114,
                                               108,
                                               103,
                                               118],
                                'ebitda': [28403582,
                                           12983608,
                                           23715739,
                                           32647736,
                                           26344285,
                                           7897589,
                                           43498503,
                                           34066962,
                                           22615389,
                                           13577962],
                                'ebitda_frac_vendite__perc_': [31.81,
                                                               15.4,
                                                               35.7,
                                                               44.5,
                                                               38.04,
                                                               47.54,
                                                               54.09,
                                                               50.17,
                                                               40.79,
                                                               40.56],
                                'moneta': ['EUR',
                                           'EUR',
                                           'EUR',
                                           'EUR',
                                           'EUR',
                                           'EUR',
                                           'EUR',
                                           'EUR',
                                           'EUR',
                                           'EUR'],
                                'patrimonio_netto': [203309390,
                                                     201344424,
                                                     127297774,
                                                     114159326,
                                                     104442226,
                                                     114718218,
                                                     116569652,
                                                     60360224,
                                                     100379379,
                                                     97280331],
                                'periodo': ['12 mesi',
                                            '12 mesi',
                                            '12 mesi',
                                            '12 mesi',
                                            '12 mesi',
                                            '3 mesi',
                                            '12 mesi',
                                            '12 mesi',
                                            '12 mesi',
                                            '12 mesi'],
                                'posizione_finanziaria_netta': [-525304,
                                                                -1214852,
                                                                -5421118,
                                                                -1102388,
                                                                -600225,
                                                                -606855,
                                                                -604955,
                                                                -500000,
                                                                -498187,
                                                                -9318735],
                                'redditivita_del_capitale_proprio__roe___perc_': [1.05,
                                                                                  1.39,
                                                                                  11.13,
                                                                                  8.54,
                                                                                  -12.34,
                                                                                  -2.8,
                                                                                  48.77,
                                                                                  7.78,
                                                                                  2.5,
                                                                                  -8.64],
                                'redditivita_del_totale_attivo__roa___perc_': [1.99,
                                                                               1.02,
                                                                               8.71,
                                                                               9.52,
                                                                               -7.29,
                                                                               -0.73,
                                                                               6.72,
                                                                               5.45,
                                                                               3.48,
                                                                               0.53],
                                'redditivita_delle_vendite__ros___perc_': [5.66,
                                                                           2.96,
                                                                           22.23,
                                                                           19.44,
                                                                           -14.06,
                                                                           -7.17,
                                                                           12.95,
                                                                           11.52,
                                                                           8.85,
                                                                           2.2],
                                'ricavi_delle_vendite': [51425537,
                                                         38188322,
                                                         41009331,
                                                         73044778,
                                                         68014095,
                                                         16153403,
                                                         74734328,
                                                         65736415,
                                                         52841149,
                                                         30272663],
                                'rotaz_cap_investito__volte_': [0.2,
                                                                0.16,
                                                                0.24,
                                                                0.49,
                                                                0.51,
                                                                0.1,
                                                                0.48,
                                                                0.46,
                                                                0.37,
                                                                0.22],
                                'totale_attivita': [254218368,
                                                    245364737,
                                                    169573179,
                                                    149854449,
                                                    133524999,
                                                    162212637,
                                                    154994713,
                                                    143549866,
                                                    141150298,
                                                    137837835],
                                'utile_netto': [2127024,
                                                2796813,
                                                14173223,
                                                9744589,
                                                -12882992,
                                                -3211300,
                                                56853220,
                                                4696848,
                                                2506548,
                                                -8401074]})
    ]
)

def test_loader():
    c = CompanyBalanceImporter("../dataset/sample-aida-single.xlsx")
    c.import_from_excel()
    assert c.company == company
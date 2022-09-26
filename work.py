import pandas as pd 
import numpy as np
import os

# utils
# Est vide pour une string
def isNaN(string):
    return string != string

# Récuparation des FINESS de tous les EHPAD
def findListeEHPAD():
    # Import de tous les FINESS
    print('Import de tous les FINESS depuis le fichier finess_etablissements de data.gouv')
    liste_ehpad_df = pd.read_csv(
        'finess_etablissements.csv',
        sep=';',
        usecols=[
            'Numéro FINESS ET ',
            'Numéro FINESS EJ ',
            'Catégorie d\x92établissement '],
        encoding='Latin-1'
        )
        # Filtre sur la catégorie d'établissement == EHPAD | EHPA
    print('Filtre sur les EHPAD : 500 et 501')
    # liste_ehpad_df = liste_ehpad_df[(liste_ehpad_df['Catégorie d\x92établissement '] == 500) | (liste_ehpad_df['Catégorie d\x92établissement '] == 501) | (liste_ehpad_df['Catégorie d\x92établissement '] == 502)] # ancien filtre avec EHPA
    liste_ehpad_df = liste_ehpad_df[(liste_ehpad_df['Catégorie d\x92établissement '] == 500) | (liste_ehpad_df['Catégorie d\x92établissement '] == 501)] # nouveau filtre avec seulement 500 et 501 à confirmer
    del liste_ehpad_df['Catégorie d\x92établissement ']
    del liste_ehpad_df['Numéro FINESS EJ ']
        # Renommage
    liste_ehpad_df.rename(columns={'Numéro FINESS ET ': 'FINESS_ET'}, 
                            inplace = True)
        # Converti les FINESS en str
    liste_ehpad_df['FINESS_ET'] = liste_ehpad_df['FINESS_ET'].astype(str)
        # Ajout du 0 quand longueur finess < 9
    liste_ehpad_df['FINESS_ET'] = liste_ehpad_df['FINESS_ET'].apply(lambda x: '0' + str(x) if len(x) == 8 else str(x))
    return liste_ehpad_df

# Récupération des données d'identification
def findIdentificationData():
    # Import des EHPAD
    liste_ehpad_df = findListeEHPAD()
    # print(liste_ehpad_df)
    # Import du finess_etablissement
    print('Import des données d identification depuis le fichier finess_etablissements de data.gouv')
    finess_etab_df = pd.read_csv(
        'finess_etablissements.csv',
        sep=';',
        usecols=[
            'Numéro FINESS ET ',
            'Numéro FINESS EJ ',
            'Raison sociale ',
            'Numéro de voie ', 
            'Type de voie ', 
            'Libellé de voie ', 
            'Complément de voie ', 
            'Lieu-dit / BP ', 
            'Code Commune ', 
            'Département ', 
            'Libellé département ',
            'Ligne d\x92acheminement (CodePostal+Lib commune) ',
            'Catégorie d\x92établissement ',
            'Libelle catégorie d\x92établissement ',
            'Code MFT ', 
            'Libelle MFT ', 
            'Code SPH ', 
            'Libelle SPH '],
        encoding='Latin-1'
        )
        # Renommage des colonnes
    finess_etab_df.rename(columns={'Numéro FINESS ET ': 'FINESS_ET',
                                   'Numéro FINESS EJ ': 'FINESS_EJ',
                                   'Raison sociale ': 'RAISON_SOCIALE',
                                   'Numéro de voie ': 'NUMERO_VOIE', 
                                   'Type de voie ': 'TYPE_VOIE', 
                                   'Libellé de voie ': 'LB_VOIE', 
                                   'Complément de voie ': 'COMPL_VOIE', 
                                   'Lieu-dit / BP ': 'LIEU_DIT_BP', 
                                   'Code Commune ': 'CD_TYPE_COMMUNE', 
                                   'Département ': 'CD_DEPARTEMENT', 
                                   'Libellé département ': 'DEPARTEMENT',
                                   'Ligne d\x92acheminement (CodePostal+Lib commune) ': 'CD_POSTAL_LB_COMMUNE',
                                   'Catégorie d\x92établissement ': 'CD_CATEGORIE_ETABLISSEMENT',
                                   'Libelle catégorie d\x92établissement ': 'CATEGORIE_ETABLISSEMENT',
                                   'Code MFT ': 'CD_ORGANISME_GESTIONNAIRE', 
                                   'Libelle MFT ': 'ORGANISME_GESTIONNAIRE', 
                                   'Code SPH ': 'CD_STATUT_JURIDIQUE', 
                                   'Libelle SPH ': 'STATUT_JURIDIQUE'}, 
                         inplace = True)
        # Conversion des codes en str pour les futurs croisements
    finess_etab_df['FINESS_ET'] = finess_etab_df['FINESS_ET'].astype(str)
    finess_etab_df['FINESS_EJ'] = finess_etab_df['FINESS_EJ'].astype(str)
    finess_etab_df['NUMERO_VOIE'] = finess_etab_df['NUMERO_VOIE'].replace(np.nan, ' ')
    finess_etab_df['NUMERO_VOIE'] = finess_etab_df['NUMERO_VOIE'].astype(str)
    finess_etab_df['NUMERO_VOIE'] = finess_etab_df['NUMERO_VOIE'].str.split('.').str[0]
    finess_etab_df['CD_TYPE_COMMUNE'] = finess_etab_df['CD_TYPE_COMMUNE'].astype(str)
    finess_etab_df['CD_DEPARTEMENT'] = finess_etab_df['CD_DEPARTEMENT'].astype(str)
        # Concaténation de l'adresse
    finess_etab_df['TYPE_VOIE'] = np.where(
        isNaN(finess_etab_df['TYPE_VOIE']),
        ' ',
        finess_etab_df['TYPE_VOIE'])
    finess_etab_df['LB_VOIE'] = np.where(
        isNaN(finess_etab_df['LB_VOIE']),
        ' ',
        finess_etab_df['LB_VOIE'])
    finess_etab_df['COMPL_VOIE'] = np.where(
        isNaN(finess_etab_df['COMPL_VOIE']),
        ' ',
        finess_etab_df['COMPL_VOIE'])
    finess_etab_df['LIEU_DIT_BP'] = np.where(
        isNaN(finess_etab_df['LIEU_DIT_BP']),
        ' ',
        finess_etab_df['LIEU_DIT_BP'])
    finess_etab_df['CD_POSTAL_LB_COMMUNE'] = np.where(
        isNaN(finess_etab_df['CD_POSTAL_LB_COMMUNE']),
        ' ',
        finess_etab_df['CD_POSTAL_LB_COMMUNE'])
    # finess_etab_df['ADRESSE'] = finess_etab_df['NUMERO_VOIE'].astype(str) +" "+ finess_etab_df['TYPE_VOIE'] +" "+ finess_etab_df['LB_VOIE'] +" "+ finess_etab_df['COMPL_VOIE'] +" "+ finess_etab_df['LIEU_DIT_BP'] +" "+ finess_etab_df['CD_POSTAL_LB_COMMUNE']
    finess_etab_df['ADRESSE'] = finess_etab_df['NUMERO_VOIE'] + ' ' + finess_etab_df['TYPE_VOIE'] + ' ' + finess_etab_df['LB_VOIE'] + ' ' + finess_etab_df['COMPL_VOIE'] + ' ' + finess_etab_df['LIEU_DIT_BP'] + ' ' + finess_etab_df['CD_POSTAL_LB_COMMUNE']
        # Ajout du 0 quand longueur finess < 9
    finess_etab_df['FINESS_ET'] = finess_etab_df['FINESS_ET'].apply(lambda x: '0' + str(x) if len(x) == 8 else str(x))
        # Normalisation des codes département - à réécrire avec une boucle si 1 car etc
    finess_etab_df['CD_DEPARTEMENT'] = finess_etab_df['CD_DEPARTEMENT'].replace(['1'],'01')
    finess_etab_df['CD_DEPARTEMENT'] = finess_etab_df['CD_DEPARTEMENT'].replace(['2'],'02')
    finess_etab_df['CD_DEPARTEMENT'] = finess_etab_df['CD_DEPARTEMENT'].replace(['3'],'03')
    finess_etab_df['CD_DEPARTEMENT'] = finess_etab_df['CD_DEPARTEMENT'].replace(['4'],'04')
    finess_etab_df['CD_DEPARTEMENT'] = finess_etab_df['CD_DEPARTEMENT'].replace(['5'],'05')
    finess_etab_df['CD_DEPARTEMENT'] = finess_etab_df['CD_DEPARTEMENT'].replace(['6'],'06')
    finess_etab_df['CD_DEPARTEMENT'] = finess_etab_df['CD_DEPARTEMENT'].replace(['7'],'07')
    finess_etab_df['CD_DEPARTEMENT'] = finess_etab_df['CD_DEPARTEMENT'].replace(['8'],'08')
    finess_etab_df['CD_DEPARTEMENT'] = finess_etab_df['CD_DEPARTEMENT'].replace(['9'],'09')
    finess_etab_df['CD_DEPARTEMENT'] = finess_etab_df['CD_DEPARTEMENT'].replace(['9A'],'971')
    finess_etab_df['CD_DEPARTEMENT'] = finess_etab_df['CD_DEPARTEMENT'].replace(['9B'],'972')
    finess_etab_df['CD_DEPARTEMENT'] = finess_etab_df['CD_DEPARTEMENT'].replace(['9C'],'973')
    finess_etab_df['CD_DEPARTEMENT'] = finess_etab_df['CD_DEPARTEMENT'].replace(['9D'],'974')
        # Split de la colonne Ligne d’acheminement (CodePostal+Lib commune) pour avoir le CD_POSTAL et le LB_COMMUNE
    finess_etab_df['CD_POSTAL'] = finess_etab_df['CD_POSTAL_LB_COMMUNE'].str[:5]
    finess_etab_df['COMMUNE'] = finess_etab_df['CD_POSTAL_LB_COMMUNE'].str[6:]
    # print(finess_etab_df)
    # Changement de l'ordre des colonnes
    finess_etab_df = finess_etab_df[['CD_DEPARTEMENT', 
                                    'DEPARTEMENT',
                                    'FINESS_ET', 
                                    'CATEGORIE_ETABLISSEMENT',
                                    'RAISON_SOCIALE', 
                                    'FINESS_EJ', 
                                    'ADRESSE', 
                                    'CD_POSTAL', 
                                    'COMMUNE']]
    # Import des codes communes et TVS
    print('Import des données d identification depuis le fichier t_finess de data.gouv')
        # code commune et principal / secondaire
    t_finess_df = pd.read_csv(
        't-finess.csv',
        sep=',',
        usecols=[
            'finess',
            'com_code',
            'ej_finess',
            'et_finess',
            'ej_rs',
            'statut_jur_lib'
        ],
        encoding='Latin-1'
    )
            # Renommage des colonnes
    t_finess_df.rename(columns={
                                'finess': 'FINESS_ET',
                                'com_code': 'CD_COMMUNE',
                                'ej_rs': 'ORGANISME_GESTIONNAIRE',
                                'statut_jur_lib': 'STATUT_JURIDIQUE'}, 
                            inplace = True)
            # Converti le FINESS en str
    t_finess_df['FINESS_ET'] = t_finess_df['FINESS_ET'].astype(str)
    t_finess_df['CD_COMMUNE'] = t_finess_df['CD_COMMUNE'].astype(str)
    t_finess_df['ej_finess'] = t_finess_df['ej_finess'].astype(str)
    t_finess_df['et_finess'] = t_finess_df['et_finess'].astype(str)
            # Ajout du 0 quand longueur finess < 9
    t_finess_df['FINESS_ET'] = t_finess_df['FINESS_ET'].apply(lambda x: '0' + str(x) if len(x) == 8 else str(x))
    t_finess_df['ej_finess'] = t_finess_df['ej_finess'].apply(lambda x: '0' + str(x) if len(x) == 8 else str(x))
    t_finess_df['et_finess'] = t_finess_df['et_finess'].apply(lambda x: '0' + str(x) if len(x) == 8 else str(x))
            # Calcul de principal / secondaire 
    t_finess_df['EST_PRINCIPAL_OU_SECONDAIRE'] = np.where(t_finess_df['ej_finess'] == t_finess_df['FINESS_ET'],
                                                            'principal',
                                                            'secondaire')
    t_finess_df['SI_SECONDAIRE_FINESS_ET_SITE_PRINCIPAL'] = np.where(t_finess_df['ej_finess'] == t_finess_df['FINESS_ET'],
                                                            '',
                                                            t_finess_df['ej_finess'])                                                            
    # print(t_finess_df)
        # TVS
    print('Import des données TVS depuis le fichier t-geo-com de data.gouv')
    t_geo_com_df = pd.read_csv(
        't-geo-com.csv',
        sep=',',
        usecols=[
            'COM_CODE',
            'TDS16_V2021_CODE',
            'TDS16_V2021_LIB'
        ],
        encoding='Latin-1'
    )
            # Renommage des colonnes
    t_geo_com_df.rename(columns={'COM_CODE': 'CD_COMMUNE',
                                    'TDS16_V2021_CODE': 'CD_TDS',
                                    'TDS16_V2021_LIB': 'TDS'}, 
                            inplace = True)
            # Converti le FINESS en str
    t_geo_com_df['CD_COMMUNE'] = t_geo_com_df['CD_COMMUNE'].astype(str)
    t_geo_com_df['CD_TDS'] = t_geo_com_df['CD_TDS'].astype(str)
    # print(t_geo_com_df)
        # Croisement code commune et TVS
    geo_df = t_finess_df.merge(t_geo_com_df,
                                     how = 'left')
    # print(geo_df)
    # Import des référentiels INSEE
    print('Import des données départements depuis le fichier departement2020 de l INSEE')
        # dépaqrtement
    departement_df = pd.read_csv(
        'departement2020.csv',
        sep=',',
        usecols=[
            'dep',
            'reg'
        ],
        encoding='Latin-1'
    )
            # Renommage des colonnes
    departement_df.rename(columns={'dep': 'CD_DEPARTEMENT'}, 
                            inplace = True)
            # Converti le FINESS en str
    departement_df['CD_DEPARTEMENT'] = departement_df['CD_DEPARTEMENT'].astype(str)
    departement_df['reg'] = departement_df['reg'].astype(str)
    # print(departement_df)
        # régions
    region_df = pd.read_csv(
        'region2020.csv',
        sep=',',
        usecols=[
            'reg',
            'ncc'
        ],
        encoding='Latin-1'
    )
            # Renommage des colonnes
    region_df.rename(columns={'ncc': 'REGION'}, 
                            inplace = True)
            # Converti le FINESS en str
    region_df['reg'] = region_df['reg'].astype(str)
    # print(region_df)
    # Croisement référentiel département et région
    referentiel_df = departement_df.merge(region_df,
                                     how = 'left')
    # print(referentiel_df)
    # Croisement pre identification
    preidentification_df = liste_ehpad_df.merge(finess_etab_df,
                                                how = 'left').merge(geo_df,
                                                                    how = 'left')
    preidentification_df['CD_DEPARTEMENT'] = preidentification_df['CD_DEPARTEMENT'].astype(str)                             
    # print(preidentification_df)
    # Croisement pre identification et référentiel
    identification_df = preidentification_df.merge(referentiel_df,
                                     how = 'left')
    identification_df['CD_DEPARTEMENT'] = identification_df['CD_DEPARTEMENT'].astype(str)
        # Renommage des colonnes
    identification_df.rename(columns={'reg': 'CD_REGION'}, 
                            inplace = True)
        # Ajout de colonnes vides
    identification_df['TERRITOIRE_PROXIMITE'] = ''
        # Changement de l'ordre des colonnes
    identification_df = identification_df[['CD_REGION',
                                    'REGION',
                                    'CD_DEPARTEMENT', 
                                    'DEPARTEMENT',
                                    'FINESS_ET', 
                                    'CATEGORIE_ETABLISSEMENT',
                                    'RAISON_SOCIALE', 
                                    'EST_PRINCIPAL_OU_SECONDAIRE',
                                    'SI_SECONDAIRE_FINESS_ET_SITE_PRINCIPAL',
                                    'FINESS_EJ', 
                                    'ORGANISME_GESTIONNAIRE', 
                                    'STATUT_JURIDIQUE', 
                                    'ADRESSE', 
                                    'CD_POSTAL',
                                    'CD_COMMUNE',
                                    'COMMUNE',
                                    'TDS',
                                    'TERRITOIRE_PROXIMITE']]
    # print(identification_df)
    return identification_df
# findIdentificationData()

# Récupération des données de capacité
def findCapaciteData():
    # Import des EHPAD
    liste_ehpad_df = findListeEHPAD()
    # print(liste_ehpad_df)
    # Import lits autorisés installés moyenne 2021
    print('Import des données lits autorisés installés moyenne 2021')
    lits_df = pd.read_csv(
        'occupation_2021.csv',
        sep=';',
        usecols=[
            'FINESS',
            'NB_LITS_AUTORISES_INSTALLES'
        ],
        encoding='Latin-1'
    )
        # Renommage des colonnes
    lits_df.rename(columns={'FINESS': 'FINESS_ET',
                            'NB_LITS_AUTORISES_INSTALLES':'CAPACITE_TOTALE_AUTO_NB_LITS_AUTORISES_INSTALLES_2021'}, 
                            inplace = True)
        # Converti le FINESS en str
    lits_df['FINESS_ET'] = lits_df['FINESS_ET'].astype(str)
    # print(lits_df)
    # Import des capacités installées ERRD 2020 
    print('Import des données capacités installées ERRD 2020')
    capacites_errd_df = pd.read_csv(
        'capacites_errd_2020.csv',
        sep=';',
        usecols=[
            'FINESS',
            'Capacité HP',
            'Capacité HT',
            'Capacité AJ'
        ],
        encoding='Latin-1'
    )
        # Renommage des colonnes
    capacites_errd_df.rename(columns={'Capacité HP': 'HP_ERRD_2020',
                                    'Capacité HT': 'HT_ERRD_2020',
                                    'Capacité AJ': 'AJ_ERRD_2020'}, 
                            inplace = True)
        # Extraction du numéro FINESS
    capacites_errd_df['FINESS_ET'] = capacites_errd_df['FINESS'].str[:9]
    del capacites_errd_df['FINESS']
        # Converti le FINESS en str
    capacites_errd_df['FINESS_ET'] = capacites_errd_df['FINESS_ET'].astype(str)
        # Ajout du 0 quand longueur finess < 9
    capacites_errd_df['FINESS_ET'] = capacites_errd_df['FINESS_ET'].apply(lambda x: '0' + str(x) if len(x) == 8 else str(x))
        # Changement de l'ordre des colonnes
    capacites_errd_df = capacites_errd_df[['FINESS_ET', 'HP_ERRD_2020', 'AJ_ERRD_2020', 'HT_ERRD_2020',]]
    # print(capacites_errd_df)
    # Croisement 
    # capacite_df = pd.merge(pd.merge(pd.merge(liste_ehpad_df,places_df, on='FINESS_ET'), lits_df, on='FINESS_ET'),capacites_errd_df, on='FINESS_ET')
    capacite_df = liste_ehpad_df.merge(lits_df,
                                     how = 'left').merge(capacites_errd_df,
                                                       how = 'left')
    # print(capacite_df)
    return capacite_df
# findCapaciteData()

# Récupération des données d'occupation
def findOccupationData():
    # Import des EHPAD
    liste_ehpad_df = findListeEHPAD()
    # print(liste_ehpad_df)
    # Import des données occupation 2019 et 2020
    print('Import des données occupation 2019 et 2020')
    occupation_2021_df = pd.read_csv(
        'occupation_2021.csv',
        sep=';',
        usecols=[
            'FINESS',
            'TAUX_OCC_2021'
        ],
        encoding='Latin-1'
    )
        # Renommage des colonnes
    occupation_2021_df.rename(columns={'FINESS': 'FINESS_ET'}, 
                            inplace = True)
        # Converti le FINESS en str
    occupation_2021_df['FINESS_ET'] = occupation_2021_df['FINESS_ET'].astype(str)
    # print(occupation_2021_df)
    # Import des données occupation 2021
    print('Import des données occupation 2021')
    occupation_2019_2020_df = pd.read_csv(
        'occupation_2019_2020.csv',
        sep=';',
        usecols=[
            'FINESS_19',
            'TAUX_OCC_2019',
            'TAUX_OCC_2020'
        ],
        encoding='Latin-1'
    )
        # Renommage des colonnes
    occupation_2019_2020_df.rename(columns={'FINESS_19': 'FINESS_ET'}, 
                            inplace = True)
        # Converti le FINESS en str
    occupation_2019_2020_df['FINESS_ET'] = occupation_2019_2020_df['FINESS_ET'].astype(str)
        # Ajout du 0 quand longueur finess < 9
    occupation_2019_2020_df['FINESS_ET'] = occupation_2019_2020_df['FINESS_ET'].apply(lambda x: '0' + str(x) if len(x) == 8 else str(x))
    # print(occupation_2019_2020_df)
    # Croisement
    occupation_df = liste_ehpad_df.merge(occupation_2021_df,
                                        how = 'left').merge(occupation_2019_2020_df,
                                                            how = 'left')
        # Changement de l'ordre des colonnes
    occupation_df = occupation_df[['FINESS_ET', 'TAUX_OCC_2019', 'TAUX_OCC_2020', 'TAUX_OCC_2021']]
    # print(occupation_df)
    return occupation_df
# findOccupationData()

# Récupération des données SNDS
def findOccupation31122021Data():
    # Import des EHPAD
    liste_ehpad_df = findListeEHPAD()
    # print(liste_ehpad_df)
    # Import nombre de résidents 
    print('Import des données nombre de résidents')
    residents_df = pd.read_csv(
        'nb_residents_ehpad.csv',
        sep=';',
        usecols=[
            'IDE_ETA_NUM',
            'nb_resid'
        ],
        encoding='Latin-1'
    )
        # Renommage des colonnes
    residents_df.rename(columns={'IDE_ETA_NUM': 'FINESS_ET',
                                    'nb_resid': 'SNDS_NB_RESIDENTS_31122021'}, 
                            inplace = True)
        # Converti le FINESS en str
    residents_df['FINESS_ET'] = residents_df['FINESS_ET'].astype(str)
    # print(residents_df)
    # Import nombre de places 
    print('Import des données nombre de places')
    places_df = pd.read_csv(
        'nb_places_ehpad.csv',
        sep=';',
        usecols=[
            'FINESS ET',
            'Places installées au 31/12/2021'
        ],
        encoding='Latin-1'
    )
        # Renommage des colonnes
    places_df.rename(columns={'FINESS ET': 'FINESS_ET',
                                    'Places installées au 31/12/2021': 'NB_PLACES_INSTALLEES_31122021'}, 
                            inplace = True)
        # Converti le FINESS en str
    places_df['FINESS_ET'] = places_df['FINESS_ET'].astype(str)
        # Ajout du 0 quand longueur finess < 9
    places_df['FINESS_ET'] = places_df['FINESS_ET'].apply(lambda x: '0' + str(x) if len(x) == 8 else str(x))
    # print(places_df)
    # Croisement
    occupation31122021_df = liste_ehpad_df.merge(residents_df,
                                     how = 'left').merge(places_df,
                                                       how = 'left')
    # Calcul du taux d'occupation au 31/12/2021
    occupation31122021_df['TAUX_OCCUPATION_31122021'] = (
        occupation31122021_df['SNDS_NB_RESIDENTS_31122021'] / occupation31122021_df['NB_PLACES_INSTALLEES_31122021']
        ) * 100
    del occupation31122021_df['NB_PLACES_INSTALLEES_31122021']
    # print(occupation31122021_df)
    return occupation31122021_df
# findOccupation31122021Data()

# # Récuparation des données profils
# # Version source diamant 2019
# def findProfilData():
#     # Import des EHPAD
#     liste_ehpad_df = findListeEHPAD()
#     # print(liste_ehpad_df)
#     # Import des données data.gouv
#     prix_df = pd.read_csv(
#         'prix_ehpad_2021.csv',
#         sep=';',
#         usecols=[
#             'finessEt',
#             'prixHebPermCs'
#         ],
#         encoding='Latin-1'
#     )
#         # Renommage des colonnes
#     prix_df.rename(columns={'finessEt': 'FINESS_ET',
#                                     'prixHebPermCs': 'PRIX_HEB_PERM_CS'}, 
#                             inplace = True)
#         # Converti le FINESS en str
#     prix_df['FINESS_ET'] = prix_df['FINESS_ET'].astype(str)
#         # Ajout du 0 quand longueur finess < 9
#     prix_df['FINESS_ET'] = prix_df['FINESS_ET'].apply(lambda x: '0' + str(x) if len(x) == 8 else str(x))
#     # print(prix_df)
#     # Import des données tdb budgétaire et gir de diamant
#     diamant_df = pd.read_csv(
#         'diamant_2019.csv',
#         sep=';',
#         usecols=[
#             'FINESS',
#             'Répartition en fonction des GIR en \x25 \x3A personnes GIR 1',
#             'Répartition en fonction des GIR en \x25 \x3A personnes GIR 2',
#             'Répartition en fonction des GIR en \x25 \x3A personnes GIR 3',
#             'GMP \x28correspondant au dernier GMP validé\x29',
#             'PMP \x28correspondant au dernier PMP validé\x29'
#         ],
#         encoding='Latin-1'
#     )
#         # Renommage des colonnes
#     diamant_df.rename(columns={'Répartition en fonction des GIR en % : personnes GIR 1': 'GIR1',
#                                 'Répartition en fonction des GIR en % : personnes GIR 2': 'GIR2',
#                                 'Répartition en fonction des GIR en % : personnes GIR 3': 'GIR3',
#                                 'GMP (correspondant au dernier GMP validé)': 'GMP',
#                                 'PMP (correspondant au dernier PMP validé)': 'PMP'}, 
#                             inplace = True)
#         # Extraction du numéro FINESS
#     diamant_df['FINESS_ET'] = diamant_df['FINESS'].str[:9]
#     del diamant_df['FINESS']
#         # Converti le FINESS en str
#     diamant_df['FINESS_ET'] = diamant_df['FINESS_ET'].astype(str)
#         # Ajout du 0 quand longueur finess < 9
#     diamant_df['FINESS_ET'] = diamant_df['FINESS_ET'].apply(lambda x: '0' + str(x) if len(x) == 8 else str(x))
#         # Modification de l'ordre des colonnes
#     diamant_df = diamant_df[['FINESS_ET', 'GIR1', 'GIR2', 'GIR3', 'GMP', 'PMP']]
#     # print(diamant_df)
#     # Croisement
#     profil_df = liste_ehpad_df.merge(prix_df,
#                                      how = 'left').merge(diamant_df,
#                                                        how = 'left')
#         # Modification de l'ordre des colonnes
#     profil_df = profil_df[['FINESS_ET', 'PRIX_HEB_PERM_CS', 'GMP', 'PMP', 'GIR1', 'GIR2', 'GIR3']]
#     # print(profil_df)
#     return profil_df
# # findProfilData()

# # Agrégation des export-tdbesms-2020-region
# def aggTdbANAP2020():
#     files = ['export-tdbesms-2020-region-*']
#     for eachFile in files:

#     return
# aggTdbANAP2020()

# Récuparation des données profils
# Version source export-tdbesms-2020-region
def findProfilData():
    # Import des EHPAD
    liste_ehpad_df = findListeEHPAD()
    # print(liste_ehpad_df)
    # Import des données data.gouv
    print('Import des données prix des EHPAD de data.gouv')
    prix_df = pd.read_csv(
        'prix_ehpad_2021.csv',
        sep=';',
        usecols=[
            'finessEt',
            'prixHebPermCs'
        ],
        encoding='Latin-1'
    )
        # Renommage des colonnes
    prix_df.rename(columns={'finessEt': 'FINESS_ET',
                                    'prixHebPermCs': 'PRIX_HEB_PERM_CS'}, 
                            inplace = True)
        # Converti le FINESS en str
    prix_df['FINESS_ET'] = prix_df['FINESS_ET'].astype(str)
        # Ajout du 0 quand longueur finess < 9
    prix_df['FINESS_ET'] = prix_df['FINESS_ET'].apply(lambda x: '0' + str(x) if len(x) == 8 else str(x))
    # print(prix_df)
    # Import des données tdb budgétaire et gir de diamant
    print('Import des données tdb budgétaire et gir de diamant')
    tdb_anap_df_1 = pd.read_csv(
        'export-tdbesms-2020-region_agrege.csv',
        sep=';',
        usecols=[
            'finess géographique',
            'Répartition en fonction des GIR en \x25 \x3A personnes GIR 1',
            'Répartition en fonction des GIR en \x25 \x3A personnes GIR 2',
            'Répartition en fonction des GIR en \x25 \x3A personnes GIR 3',
            'GMP \x28correspondant au dernier GMP validé\x29',
            'PMP \x28correspondant au dernier PMP validé\x29'
        ],
        encoding='Latin-1'
    )
        # Renommage des colonnes
    tdb_anap_df_1.rename(columns={'finess géographique': 'FINESS_ET',
                                'Répartition en fonction des GIR en % : personnes GIR 1': 'GIR1',
                                'Répartition en fonction des GIR en % : personnes GIR 2': 'GIR2',
                                'Répartition en fonction des GIR en % : personnes GIR 3': 'GIR3',
                                'GMP (correspondant au dernier GMP validé)': 'GMP',
                                'PMP (correspondant au dernier PMP validé)': 'PMP'}, 
                            inplace = True)
        # Converti le FINESS en str
    tdb_anap_df_1['FINESS_ET'] = tdb_anap_df_1['FINESS_ET'].astype(str)
        # Ajout du 0 quand longueur finess < 9
    tdb_anap_df_1['FINESS_ET'] = tdb_anap_df_1['FINESS_ET'].apply(lambda x: '0' + str(x) if len(x) == 8 else str(x))
        # Modification de l'ordre des colonnes
    tdb_anap_df_1 = tdb_anap_df_1[['FINESS_ET', 'GIR1', 'GIR2', 'GIR3', 'GMP', 'PMP']]
    # print(diamant_df)
    # Croisement
    profil_df = liste_ehpad_df.merge(prix_df,
                                     how = 'left').merge(tdb_anap_df_1,
                                                       how = 'left')
        # Modification de l'ordre des colonnes
    profil_df = profil_df[['FINESS_ET', 'PRIX_HEB_PERM_CS', 'GMP', 'PMP', 'GIR1', 'GIR2', 'GIR3']]
    # print(profil_df)
    return profil_df
# findProfilData()

# Récupération des données tdb ANAP
def findPerformanceData():
    # Import des EHPAD
    liste_ehpad_df = findListeEHPAD()
    # print(liste_ehpad_df)
    # Import des données DIAMANT issues des TdB de la Performance ANAP - 2018
    print('Import des données DIAMANT issues des TdB de la Performance ANAP - 2018')
    anap_2018_df = pd.read_csv(
        'diamant_2018.csv',
        sep=';',
        usecols=[
            'FINESS',
            'Nombre total de personnes accompagnées sur l\x27année',
            'Taux d\x27ETP vacants en %',
            'Taux d\x27absentéisme (hors formation) en %',
            'Taux de rotation des personnels en %',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Direction/Encadrement',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Administration / Gestion',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Services généraux',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Restauration',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Socio\x2Déducatif',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Paramédical',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 de psychologue',
            'Répartition du personnel par fonction \x2D Nombre d\x92ETP réels au 31\x2E12 d\x92ASH',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Médical',
            'Répartition du personnel par fonction \x2D Nombre d\x92ETP réels au 31\x2E12 de personnel Education nationale',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Autres fonctions'
        ],
        encoding='Latin-1'
    )
        # Extraction du numéro FINESS
    anap_2018_df['FINESS_ET'] = anap_2018_df['FINESS'].str[:9]
    del anap_2018_df['FINESS']
        # Renommage des colonnes
    anap_2018_df.rename(columns={anap_2018_df.columns[0]: 'nombre d usagers',
                                anap_2018_df.columns[2]: 'Taux d absentéisme 2018',
                                anap_2018_df.columns[3]: 'Taux de rotation du personnel titulaire 2018',
                                anap_2018_df.columns[1]: 'ETP vacants 2018'}, 
                            inplace = True)
        # Converti le FINESS en str
    anap_2018_df['FINESS_ET'] = anap_2018_df['FINESS_ET'].astype(str)
        # Ajout du 0 quand longueur finess < 9
    anap_2018_df['FINESS_ET'] = anap_2018_df['FINESS_ET'].apply(lambda x: '0' + str(x) if len(x) == 8 else str(x))
        # Suppression des 0 dans nombre d'usagers
    anap_2018_df['nombre d usagers'] = anap_2018_df['nombre d usagers'].replace(0, np.nan)
        # Calcul du nombre d'ETP
    anap_2018_df['Total du nombre d\x92ETP'] = anap_2018_df['Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Direction/Encadrement'] + anap_2018_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Administration / Gestion'] + anap_2018_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Services généraux'] + anap_2018_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Restauration'] + anap_2018_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Socio-éducatif'] + anap_2018_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Paramédical'] + anap_2018_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 de psychologue'] + anap_2018_df['Répartition du personnel par fonction - Nombre d\x92ETP réels au 31.12 d\x92ASH'] + anap_2018_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Médical'] + anap_2018_df['Répartition du personnel par fonction - Nombre d\x92ETP réels au 31.12 de personnel Education nationale'] + anap_2018_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Autres fonctions']
    del anap_2018_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Direction/Encadrement'] 
    del anap_2018_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Administration / Gestion'] 
    del anap_2018_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Services généraux'] 
    del anap_2018_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Restauration']
    del anap_2018_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Socio-éducatif'] 
    del anap_2018_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Paramédical'] 
    del anap_2018_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 de psychologue'] 
    del anap_2018_df['Répartition du personnel par fonction - Nombre d\x92ETP réels au 31.12 d\x92ASH'] 
    del anap_2018_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Médical'] 
    del anap_2018_df['Répartition du personnel par fonction - Nombre d\x92ETP réels au 31.12 de personnel Education nationale'] 
    del anap_2018_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Autres fonctions']
        # Calcul du Nombre total d'ETP par usager en 2018
    anap_2018_df['Nombre d\x92ETP par usager en 2018'] = (
        anap_2018_df['Total du nombre d\x92ETP'] / anap_2018_df['nombre d usagers']
        ) * 100
    del anap_2018_df['Total du nombre d\x92ETP']
    del anap_2018_df['nombre d usagers']
        # Modification de l'ordre des colonnes
    anap_2018_df = anap_2018_df[['FINESS_ET', 'Taux d absentéisme 2018', 'Taux de rotation du personnel titulaire 2018', 'ETP vacants 2018', 'Nombre d\x92ETP par usager en 2018']]
    # print(anap_2018_df)
    # Import des données DIAMANT issues des TdB de la Performance ANAP - 2019
    print('Import des données DIAMANT issues des TdB de la Performance ANAP - 2019')
    anap_2019_df = pd.read_csv(
        'diamant_2019.csv',
        sep=';',
        usecols=[
            'FINESS',
            'Nombre total de personnes accompagnées sur l\x27année',
            'Taux d\x27ETP vacants en %',
            'Taux d\x27absentéisme (hors formation) en %',
            'Taux de rotation des personnels en %',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Direction/Encadrement',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Administration / Gestion',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Services généraux',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Restauration',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Socio\x2Déducatif',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Paramédical',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 de psychologue',
            'Répartition du personnel par fonction \x2D Nombre d\x92ETP réels au 31.12 d\x92ASH',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Médical',
            'Répartition du personnel par fonction \x2D Nombre d\x92ETP réels au 31\x2E12 de personnel Education nationale',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Autres fonctions'
        ],
        decimal=",",
        encoding='Latin-1'
    )
        # Extraction du numéro FINESS
    anap_2019_df['FINESS_ET'] = anap_2019_df['FINESS'].str[:9]
    del anap_2019_df['FINESS']
        # Renommage des colonnes
    anap_2019_df.rename(columns={anap_2019_df.columns[0]: 'nombre d usagers',
                                anap_2019_df.columns[2]: 'Taux d absentéisme 2019',
                                anap_2019_df.columns[3]: 'Taux de rotation du personnel titulaire 2019',
                                anap_2019_df.columns[1]: 'ETP vacants 2019'},
                            inplace = True)
        # Converti le FINESS en str
    anap_2019_df['FINESS_ET'] = anap_2019_df['FINESS_ET'].astype(str)
        # Ajout du 0 quand longueur finess < 9
    anap_2019_df['FINESS_ET'] = anap_2019_df['FINESS_ET'].apply(lambda x: '0' + str(x) if len(x) == 8 else str(x))
        # Calcul du nombre d'ETP
    anap_2019_df['Total du nombre d\x92ETP'] = anap_2019_df['Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Direction/Encadrement'] + anap_2019_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Administration / Gestion'] + anap_2019_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Services généraux'] + anap_2019_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Restauration'] + anap_2019_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Socio-éducatif'] + anap_2019_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Paramédical'] + anap_2019_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 de psychologue'] + anap_2019_df['Répartition du personnel par fonction - Nombre d\x92ETP réels au 31.12 d\x92ASH'] + anap_2019_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Médical'] + anap_2019_df['Répartition du personnel par fonction - Nombre d\x92ETP réels au 31.12 de personnel Education nationale'] + anap_2019_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Autres fonctions']
        # Suppression des 0 dans nombre d'usagers
    anap_2019_df['nombre d usagers'] = anap_2019_df['nombre d usagers'].replace(0, np.nan)
        # Calcul du Nombre total d'ETP par usager en 2019
    anap_2019_df['Nombre d\x92ETP par usager en 2019'] = (
        anap_2019_df['Total du nombre d\x92ETP'] / anap_2019_df['nombre d usagers']
        ) * 100
    del anap_2019_df['Total du nombre d\x92ETP']
    del anap_2019_df['nombre d usagers']
    del anap_2019_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Direction/Encadrement'] 
    del anap_2019_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Administration / Gestion'] 
    del anap_2019_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Services généraux'] 
    del anap_2019_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Restauration']
    del anap_2019_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Socio-éducatif'] 
    del anap_2019_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Paramédical'] 
    del anap_2019_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 de psychologue'] 
    del anap_2019_df['Répartition du personnel par fonction - Nombre d\x92ETP réels au 31.12 d\x92ASH'] 
    del anap_2019_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Médical'] 
    del anap_2019_df['Répartition du personnel par fonction - Nombre d\x92ETP réels au 31.12 de personnel Education nationale'] 
    del anap_2019_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Autres fonctions']
     # Modification de l'ordre des colonnes
    anap_2019_df = anap_2019_df[['FINESS_ET', 'Taux d absentéisme 2019', 'Taux de rotation du personnel titulaire 2019', 'ETP vacants 2019', 'Nombre d\x92ETP par usager en 2019']]
    # print(anap_2019_df)
    # Import des données ATIH issues des TdB de la Performance ANAP - 2020
    print('Import des données DIAMANT issues des TdB de la Performance ANAP - 2020')
    anap_2020_df = pd.read_csv(
        'export-tdbesms-2020-region_agrege.csv',
        sep=';',
        usecols=[
            'finess géographique',
            'Nombre total de personnes accompagnées sur l\x27année',
            'Taux d\x27ETP vacants en %',
            'Dont taux d\x27ETP vacants concernant la fonction SOINS',
            'Dont taux d\x27ETP vacants concernant la fonction SOCIO EDUCATIVE',
            'Taux d\x27absentéisme (hors formation) en %',
            'Taux de rotation des personnels en %',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Direction/Encadrement',
            'Dont nombre d\x27ETP réels de personnel médical d\x27encadrement',
            'Dont Autre Direction/Encadrement',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Administration / Gestion',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Services généraux',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Restauration',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Socio\x2Déducatif',
            'Dont nombre d\x27ETP réels d\x27aide médico\x2Dpsychologique',
            'Dont nombre d\x27ETP réels d\x27animateur',
            'Dont nombre d\x27ETP réels de moniteur éducateur au 31.12',
            'Dont nombre d\x92ETP réels d\x92éducateur spécialisé au 31.12',
            'Dont nombre d\x92ETP réels d\x92assistant social au 31.12',
            'Dont Autre Socio-éducatif',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Paramédical',
            'Dont nombre d\x27ETP réels d\x27infirmier',
            'Dont nombre d\x27ETP réels d\x27aide médico\x2Dpsychologique 2',
            'Dont nombre d\x27ETP réels d\x27aide soignant',
            'Dont nombre d\x27ETP réels de kinésithérapeute',
            'Dont nombre d\x27ETP réels de psychomotricien',
            'Dont nombre d\x27ETP réels d\x27ergothérapeute',
            'Dont nombre d\x27ETP réels d\x27orthophoniste',
            'Dont Autre Paramédical',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 de psychologue',
            'Répartition du personnel par fonction \x2D Nombre d\x92ETP réels au 31.12 d\x92ASH',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Médical',
            'Dont nombre d\x27ETP réels de médecin coordonnateur',
            'Dont Autre Médical',
            'Répartition du personnel par fonction \x2D Nombre d\x92ETP réels au 31\x2E12 de personnel Education nationale',
            'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Autres fonctions'
        ],
        decimal=",",
        encoding='Latin-1'
    )
        # Renommage des colonnes
    anap_2020_df.rename(columns={anap_2020_df.columns[0]: 'FINESS_ET',
                                anap_2020_df.columns[35]: 'nombre d usagers',
                                anap_2020_df.columns[4]: 'Taux d absentéisme 2020',
                                anap_2020_df.columns[5]: 'Taux de rotation du personnel titulaire 2020',
                                anap_2020_df.columns[1]: 'ETP vacants 2020', 
                                anap_2020_df.columns[2]: 'Dont ETP Vacants concernant la fonction SOINS 2020', 
                                anap_2020_df.columns[3]: 'Dont ETP Vacants concernant la fonction SOCIO EDUCATIVE 2020'},
                            inplace = True)
        # Converti le FINESS en str
    anap_2020_df['FINESS_ET'] = anap_2020_df['FINESS_ET'].astype(str)
        # Ajout du 0 quand longueur finess < 9
    anap_2020_df['FINESS_ET'] = anap_2020_df['FINESS_ET'].apply(lambda x: '0' + str(x) if len(x) == 8 else str(x))
        # Calcul du nombre d'ETP
    anap_2020_df['Total du nombre d\x92ETP'] = anap_2020_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Direction/Encadrement'] + anap_2020_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Administration / Gestion'] + anap_2020_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Services généraux'] + anap_2020_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Restauration'] + anap_2020_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Socio-éducatif'] + anap_2020_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Paramédical'] + anap_2020_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 de psychologue'] + anap_2020_df['Répartition du personnel par fonction - Nombre d\x92ETP réels au 31.12 d\x92ASH'] + anap_2020_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Médical'] + anap_2020_df['Répartition du personnel par fonction - Nombre d\x92ETP réels au 31.12 de personnel Education nationale'] + anap_2020_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Autres fonctions']
        # Suppression des 0 dans nombre d'usagers
    anap_2020_df['nombre d usagers'] = anap_2020_df['nombre d usagers'].replace(0, np.nan)
        # Calcul du Nombre total d'ETP par usager en 2020
    anap_2020_df['Nombre d\x92ETP par usager en 2020'] = (
        anap_2020_df['Total du nombre d\x92ETP'] / anap_2020_df['nombre d usagers']
        ) * 100
        # Calcul ETP "soins" par usager en 2020
    anap_2020_df['ETP soins par usager en 2020'] = ((anap_2020_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Médical'] + anap_2020_df['Répartition du personnel par fonction - Nombre d\x27ETP réels au 31.12 Paramédical']) / anap_2020_df['nombre d usagers']
        ) * 100
    # print(anap_2020_df)
    # Croisement
    # performance_df = liste_ehpad_df.merge(anap_2018_df,
    #                                  how = 'left').merge(anap_2019_df,
    #                                                    how = 'left').merge(anap_2020_df,
    #                                                                     how = 'left')
    perf1_df = liste_ehpad_df.merge(anap_2018_df,
                                     how = 'left')
    perf2_df = liste_ehpad_df.merge(anap_2019_df,
                                     how = 'left')
    perf3_df = liste_ehpad_df.merge(anap_2020_df,
                                     how = 'left')     
    performance_df = liste_ehpad_df.merge(perf1_df,
                                     how = 'left').merge(perf2_df,
                                                       how = 'left').merge(perf3_df,
                                                                        how = 'left')                                                                                              
        # Ajout des colonnes sans donnée
    performance_df['Absentéisme moyen sur la période 2018-2020'] = ''
    performance_df['Rotation moyenne du personnel sur la période 2018-2020'] = ''
    performance_df['Nombre moyen d\x27ETP par usager sur la période 2018-2020'] = ''
        # Modification de l'ordre des colonnes
    performance_df = performance_df[['FINESS_ET', 
                                'Taux d absentéisme 2018',
                                'Taux d absentéisme 2019',
                                'Taux d absentéisme 2020',
                                'Absentéisme moyen sur la période 2018-2020',
                                'Taux de rotation du personnel titulaire 2018',
                                'Taux de rotation du personnel titulaire 2019',
                                'Taux de rotation du personnel titulaire 2020',
                                'Rotation moyenne du personnel sur la période 2018-2020',
                                'ETP vacants 2018',
                                'ETP vacants 2019',
                                'ETP vacants 2020',
                                'Dont ETP Vacants concernant la fonction SOINS 2020',
                                'Dont ETP Vacants concernant la fonction SOCIO EDUCATIVE 2020',
                                'Nombre d\x92ETP par usager en 2018',
                                'Nombre d\x92ETP par usager en 2019',
                                'Nombre d\x92ETP par usager en 2020',
                                'Nombre moyen d\x27ETP par usager sur la période 2018-2020',
                                'ETP soins par usager en 2020',
                                'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Direction/Encadrement',
                                'Dont nombre d\x27ETP réels de personnel médical d\x27encadrement',
                                'Dont Autre Direction/Encadrement',
                                'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Administration / Gestion',
                                'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Services généraux',
                                'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Restauration',
                                'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Socio\x2Déducatif',
                                'Dont nombre d\x27ETP réels d\x27aide médico\x2Dpsychologique',
                                'Dont nombre d\x27ETP réels d\x27animateur',
                                'Dont nombre d\x27ETP réels de moniteur éducateur au 31.12',
                                'Dont nombre d\x92ETP réels d\x92éducateur spécialisé au 31.12',
                                'Dont nombre d\x92ETP réels d\x92assistant social au 31.12',
                                'Dont Autre Socio-éducatif',
                                'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Paramédical',
                                'Dont nombre d\x27ETP réels d\x27infirmier',
                                'Dont nombre d\x27ETP réels d\x27aide médico\x2Dpsychologique 2',
                                'Dont nombre d\x27ETP réels d\x27aide soignant',
                                'Dont nombre d\x27ETP réels de kinésithérapeute',
                                'Dont nombre d\x27ETP réels de psychomotricien',
                                'Dont nombre d\x27ETP réels d\x27ergothérapeute',
                                'Dont nombre d\x27ETP réels d\x27orthophoniste',
                                'Dont Autre Paramédical',
                                'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 de psychologue',
                                'Répartition du personnel par fonction \x2D Nombre d\x92ETP réels au 31.12 d\x92ASH',
                                'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Médical',
                                'Dont nombre d\x27ETP réels de médecin coordonnateur',
                                'Dont Autre Médical',
                                'Répartition du personnel par fonction \x2D Nombre d\x92ETP réels au 31.12 de personnel Education nationale',
                                'Répartition du personnel par fonction \x2D Nombre d\x27ETP réels au 31.12 Autres fonctions',
                                'Total du nombre d\x92ETP']]                                                   
    # print(performance_df)
    return performance_df
# findPerformanceData()

# Prompt des variables à modifier
## Valeurs pour tester
### Cont EPHAD - Traitement RECLAMATIONS V3.csv
### ARA-V2-Cont EHPAD - Traitement SIGNALEMENTS.csv
### 84 
def promptVariableRecla():
    recla_fichier = input('Nom du fichier des réclamations : ')
    print('Le fichier des réclamations pris en compte est : '+ recla_fichier)
    return recla_fichier
# promptVariableRecla()
def promptVariableSignal():
    signal_fichier = input('Nom du fichier des signalements : ')
    print('Le fichier des signalements pris en compte est : '+ signal_fichier)
    return signal_fichier
# promptVariableSignal()
def promptVariableReg():
    filtre_region = input('Région à filtrer : ')
    print('La région filtrée est : '+ filtre_region)
    return filtre_region
# promptVariableReg()

# Récupération des données réclamations et signalements
def findReclamationSignalementData():
    # Import des EHPAD
    liste_ehpad_df = findListeEHPAD()
    # print(liste_ehpad_df)
    # Import des données réclamations
    recle_file = promptVariableRecla()
    recla_df = pd.read_csv(recle_file,
            usecols = ['FINESS géographique', 
                        'Nombre de réclamations', 
                        'RECLAMATION relevant de la thématique Chute',
                        'RECLAMATION  relevant de la thématique Hygiène',
                        'RECLAMATION  relevant de la thématique Violence',
                        'RECLAMATION relevant de la thématique Soins',
                        'RECLAMATION relevant de la thématique Repas',
                        'RECLAMATION TOTAL relevant des thématiques chutes  soins  hygiène  violence  repas',
                        'RECLAMATION    Motif IGAS   Hôtellerie  locaux  restauration',
                        'RECLAMATION    Motif IGAS   Problème d  organisation ou de fonctionnement de l  établissement ou du service',
                        'RECLAMATION    Motif IGAS   Problème de qualité des soins médicaux',
                        'RECLAMATION    Motif IGAS   Problème de qualité des soins paramédicaux',
                        'RECLAMATION    Motif IGAS   Recherche d  établissement ou d  un professionnel',
                        'RECLAMATION    Motif IGAS   Mise en cause attitude des professionnels',
                        'RECLAMATION    Motif IGAS   Informations et droits des usagers',
                        'RECLAMATION    Motif IGAS   Facturation et honoraires',
                        'RECLAMATION    Motif IGAS   Santé  environnementale',
                        'RECLAMATION    Motif IGAS   Activités d  esthétique réglementées',
                        'RECLAMATION    Motif IGAS   A renseigner',
                        'RECLAMATION    Motif IGAS   COVID  19'],
            sep = ';',
            encoding = 'Latin-1'
    )
        # Renomme le FINESS
    recla_df.rename(columns={recla_df.columns[0]: 'FINESS_ET'},
                            inplace = True)
        # Converti le FINESS en str
    recla_df['FINESS_ET'] = recla_df['FINESS_ET'].astype(str)
        # Ajout du 0 devant le FINESS quand la longueur < 9 caractères
    recla_df['FINESS_ET'] = recla_df['FINESS_ET'].apply(lambda x: '0' + str(x) if len(x) == 8 else str(x))
    # print(recla_df)
    # # Import des données signalements 
    signal_file = promptVariableSignal()
    signal_df = pd.read_csv('ARA-V2-Cont EHPAD - Traitement SIGNALEMENTS.csv', #-- A MODIFIER SELON REGION
            usecols = ['FINESS géographique', 
                        'Nombre de signalements',
                        'SIGNALEMENT relevant de la thématique Chute',
                        'SIGNALEMENT relevant de la thématique Hygiène',
                        'SIGNALEMENT relevant de la thématique Violence',
                        'SIGNALEMENT relevant de la thématique Soins',
                        'SIGNALEMENT relevant de la thématique Repas',
                        'SIGNALEMENT TOTAL relevant des thématiques chutes  soins  hygiène  violence  repas'],
            sep = ';',
            encoding = 'Latin-1'
    )
        # Renomme le FINESS
    signal_df.rename(columns={signal_df.columns[0]: 'FINESS_ET'},
                            inplace = True)
        # Converti le FINESS en str
    signal_df['FINESS_ET'] = signal_df['FINESS_ET'].astype(str)
        # Ajout du 0 devant le FINESS quand la longueur < 9 caractères
    signal_df['FINESS_ET'] = signal_df['FINESS_ET'].apply(lambda x: '0' + str(x) if len(x) == 8 else str(x))
    # print(recla_df)
    # # Croisement
    recla_signal_df = liste_ehpad_df.merge(recla_df,
                                     how = 'left').merge(signal_df,
                                                       how = 'left')    
        # Modification de l'ordre des colonnes
    recla_signal_df = recla_signal_df[['FINESS_ET', 
                                        'Nombre de signalements',
                                        'Nombre de réclamations', 
                                        'RECLAMATION relevant de la thématique Chute',
                                        'RECLAMATION  relevant de la thématique Hygiène',
                                        'RECLAMATION  relevant de la thématique Violence',
                                        'RECLAMATION relevant de la thématique Soins',
                                        'RECLAMATION relevant de la thématique Repas',
                                        'RECLAMATION TOTAL relevant des thématiques chutes  soins  hygiène  violence  repas',
                                        'SIGNALEMENT relevant de la thématique Chute',
                                        'SIGNALEMENT relevant de la thématique Hygiène',
                                        'SIGNALEMENT relevant de la thématique Violence',
                                        'SIGNALEMENT relevant de la thématique Soins',
                                        'SIGNALEMENT relevant de la thématique Repas',
                                        'SIGNALEMENT TOTAL relevant des thématiques chutes  soins  hygiène  violence  repas',
                                        'RECLAMATION    Motif IGAS   Hôtellerie  locaux  restauration',
                                        'RECLAMATION    Motif IGAS   Problème d  organisation ou de fonctionnement de l  établissement ou du service',
                                        'RECLAMATION    Motif IGAS   Problème de qualité des soins médicaux',
                                        'RECLAMATION    Motif IGAS   Problème de qualité des soins paramédicaux',
                                        'RECLAMATION    Motif IGAS   Recherche d  établissement ou d  un professionnel',
                                        'RECLAMATION    Motif IGAS   Mise en cause attitude des professionnels',
                                        'RECLAMATION    Motif IGAS   Informations et droits des usagers',
                                        'RECLAMATION    Motif IGAS   Facturation et honoraires',
                                        'RECLAMATION    Motif IGAS   Santé  environnementale',
                                        'RECLAMATION    Motif IGAS   Activités d  esthétique réglementées',
                                        'RECLAMATION    Motif IGAS   A renseigner',
                                        'RECLAMATION    Motif IGAS   COVID  19']]
    return recla_signal_df
# findReclamationSignalementData()

# Croisement de toutes les données
def croisementData():
    print('Lancement de l agrégation des données de préciblage des EHPAD ...')
    # Chargement de tous les dataframes
    identification_df = findIdentificationData()
    capacite_df = findCapaciteData()
    occupation_df = findOccupationData()
    occupation31122021_df = findOccupation31122021Data()
    profil_df = findProfilData()
    performance_df = findPerformanceData()
    recla_signal_df = findReclamationSignalementData()
    # Croisement des dataframes
    print('Croisement de tous les fichiers importés')
    all_data_df = identification_df.merge(capacite_df,
                                     how = 'left').merge(occupation_df,
                                                       how = 'left').merge(occupation31122021_df,
                                                                        how = 'left').merge(profil_df,
                                                                                        how = 'left').merge(performance_df,
                                                                                                        how = 'left').merge(recla_signal_df,
                                                                                                                        how = 'left')            
    # Transformation en texte
    all_data_df['FINESS_ET'] = all_data_df['FINESS_ET'].map(str)
    all_data_df['SI_SECONDAIRE_FINESS_ET_SITE_PRINCIPAL'] = all_data_df['SI_SECONDAIRE_FINESS_ET_SITE_PRINCIPAL'].map(str)
    all_data_df['FINESS_EJ'] = all_data_df['FINESS_EJ'].map(str)
    all_data_df['CD_POSTAL'] = all_data_df['CD_POSTAL'].map(str)
    all_data_df['CD_COMMUNE'] = all_data_df['CD_COMMUNE'].map(str)
    # Correction des FINESS
    all_data_df['FINESS_ET'] = all_data_df['FINESS_ET'].apply(lambda x: '0' + str(x) if len(x) == 8 else str(x))
    all_data_df['SI_SECONDAIRE_FINESS_ET_SITE_PRINCIPAL'] = all_data_df['SI_SECONDAIRE_FINESS_ET_SITE_PRINCIPAL'].apply(lambda x: '0' + str(x) if len(x) == 8 else str(x))
    all_data_df['FINESS_EJ'] = all_data_df['FINESS_EJ'].apply(lambda x: '0' + str(x) if len(x) == 8 else str(x))
    # Correction des codes communes
    all_data_df['CD_COMMUNE'] = all_data_df['CD_COMMUNE'].apply(lambda x: '0' + str(x) if len(x) == 4 else str(x))                                                 
    # Filtre sur la région 
    region_filter = promptVariableReg()
    mask = all_data_df['CD_REGION']==region_filter 
    all_data_df_filtered = all_data_df[mask]
    # print(all_data_df.dtypes)  
    # print(all_data_df)
    # Création du nom du fichier à produire
    file_to_create = region_filter+'_data_pour_preciblage_ehpad.csv'
    # Suppression du fichier de sortie s'il existe déjà
    if os.path.exists(file_to_create):
        os.remove(file_to_create) 
        print('Le fichier a été supprimé car il existe déjà.')
    else:
        print('Le fichier n existe pas.')
    save_all_data = all_data_df_filtered.to_csv(file_to_create, 
                                    sep= ';',
                                    decimal=',',
                                    encoding='Latin-1')
    print('Le fichier '+file_to_create+' des données de préciblage des EHPAD a été créé.')                                
    return 
croisementData()
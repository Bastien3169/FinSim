import pandas as pd
import yfinance as yf
import time
import os
import scraping_tickers  # Import de ta fonction scraping


def get_stock_data(tickers, indice_name, Ticker_Yahoo_Indice, file_path):
    
    # Création du DataFrame initial avec une colonne vide
    df = pd.DataFrame({'Ticker_Yahoo_Finance': tickers})

    # Récupérer toutes les données en une seule requête
    tickers_obj = yf.Tickers(" ".join(tickers))  # Récupération groupée des tickers

    # Initialisation des listes pour stocker les données
    noms_entreprises = []
    pays = []
    place_boursiere = []
    secteur_activite = []
    capitalisation_boursiere = []
    tickers_sans_suffixe = []

    for i in tickers:
        try:
            # Récupérer les informations via l'objet Tickers
            info = tickers_obj.tickers[i].info

            # Extraction du ticker sans suffixe
            symbole_sans_suffixe = i.split(".")[0]
            tickers_sans_suffixe.append(symbole_sans_suffixe)

            # Ajouter les informations dans leurs listes respectives
            noms_entreprises.append(info.get('shortName', 'Non disponible'))
            pays.append(info.get('country', 'Non disponible'))
            place_boursiere.append(info.get('exchange', 'Non disponible'))
            secteur_activite.append(info.get('sector', 'Non disponible'))
            capitalisation_boursiere.append(info.get('marketCap', None))

        except Exception as e:
            print(f"Erreur lors de la récupération des données pour {i}: {e}")
            noms_entreprises.append('Non disponible')
            pays.append('Non disponible')
            place_boursiere.append('Non disponible')
            secteur_activite.append('Non disponible')
            capitalisation_boursiere.append(None)
            tickers_sans_suffixe.append(i)  # Ajouter le ticker original en cas d'erreur

        time.sleep(0.5)  # Petite pause pour éviter le blocage

    # Ajout des colonnes au DataFrame
    df['Nom_Entreprise'] = noms_entreprises
    df['Pays'] = pays
    df['Place_Boursiere'] = place_boursiere
    df['Secteur_Activite'] = secteur_activite
    df['Capitalisation_Boursiere'] = capitalisation_boursiere
    df['Ticker'] = tickers_sans_suffixe
    df['Nom_Indice'] = indice_name
    df['Nombres_Entreprises'] = len(noms_entreprises)
    df['Ticker_Indice_Yahoo'] = Ticker_Yahoo_Indice

    # Calcul de la capitalisation boursière totale
    total_capitalisation = df['Capitalisation_Boursiere'].fillna(0).sum()

    # Calcul pondération
    df['Ponderation'] = round((df['Capitalisation_Boursiere'] / total_capitalisation) * 100, 2)

    # Réorganisation des colonnes
    df = df[
        ['Nom_Entreprise', 'Ticker', 'Ticker_Yahoo_Finance', 'Ponderation', 'Secteur_Activite', 'Nom_Indice',
         'Ticker_Indice_Yahoo', 'Pays', 'Place_Boursiere', 'Nombres_Entreprises', 'Capitalisation_Boursiere']
    ]

    # Exportation en CSV
    df.to_csv(file_path, index=False, encoding='utf-8')
    print(f"[✅] Le fichier pour l'indice '{indice_name}' a bien été enregistré sous le nom : {file_path}")

    return df


def csv_indices(dossier_csv):

    # Récupérer les tickers via scraping_tickers.all_tickers_yf()
    tickers_yf = scraping_tickers.all_tickers_yf()
    
    df_cac40 = get_stock_data(tickers_yf["CAC40"], "CAC 40", "^FCHI", os.path.join(dossier_csv, "composition_france.csv"))
    df_dax40 = get_stock_data(tickers_yf["DAX40"], "DAX", "^GDAXI", os.path.join(dossier_csv, "composition_dax.csv"))
    df_italie40 = get_stock_data(tickers_yf["Italie40"], "FTSE MIB Index", "FTSEMIB.MI", os.path.join(dossier_csv, "composition_italie.csv"))
    df_espagne35 = get_stock_data(tickers_yf["Espagne35"], "IBEX 35", "^IBEX", os.path.join(dossier_csv, "composition_espagne.csv"))
    df_angleterre = get_stock_data(tickers_yf["Angleterre100"], "FTSE 100", "^FTSE", os.path.join(dossier_csv, "composition_angleterre.csv"))
    df_nasdaq100 = get_stock_data(tickers_yf["NASDAQ100"], "NASDAQ 100", "^NDX", os.path.join(dossier_csv, "composition_nasdaq100.csv"))
    df_dowjones = get_stock_data(tickers_yf["Dow Jones"], "Dow Jones 30", "^DJI", os.path.join(dossier_csv, "composition_dowjones.csv"))
    df_belgique = get_stock_data(tickers_yf["Belgique20"], "BEL 20", "^BFX", os.path.join(dossier_csv, "composition_belgique.csv"))
    df_pays_bas = get_stock_data(tickers_yf["Paysbas25"], "AEX-Index", "^AEX", os.path.join(dossier_csv, "composition_paysbas.csv"))
    df_finlande = get_stock_data(tickers_yf["Finlande25"], "OMX Helsinki 25", "^OMXH25", os.path.join(dossier_csv, "composition_finlande.csv"))
    df_suede = get_stock_data(tickers_yf["Suède30"], "OMX Stockholm 30", "^OMXS30", os.path.join(dossier_csv, "composition_suede.csv"))
    df_danemark = get_stock_data(tickers_yf["Danemark25"], "OMX Copenhagen 25", "^OMXC25", os.path.join(dossier_csv, "composition_danemark.csv"))
    df_stoxx50 = get_stock_data(tickers_yf["STOXX50"], "STOXX 50", "^STOXX50E", os.path.join(dossier_csv, "composition_europe50.csv"))
    df_sp500 = get_stock_data(tickers_yf["SP500"], "S&P 500", "^GSPC", os.path.join(dossier_csv, "composition_sp500.csv"))
    df_japon225 = get_stock_data(tickers_yf["Japon225"], "Nikkei 225", "^N225", os.path.join(dossier_csv, "composition_japon.csv"))


if __name__ == "__main__":
    indices_csv = csv_indices("csv") #Appel de la fonction 
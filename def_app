# functions.py
import sqlite3
import pandas as pd
import hashlib

""" Les guillemets autour de '{}', n'est pas nécessaire dans la requête SQL mais pour s'aasurer qu'il n'y ait aucune erreur due à des noms de tables ayant des caractères spéciaux ou des espaces, c'est une bonne pratique."""


####################################### CONNEXION BD POUR DATAS ET HIST ACTIFS  #######################################

def connect_to_db(db_path):
    """ Connexion à la base de données SQLite """
    return sqlite3.connect(db_path)


def get_list_actif(conn, table_hist_actif):
    """ Récupérer la liste des indices qui ont des historiques (on peut utiliser la table infos_indices mais pas sûr qu'il ait des historique dans la liste des indices de cette table (en l'occurence sir car table fait à partir des tikers infos_indices) """
    #return pd.read_sql(f"SELECT DISTINCT Ticker_Yahoo_Finance FROM '{table_hist_actif}'", conn)["Ticker_Yahoo_Finance"].tolist()
    df = pd.read_sql(f"SELECT DISTINCT Short_Name FROM '{table_hist_actif}'", conn)
    return df["Short_Name"].tolist()


def get_infos_actif(conn, table_infos_actif):
    """ Récupérer les informations sur l'actif """
    return pd.read_sql(f"SELECT * FROM '{table_infos_actif}'", conn)


def get_prix_date(conn, table_hist_actif, actif):
    """ Récupérer les données de l'actif pour le graphique """
    df = pd.read_sql(f"SELECT Date, Close FROM {table_hist_actif} WHERE Short_Name = '{actif}' ORDER BY Date", conn)
    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
        df = df.set_index("Date").resample("W").last().reset_index()
    return df



# Mapping des indices vers les fichiers correspondants
mapping_indices = {
    "CAC 40": "composition_france",
    "DAX                           P": "composition_allemagne",
    "FTSE MIB Index": "composition_italie",
    "IBEX 35...": "composition_espagne",
    "BEL 20": "composition_belgique",
    "AEX-Index": "composition_paysbas",
    "FTSE 100": "composition_angleterre",
    "S&P 500": "composition_sp500",
    "NASDAQ 100": "composition_nasdaq100",
    "Dow Jones Industrial Average": "composition_dowjones",
    "OMX Helsinki 25": "composition_finlande",
    "OMX Stockholm 30 Index": "composition_suede",
    "OMX Copenhagen 25 Index": "composition_danemark",
    "EURO STOXX 50                 I": "composition_europe50",
    "Nikkei 225": "composition_japon",
}

def get_composition_indice(conn, selected_indice):
    """ Récupère la composition de l'indice depuis la base de données """
    try:
        table_name = mapping_indices.get(selected_indice)
        query = f"SELECT * FROM {table_name}"
        df_composition = pd.read_sql(query, conn)
        return df_composition
    except Exception as e:
        print(f"Erreur lors de la récupération de la table '{selected_indice}': {e}")


####################################### CALCUL RENDEMENTS ACTIFS #######################################

def calculate_rendement(df, periods):
    """ Calculer les rendements pour chaque période """
    rendement = {}
    for period_months in periods:
        start_date = df["Date"].max() - pd.DateOffset(months=period_months)
        df_period = df[df["Date"] >= start_date]
        if len(df_period) > 1:  # Si on a plus d'une donnée dans la période
            start_close = df_period.iloc[0]["Close"]
            end_close = df_period.iloc[-1]["Close"]
            rendement[f"{period_months} mois"] = "{:.2f}".format((end_close - start_close) / start_close * 100) # arrondie 2 chif
        else:
            rendement[f"{period_months} mois"] = None
    return rendement



####################################### STYLE DU TABLEAU DE RENDEMENT #######################################

def style_rendement(df, periods):
    """ Appliquer un style de couleur sur les rendements """
    def color_rendement(val):
        color = 'green' if float(val) > 0 else ('red' if float(val) < 0 else 'black')
        return f'color: {color}'  
    return df.style.applymap(color_rendement, subset=[f"{p} mois" for p in periods])






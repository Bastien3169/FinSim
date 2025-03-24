# functions.py
import sqlite3
import pandas as pd
from fastapi import FastAPI
import requests
import plotly.graph_objects as go
from fastapi.middleware.cors import CORSMiddleware


""" Les guillemets autour de '{}', n'est pas nécessaire dans la requête SQL mais pour s'aasurer qu'il n'y ait aucune erreur due à des noms de tables ayant des caractères spéciaux ou des espaces, c'est une bonne pratique."""

app = FastAPI()

'''
# Configuration CORS (important pour Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''

db_path = "/Users/bastoch/ProjectFinance_alleger/ProjectFinance_Streamlit/sql/data_indices_stocks.db"

def connect_to_db():
    """ Connexion à la base de données SQLite """
    return sqlite3.connect(db_path)


'''
def get_list_actif(conn, table_hist_actif):
    """ Récupérer la liste des indices qui ont des historiques (on peut utiliser la table infos_indices mais pas sûr qu'il ait des historique dans la liste des indices de cette table (en l'occurence sir car table fait à partir des tikers infos_indices) """
    #return pd.read_sql(f"SELECT DISTINCT Ticker_Yahoo_Finance FROM '{table_hist_actif}'", conn)["Ticker_Yahoo_Finance"].tolist()
    df = pd.read_sql(f"SELECT DISTINCT Ticker_Yahoo_Finance FROM '{table_hist_actif}'", conn)
    return df["Ticker_Yahoo_Finance"].tolist()
'''


@app.get("/indices")
def get_list_actif(table_hist_actif: str = "historique_indices"):
    """ Récupérer la liste des indices qui ont des historiques """
    conn = connect_to_db()
    df = pd.read_sql(f"SELECT DISTINCT Ticker_Yahoo_Finance FROM {table_hist_actif}", conn)
    conn.close()
    return df["Ticker_Yahoo_Finance"].tolist()



def get_infos_actif(table_infos_actif):
    """ Récupérer les informations sur l'actif """
    conn = connect_to_db()
    df = pd.read_sql(f"SELECT Ticker_Yahoo_Finance, Nom_Indice, Pays FROM {table_infos_actif}", conn)
    conn.close()
    return df



@app.get("/historique")
def get_hist_actif_for_graph(table_hist_actif: str = "historique_indices", actif: str = ""):
    """ Récupérer les données de l'actif pour le graphique """
    conn = connect_to_db()
    df = pd.read_sql(f"SELECT Date, Close FROM {table_hist_actif} WHERE Ticker_Yahoo_Finance = ?", conn, params=(actif,))
    conn.close()
    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
        df = df.set_index("Date").resample("W").last().reset_index()
    return df



'''
@app.get("/historique/{type_actif}")
def get_historique(type_actif: str, actif: str):
    if type_actif == "indices":
        table = "historique_indices"
    elif type_actif == "entreprises":
        table = "historique_entreprises"
    else:
        return {"error": "Type d'actif inconnu"}
    df = pd.read_sql("SELECT Date, Close FROM {} WHERE Ticker_Yahoo_Finance = ?".format(table), conn, params=(actif,))
    return df.to_dict(orient="records")
'''


















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


def style_rendement(df, periods):
    """ Appliquer un style de couleur sur les rendements """
    def color_rendement(val):
        color = 'green' if float(val) > 0 else ('red' if float(val) < 0 else 'black')
        return f'color: {color}'  
    return df.style.applymap(color_rendement, subset=[f"{p} mois" for p in periods])


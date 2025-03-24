from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import numpy as np
import yfinance as yf
import html5lib
import os
import glob


# Récupération les données historiques pour chaque entreprise (je passe par google colab car fonctionne pas ici ????)

# Charger le fichier et prendre la liste de tous les tikers yahoo des entreprises avec les tikers les infos hist sur yfinance
df = pd.read_csv("/Users/bastoch/ProjectFinance_alleger/data_csv/infos_indices/infos_indices.csv", encoding="utf-8")

stocks_tickers_yahoo = df["Ticker_Yahoo_Finance"].to_list()

# Liste pour stocker les DataFrames
dfs = []

for i in liste_stocks_concat:
    try:
        # Récupération des données historiques
        hist = yf.Ticker(i).history(period="max", interval="1wk")

        # Ajouter les colonnes 'Ticker' et 'ShortName'
        hist['Ticker'] = i
        hist['Short_Name'] = yf.Ticker(i).info.get("shortName", "N/A")

        # Ajouter le DataFrame historique dans la liste
        dfs.append(hist)
      
    except Exception as e:
        print(f"Erreur lors de la récupération des données pour {ticker}: {e}")

# Concaténation de tous les DataFrames
df_final = pd.concat(dfs)

# Exportation en CSV
df_final.to_csv("/Users/bastoch/ProjectFinance_alleger/data_csv/historique_indices", index=True, encoding='utf-8')

# Affichage des résultats
display(df_final)



# On clean le fichier !

# Charger le fichier principal
df = pd.read_csv("/Users/bastoch/ProjectFinance_alleger/data_csv/historique_indices/historique_indices.csv", encoding="utf-8")

# Fichier cible pour rajouter Ticker
df1 = pd.read_csv("/Users/bastoch/ProjectFinance_alleger/data_csv/infos_indices/infos_indices.csv", encoding="utf-8")

# Supprimer colonnes inutiles
df = df.drop(columns=["Open", "High", "Low", "Volume", "Dividends", "Stock Splits"], errors="ignore")

# Convertir la colonne "Date" en format datetime et reformater en "JJ-MM-AAAA"
df["Date"] = pd.to_datetime(df["Date"], errors="coerce", utc=True).dt.strftime("%d-%m-%Y")

# Renommer la colonne (si nécessaire)
df = df.rename(columns={"Ticker": "Ticker_Yahoo_Finance"})

# Fusionner df avec df1 sur "Ticker_Yahoo_Finance"
df = df.merge(df1[["Ticker_Yahoo_Finance", "Ticker"]], on="Ticker_Yahoo_Finance", how="left")

# Arrondir la colonne "Close"
df["Close"] = df["Close"].round(4)

# Réorganiser les colonnes dans l'ordre souhaité
df = df[["Date", "Close", "Ticker", "Ticker_Yahoo_Finance", "Short_Name"]]

# Enregistrer le fichier modifié
df.to_csv("/Users/bastoch/ProjectFinance_alleger/data_csv/historique_indices/historique_indices_clean.csv", index=False, encoding="utf-8")

# Afficher un aperçu
display(df.head())
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
df = pd.read_csv("/Users/bastoch/ProjectFinance_alleger/data_csv/infos_stocks_concat/infos_stocks_concat.csv", encoding="utf-8")

stocks_tickers_yahoo = df["Ticker_Yahoo_Finance"].to_list()

# Liste pour stocker les DataFrames
dfs = []

for i in liste_stocks_concat:
    try:
        # Récupération des données historiques
        hist = yf.Ticker(i).history(period="max", interval="1wk")

        # Ajouter les colonnes 'Ticker' et 'ShortName'
        hist['Ticker'] = i

        # Ajouter le DataFrame historique dans la liste
        dfs.append(hist)
      
    except Exception as e:
        print(f"Erreur lors de la récupération des données pour {ticker}: {e}")

# Concaténation de tous les DataFrames
df_final = pd.concat(dfs)

# Exportation en CSV
df_final.to_csv("/Users/bastoch/ProjectFinance_alleger/data_csv/historique_stocks_concat/historique_stocks_concat.csv", index=True, encoding='utf-8')

# Affichage des résultats
display(df_final)



# On clean le fichier !

# Charger le fichier principal
df = pd.read_csv("/Users/bastoch/ProjectFinance_alleger/data_csv/historique_stocks_concat/historique_stocks_concat.csv", encoding="utf-8")

# Supprimer colonnes inutiles
df = df.drop(columns=["Open", "High", "Low", "Volume", "Dividends", "Stock Splits", "Capital Gains", "Adj Close"], errors="ignore")

# Convertir la colonne "Date" en format datetime et reformater en "JJ-MM-AAAA"
df["Date"] = pd.to_datetime(df["Date"], errors="coerce", utc=True).dt.strftime("%d-%m-%Y")

# Renommer la colonne (si nécessaire)
df = df.rename(columns={"Ticker": "Ticker_Yahoo_Finance"})

# Création colonne Ticker sans suffix
df["Ticker"] = df["Ticker_Yahoo_Finance"].str.split(".").str[0]

# Arrondir la colonne "Close"
df["Close"] = df["Close"].round(4)

# Réorganiser les colonnes dans l'ordre souhaité
df = df[["Date", "Close", "Ticker", "Ticker_Yahoo_Finance"]]

# Enregistrer le fichier modifié
df.to_csv("/Users/bastoch/ProjectFinance_alleger/data_csv/historique_stocks_concat/historique_stocks_concat_clean.csv", index=False, encoding="utf-8")

# Afficher un aperçu
display(df.head())
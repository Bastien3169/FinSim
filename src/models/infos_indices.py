from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import numpy as np
import yfinance as yf
import html5lib


def infos_indices():
    
    indices = {
    "Nom_Indice": ['CAC40', 'DAX40', 'FTSE MIB40', 'IBEX35', 'BEL20', 'AEX25', 'FTSE100', 'SP500', 'NASDAQ100', 'DowJones30', 
                   'OMX Helsinki 25', 'OMX Stockholm 30', 'OMX Copenhagen 25', 'STOXX50', 'NIKKEI225'],
    "Ticker": ['PX1', 'DAX', 'FTSEMIB', 'INDI', 'BEL20', 'AEX', 'UKX', 'GSPC', 'NDX', 'DJI', 'OMCH25', 'OMXS30', 'OMXC25', 'SX5E', 'NI225'],
    "Ticker_Yahoo_Finance": ['^FCHI', '^GDAXI', 'FTSEMIB.MI', '^IBEX', '^BFX', '^AEX', '^FTSE', '^GSPC', '^NDX', '^DJI', 
                             '^OMXH25', '^OMX', '^OMXC25', '^STOXX50E', '^N225'],
    "Pays": ['France', 'Germany', 'Italy', 'Spain', 'Belgium', 'Netherlands', 'United Kingdom', 'United States', 'United States', 
             'United States', 'Finland', 'Sweden', 'Danemark', 'Europe', 'Japan'],
    "Nombres_Entreprises": [40, 40, 40, 35, 20, 25, 100, 500, 100, 30, 25, 30, 25, 50, 225],
    }

    # Création du DataFrame
    df = pd.DataFrame(indices)
    
    # Listes pour stocker les nouvelles informations
    currencies = []
    place_boursiere = []
    short_name = []
    
    # Récupération des informations via yfinance
    for i in df["Ticker_Yahoo_Finance"]:
        try:
            info = yf.Ticker(i).info  # Récupération des infos générales
            
            # Extraction des données
            currency = info.get("currency", "Non disponible")
            exchange = info.get("exchange", "Non disponible")
            short_name_entreprise = info.get('shortName', 'Non disponible')
            
        except Exception as e:
            currency = "Non disponible"
            exchange = "Non disponible"
            short_name_entreprise = "Non disponible"
            
        # Ajout des valeurs aux listes
        currencies.append(currency)
        place_boursiere.append(exchange)
        short_name.append(short_name_entreprise)
    
    # Ajout des nouvelles colonnes au DataFrame
    df["Devise"] = currencies
    df["Place_Boursiere"] = place_boursiere
    df["Short_Name"] = short_name
    
    # Réorganisation des colonnes
    df = df[
        ["Nom_Indice", 'Ticker', 'Ticker_Yahoo_Finance', "Short_Name", 'Pays', 'Place_Boursiere', 'Nombres_Entreprises', "Devise"]
        ]
    
    # Enregistrement du fichier .csv
    df.to_csv("ProjectFinance_alleger/ProjectFinance_Streamlit/src/modelels/csv/infos_indices.csv", index=False, encoding='utf-8')
    
    return df



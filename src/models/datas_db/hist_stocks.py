import pandas as pd
import yfinance as yf
import os


def recuperer_et_clean_stocks(dossier_csv):


    # Charger le fichier et prendre la liste de tous les tikers yahoo des entreprises avec les tikers les infos hist sur yfinance
    df_tickers = pd.read_csv(os.path.join(dossier_csv, "infos_stocks.csv"), encoding="utf-8")
    
    tickers_yahoo = df_tickers["Ticker_Yahoo_Finance"].dropna().unique().tolist()
    
    # Liste pour stocker les DataFrames
    dfs = []
   
    for i in tickers_yahoo:
        try:
            # Récupération des données historiques
            hist = yf.Ticker(i).history(period="max", interval="1wk")
    
            # Ajouter les colonnes 'Ticker_Yahoo_Finance'
            hist['Ticker_Yahoo_Finance'] = i
    
            # Ajouter le DataFrame historique dans la liste
            dfs.append(hist)
          
        except Exception as e:
            print(f"Erreur lors de la récupération des données pour {i}: {e}")
    
    # Concaténation de tous les DataFrames
    df = pd.concat(dfs)
    df.reset_index(inplace=True)
    
  
############################################ NETTOYAGE DATAFRAME ############################################

    # Supprimer colonnes inutiles
    df = df.drop(columns=["Open", "High", "Low", "Volume", "Dividends", "Stock Splits", "Capital Gains", "Adj Close"], errors="ignore")
    
    # Convertir la colonne "Date" en format datetime et reformater en "JJ-MM-AAAA"
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", utc=True).dt.strftime("%d-%m-%Y")
    
    # Création colonne Ticker sans suffix
    df["Ticker"] = df["Ticker_Yahoo_Finance"].str.split(".").str[0]
    
    # Arrondir la colonne "Close"
    df["Close"] = df["Close"].round(4)

    # Jointure avec le fichier original pour ajouter la colonne 'ShortName'
    df = df.merge(df_tickers[["Ticker_Yahoo_Finance", "Nom_Entreprise"]], on="Ticker_Yahoo_Finance", how="left")

    # Réorganiser les colonnes dans l'ordre souhaité
    df = df[["Date", "Close", "Ticker", "Ticker_Yahoo_Finance", "Nom_Entreprise"]]
    
    # Enregistrer le fichier modifié
    df.to_csv(os.path.join(dossier_csv, "historique_stocks.csv"), index=False, encoding="utf-8")
    print(f"[✅] Le fichier historique stocks a bien été enregistré sous le nom")
    
    return df

if __name__ == "__main__":
    recuperer_et_clean_stocks = recuperer_et_clean_stocks("csv") #Appel de la fonction

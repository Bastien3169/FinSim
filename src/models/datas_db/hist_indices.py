import pandas as pd
import yfinance as yf
import os


def recuperer_et_clean_indices(dossier_csv):

    # Charger les tickers
    df_infos = pd.read_csv(os.path.join(dossier_csv, "infos_indices.csv"), encoding="utf-8")
    tickers_yahoo = df_infos["Ticker_Yahoo_Finance"].dropna().unique().tolist()

    dfs = []

    for i in tickers_yahoo:
        try:
            # Récupération des données historiques
            hist = yf.Ticker(i).history(period="max", interval="1wk")
    
            # Ajouter les colonnes 'Ticker' et 'ShortName'
            hist['Ticker'] = i
            hist['Short_Name'] = yf.Ticker(i).info.get("shortName", "N/A")
    
            # Ajouter le DataFrame historique dans la liste
            dfs.append(hist)
          
        except Exception as e:
            print(f"Erreur de récupération pour {i}: {e}")

    
    if not dfs:
        return pd.DataFrame()  # ← En dehors de la boucle maintenant

    # Fusion de tous les historiques
    df = pd.concat(dfs)
    df.reset_index(inplace=True)

    
############################################ NETTOYAGE DATAFRAME ############################################
    
    # Supprimer colonnes inutiles
    df = df.drop(columns=["Open", "High", "Low", "Volume", "Dividends", "Stock Splits"], errors="ignore")

    # Convertir la colonne "Date" en format datetime et reformater en "JJ-MM-AAAA"
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", utc=True).dt.strftime("%d-%m-%Y")

    df.rename(columns={"Ticker": "Ticker_Yahoo_Finance"}, inplace=True)
    df = df.merge(df_infos[["Ticker_Yahoo_Finance", "Ticker"]], on="Ticker_Yahoo_Finance", how="left")

    # Arrondir la colonne "Close"
    df["Close"] = df["Close"].round(4)

    # Réorganiser les colonnes dans l'ordre souhaité
    df = df[["Date", "Close", "Ticker", "Ticker_Yahoo_Finance", "Short_Name"]]

    # Sauvegarde
    df.to_csv(os.path.join(dossier_csv, "historique_indices.csv"), index=False, encoding="utf-8")
    print(f"[✅] Le fichier historique indices a bien été enregistré sous le nom")
    
    return df

if __name__ == "__main__":
    recuperer_et_clean_indices = recuperer_et_clean_indices("csv") #Appel de la fonction
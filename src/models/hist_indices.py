import pandas as pd
import yfinance as yf


def recuperer_et_clean_indices(
    chemin_tickers="ProjectFinance_alleger/ProjectFinance_Streamlit/src/modelels/csv/infos_indices.csv",
    chemin_output="ProjectFinance_alleger/ProjectFinance_Streamlit/src/modelels/csv/historique_indices.csv"
):
    """
    Récupère les historiques hebdomadaires des indices depuis yfinance,
    les nettoie et les sauvegarde directement dans un fichier CSV.
    """

    # Charger les tickers
    df_infos = pd.read_csv(chemin_tickers, encoding="utf-8")
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
            print(f"Erreur de récupération pour {ticker}: {e}")

        return pd.DataFrame()

    # Fusion de tous les historiques
    df = pd.concat(dfs)
    df.reset_index(inplace=True)

    
############################################ NETTOYAGE DATAFRAME ############################################
    
    # Supprimer colonnes inutiles
    df = df.drop(columns=["Open", "High", "Low", "Volume", "Dividends", "Stock Splits"], errors="ignore")

    # Convertir la colonne "Date" en format datetime et reformater en "JJ-MM-AAAA"
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", utc=True).strftime("%d-%m-%Y")

    # Ajouter le ticker simplifié en fusionnant sur "Ticker_Yahoo_Finance"
    df = df.merge(df_infos[["Ticker_Yahoo_Finance", "Ticker"]], on="Ticker_Yahoo_Finance", how="left")

    # Arrondir la colonne "Close"
    df["Close"] = df["Close"].round(4)

    # Réorganiser les colonnes dans l'ordre souhaité
    df = df[["Date", "Close", "Ticker", "Ticker_Yahoo_Finance", "Short_Name"]]

    # Sauvegarde
    df.to_csv(chemin_output, index=False, encoding="utf-8")
    print(f"✅ Données récupérées et nettoyées enregistrées dans : {chemin_output}")
    
    return df
import pandas as pd
import yfinance as yf
import os


def hist_etfs(csv_bdd):
    # Charger le fichier de tickers et infos
    df = pd.read_csv(os.path.join(csv_bdd, "etfs_infos.csv"), encoding="utf-8")

    dfs = []
    for idx, row in df.iterrows():
        ticker_yf = row["Ticker_Etf_Yf"]
        short_name = row["Short_Name_Etf"]
        
        try:
            ticker = yf.Ticker(ticker_yf)
            hist = ticker.history(period="max", interval="1mo")

            if hist.empty:
                print(f"⚠️ Historique vide pour {ticker_yf}.")
                continue

            # Reset index pour que la date devienne une colonne
            hist = hist.reset_index()

            # Conversion de la colonne Date au format souhaité
            hist["Date"] = pd.to_datetime(hist["Date"], errors="coerce").dt.strftime("%d-%m-%Y")

            # Ne garder que les colonnes souhaitées
            hist["Close"] = hist["Close"].round(4)
            hist["Ticker_Etf_Yf"] = ticker_yf
            hist["Short_Name_Etf"] = short_name

            dfs.append(hist)
            print(f"✅ Historique récupéré pour {ticker_yf}.")
        
        except Exception as e:
            print(f"Erreur pour {ticker_yf}: {e}")
            continue

    if dfs:
        df_hist = pd.concat(dfs, ignore_index=True)  # concat avec reset de l'index
        df_hist = df_hist[["Date", "Close", "Ticker_Etf_Yf", "Short_Name_Etf"]]
        df_hist.to_csv(os.path.join(csv_bdd, "historique_etfs.csv"), index=False, encoding="utf-8")
        print(f"[✅] CSV de l'historique des ETFs récupéré avec {len(df_hist)} entrées.")
        #display(df_hist)
    else:
        print("❌ Aucun historique récupéré.")
        df_hist = pd.DataFrame(columns=["Date", "Close", "Ticker_Etf_Yf", "Short_Name_Etf"])

    # Filtrer le fichier infos pour ne garder que les tickers des ETFs avec historique
    df_infos = pd.read_csv(os.path.join(csv_bdd, "etfs_infos.csv"), encoding="utf-8")
    df_infos_filtre = df_infos.merge(df_hist[["Ticker_Etf_Yf"]].drop_duplicates(), on="Ticker_Etf_Yf", how="inner")
    df_infos_filtre.to_csv(os.path.join(csv_bdd, "etfs_infos.csv"), index=False, encoding="utf-8")

if __name__ == "__main__":
    hist_etfs(csv_bdd = "csv/csv_bdd/")
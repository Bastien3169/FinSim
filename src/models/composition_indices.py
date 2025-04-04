import pandas as pd
import yfinance as yf
from scraping_tickers import all_tickers_yf  # Import de ta fonction scraping

def get_stock_data(ticker_list, index_name, index_ticker, output_file):
    data = []
    for ticker in ticker_list:
        try:
            info = yf.Ticker(ticker).info
            data.append({
                "Nom": info.get("shortName", ""),
                "Ticker": ticker,
                "Secteur": info.get("sector", ""),
                "Pays": info.get("country", ""),
                "Capitalisation": info.get("marketCap", ""),
                "Indice": index_name,
                "Ticker Indice": index_ticker
            })
        except Exception as e:
            print(f"Erreur pour {ticker}: {e}")
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"{index_name} → {output_file} : {len(df)} lignes")
    return df


if __name__ == "__main__":
    tickers_yf = all_tickers_yf() # Appel de la fonction
    get_stock_data(tickers_yf["CAC40"], "CAC 40", "^FCHI", "composition_france.csv")

    # Tu peux décommenter les lignes ci-dessous quand tu veux générer tous les CSV
    '''
    get_stock_data(tickers_yf["DAX40"], "DAX 40", "^GDAXI", "composition_dax.csv")
    get_stock_data(tickers_yf["Italie40"], "FTSE MIB", "FTSEMIB.MI", "composition_italie.csv")
    get_stock_data(tickers_yf["Espagne35"], "IBEX 35", "^IBEX", "composition_espagne.csv")
    get_stock_data(tickers_yf["Angleterre100"], "FTSE 100", "^FTSE", "composition_uk.csv")
    get_stock_data(tickers_yf["NASDAQ100"], "NASDAQ 100", "^NDX", "composition_nasdaq.csv")
    get_stock_data(tickers_yf["Dow Jones"], "Dow Jones", "^DJI", "composition_dow.csv")
    get_stock_data(tickers_yf["SP500"], "S&P 500", "^GSPC", "composition_sp500.csv")
    get_stock_data(tickers_yf["STOXX50"], "STOXX 50", "^STOXX50E", "composition_stoxx50.csv")
    '''

from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import numpy as np
import yfinance as yf
import html5lib

from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import asyncio
import nest_asyncio


# I- SCRAPPING DES DATAS DES DIFFIRENTES STOCKS DES INDICES

    # 1) CAC40, DAX40, FTSE MIB40 (Italie), IBEX35 (Espagne), FTSE100 (UK), NASDAQ100 (US), DowJones30 (US), NIKKEI225 (Japon)


# Liste des URLs correctement séparées
urls = [
    "https://fr.tradingview.com/symbols/EURONEXT-PX1/components/",  #CAC 40 - France / .PA
    "https://fr.tradingview.com/symbols/XETR-DAX/components/",      #DAX 40 - Allemagne / .DE
    "https://fr.tradingview.com/symbols/INDEX-FTSEMIB/components/", #ftse mib 40 - italie / .MI
    "https://fr.tradingview.com/symbols/BME-IBC/components/",       #IBEX 35 - Espagne / .MC
    "https://fr.tradingview.com/symbols/FTSE-UKX/components/",      #FTSE 100 (que 95/100) - Royaume-Uni / .L
    "https://fr.tradingview.com/symbols/NASDAQ-NDX/components/",    #nasdaq100 - us / rien
    "https://fr.tradingview.com/symbols/DJ-DJI/components/",        #dowjones - us / rien
    #"https://fr.tradingview.com/symbols/TVC-NI225/components/",     #nikkei225 - Japon / .T (Trop de ticker, faire avec Selenium)
]

indice = ["CAC40", "DAX40", "Italie40", "Espagne35", "Angleterre100", "NASDAQ100", "Dow Jones"]

# User-Agent pour éviter d'être bloqué par le site
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

# Dictionnaire pour stocker les tickers de chaque indice
tickers_list_Vfinal = []

for i in urls:
    response = requests.get(i, headers=header)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Sélectionner tous les liens des tickers
    tickers = soup.select("a.tickerNameBox-GrtoTeat")

    # Extraire le texte des tickers
    tickers_list = []
    for i in tickers:
        text_ticker = i.text.strip()
        tickers_list.append(text_ticker)

    tickers_list_Vfinal.append(tickers_list)


# Affichage des tickers avec le nom de l'indice
for index, tickers in enumerate(tickers_list_Vfinal):
    print(f"{indice[index]}: {tickers}")
    print("-"*50)



# CONVERSION EN TIKERS YFINANCE

france_ticker = tickers_list_Vfinal[0]
allemagne_ticker = tickers_list_Vfinal[1]
italie_ticker = tickers_list_Vfinal[2]
espagne_ticker = tickers_list_Vfinal[3]
angleterre_ticker = tickers_list_Vfinal[4]
angleterre_ticker_sans_point = [i.rstrip('.') for i in angleterre_ticker] # Certains tickers finissent par un ".", je le supprime
angleterre_ticker_clean = [ticker.replace('.', '-') for ticker in angleterre_ticker_sans_point] # Un ticker possède un "." en son milieu. je remplace par "-"
nasdaq_ticker = tickers_list_Vfinal[5]
dowjones_ticker = tickers_list_Vfinal[6]
#japon_ticker = tickers_list_Vfinal[7]

france_ticker_yf = [ticker + ".PA" for ticker in france_ticker]
france_ticker_yf.append("MT.AS") # Rajout car seule action pas en .PA
allemagne_ticker_yf= [ticker + ".DE" for ticker in allemagne_ticker]
italie_ticker_yf = [ticker + ".MI" for ticker in italie_ticker]
espagne_ticker_yf = [ticker + ".MC" for ticker in espagne_ticker]
angleterre_ticker_yf = [ticker + ".L" for ticker in angleterre_ticker_clean]
nasdaq_ticker_yf = nasdaq_ticker
dowjones_ticker_yf = dowjones_ticker
#japon_ticker_yf = [ticker + ".T" for ticker in tickers_list_Vfinal[7]]


# 2) BEL20 (Belgique 20), AEX (Pays-Bas 25), OMX Helsinki (Finlande 25), OMX Stockholm 30 (Suède 30), OMX Copenhagen 20 (Danemark 20)

# Scrapper via Yahoo finance

# Liste des URL pour les différents indices
urls = [
    "https://finance.yahoo.com/quote/BEL20.BR/components/",  # BEL20 (Belgique 20) / 19 .BR et .AS
    "https://finance.yahoo.com/quote/%5EAEX/components/",  # AEX (Pays-Bas 25) / 22 .AS
    "https://finance.yahoo.com/quote/%5EOMXH25/components/",  # OMX Helsinki (Finlande 25) / 25 .HE
    "https://finance.yahoo.com/quote/%5EOMX/components/", # OMX Stockholm 30 (Suède 30) / 30 .ST
    "https://finance.yahoo.com/quote/%5EOMXC25/components/" # OMX Copenhagen 20 (Danemark 20) / 20 .CO
]

# En-tête pour éviter le blocage du site
header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}

# Dictionnaire pour stocker les noms des entreprises et les tickers de chaque indice. 
# Clé=nom_indice : valeur=dico dans ce dico, Clé1=nom : valeur1=liste des entreprises et Clé2=tiker : valeur2=liste des tikers
tickers = []

# Boucle sur chaque URL pour récupérer les données du tableau
for url in urls:
    # Envoi de la requête
    reponse = requests.get(url, headers=header) # Capture et lecture de l'url
    reponse.encoding = 'utf-8'
    html = reponse.text # Page html retrancrite en format .text pour récupérer ce qu'on veut
    time.sleep(1) # Delais pour bien que les pages s'affiches
    
    # Récupération du tableau
    df = pd.read_html(html)[0] # Retourne une liste des tables de la page. On veut le 1er
    #display(df)
    
    # Extraction des noms d'entreprises et tickers du tableau et création d'une liste
    ticker = df["Symbol"].tolist()

    # Ajout ticker dans la liste vide tickers
    tickers.append(ticker) # Ajout de la structure du nouveau dico


belgique_ticker = tickers[0]
pays_bas_ticker = tickers[1]
finlande_ticker = tickers[2]
suede_ticker = tickers[3]
danemark_ticker = tickers[4]


#3) STOXX50

# Scrappé il y a longtemps
stoxx50_ticker = [
        'MC.PA', 'SAP.DE', 'RMS.PA', 'ASML.AS', 'OR.PA', 'ITX.MC', 'SIE.DE', 
        'DTE.DE', 'SU.PA', 'AIR.PA', 'SAN.PA', 'TTE.PA', 'ALV.DE', 'EL.PA', 
        'SAF.PA', 'AI.PA', 'ABI.BR', 'PRX.AS', 'IBE.MC', 'CS.PA', 'SAN.MC', 
        'ISP.MI', 'RACE.MI', 'BNP.PA', 'MUV2.DE', 'UCG.MI', 'ENEL.MI', 
        'BBVA.MC', 'DG.PA', 'MBG.DE', 'INGA.AS', 'VOW3.DE', 'BMW.DE', 
        'ADYEN.AS', 'ADS.DE', 'SGO.PA', 'DB1.DE', 'BN.PA', 'IFX.DE', 'BAS.DE', 
        'ENI.MI', 'WKL.AS', 'DHL.DE', 'NDA-SE.ST', 'STLAP.PA', 'AD.AS', 'KER.PA', 
        'RI.PA', 'NOKIA.HE', 'BAYN.DE']


# 4) SP500 VIA PLAYWRIGHT VIA TRAIDINGVIEW

async with async_playwright() as p:
    # Lancer le navigateur Chromium en mode asynchrone car sur Jupytair il faut être asynchrone
    browser = await p.chromium.launch(headless=True)  # headless=False pour voir le navigateur
    page = await browser.new_page() # Ouvre une nouvelle page
    
    await page.goto("https://fr.tradingview.com/symbols/SPX/components/") # Va sur l'URL demandé
    #Boucle pour cliquer sur "Charger plus" 5 fois
    for _ in range(5):
        await page.get_by_role("button", name="Charger plus").click()
        
    # Sélectionner toutes les balises <a> avec la classe spécifique et récupération du text
    sp500_ticker = await page.locator("a.tickerNameBox-GrtoTeat").all_inner_texts()
    print(sp500_ticker)
    
    await browser.close()
    

# 5) NIKKEY225 (Japon 225) VIA PLAYWRIGHT VIA TRAIDINGVIEW

async with async_playwright() as p:
    # Lancer le navigateur Chromium en mode asynchrone car sur Jupytair il faut être asynchrone
    browser = await p.chromium.launch(headless=True)  # headless=False pour voir le navigateur
    page = await browser.new_page() # Ouvre une nouvelle page
    
    await page.goto("https://fr.tradingview.com/symbols/TVC-NI225/components/") # Va sur l'URL demandé
    #Boucle pour cliquer sur "Charger plus" 2 fois
    for _ in range(2):
        await page.get_by_role("button", name="Charger plus").click()
        
    # Sélectionner toutes les balises <a> avec la classe spécifique et récupération du text
    japon_ticker = await page.locator("a.tickerNameBox-GrtoTeat").all_inner_texts()
    japon_ticker_yf = [ticker + ".T" for ticker in japon_ticker]
    
    await browser.close()
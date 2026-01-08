"""
Page de comparaison de TOUS les actifs (indices, stocks, cryptos)
"""
import streamlit as st
from src.models.control_datas.connexion_db_datas import *
from src.components.components_views import *

def actifs_page(go_to):
    
    # ================= CSS =================
    load_css()
    
    # ================= CONNEXIONS DB =================
    db_path="data.db"

    # Indices
    datas_indices = FinanceDatabaseIndice(db_path)
    liste_indices = datas_indices.get_list_indices()
    indice_default = "S&P 500"
    
    # Stocks
    datas_stocks = FinanceDatabaseStocks(db_path)
    liste_stocks = datas_stocks.get_list_stocks()
    stock_default = "Apple Inc."
    
    # Cryptos
    datas_cryptos = FinanceDatabaseCryptos(db_path)
    liste_cryptos = datas_cryptos.get_list_cryptos()
    crypto_default = "Bitcoin"
    
    # ================= TITRE =================
    display_page_title("COMPARAISON DES ACTIFS")
    
    # ================= RENDEMENTS MULTI-ACTIFS =================
    display_multi_actifs_rendement_section(
        datas_indices=datas_indices,
        datas_stocks=datas_stocks,
        datas_cryptos=datas_cryptos,
        liste_indices=liste_indices,
        liste_stocks=liste_stocks,
        liste_cryptos=liste_cryptos,
        indice_default=indice_default,
        stock_default=stock_default,
        crypto_default=crypto_default,
        calculate_rendement_func=calculate_rendement,
        style_rendement_func=style_rendement,
        default_periods=[6, 12, 24, 60, 120, 180]
    )
    
    # ================= BOUTON RETOUR =================
    bout_accueil(back_callback=go_to)
    
    # ================= FOOTER =================
    footer()
import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from src.controllers.LP_VS_DCA import *


st.set_page_config(layout="wide", page_title="DCA vs Lump Sum", page_icon="🏛️")
############################################ MISE EN PLACE DU CSS + IMAGE ############################################
# Chargement du fichier CSS
with open("src/assets/css/streamlit.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# CSS titre principal
#st.title("📊 LES INDICES BOURSIERS")
st.markdown(f"""<div class="main-container"><h1>LUMP SUM VS DCA</h1></div>""", unsafe_allow_html=True)
st.markdown(f"""<div class="main-container"><h2>🏛️ Simulation DCA vs Lump Sum</h2></div>""", unsafe_allow_html=True)

# Paramètres utilisateur
ticker = st.text_input("Ticker Yahoo Finance", value="^GSPC")
somme_investie = st.number_input("Montant à investir (€)", value=100000, step=1000)
# Durées d'investissement (en années) : saisie de l'utilisateur
durees_input = st.text_input("⏳ Durées d'investissement (en années)", "5,10,15,20,25")  # Format : 5,10,15,...
durees = [int(annee.strip()) for annee in durees_input.split(",")]

# Mois de DCA : saisie de l'utilisateur
mois_dca_list_input = st.text_input("📆 Mois de DCA", "6,12,24,48")  # Format : 6,12,24,...
mois_dca_list = [int(mois.strip()) for mois in mois_dca_list_input.split(",")]

if st.button("Lancer la simulation"):
    with st.spinner("Calcul en cours..."):
        df_resultats = calcul_rendements_durations(durees, mois_dca_list, somme_investie, ticker)
        df = calcul_multiple_rendements(durees, mois_dca_list, somme_investie, ticker)
        st.success("Calcul terminé.")
        

        st.markdown(f"""<div class="main-container"><h2>📈 Les montants finaux obtenus en fonction de la durée de vos placements — DCA vs LS</h2></div>""", unsafe_allow_html=True)
        fig = graphe_barre(df_resultats)
        st.plotly_chart(fig, use_container_width=True)


        st.markdown(f"""<div class="main-container"><h2>📈 Les évolutions de vos placements en fonctions du temps - DCA vs LS</h2></div>""", unsafe_allow_html=True)
        fig = graphe_line(df, somme_investie)
        st.plotly_chart(fig, use_container_width=True)

        
        st.markdown(f"""<div class="main-container"><h2>📈 Tableaux des rendements comparatifs DCA vs Lump Sum</h2></div>""", unsafe_allow_html=True)
        st.write("Tableau des montants finaux obtenus en fonction de la durée du placement — DCA vs LS")
        st.dataframe(df_resultats.head(10), use_container_width=True)
        st.write("Tableau des évolutions de vos placements en fonction du temps  — DCA vs LS")
        st.dataframe(df.head(10), use_container_width=True)


else:
    df_resultats = calcul_rendements_durations(durees=range(1, 26), mois_dca_list=[6, 12, 18, 24], somme_investie=100000, ticker="^GSPC")
    df = calcul_multiple_rendements(durees = [25, 20, 15, 10,5], mois_dca_list = [6, 12, 18, 24], somme_investie  = 100000, ticker = "^GSPC")
    
    
    st.markdown(f"""<div class="main-container"><h2>📈 Exemple: Montant final obtenu en fonction de la durée du placement — DCA vs LS</h2></div>""", unsafe_allow_html=True)
    fig = graphe_barre(df_resultats)
    st.plotly_chart(fig, use_container_width=True)
    
    
    st.markdown(f"""<div class="main-container"><h2>📈 Exemple : Evolution du placement en fonction du temps - DCA vs LS</h2></div>""", unsafe_allow_html=True)
    fig = graphe_line(df, somme_investie)
    st.plotly_chart(fig, use_container_width=True)
    
    
    st.markdown(f"""<div class="main-container"><h2>📈 Exemple : Tableau rendement comparatif DCA vs Lump Sum</h2></div>""", unsafe_allow_html=True)
    st.dataframe(df_resultats)


############################################### FOOTER ###############################################
st.markdown("""<div class="footer"> © 2025 Bastien M. - Projet finance — Tous droits réservés.</div>""", unsafe_allow_html=True)

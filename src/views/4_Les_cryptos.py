import streamlit as st
from streamlit.components.v1 import html
import sqlite3
import pandas as pd
import plotly.graph_objects as go
from base64 import b64encode # Convertir le chemin en une URL utilisable avec `st.markdown()` pour les photos
#from def_app import *
#connect_to_db, get_list_actif, get_infos_actif,  get_prix_date, calculate_rendement, style_rendement, get_composition_indice
#import indices_app  # Si tu as aussi du code pour les indices
#import etf_app  # Si tu as du code pour les ETF
#import lp_dca_app  # Si tu as du code pour DCA vs LumpSum
#import con_user_app
############################################### MISE EN PLACE DU CSS + IMAGE ###############################################
st.set_page_config(layout="wide", page_title="Accueil", page_icon="🏛️")

# Chargement du fichier CSS
with open("src/assets/css/streamlit.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)


####################################### MISE EN PLACE DU SQUELETTE STREAMLIT  #######################################

# CSS titre principal
#st.title("📊 LES INDICES BOURSIERS")
st.markdown(f"""<div class="main-container"><h1>LES CRYPTOS</h1></div>""", unsafe_allow_html=True)

st.markdown(f"""<div class="main-container"><p>
Coming soon...
</p></div>""", unsafe_allow_html=True)

# Footer en bas de page
st.markdown("""<div class="footer"> © 2025 Bastien M. - Projet finance — Tous droits réservés.</div>""", unsafe_allow_html=True)


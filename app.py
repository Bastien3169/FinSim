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
# Mettre venv : source .venv/bin/activate
# Arreter venv : deactivate

############################################### MISE EN PLACE DU CSS + IMAGE ###############################################
st.set_page_config(layout="wide", page_title="Accueil", page_icon="🏛️")

# Chargement du fichier CSS
with open("src/assets/css/streamlit.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)


# CSS pour centrer image
image_path = "src/assets/images/indices.jpeg"

with open(image_path, "rb") as img_file:
    encoded = b64encode(img_file.read()).decode()


# CSS image
st.markdown(f"""
<div class="main-container"><img src="data:image/jpeg;base64,{encoded}" class="center-image"></div>""", unsafe_allow_html=True)



####################################### MISE EN PLACE DU SQUELETTE STREAMLIT  #######################################

# CSS titre principal
#st.title("📊 LES INDICES BOURSIERS")
st.markdown(f"""<div class="main-container"><h1>COMPARER ET SIMULER LES ACTIFS FINANCIERS</h1></div>""", unsafe_allow_html=True)

st.markdown(f"""<div class="main-container"><p>
Un site permettant de simuler et comparer les performances d’un investissement en DCA (investissement progressif) versus Lump Sum (investissement en une fois). L’outil est conçu pour être accessible à tous, même pour ceux qui découvrent la bourse, les rendements et les différentes stratégies d’investissement. Il permet également de visualiser et comparer facilement différents actifs : actions, indices, cryptomonnaies, etc...<br>
Bonne visite et bon apprentissage !
</p></div>""", unsafe_allow_html=True)

# Footer en bas de page
st.markdown("""<div class="footer"> © 2025 Bastien M. - Projet finance — Tous droits réservés.</div>""", unsafe_allow_html=True)

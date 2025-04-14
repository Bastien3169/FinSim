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
st.markdown(f"""<div class="main-container"><h1>FINANCE PROJECT</h1></div>""", unsafe_allow_html=True)

st.markdown(f"""<div class="main-container"><p>Le projet consiste à développer une application Streamlit pour la gestion et l'analyse de données financières, principalement axée sur les indices boursiers et les actions. L'objectif est de collecter des données financières à partir de différentes sources, telles que des fichiers CSV et des API comme yfinance, et de les organiser dans une base de données relationnelle SQLite. Cette base contient des informations sur les indices (nom, ticker, pays, etc.), les entreprises (nom, secteur, capitalisation, etc.), et l'historique des prix. L'application permet aux utilisateurs de s'inscrire, se connecter et consulter ces données sous forme de graphiques et de tableaux. En plus de la gestion des utilisateurs, l'application permet de mettre à jour la base de données via un processus en plusieurs étapes, en scrappant les tickers, récupérant les données historiques des indices et entreprises, et nettoyant ces données avant leur insertion dans la base de données. Le projet inclut également une interface utilisateur conviviale, avec des fonctionnalités de session et de gestion d'erreurs pour assurer une expérience fluide.</p></div>""", unsafe_allow_html=True)

# Menu de navigation dans la barre latérale
#st.sidebar.title("Navigation")
#menu_options = ["Présentation","Datas indices", "Datas stocks", "Data ETF", "DCA VS LumpSum", "Connexion"]
#selected_page = st.sidebar.radio("Choisissez une page", menu_options)

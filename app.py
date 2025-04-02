import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
from base64 import b64encode # Convertir le chemin en une URL utilisable avec `st.markdown()` pour les photos
from def_app import *
#connect_to_db, get_list_actif, get_infos_actif,  get_prix_date, calculate_rendement, style_rendement, get_composition_indice
import indices_app  # Si tu as aussi du code pour les indices
#import etf_app  # Si tu as du code pour les ETF
#import lp_dca_app  # Si tu as du code pour DCA vs LumpSum
import con_user_app


st.set_page_config(page_title="Finance Project Dashboard", page_icon="📊", layout="wide")
    
############################################### MISE EN PLACE DU CSS + IMAGE ###############################################

# Chargement du fichier CSS
with open("css/streamlit.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# CSS pour centrer image
image_path = "images/indices.jpeg"

with open(image_path, "rb") as img_file:
    encoded = b64encode(img_file.read()).decode()

# CSS image
st.markdown(f"""
<div class="main-container"><img src="data:image/jpeg;base64,{encoded}" class="center-image"></div>""", unsafe_allow_html=True)



####################################### MISE EN PLACE DU SQUELETTE STREAMLIT  #######################################

# CSS titre principal
#st.title("📊 LES INDICES BOURSIERS")
st.markdown(f"""<div class="main-container"><h1>FINANCE PROJECT</h1></div>""", unsafe_allow_html=True)

# Menu de navigation dans la barre latérale
#st.sidebar.title("Navigation")
#menu_options = ["Présentation","Datas indices", "Datas stocks", "Data ETF", "DCA VS LumpSum", "Connexion"]
#selected_page = st.sidebar.radio("Choisissez une page", menu_options)


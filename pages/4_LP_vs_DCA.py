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
from src.models.users_db.models_db_users_test import AuthManager, AdminManager


st.set_page_config(layout="wide", page_title="DCA vs Lump Sum", page_icon="🏛️")

############################################ MISE EN PLACE DU CSS + IMAGE ############################################
# Chargement du fichier CSS
with open("src/assets/css/streamlit.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# CSS titre principal
#st.title("📊 LES INDICES BOURSIERS")
st.markdown(f"""<div class="main-container"><h1>LUMP SUM VS DCA</h1></div>""", unsafe_allow_html=True)


auth_manager = AuthManager()  # Instanciation de la classe AuthManager
user = auth_manager.get_current_user() # Vérifie s'il cookie existe et pas expiré

if user:
    st.success(f"Bienvenue, {user['username']} !")
    if st.button("Se déconnecter"):
        auth_manager.logout()
        st.rerun()
    
################################## CONNEXION .db ET RECUPERATION DATAS ET VARIABLES STREAMLIT ##################################
    # Connexion à la base SQLite
    db_path = "data.db"
    conn = connect_to_db(db_path)
    
    # Mise en place des paramètre pour les fonctions des requêtes SQL
    table_hist_actif = "historique_indices"
    actif = "S&P 500" 
    
    # Récupérer la liste des indices et leurs infos
    data_financiere = get_prix_date(conn, table_hist_actif, actif)
    
    
################################## STREAMLIT ##################################
    st.markdown(f"""<div class="main-container"><h2>🏛️ Simulation DCA vs Lump Sum</h2></div>""", unsafe_allow_html=True)
    # Paramètres utilisateur
    ticker = st.text_input("Ticker Yahoo Finance", value="^GSPC")
    somme_investie = st.number_input("Montant à investir (€)", value=100000, step=1000)
    # Durées d'investissement (en années) : saisie de l'utilisateur
    durees_input = st.text_input("⏳ Durées d'investissement (en années)", "5,10,15,20,25")  # Format : 5,10,15,...
    durees = [int(annee.strip()) for annee in durees_input.split(",")]
    
    # Mois de DCA : saisie de l'utilisateur
    mois_dca_list_input = st.text_input("📆 Mois de DCA", "6,12,24")  # Format : 6,12,24,...
    mois_dca_list = [int(mois.strip()) for mois in mois_dca_list_input.split(",")]
    
    if st.button("Lancer la simulation"):
        with st.spinner("Calcul en cours..."):
            df_resultats = calcul_rendements_durations(durees, mois_dca_list, somme_investie, ticker)
            df = calcul_multiple_rendements(durees, mois_dca_list, somme_investie, ticker)
            st.success("Calcul terminé.")
            
    
            st.markdown(f"""<div class="main-container"><h3>📈 Les montants finaux obtenus en fonction de la durée de vos placements</h3></div>""", unsafe_allow_html=True)
            fig = graphe_barre(df_resultats)
            st.plotly_chart(fig, use_container_width=True)
    
    
            st.markdown(f"""<div class="main-container"><h3>📈 Les évolutions de vos placements en fonctions du temps</h3></div>""", unsafe_allow_html=True)
            fig = graphe_line(df, somme_investie)
            st.plotly_chart(fig, use_container_width=True)
    
            
            st.markdown(f"""<div class="main-container"><h3>📋 Tableaux des rendements comparatifs DCA vs Lump Sum</h3></div>""", unsafe_allow_html=True)
            st.write("Tableau des montants finaux obtenus en fonction de la durée du placement — DCA vs LS")
            st.dataframe(df_resultats.head(10), use_container_width=True)
            st.write("Tableau des évolutions de vos placements en fonction du temps  — DCA vs LS")
            st.dataframe(df.head(10), use_container_width=True)
    
    
    else:
        df_resultats = calcul_rendements_durations(durees=range(1, 26), mois_dca_list=[6, 12, 18, 24], somme_investie=100000, ticker="^GSPC")
        df = calcul_multiple_rendements(durees = [25, 20, 15, 10,5], mois_dca_list = [6, 12, 18, 24], somme_investie  = 100000, ticker = "^GSPC")
        
        
        st.markdown(f"""<div class="main-container"><h3>📈 Exemple: Montant final obtenu en fonction de la durée du placement</h3></div>""", unsafe_allow_html=True)
        fig = graphe_barre(df_resultats)
        st.plotly_chart(fig, use_container_width=True)
        
        
        st.markdown(f"""<div class="main-container"><h3>📈 Exemple : Evolution du placement en fonction du temps</h3></div>""", unsafe_allow_html=True)
        fig = graphe_line(df, somme_investie)
        st.plotly_chart(fig, use_container_width=True)
        
        
        st.markdown(f"""<div class="main-container"><h3>📋 Exemple : Tableau des rendements comparatifs DCA vs LS</h3></div>""", unsafe_allow_html=True)
        st.dataframe(df_resultats)


# ===================================== VISIBLE SI PAS CONNECTE ==================================== # 
else:
    st.markdown("""<div class="auth-container">""", unsafe_allow_html=True)
    st.error("Connecte-toi ou inscris-toi pour faire les simulations de LS vs DCA ! ✅")
    
    menu = st.radio("Connexion ou Inscription ?", ["Connexion", "Inscription"],horizontal=True)

    # Se connecter
    if menu == "Connexion":
        username = st.text_input("Nom d'utilisateur")
        email = st.text_input("Votre email")
        password = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter"):
            success, message = auth_manager.login(email, password)
            if success:
                st.success(message)
                st.rerun()  # Force le rafraîchissement avec cookie pris en compte
            else:
                st.error(message)

    # S'inscrire
    elif menu == "Inscription":
        username = st.text_input("Nom d'utilisateur")
        email = st.text_input("Votre email")
        password = st.text_input("Mot de passe", type="password")
        confirm_password = st.text_input("Confirmez le mot de passe", type="password")

        if st.button("S'inscrire"):
            if password != confirm_password:
                st.error("❌ Les mots de passe ne correspondent pas")
            else:
                success, message = auth_manager.register(username, email, password)
                if not success:
                    st.error(message)
                else:
                    st.success(message)
                        

    st.markdown("""</div>""", unsafe_allow_html=True)

############################################### FOOTER ###############################################
st.markdown("""<div class="footer"> © 2025 Bastien M. - Projet finance — Tous droits réservés.</div>""", unsafe_allow_html=True)

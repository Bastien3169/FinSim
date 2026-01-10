import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Doit être mis en premier avec chargement de tte page avec du st.xxxx (comme il peut y en avoir dans les imports de fichier avec %)
st.set_page_config(layout="wide", page_title="DCA vs Lump Sum", page_icon="🏛️")

from src.controllers.LP_VS_DCA import *
#from src.controllers.connexion_db_datas import *
from src.models.control_datas.connexion_db_datas import *
from src.models.users_db.models_db_users_test import AuthManager, AdminManager



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
    
    # Création d'une instance de l'objet
    datas_indices = FinanceDatabaseIndice(db_path="data.db")
    
    # Appel méthodes
    liste_indices = datas_indices.get_list_indices()

    
################################## STREAMLIT ##################################
    st.markdown(f"""<div class="main-container"><h2>🏛️ Simulation DCA vs Lump Sum</h2></div>""", unsafe_allow_html=True)
    
    # Sélection de l’indice
    indice_default = "S&P 500"
    ticker = st.selectbox("Choisissez un indice pour le graphique", liste_indices, index=liste_indices.index(indice_default)) # arg1 : nom liste déroulante / arg2 : liste pour la liste déroulante / arg3 : opt par défaut de l'actif pour visualisation graph.

    # Paramètres utilisateur
    somme_investie = st.number_input("Montant à investir (€)", value=100000, step=1000)
    
    # Durées d'investissement (en années) : saisie de l'utilisateur
    durees_input = st.text_input("⏳ Durées d'investissement (en années)", "5,10,15,20,25")  # Format : 5,10,15,...
    durees = [int(annee.strip()) for annee in durees_input.split(",")]
    
    # Mois de DCA : saisie de l'utilisateur
    mois_dca_list_input = st.text_input("📆 Mois de DCA", "6,12,24")  # Format : 6,12,24,...
    mois_dca_list = [int(mois.strip()) for mois in mois_dca_list_input.split(",")]

    # Prend l'hist des prix du ticker
    data_financiere = datas_indices.get_prix_date(ticker)
    
    if st.button("Lancer la simulation"):
        with st.spinner("Calcul en cours..."):
            df_resultats = calcul_rendements_durations(durees, mois_dca_list, somme_investie, ticker)
            df = calcul_multiple_rendements(durees, mois_dca_list, somme_investie, ticker)
            st.success("Calcul terminé.")
            

            # Plot des montants finaux obtenus en fonction de la durée des placements
            st.markdown(f"""<div class="main-container"><h3>📈 Les montants finaux obtenus en fonction de la durée de vos placements</h3></div>""", unsafe_allow_html=True)
            fig = graphe_barre(df_resultats)
            st.plotly_chart(fig, use_container_width=True)
    

            # Plot de l'évolutions des placements en fonctions du temps
            st.markdown(f"""<div class="main-container"><h3>📈 Les évolutions de vos placements en fonctions du temps</h3></div>""", unsafe_allow_html=True)
            fig = graphe_line(df, somme_investie)
            st.plotly_chart(fig, use_container_width=True)
    
            # df des rendements comparatifs DCA vs LS
            st.markdown(f"""<div class="main-container"><h3>📋 Tableaux des rendements comparatifs DCA vs Lump Sum</h3></div>""", unsafe_allow_html=True)
            st.write("Tableau des montants finaux obtenus en fonction de la durée du placement — DCA vs LS")
            st.dataframe(df_resultats.tail(10), use_container_width=True)

            # df des évolutions des placements en fonction du temps  — DCA vs LS
            st.write("Tableau des évolutions de vos placements en fonction du temps  — DCA vs LS")
            st.dataframe(df.tail(10), use_container_width=True)
    
    
    else:
        df_resultats = calcul_rendements_durations(durees=range(1, 26), mois_dca_list=[6, 12, 18, 24], somme_investie=100000, ticker="S&P 500")
        df = calcul_multiple_rendements(durees = [25, 20, 15, 10,5], mois_dca_list = [6, 12, 18, 24], somme_investie  = 100000, ticker = "S&P 500")
        
        
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

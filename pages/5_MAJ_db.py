import sqlite3
import hashlib
import streamlit as st
from datetime import datetime
from src.models.users_db.models_db_users import *


########################################## INITIALISE LA BASE DE DONNEE "users.db" ##########################################

init_db(db_path)


########################################## INTERFACE CSS PRINCIPALE ##########################################

with open("src/assets/css/streamlit.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

st.markdown("""<div class="main-container"><h1>MISE À JOUR BASE DE DONNÉE</h1></div>""", 
            unsafe_allow_html=True)



# ===================================== VISIBLE SI CONNECTE ==================================== #
if "user" in st.session_state:
    st.success(f"Bienvenue, {st.session_state.user} !")
    logout()

    # CSS titre et sous-titre
    st.markdown(f"""<div class="main-container"><h1>MISE A JOUR BASE DE DONNEE</h1></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="main-container"><h2>🔄 Mise à jour</h2></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="main-container"><p>La mise à jour peut prendre entre 20 et 30 minutes</p></div>""", unsafe_allow_html=True)

    
    if st.button("Cliquez ici pour mettre à jour la base de données"):
        progress_bar = st.progress(0)
        
        try:
            # Étape 1/6
            progress_bar.progress(17)
            composition_indices.csv_indices(dossier_csv)
            st.write("✅ Étape 1 terminée - Scraping des tickers et composition des indices enregistrés")
            
            # Étape 2/6
            progress_bar.progress(34)
            infos_stocks.infos_stocks(dossier_csv)
            st.write("✅ Étape 2 terminée - Informations des entreprises enregistrées")
            
            # Étape 3/6
            progress_bar.progress(50)
            infos_indices.infos_indices(dossier_csv)
            st.write("✅ Étape 3 terminée - Informations des indices enregistrées")
            
            # Étape 4/6
            progress_bar.progress(67)
            hist_indices.recuperer_et_clean_indices(dossier_csv)
            st.write("✅ Étape 4 terminée - Historique des indices enregistré")
            
            # Étape 5/6
            progress_bar.progress(83)
            hist_stocks.recuperer_et_clean_stocks(dossier_csv)
            st.write("✅ Étape 5 terminée - Historique des entreprise enregistré")
            
            # Étape 6/6
            progress_bar.progress(100)
            sql_datas.main_creation_db(dossier_csv, db_path)
            st.write("✅ Étape 6 terminée - Base de donnée enregistrée")
            
            st.success("✅ ✅ Base de données mise à jour avec succès !")
            
        except Exception as e:
            st.error(f"❌ Erreur : {e}")
            progress_bar.progress(0)  # Réinitialise en cas d'erreur Configuration des utilisateurs (remplace par une base de 


# ===================================== VISIBLE SI PAS CONNECTE ==================================== #
    
else:
    st.markdown("""<div class="auth-container">""", unsafe_allow_html=True)
    st.error("Connecte-toi ou inscris-toi pour mettre à jour la base de données ! ✅")
    
    choice = st.radio("Connexion ou Inscription ?", ["Connexion", "Inscription"],horizontal=True)

    # Conncexion user
    if choice == "Connexion":
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter"):
            error_msg = login(username, password, db_path)
            if error_msg:
                st.error(error_msg)
            else:
                st.session_state.user = username
                st.success(f"Connexion réussie. Bienvenue {username} ! Tu peux à présent te connecter.")
                st.rerun()
        
    # Inscription user
    if choice == "Inscription":
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        confirm_password = st.text_input("Confirmez le mot de passe", type="password")
        if st.button("S'inscrire"):
            if password == confirm_password:
                result = register(username, password, db_path)
                if result.startswith("✅"):
                    st.success(result)
                else:
                    st.error(result)
            else:
                st.error("❌ Les mots de passe ne correspondent pas")
           
    
    st.markdown("""</div>""", unsafe_allow_html=True)
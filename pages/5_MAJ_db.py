import sqlite3
import hashlib
import pandas as pd
import streamlit as st
from datetime import datetime
from src.models.datas_db.main_db_datas import *
from src.models.users_db.models_db_users_test import AuthManager, AdminManager


st.set_page_config(layout="wide", page_title="DCA vs Lump Sum", page_icon="🏛️")

############################################ MISE EN PLACE DU CSS + TITRE DE PAGE ############################################
# Chargement du fichier CSS
with open("src/assets/css/streamlit.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

#st.title("📊 LES INDICES BOURSIERS")
st.markdown(f"""<div class="main-container"><h1>👑 ADMINISTRATEUR : MISE À JOUR DES BDD</h1></div>""", unsafe_allow_html=True)


auth_manager = AuthManager() # Instanciation de la classe AuthManager
admin_manager = AdminManager()  # Instanciation de la classe AdminManager

################################## CREATION ADMIN VIA BOUTON QUI DISPARAIT SI ADMIN EXISTE##################################
user = auth_manager.get_current_user()
admin_exists = False

# On cherche 'admin' dans la table
for i in admin_manager.get_all_users():
    if i[1] == 'admin':  # Si on trouve un admin
        admin_exists = True
        break  # On sort de la boucle dès qu'on trouve un admin

# Si 'admin' existe, message ok
if admin_exists:
    st.success("👑 L'utilisateur admin existe déjà.")
# Si 'admin' existe pas, création bouton unique pour créer admin
else:
    st.warning("Aucun compte administrateur détecté.")
    if st.button("Créer l'utilisateur admin initial"):
        admin_manager.create_admin_user('admin', 'jolie.mountain@gmail.com', 'Admin#1')
        st.success("👑 Admin créé avec succès")
        st.rerun()


################################## VISIBLE SI PAS ADMIN ##################################
if user is None or user.get("role") != "admin":
    st.warning("Accès réservé aux administrateurs.")
    
    email = st.text_input("Email administrateur")
    password = st.text_input("Mot de passe", type="password")
    
    if st.button("Se connecter"):
        success, message = auth_manager.login(email, password)
        
        if success:
            current_user = auth_manager.get_current_user()
            
            if current_user and current_user.get("role") == "admin":
                st.success("✅ Connexion réussie, bienvenue administrateur !")
                st.rerun()
            else:
                auth_manager.logout()
                st.error("❌ Accès refusé : vous n'avez pas les droits administrateur.")
        else:
            st.error(message)


################################## VISIBLE SI ADMIN CONNECTE ##################################
if user and user.get("role") == "admin":

################################## BDD DATAS ##################################
    #init_db(db_path)
    st.markdown(f"""<div class="main-container"><h2>🔄 Mise à jours BDD datas</h2></div>""", unsafe_allow_html=True)
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
            progress_bar.progress(0)  # Réinitialise en cas d'erreur Configuration des utilisateurs


    
################################## BDD USER ##################################
    
    st.markdown(f"""<div class="main-container"><h2>📝 Modifications BDD users</h2></div>""", unsafe_allow_html=True)

#--------------------------- Trouver un utilisateur par email ou username ---------------------------#
    search = st.text_input("Rechercher un utilisateur par email ou username")

    # Bouton pour valider la recherche
    if st.button("Valider la recherche", key="valider_recherche"):
        # Si un email est saisi, on effectue la recherche
        if search:
            # Utiliser la méthode get_user_by_email pour obtenir l'utilisateur correspondant
            user = admin_manager.get_user_by_email_username(search)
            
            # Si un utilisateur est trouvé
            if user:

                # Affichage de l'en-tête du tableau
                headers = ["🆔 ID", "👤 Username", "📧 Email", "🔐 Rôle", "🗓️ Date d'inscription", "🗑️ Supprimer", "✏️ Modifier"]
                col_h1, col_h2, col_h3, col_h4, col_h5, col_h6, col_h7 = st.columns([1, 2, 3, 1, 2, 2, 2])
                for col, header in zip([col_h1, col_h2, col_h3, col_h4, col_h5, col_h6, col_h7], headers):
                    with col:
                        st.markdown(f"<b style='color: #00B388;'>{header}</b>",unsafe_allow_html=True)
                
                id, username, email, role, registration_date = user
                col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 2, 3, 1, 2, 2, 2])
                with col1:
                    st.write(id)
                with col2:
                    st.write(username)
                with col3:
                    st.write(email)
                with col4:
                    st.write(role)
                with col5:
                    st.write(registration_date)
                with col6:
                    if st.button("Supprimer", key=f"btn_supprimer_rech_{email}"):
                        admin_manager.delete_user(email)
                        st.success(f"Utilisateur {username} supprimé.")
                        st.rerun()
                with col7:
                    if st.button("Modifier", key=f"btn_modifier_rech_{email}"):
                        st.session_state[f"editing_{email}"] = True   
        
                if st.session_state.get(f"editing_{email}", False):
                    st.markdown(f"""<div class="main-container"><h3>Modifications user</h3></div>""", unsafe_allow_html=True)
                    new_username = st.text_input("Nouveau nom d'utilisateur", value=username)
                    new_role = st.radio("Nouveau rôle", ['admin', 'user'], index=0 if role == 'admin' else 1)
        
                    # Réinitialisation d'un mdp par '0000'
                    st.markdown(f"""<div class="main-container"><h3>Réinitialiser le mot de passe</h3></div>""", unsafe_allow_html=True)
                    if st.button("Réinitialiser le mot de passe", key=f"reset_rech_{id}"):
                        # Demander un nouveau mot de passe via un champ de texte
                        new_password = st.text_input("Nouveau mot de passe", type='password', max_chars=20)
                        
                        if new_password:
                            admin_manager.update_user(email=email, password=new_password)
                            st.success(f"Mot de passe de {username} réinitialisé à {new_password}.")
                            st.rerun()
                        else:
                            st.warning("Veuillez entrer un mot de passe.")
        
                    # Valider les modifications
                    st.markdown(f"""<div class="main-container"><h3>Valider les modifications</h3></div>""", unsafe_allow_html=True)
                    if st.button("Valider les modifications", key=f"submit_rech_{email}"):
                        admin_manager.update_user(email=email, username=new_username, role=new_role)
                        st.success(f"✅ Utilisateur {new_username} modifié avec succès.")
                        st.session_state[f"editing_{email}"] = False
                        st.rerun()
            else:
                st.warning("Aucun utilisateur trouvé avec cet email.")
    

#--------------------------- Version Desktop ---------------------------#
    mobile_mode = st.checkbox("💡 Activer l'affichage mobile")

    if not mobile_mode:
        headers = ["🆔 ID", "👤 Username", "📧 Email", "🔐 Rôle", "🗓️ Date d'inscription", "🗑️ Supprimer", "✏️ Modifier"]
        cols = st.columns([1, 2, 3, 1, 2, 2, 2])
        for i, header in enumerate(headers):
            with cols[i]:
                st.markdown(f"<b style='color: #00B388;'>{header}</b>",unsafe_allow_html=True)
    
        for user in admin_manager.get_all_users():
            id, username, email, role, registration_date = user
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 2, 3, 1, 2, 2, 2])
            with col1:
                st.write(id)
            with col2:
                st.write(username)
            with col3:
                st.write(email)
            with col4:
                st.write(role)
            with col5:
                st.write(registration_date)
            with col6:
                if st.button("Supprimer", key=f"btn_supprimer_{email}"):
                    admin_manager.delete_user(email)
                    st.success(f"Utilisateur {username} supprimé.")
                    st.experimental_rerun()
            with col7:
                if st.button("Modifier", key=f"btn_modifier_{email}"):
                    st.session_state[f"editing_{email}"] = True


            # MODIFICATIONS USERS !!!
            if st.session_state.get(f"editing_{email}", False):
                with st.expander("CLIQUER POUR DEPLIER ET MODIFIER", expanded=True):
                    
                    # Changer nom utilisateur
                    st.markdown(f"""<div class="main-container"><h3>Modifier nom d'utilisateur</h3></div>""", unsafe_allow_html=True)
                    new_username = st.text_input("", value=username)

                    # Changer rôle utilisateur
                    st.markdown(f"""<div class="main-container"><h3>Modifier rôle utilisateur</h3></div>""", unsafe_allow_html=True)
                    new_role = st.radio("", ['admin', 'user'], index=0 if role == 'admin' else 1)
        
                    # Réinitialisation d'un mdp par '0000'
                    st.markdown(f"""<div class="main-container"><h3>Réinitialiser le mot de passe</h3></div>""", unsafe_allow_html=True)
                    if st.button("Réinitialiser le mot de passe", key=f"reset_{id}"):
                        # Demander un nouveau mot de passe via un champ de texte
                        new_password = st.text_input("Nouveau mot de passe", type='password', max_chars=20)    
                        if new_password:
                            admin_manager.update_user(email=email, password=new_password)
                            st.success(f"Mot de passe de {username} réinitialisé à {new_password}.")
                            st.rerun()
                        else:
                            st.warning("Veuillez entrer un mot de passe.")
        
                    # Valider les modifs
                    st.markdown(f"""<div class="main-container"><h3>Valider les modifications</h3></div>""", unsafe_allow_html=True)
                    if st.button("Valider les modifications", key=f"submit_{email}"):
                        admin_manager.update_user(email=email, username=new_username, role=new_role)
                        st.success(f"✅ Utilisateur {new_username} modifié avec succès.")
                        st.session_state[f"editing_{email}"] = False
                        st.rerun()


#--------------------------- Version mobile ---------------------------#
 
    else:
        st.markdown("### Mode mobile activé")
        # Récupération des utilisateurs
        users = admin_manager.get_all_users()

        df = pd.DataFrame(users)
        # Affichage avec st.dataframe()
        st.dataframe(df, use_container_width=True)
        
        if not users:
            st.info("Aucun utilisateur enregistré.")
        else:
            # Barre de recherche
            search_query = st.text_input("🔍 Rechercher un utilisateur (nom ou email)").lower()
    
            # Filtrage
            filtered_users = [u for u in users if search_query in u[1].lower() or search_query in u[2].lower()]
    
            if not filtered_users:
                st.warning("Aucun utilisateur ne correspond à la recherche.")
            else:
                # Initialisation de l'index
                if "user_index" not in st.session_state:
                    st.session_state.user_index = 0
    
                # Données utilisateur affiché
                id, username, email, role, registration_date = filtered_users[st.session_state.user_index]
    
                st.markdown("---")
                st.write(f"**🆔 ID :** {id}")
                st.write(f"**👤 Nom d'utilisateur :** `{username}`")
                st.write(f"**📧 Email :** `{email}`")
                st.write(f"**🔐 Rôle :** `{role}`")
                st.write(f"**🗓️ Date d'inscription :** {registration_date}")
    
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Supprimer", key=f"btn_supprimer_{email}"):
                        admin_manager.delete_user(email)
                        st.success(f"Utilisateur {username} supprimé.")
                        st.experimental_rerun()
                with col2:
                    if st.button("Modifier", key=f"btn_modifier_{email}"):
                        st.session_state[f"editing_{email}"] = True


                # MODIFICATIONS USERS !!!
                if st.session_state.get(f"editing_{email}", False):
                    with st.expander("CLIQUER POUR DEPLIER ET MODIFIER", expanded=True):
                        
                        # Changer nom utilisateur
                        st.markdown(f"""<div class="main-container"><h3>Modifier nom d'utilisateur</h3></div>""", unsafe_allow_html=True)
                        new_username = st.text_input("", value=username)
    
                        # Changer rôle utilisateur
                        st.markdown(f"""<div class="main-container"><h3>Modifier rôle utilisateur</h3></div>""", unsafe_allow_html=True)
                        new_role = st.radio("", ['admin', 'user'], index=0 if role == 'admin' else 1)
            
                        # Réinitialisation d'un mdp par '0000'
                        st.markdown(f"""<div class="main-container"><h3>Réinitialiser le mot de passe</h3></div>""", unsafe_allow_html=True)
                        if st.button("Réinitialiser le mot de passe", key=f"reset_{id}"):
                            # Demander un nouveau mot de passe via un champ de texte
                            new_password = st.text_input("Nouveau mot de passe", type='password', max_chars=20)    
                            if new_password:
                                admin_manager.update_user(email=email, password=new_password)
                                st.success(f"Mot de passe de {username} réinitialisé à {new_password}.")
                                st.rerun()
                            else:
                                st.warning("Veuillez entrer un mot de passe.")
            
                        # Valider les modifs
                        st.markdown(f"""<div class="main-container"><h3>Valider les modifications</h3></div>""", unsafe_allow_html=True)
                        if st.button("Valider les modifications", key=f"submit_{email}"):
                            admin_manager.update_user(email=email, username=new_username, role=new_role)
                            st.success(f"✅ Utilisateur {new_username} modifié avec succès.")
                            st.session_state[f"editing_{email}"] = False
                            st.rerun()
        

############################################### FOOTER ###############################################
st.markdown("""<div class="footer"> © 2025 Bastien M. - Projet finance — Tous droits réservés.</div>""", unsafe_allow_html=True)

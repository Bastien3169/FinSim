import sqlite3
import hashlib
import streamlit as st
from datetime import datetime
from src.models.users_db.models_db_users import *
from src.models.users_db.models_db_usersV2 import AuthManager, AdminManager


st.set_page_config(layout="wide", page_title="DCA vs Lump Sum", page_icon="🏛️")

############################################ MISE EN PLACE DU CSS + TITRE DE PAGE ############################################
# Chargement du fichier CSS
with open("src/assets/css/streamlit.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

#st.title("📊 LES INDICES BOURSIERS")
st.markdown(f"""<div class="main-container"><h1>MISE À JOUR DES BASES DE DONNÉES : 👑 ADMINISTRATEUR</h1></div>""", unsafe_allow_html=True)


################################## CREATION ADMIN VIA BOUTON QUI DISPARAIT SI ADMIN EXISTE##################################
admin_manager = AdminManager()  # Instanciation de la classe AdminManager
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


################################## VISIBLE SI ADMIN ##################################
if st.session_state.get('role') != 'admin':
    st.warning("Accès réservé aux administrateurs.")
    username = st.text_input("Nom admin")
    email = st.text_input("Votre email admin")
    password = st.text_input("Mot de passe admin", type="password")
    if st.button("Se connecter"):
        # Vérification des identifiants
        if username == 'admin' and email == 'jolie.mountain@gmail.com' and password == 'Admin#1':
            st.session_state['user'] = username  # Sauvegarde de l'utilisateur dans la session
            st.session_state['role'] = 'admin'  # Sauvegarde du rôle
            st.success(f"Connexion réussie, bienvenue {username} !")
            st.rerun()
            
        else:
            st.error("Identifiants incorrects.")


################################## VISIBLE SI ADMIN CONNECTE ##################################
if st.session_state.get('role') == 'admin':

################################## BDD DATAS ##################################
    init_db(db_path)
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
#--------------------------- Trouver un utilisateur par email ---------------------------#
    st.markdown(f"""<div class="main-container"><h3>Rechercher un utilisateur par email</h3></div>""", unsafe_allow_html=True)
    search_email = st.text_input("Rechercher un utilisateur par email")

    # Bouton pour valider la recherche
    if st.button("Valider la recherche", key="valider_recherche"):
        # Si un email est saisi, on effectue la recherche
        if search_email:
            # Utiliser la méthode get_user_by_email pour obtenir l'utilisateur correspondant
            user = admin_manager.get_user_by_email(search_email)
            
            # Si un utilisateur est trouvé
            if user:
                id, username, email, role, registration_date = user
                col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 3, 1, 2, 2, 2])
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
    

#--------------------------- Afficher les utilisateurs inscris et modifier un utilisateur ---------------------------#
    # Afficher tableau des utilisateurs
    for user in admin_manager.get_all_users():
        id, username, email, role, registration_date = user
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 3, 1, 2, 2, 2])
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
                st.rerun()
        with col7:
            if st.button("Modifier", key=f"btn_modifier_{email}"):
                st.session_state[f"editing_{email}"] = True   

        
        if st.session_state.get(f"editing_{email}", False):    

            with st.container():
                
                # Changer rôle utilisateur (user ou admin)
                st.markdown(f"""<div class="main-container"><h3>Modifications user</h3></div>""", unsafe_allow_html=True)
                new_username = st.text_input("Nouveau nom d'utilisateur", value=username)
                new_role = st.radio("Nouveau rôle", ['admin', 'user'], index=0 if role == 'admin' else 1)
    
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
    
                #définit l'index par défaut. Si rôle ="admin", l'index = 0 (le premier élément, "admin"), sinon = 1 (le second élément, "user").
                st.markdown(f"""<div class="main-container"><h3>Valider les modifications</h3></div>""", unsafe_allow_html=True)
                if st.button("Valider les modifications", key=f"submit_{email}"):
                    admin_manager.update_user(email=email, username=new_username, role=new_role)
                    st.success(f"✅ Utilisateur {new_username} modifié avec succès.")
                    st.session_state[f"editing_{email}"] = False
                    st.rerun()
    
                st.markdown("""</div>""", unsafe_allow_html=True)
            st.markdown("""<div class="modif_user">""", unsafe_allow_html=True)

############################################### FOOTER ###############################################
st.markdown("""<div class="footer"> © 2025 Bastien M. - Projet finance — Tous droits réservés.</div>""", unsafe_allow_html=True)

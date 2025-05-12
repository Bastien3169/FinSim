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


# ===================================== VISIBLE SI ADMIN EXISTE ##################################
# Vérifie si un admin existe déjà
for i in admin_manager.get_all_users():
    if i[1] == 'admin':  # Si on trouve un admin
        admin_exists = True
        st.success("👑 L'utilisateur admin existe déjà.")
        break  # On sort de la boucle dès qu'on trouve un admin


# ===================================== VISIBLE SI ADMIN EXISTE PAS ##################################
# Si aucun admin n'a été trouvé après la boucle
if not admin_exists:
    st.warning("Aucun compte administrateur détecté.")
    if st.button("Créer l'utilisateur admin initial"):
        admin_manager.create_admin_user('admin', 'jolie.mountain@gmail.com', 'Admin#1')
        st.success("👑 Admin créé avec succès")
        st.rerun()  # Utiliser st.rerun() au lieu de st.stop() pour rafraîchir la page


################################## VISIBLE SI ADMIN EXISTE MAIS PAS CONNECTE ##################################
if 'user' not in st.session_state or st.session_state.get('role') != 'admin':
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
            st.stop()  # Stoppe le script si les identifiants sont invalides


################################## VISIBLE SI ADMIN CONNECTE ##################################
if 'user' in st.session_state or st.session_state.get('role') == 'admin':
    st.subheader("Liste des utilisateurs")




############################################### FOOTER ###############################################
st.markdown("""<div class="footer"> © 2025 Bastien M. - Projet finance — Tous droits réservés.</div>""", unsafe_allow_html=True)

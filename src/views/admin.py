import sqlite3
import hashlib
import pandas as pd
import streamlit as st
from datetime import datetime
from src.components.components_views import *
from src.models.datas_db.main_db_datas import *


def admin_page(go_to):
    ############################################ MISE EN PLACE DU CSS + TITRE DE PAGE ############################################
    load_css()
    display_page_title("👑 ADMINISTRATEUR : MISE À JOUR DES BDD")

    # ⭐ RÉCUPÉRER L'INSTANCE EXISTANTE (créée dans main.py)
    auth_manager = st.session_state.auth_manager

    ################################## BDD DATAS ##################################
    st.markdown(f"""<div class="main-container"><h2>🔄 Mise à jours BDD datas</h2></div>""", 
                unsafe_allow_html=True)
    st.markdown(f"""<div class="main-container"><p>La mise à jour peut prendre entre 20 et 30 minutes</p></div>""", 
                unsafe_allow_html=True)

    dossier_csv = "csv"
    csv_bdd = "csv/csv_bdd"
    db_path = "datas.bd"

    if st.button("Cliquez ici pour mettre à jour la base de données"):
        progress_bar = st.progress(0)

        try:
            # Étape 1/6
            progress_bar.progress(17)
            composition_indices.csv_indices(dossier_csv)
            st.write("✅ Étape 1 terminée - Scraping des tickers et composition des indices enregistrés")

            # Étape 2/6
            progress_bar.progress(34)
            infos_stocks.infos_stocks(dossier_csv, csv_bdd)
            st.write("✅ Étape 2 terminée - Informations des entreprises enregistrées")

            # Étape 3/6
            progress_bar.progress(50)
            infos_indices.infos_indices(dossier_csv, csv_bdd)
            st.write("✅ Étape 3 terminée - Informations des indices enregistrées")

            # Étape 4/6
            progress_bar.progress(67)
            hist_indices.recuperer_et_clean_indices(csv_bdd)
            st.write("✅ Étape 4 terminée - Historique des indices enregistré")

            # Étape 5/6
            progress_bar.progress(83)
            hist_stocks.recuperer_et_clean_stocks(csv_bdd)
            st.write("✅ Étape 5 terminée - Historique des entreprise enregistré")

            # Étape 6/6
            progress_bar.progress(100)
            sql_datas.main_creation_db(csv_bdd, db_path)
            st.write("✅ Étape 6 terminée - Base de donnée enregistrée")

            st.success("✅ ✅ Base de données mise à jour avec succès !")

        except Exception as e:
            st.error(f"❌ Erreur : {e}")
            progress_bar.progress(0)

    ################################## BDD USER ##################################
    st.markdown(f"""<div class="main-container"><h2>📝 Modifications BDD users</h2></div>""", 
                unsafe_allow_html=True)

    # --------------------------- Trouver un utilisateur par email ou username ---------------------------#
    search = st.text_input("Rechercher un utilisateur par email ou username")

    if st.button("Valider la recherche", key="valider_recherche"):
        if search:
            user_found = get_user_by_email_or_username(auth_manager.db_path, search)

            if user_found:
                headers = ["🆔 ID", "👤 Username", "📧 Email", "🔐 Rôle",
                          "🗓️ Date d'inscription", "🗑️ Supprimer", "✏️ Modifier"]
                col_h1, col_h2, col_h3, col_h4, col_h5, col_h6, col_h7 = st.columns([1, 2, 3, 1, 2, 2, 2])
                for col, header in zip([col_h1, col_h2, col_h3, col_h4, col_h5, col_h6, col_h7], headers):
                    with col:
                        st.markdown(f"<b style='color: #00B388;'>{header}</b>", unsafe_allow_html=True)

                id, username, email, role, registration_date = user_found
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
                        delete_user(auth_manager.db_path, email)
                        st.success(f"Utilisateur {username} supprimé.")
                        st.rerun()
                with col7:
                    if st.button("Modifier", key=f"btn_modifier_rech_{email}"):
                        st.session_state[f"editing_{email}"] = True

                if st.session_state.get(f"editing_{email}", False):
                    st.markdown(f"""<div class="main-container"><h3>Modifications user</h3></div>""", 
                              unsafe_allow_html=True)
                    new_username = st.text_input("Nouveau nom d'utilisateur", value=username, 
                                                key=f"rech_username_{email}")
                    new_role = st.radio("Nouveau rôle", ['admin', 'user'], 
                                      index=0 if role == 'admin' else 1, key=f"rech_role_{email}")

                    st.markdown(f"""<div class="main-container"><h3>Réinitialiser le mot de passe</h3></div>""", 
                              unsafe_allow_html=True)
                    new_password = st.text_input("Nouveau mot de passe", type='password', 
                                                max_chars=20, key=f"rech_pwd_{id}")
                    
                    if st.button("Réinitialiser le mot de passe", key=f"reset_rech_{id}"):
                        if new_password:
                            update_user(auth_manager.db_path, email, auth_manager, password=new_password)
                            st.success(f"Mot de passe de {username} réinitialisé.")
                            st.rerun()
                        else:
                            st.warning("Veuillez entrer un mot de passe.")

                    st.markdown(f"""<div class="main-container"><h3>Valider les modifications</h3></div>""", 
                              unsafe_allow_html=True)
                    if st.button("Valider les modifications", key=f"submit_rech_{email}"):
                        update_user(auth_manager.db_path, email, auth_manager, username=new_username, role=new_role)
                        st.success(f"✅ Utilisateur {new_username} modifié avec succès.")
                        st.session_state[f"editing_{email}"] = False
                        st.rerun()
            else:
                st.warning("Aucun utilisateur trouvé avec cet email.")

    # --------------------------- Version Desktop ---------------------------#
    mobile_mode = st.checkbox("💡 Activer l'affichage mobile")

    if not mobile_mode:
        headers = ["🆔 ID", "👤 User", "📧 Email", "🔐 Rôle",
                  "🗓️ Date inscription", "🗑️ Delete", "✏️ Modifier"]
        cols = st.columns([1, 1, 2, 1, 2, 1, 1])
        for i, header in enumerate(headers):
            with cols[i]:
                st.markdown(f"<b style='color: #00B388;'>{header}</b>", unsafe_allow_html=True)

        all_users = get_all_users(auth_manager.db_path)
        for user_item in all_users:
            id, username, email, role, registration_date = user_item
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 2, 1, 2, 1, 1])
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
                if st.button("🗑️", key=f"btn_supprimer_{email}"):
                    delete_user(auth_manager.db_path, email)
                    st.success(f"Utilisateur {username} supprimé.")
                    st.rerun()
            with col7:
                if st.button("✏️", key=f"btn_modifier_{email}"):
                    st.session_state[f"editing_{email}"] = True

            if st.session_state.get(f"editing_{email}", False):
                with st.expander("CLIQUER POUR DEPLIER ET MODIFIER", expanded=True):
                    st.markdown(f"""<div class="main-container"><h3>Modifier nom d'utilisateur</h3></div>""", 
                              unsafe_allow_html=True)
                    new_username = st.text_input("", value=username, key=f"desktop_username_{email}")

                    st.markdown(f"""<div class="main-container"><h3>Modifier rôle utilisateur</h3></div>""", 
                              unsafe_allow_html=True)
                    new_role = st.radio("", ['admin', 'user'], 
                                      index=0 if role == 'admin' else 1, key=f"desktop_role_{email}")

                    st.markdown(f"""<div class="main-container"><h3>Réinitialiser le mot de passe</h3></div>""", 
                              unsafe_allow_html=True)
                    new_password = st.text_input("Nouveau mot de passe", type='password', 
                                                max_chars=20, key=f"desktop_pwd_{id}")
                    
                    if st.button("Réinitialiser le mot de passe", key=f"reset_{id}"):
                        if new_password:
                            update_user(auth_manager.db_path, email, auth_manager, password=new_password)
                            st.success(f"Mot de passe de {username} réinitialisé.")
                            st.rerun()
                        else:
                            st.warning("Veuillez entrer un mot de passe.")

                    st.markdown(f"""<div class="main-container"><h3>Valider les modifications</h3></div>""", 
                              unsafe_allow_html=True)
                    if st.button("Valider les modifications", key=f"submit_{email}"):
                        update_user(auth_manager.db_path, email, auth_manager, username=new_username, role=new_role)
                        st.success(f"✅ Utilisateur {new_username} modifié avec succès.")
                        st.session_state[f"editing_{email}"] = False
                        st.rerun()

    # --------------------------- Version mobile ---------------------------#
    else:
        st.markdown("### Mode mobile activé")
        users = get_all_users(auth_manager.db_path)
        
        if users:
            df = pd.DataFrame(users, columns=["ID", "Username", "Email", "Role", "Date inscription"])
            st.dataframe(df, use_container_width=True)

            search_query = st.text_input("🔍 Rechercher un utilisateur (nom ou email)").lower()
            filtered_users = [u for u in users if search_query in u[1].lower() or search_query in u[2].lower()]

            if not filtered_users:
                st.warning("Aucun utilisateur ne correspond à la recherche.")
            else:
                if "user_index" not in st.session_state:
                    st.session_state.user_index = 0

                id, username, email, role, registration_date = filtered_users[st.session_state.user_index]

                st.markdown("---")
                st.write(f"**🆔 ID :** {id}")
                st.write(f"**👤 Nom d'utilisateur :** `{username}`")
                st.write(f"**📧 Email :** `{email}`")
                st.write(f"**🔐 Rôle :** `{role}`")
                st.write(f"**🗓️ Date d'inscription :** {registration_date}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Supprimer", key=f"btn_supprimer_mobile_{email}"):
                        delete_user(auth_manager.db_path, email)
                        st.success(f"Utilisateur {username} supprimé.")
                        st.rerun()
                with col2:
                    if st.button("Modifier", key=f"btn_modifier_mobile_{email}"):
                        st.session_state[f"editing_{email}"] = True

                if st.session_state.get(f"editing_{email}", False):
                    with st.expander("CLIQUER POUR DEPLIER ET MODIFIER", expanded=True):
                        st.markdown(f"""<div class="main-container"><h3>Modifier nom d'utilisateur</h3></div>""", 
                                  unsafe_allow_html=True)
                        new_username = st.text_input("", value=username, key=f"mobile_username_{email}")

                        st.markdown(f"""<div class="main-container"><h3>Modifier rôle utilisateur</h3></div>""", 
                                  unsafe_allow_html=True)
                        new_role = st.radio("", ['admin', 'user'], 
                                          index=0 if role == 'admin' else 1, key=f"mobile_role_{email}")

                        st.markdown(f"""<div class="main-container"><h3>Réinitialiser le mot de passe</h3></div>""", 
                                  unsafe_allow_html=True)
                        new_password = st.text_input("Nouveau mot de passe", type='password', 
                                                    max_chars=20, key=f"mobile_pwd_{id}")
                        
                        if st.button("Réinitialiser le mot de passe", key=f"mobile_reset_{id}"):
                            if new_password:
                                update_user(auth_manager.db_path, email, auth_manager, password=new_password)
                                st.success(f"Mot de passe de {username} réinitialisé.")
                                st.rerun()
                            else:
                                st.warning("Veuillez entrer un mot de passe.")

                        st.markdown(f"""<div class="main-container"><h3>Valider les modifications</h3></div>""", 
                                  unsafe_allow_html=True)
                        if st.button("Valider les modifications", key=f"mobile_submit_{email}"):
                            update_user(auth_manager.db_path, email, auth_manager, username=new_username, role=new_role)
                            st.success(f"✅ Utilisateur {new_username} modifié avec succès.")
                            st.session_state[f"editing_{email}"] = False
                            st.rerun()
        else:
            st.info("Aucun utilisateur enregistré.")

    bout_accueil(back_callback=go_to)
    footer()


# ⭐ FONCTIONS UTILITAIRES ADMIN
def get_all_users(db_path):
    """Récupère tous les utilisateurs"""
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("SELECT id, username, email, role, registration_date FROM users ORDER BY id DESC")
        return c.fetchall()


def get_user_by_email_or_username(db_path, search):
    """Recherche un utilisateur par email ou username"""
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute(
            "SELECT id, username, email, role, registration_date FROM users WHERE email = ? OR username = ?",
            (search, search)
        )
        return c.fetchone()


def delete_user(db_path, email):
    """Supprime un utilisateur"""
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        
        if user:
            user_id = user[0]
            c.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
            c.execute("DELETE FROM users WHERE email = ?", (email,))
            conn.commit()
            return True
        return False


def update_user(db_path, email, auth_manager, username=None, role=None, password=None):
    """Met à jour un utilisateur"""
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        
        if username is not None:
            c.execute("UPDATE users SET username = ? WHERE email = ?", (username, email))
        
        if role is not None:
            c.execute("UPDATE users SET role = ? WHERE email = ?", (role, email))
        
        if password is not None:
            hashed = auth_manager.hash_password(password)
            c.execute("UPDATE users SET password = ? WHERE email = ?", (hashed, email))
        
        conn.commit()
        return True
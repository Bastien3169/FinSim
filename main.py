import streamlit as st
# ---------------------------------------------------------
# CONFIG GLOBALE
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="FinSim", page_icon="🏛️")
# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------
from auth import login_page  # ⭐ NOUVEAU
from src.views.home import home_page
from src.views.indices import indices_page
from src.views.stocks import stocks_page
from src.views.cryptos import cryptos_page
from src.views.ETFs import etfs_page
from src.views.dca_vs_ls import dca_vs_ls_page
from src.views.comparaison_actifs import actifs_page
from src.views.admin import admin_page
from src.models.users_db.models_db_users_test import AuthManager

# ---------------------------------------------------------
# AUTH MANAGER — CRÉER UNE SEULE FOIS VIA SESSION_STATE
# ---------------------------------------------------------
if "auth_manager" not in st.session_state:
    st.session_state.auth_manager = AuthManager(db_path="users.db")

auth_manager = st.session_state.auth_manager

# Initialiser la page par défaut sur AUTHENTIFICATION
if "page" not in st.session_state:
    st.session_state.page = "auth" 

# ---------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------
def go_to(page: str):
    st.session_state.page = page
    st.rerun()

# ---------------------------------------------------------
# AUTO-LOGIN (RESTER CONNECTÉ)
# ---------------------------------------------------------
if st.session_state.page not in ["auth", "inscription"]:  # ⭐ Exclure les 2 pages publiques
    user = auth_manager.get_current_user()
    if not user:
        st.session_state.page = "auth"  # ⭐ Rediriger vers auth
        st.rerun()
    else:
        st.session_state.auth = True
        st.session_state.user_role = user["role"]
        st.session_state.user_email = user["email"]

# ---------------------------------------------------------
# ROUTER
# ---------------------------------------------------------
def router():
    page = st.session_state.page
    
    # Pages publiques (sans authentification)
    if page == "auth":
        login_page(auth_manager, go_to_register=lambda: go_to("inscription"))
        return

    # Pages protégées (avec authentification)
    user = auth_manager.get_current_user()
    if not user:
        st.session_state.page = "auth"
        st.rerun()
        return
    
    routes = {
        "home": lambda: home_page(go_to, auth_manager),
        "indices": lambda: indices_page(go_to),
        "stocks": lambda: stocks_page(go_to),
        "cryptos": lambda: cryptos_page(go_to),
        "etfs": lambda: etfs_page(go_to),
        "dca_vs_ls": lambda: dca_vs_ls_page(go_to),
        "comparaison_actifs": lambda: actifs_page(go_to),
        "admin": lambda: admin_page(go_to),
    }
    
    if page not in routes:
        st.session_state.page = "home"
        st.rerun()
    
    if page == "admin" and st.session_state.user_role != "admin":
        st.error("⛔ Accès interdit")
        return
    
    routes[page]()

# ---------------------------------------------------------
# APP
# ---------------------------------------------------------
router()
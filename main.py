import streamlit as st

# ✅ CONFIGURATION GLOBALE (UNE SEULE FOIS)

st.set_page_config(layout="wide", page_title="FinSim", page_icon="🏛️")

from auth import login_page
from home import home_page
from src.models.users_db.models_db_users_test import AuthManager

# ---------------------------------------------------------
# ✅ INITIALISATION AUTH MANAGER
# ---------------------------------------------------------
if "auth_manager" not in st.session_state:
    st.session_state.auth_manager = AuthManager(db_path="users.db")

# ---------------------------------------------------------
# ✅ ÉTAT GLOBAL
# ---------------------------------------------------------
if "auth" not in st.session_state:
    st.session_state.auth = False

if "user_role" not in st.session_state:
    st.session_state.user_role = None

if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to(page):
    st.session_state.page = page

# ---------------------------------------------------------
# ✅ ROUTAGE PRINCIPAL
# ---------------------------------------------------------
if not st.session_state.auth:
    # ✅ Passe auth_manager à la page de login
    login_page(st.session_state.auth_manager)

else:
    # Affiche la bonne page
    if st.session_state.page == "home":
        home_page(go_to)
    
    # elif st.session_state.page == "indices":
    #     indices_page(go_to)
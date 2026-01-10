import streamlit as st
from src.components.components_views import *

def login_page(auth_manager):
    # ================= CSS =================
    load_css()

    # =============== Titre de la page ================
    display_page_title("🔐 AUTHENTIFICATION FinSim")

    email = st.text_input("📧 Email", key="login_email")
    password = st.text_input("🔒 Mot de passe", type="password", key="login_password")
    stay_connected = st.checkbox("Rester connecté", value=False)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Se connecter", use_container_width=True):
            if not email or not password:
                st.error("❌ Veuillez remplir tous les champs")
            else:
                success, message, role = auth_manager.login(email, password, stay_connected)
                if success:
                    st.session_state.auth = True
                    st.session_state.user_email = email
                    st.session_state.user_role = role
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

    with col2:
        if st.button("S'inscrire", use_container_width=True):
            st.info("🚧 Fonctionnalité à venir...")

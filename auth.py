import streamlit as st
from pathlib import Path

# ❌ SUPPRIME CETTE LIGNE (déjà dans main.py)
# st.set_page_config(layout="wide", page_title="Authentification", page_icon="🏛️")


def login_page(auth_manager):

    # Chargement CSS
    with open("src/assets/css/streamlit.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    st.markdown(f"""<div class="main-container"><h1>🔐 AUTHENTIFICATION FinSim</h1></div>""", unsafe_allow_html=True)
    
    # Formulaire de connexion
    email = st.text_input("📧 Email", key="login_email")
    password = st.text_input("🔒 Mot de passe", type="password", key="login_password")
    
    # Checkbox "Rester connecté"
    stay_connected = st.checkbox("Rester connecté", value=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Se connecter", type="primary", use_container_width=True):
            if not email or not password:
                st.error("❌ Veuillez remplir tous les champs")
            else:
                # ✅ CORRECTION : login() retourne (success, message, role)
                success, message, user_role = auth_manager.login(email, password, stay_connected)
                
                if success:
                    # ✅ Mise à jour de l'état
                    st.session_state.auth = True
                    st.session_state.user_role = user_role
                    st.session_state.user_email = email
                    st.success(message)
                    st.rerun()  # ✅ Moderne (au lieu de experimental_rerun)
                else:
                    st.error(message)
    
    with col2:
        if st.button("S'inscrire", use_container_width=True):
            st.info("🚧 Fonctionnalité à venir...")
            # go_to("inscription")
            # Ou redirige vers page d'inscription
            # st.session_state.page = "register"
            # st.rerun()

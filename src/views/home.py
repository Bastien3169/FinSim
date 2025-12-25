import streamlit as st
from base64 import b64encode
from src.models.users_db.models_db_users_test import AuthManager
from src.components.components_views import *


def home_page(go_to, auth_manager):

    # ---------------------------------------------------------
    # CSS et assets
    # ---------------------------------------------------------
    load_css()

    image_path = "src/assets/images/indices.jpeg"
    with open(image_path, "rb") as img_file:
        encoded = b64encode(img_file.read()).decode()

    st.markdown(f""" <div class="main-container"><img src="data:image/jpeg;base64,{encoded}" class="center-image"> </div> """, unsafe_allow_html=True,)

    # ---------------------------------------------------------
    # TITRE
    # ---------------------------------------------------------
    st.markdown( """<div class="main-container"><h1>🏠 Bienvenue sur FinSim</h1></div>""",unsafe_allow_html=True,)

    # ---------------------------------------------------------
    # TEXTE INTRO
    # ---------------------------------------------------------
    st.markdown(
        """
        <div class="main-container">
            <p>
             Comparez facilement différents placements (actions, indices, cryptos et ETF) et visualisez leur performance historique en un clin d'œil. 
             Découvrez deux stratégies clés : l'investissement progressif (DCA) ou en une seule fois (Lump Sum), pour voir ce qui correspond le 
             mieux à vos objectifs personnels. C'est un outil purement pédagogique basé sur des données passées, sans conseil 
             financier ni incitation à investir – simplement pour vous aider à comprendre et apprendre sans risque.
            <br><br>
            Bonne visite et bon apprentissage !
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


    # ---------------------------------------------------------
    # BOUTON LOGOUT
    # ---------------------------------------------------------
    if st.session_state.get("auth"):
        if st.button("🔓 Se déconnecter"):
            auth_manager.logout()  # supprime la session dans la BDD et le cookie
            # Nettoie session_state
            for key in ["auth", "user_role", "user_email"]:
                if key in st.session_state:
                    del st.session_state[key]
            go_to("login")  # redirige vers la page login
            st.stop()  # stoppe le script pour forcer reload


    # ---------------------------------------------------------
    # TUILES DE NAVIGATION
    # ---------------------------------------------------------
    st.markdown("## 📊 Explorer les actifs")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📈 Indices", use_container_width=True):
            go_to("indices")
            st.rerun()

    with col2:
        if st.button("🏢 Stocks", use_container_width=True):
            go_to("stocks")
            st.rerun()

    with col3:
        if st.button("📊 ETFs", use_container_width=True):
            go_to("etfs")
            st.rerun()

    col4, col5, col6 = st.columns(3)

    with col4:
        if st.button("🪙 Cryptos", use_container_width=True):
            go_to("cryptos")
            st.rerun()

    with col5:
        if st.button("🪙 Tous actifs", use_container_width=True):
            go_to("tous_actifs")
            st.rerun()

    with col6:
        if st.button("🪙 DCA vs LP", use_container_width=True):
            go_to("dca_vs_lp")
            st.rerun()

    col7, col8, col9 = st.columns(3)
    # ---------------------------------------------------------
    # TUile ADMIN (VISIBLE UNIQUEMENT SI ADMIN)
    # ---------------------------------------------------------
    if st.session_state.get("user_role") == "admin":
        with col8:
            if st.button("🛠️ Administration", use_container_width=True):
                go_to("admin")
                st.rerun()

    # ---------------------------------------------------------
    # FOOTER
    # ---------------------------------------------------------
    footer()

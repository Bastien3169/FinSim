import streamlit as st
from base64 import b64encode

def home_page(go_to):

    # ---------------------------------------------------------
    # CSS et assets
    # ---------------------------------------------------------
    with open("src/assets/css/streamlit.css") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

    image_path = "src/assets/images/indices.jpeg"

    with open(image_path, "rb") as img_file:
        encoded = b64encode(img_file.read()).decode()

    st.markdown(f"""<div class="main-container"><img src="data:image/jpeg;base64,{encoded}" class="center-image"></div>""", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # TITRE
    # ---------------------------------------------------------
    st.markdown(f"""<div class="main-container"><h1>COMPARER ET SIMULER LES ACTIFS FINANCIERS</h1></div>""", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # TEXTE INTRO
    # ---------------------------------------------------------
    st.markdown(f"""<div class="main-container"><p>
        Un site permettant de simuler et comparer les performances d’un investissement en DCA 
        (investissement progressif) versus Lump Sum (investissement en une fois).
        L’outil est conçu pour être accessible à tous, même pour ceux qui découvrent la bourse.
        <br>
        Bonne visite et bon apprentissage !
        </p></div>""", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # FOOTER
    # ---------------------------------------------------------
    st.markdown("""<div class="footer"> © 2025 Bastien M. - Projet finance — Tous droits réservés.</div>""", unsafe_allow_html=True)

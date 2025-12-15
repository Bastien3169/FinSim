import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from base64 import b64encode

from src.models.control_datas.connexion_db_datas import *


def indices_page(go_to):
    # ---------------------------------------------------------
    # CSS
    # ---------------------------------------------------------
    with open("src/assets/css/streamlit.css") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # TITRE
    # ---------------------------------------------------------
    st.markdown(
        """<div class="main-container"><h1>LES INDICES BOURSIERS</h1></div>""",
        unsafe_allow_html=True
    )

    # Bouton retour (bonne UX)
    if st.button("⬅️ Retour à l'accueil"):
        go_to("home")
        return

    # ---------------------------------------------------------
    # CONNEXION DB
    # ---------------------------------------------------------
    datas_indices = FinanceDatabaseIndice(db_path="data.db")

    liste_indices = datas_indices.get_list_indices()
    infos_indices = datas_indices.get_infos_indices()

    indice_default = "S&P 500"

    # ---------------------------------------------------------
    # GRAPHIQUE
    # ---------------------------------------------------------
    st.markdown(
        """<div class="main-container"><h2>📈 Graphiques des indices</h2></div>""",
        unsafe_allow_html=True
    )

    selected_indice = st.selectbox(
        "Choisissez un indice pour le graphique",
        liste_indices,
        index=liste_indices.index(indice_default)
    )

    df = datas_indices.get_prix_date(selected_indice)

    if not df.empty:
        fig = go.Figure(
            go.Scatter(
                x=df["Date"],
                y=df["Close"],
                mode="lines",
                name=selected_indice,
                line=dict(color="#6DBE8C", width=2)
            )
        )
        fig.update_layout(
            title=f"Évolution de {selected_indice}",
            xaxis_title="Date",
            yaxis_title="Prix de clôture"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Aucune donnée disponible.")

    # ---------------------------------------------------------
    # TABLEAU RENDEMENTS
    # ---------------------------------------------------------

    # TITRE
    st.markdown("""<div class="main-container"><h2>💯 Rendements (%)</h2></div>""", unsafe_allow_html=True)

    # ✅ 1. Sélection des indices
    selected_indices = st.multiselect(
        "Comparer les indices",
        liste_indices,
        default=[indice_default]
    )

    st.markdown("---")

    # ✅ 2. Gestion des périodes
    if "periods" not in st.session_state:
        st.session_state.periods = [6, 12, 24, 60, 120, 180]


    period_input = st.text_input("Ajouter des périodes (en mois), séparées par des virgules", value="", placeholder="Ex: 1,3,6,12")


    if st.button("➕ Ajouter"):
        try:
            new_periods = [int(p.strip()) for p in period_input.split(",") if p.strip()]
        except ValueError:
            st.error("⚠️ Veuillez entrer uniquement des nombres séparés par des virgules.")
            new_periods = []

        added = []
        for p in new_periods:
            if p not in st.session_state.periods:
                st.session_state.periods.append(p)
                added.append(p)
        if added:
            st.session_state.periods.sort()
            st.session_state.rendement_data = pd.DataFrame()  # Force recalcul
            st.success(f"Périodes ajoutées : {added}")
            st.rerun()
        elif new_periods:
            st.warning("⚠️ Toutes les périodes existaient déjà")
                

    # Affichage des périodes existantes avec possibilité de suppression
    for i in range(0, len(st.session_state.periods), 10):
        cols = st.columns(min(10, len(st.session_state.periods) - i))
        for idx, period in enumerate(st.session_state.periods[i:i+10]):
            with cols[idx]:
                if st.button(f"❌ {period}m", key=f"remove_{period}", type="secondary"):
                    st.session_state.periods.remove(period)
                    st.session_state.rendement_data = pd.DataFrame()
                    st.rerun()

    st.markdown("---")

    # ✅ 3. Initialisation du DataFrame de rendements
    if "rendement_data" not in st.session_state:
        st.session_state.rendement_data = pd.DataFrame()

    # Garde seulement les indices sélectionnés
    st.session_state.rendement_data = st.session_state.rendement_data.loc[
        st.session_state.rendement_data.index.intersection(selected_indices)
    ]

    periods = st.session_state.periods

    # ✅ 4. Calcul des rendements
    for indice in selected_indices:
        expected_cols = [f"{p} mois" for p in periods]
        needs_recalc = (
            indice not in st.session_state.rendement_data.index or
            not all(col in st.session_state.rendement_data.columns for col in expected_cols)
        )
        if needs_recalc:
            df_prix = datas_indices.get_prix_date(indice)
            if df_prix.empty:
                continue
            
            df_rendement = calculate_rendement(df_prix, periods)
            info = infos_indices[infos_indices["Short_Name_Indice"] == indice]
            if not info.empty:
                for col in ["Ticker_Indice_Yf", "Place_Boursiere_Indice", "Nombres_Entreprises", "Devise"]:
                    df_rendement[col] = info.iloc[0][col]
            
            if indice in st.session_state.rendement_data.index:
                st.session_state.rendement_data = st.session_state.rendement_data.drop(indice)
            
            st.session_state.rendement_data = pd.concat(
                [st.session_state.rendement_data, pd.DataFrame(df_rendement, index=[indice])]
            )

    # ✅ 5. Affichage du tableau avec colonnes existantes uniquement
    if not st.session_state.rendement_data.empty and selected_indices:
        cols_order = [f"{p} mois" for p in periods] + ["Ticker_Indice_Yf", "Place_Boursiere_Indice", "Nombres_Entreprises", "Devise"]
        cols_order = [c for c in cols_order if c in st.session_state.rendement_data.columns]

        df_display = st.session_state.rendement_data[cols_order].loc[selected_indices]
        styled_df = style_rendement(df_display, periods)

        st.dataframe(styled_df, use_container_width=True)
    else:
        st.info("📊 Sélectionnez des indices pour afficher les rendements")

    # ---------------------------------------------------------
    # COMPOSITION
    # ---------------------------------------------------------
    st.markdown(
        """<div class="main-container"><h2>🗂 Composition de l'indice</h2></div>""",
        unsafe_allow_html=True
    )

    selected_comp = st.selectbox(
        "Choisissez un indice",
        liste_indices,
        index=liste_indices.index(indice_default)
    )

    df_comp = datas_indices.get_composition_indice(selected_comp)
    if not df_comp.empty:
        st.dataframe(df_comp, use_container_width=True)
    else:
        st.info("Aucune donnée disponible.")

    # ---------------------------------------------------------
    # FOOTER
    # ---------------------------------------------------------
    st.markdown(
        """<div class="footer">© 2025 Bastien M. - Projet finance</div>""",
        unsafe_allow_html=True
    )

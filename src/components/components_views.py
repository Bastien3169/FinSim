import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path


# ========================================
# 1. CHARGEMENT CSS
# ========================================
def load_css(css_path="src/assets/css/streamlit.css"):
    # Charger le fichier CSS pour le style personnalisé
    try:
        css_file = Path(css_path)
        if css_file.exists():
            with open(css_file, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ CSS non trouvé : {css_path}")
    except Exception as e:
        st.error(f"❌ Erreur chargement CSS : {e}")


# ========================================
# 2. COMPOSANTS UI
# ========================================
def page_title(title, with_back_button=True, back_callback=None):
    st.markdown(f"""<div class="main-container"><h1>{title}</h1></div>""", unsafe_allow_html=True)
    
    if with_back_button and back_callback:
        if st.button("⬅️ Retour à l'accueil"):
            back_callback("home")
            return True
    return False


def footer(text="© 2025 Bastien M. - Projet finance"):
    st.markdown(f"""<div class="footer">{text}</div>""", unsafe_allow_html=True)


# ========================================
# 3. GRAPHIQUE INTERACTIF
# ========================================
def display_chart_section(datas_manager, liste_actifs, actif_default, actif_type="indice", color="#6DBE8C"):

    selected_actif = st.selectbox(f"Choisissez un {actif_type} pour le graphique", liste_actifs, index=liste_actifs.index(actif_default) if actif_default in liste_actifs else 0)

    df = datas_manager.get_prix_date(selected_actif)

    if df.empty:
        st.error("Aucune donnée disponible.")
        return

    fig = go.Figure(go.Scatter(x=df["Date"], y=df["Close"], mode="lines", name=selected_actif, line=dict(color=color, width=2)))

    fig.update_layout(title=f"Évolution de {selected_actif}", xaxis_title="Date", yaxis_title="Prix de clôture", hovermode="x unified")

    st.plotly_chart(fig, use_container_width=True)


# ========================================
# 4. RENDEMENTS
# ========================================
def display_rendement_section(datas_manager, infos_df, liste_actifs, actif_default, calculate_rendement_func, style_rendement_func, actif_type="indice", default_periods=None):
    if default_periods is None:
        default_periods = [6, 12, 24, 60, 120, 180]

    # -------------------- INIT SESSION --------------------
    if "periods" not in st.session_state:
        st.session_state.periods = default_periods.copy()

    if "rendement_data" not in st.session_state:
        st.session_state.rendement_data = pd.DataFrame()

    # -------------------- SÉLECTION ACTIFS --------------------
    selected_actifs = st.multiselect(f"Comparer les {actif_type}s", liste_actifs, default=[actif_default] if actif_default in liste_actifs else [])

    st.markdown("---")

    # -------------------- GESTION DES PÉRIODES --------------------
    period_input = st.text_input("Ajouter des périodes (en mois), séparées par des virgules", placeholder="Ex: 1,3,6,12")

    if st.button("➕ Ajouter"):
        try:
            new_periods = [int(p.strip()) for p in period_input.split(",") if p.strip()]
            added = []
            for p in new_periods:
                if p > 0 and p not in st.session_state.periods:
                    st.session_state.periods.append(p)
                    added.append(p)

            if added:
                st.session_state.periods.sort()
                st.session_state.rendement_data = pd.DataFrame()
                st.rerun()
        except ValueError:
            st.error("⚠️ Veuillez entrer uniquement des nombres")

    # Suppression des périodes
    for i in range(0, len(st.session_state.periods), 10):
        cols = st.columns(min(10, len(st.session_state.periods) - i))
        for idx, p in enumerate(st.session_state.periods[i:i+10]):
            with cols[idx]:
                if st.button(f"❌ {p}m", key=f"remove_{p}"):
                    st.session_state.periods.remove(p)
                    st.session_state.rendement_data = pd.DataFrame()
                    st.rerun()

    periods = st.session_state.periods
    st.markdown("---")

    # -------------------- CALCUL RENDEMENTS --------------------
    st.session_state.rendement_data = st.session_state.rendement_data.loc[st.session_state.rendement_data.index.intersection(selected_actifs)]

    for actif in selected_actifs:
        expected_cols = [f"{p} mois" for p in periods]
        needs_recalc = (actif not in st.session_state.rendement_data.index or not all(col in st.session_state.rendement_data.columns for col in expected_cols))

        if not needs_recalc:
            continue

        df_prix = datas_manager.get_prix_date(actif)
        if df_prix.empty:
            continue

        df_rend = calculate_rendement_func(df_prix, periods)

        info = infos_df[infos_df["Short_Name_Indice"] == actif]
        if not info.empty:
            for col in ["Ticker_Indice_Yf", "Place_Boursiere_Indice","Nombres_Entreprises", "Devise"]:
                if col in info.columns:
                    df_rend[col] = info.iloc[0][col]

        st.session_state.rendement_data = st.session_state.rendement_data.drop(actif, errors="ignore")

        st.session_state.rendement_data = pd.concat([st.session_state.rendement_data, pd.DataFrame(df_rend, index=[actif])])

    # -------------------- AFFICHAGE --------------------
    if not st.session_state.rendement_data.empty and selected_actifs:
        cols_order = [f"{p} mois" for p in periods] + ["Ticker_Indice_Yf", "Place_Boursiere_Indice", "Nombres_Entreprises", "Devise"]
        cols_order = [c for c in cols_order if c in st.session_state.rendement_data.columns]

        df_display = st.session_state.rendement_data[cols_order].loc[selected_actifs]
        st.dataframe(style_rendement_func(df_display, periods), use_container_width=True)
    else:
        st.info(f"📊 Sélectionnez des {actif_type}s pour afficher les rendements")


# ========================================
# 5. COMPOSITION
# ========================================
def display_composition_section(datas_manager, liste_actifs, actif_default, actif_type="indice"):
    
    selected_comp = st.selectbox(f"Choisissez un {actif_type}", liste_actifs, index=liste_actifs.index(actif_default) if actif_default in liste_actifs else 0)
    
    df_comp = datas_manager.get_composition_indice(selected_comp)
    
    if not df_comp.empty:
        st.dataframe(df_comp, use_container_width=True)
    else:
        st.info("Aucune donnée disponible.")
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path


# ========================================
# 1. CHARGEMENT CSS
# ========================================
def load_css(css_path="src/assets/css/streamlit.css"):
    # Charger le fichier CSS pour le style personnalisé
    with open(css_path) as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# ========================================
# 2. COMPOSANTS UI
# ========================================
def display_page_title(title):
    st.markdown(f"""<div class="main-container"><h1>{title}</h1></div>""", unsafe_allow_html=True)

def bout_accueil(back_callback, label="⬅️ Retour à l'accueil"):
    if st.button(label):
        back_callback("home")
        return True
    return False

def footer(text="© 2025 Bastien M. - FinSim — Tous droits réservés."):
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
def display_rendement_section(datas_manager, infos_df, liste_actifs, actif_default, calculate_rendement_func, style_rendement_func, actif_type="actif", default_periods=None):

    
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
        cols = st.columns(10, gap="small")
        for idx, p in enumerate(st.session_state.periods[i:i+10]):
            with cols[idx]:
                if st.button(f"❌ {p}m", key=f"remove_{p}", use_container_width=True):
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

        st.session_state.rendement_data = st.session_state.rendement_data.drop(actif, errors="ignore")

        st.session_state.rendement_data = pd.concat([st.session_state.rendement_data, pd.DataFrame(df_rend, index=[actif])])

    # -------------------- AFFICHAGE --------------------
    if not st.session_state.rendement_data.empty and selected_actifs:
        cols_order = [f"{p} mois" for p in periods] 
        cols_order = [c for c in cols_order if c in st.session_state.rendement_data.columns]

        df_display = st.session_state.rendement_data[cols_order].loc[selected_actifs]
        
        # Renommer l'index pour afficher "Indices" en en-tête
        df_display.index.name = actif_type.capitalize() + "s"
        
        styled_df = style_rendement_func(df_display, periods) 
        
        # Configuration pour agrandir la colonne
        column_config = {df_display.index.name: st.column_config.TextColumn(df_display.index.name, width="medium",)}
        
        # Ajout de column_config
        st.dataframe(styled_df, use_container_width=True, column_config=column_config)
    else:
        st.info(f"📊 Sélectionnez des {actif_type}s pour afficher les rendements")


# ========================================
# 5. INFOS ACTIF + COMPOSITION POUR INDICES
# ========================================
def infos_composition_actif(datas_manager, liste_actifs, actif_default, actif_type="indice"):
    
    selected_comp = st.selectbox(f"Choisissez un {actif_type}", liste_actifs, index=liste_actifs.index(actif_default) if actif_default in liste_actifs else 0)

    st.markdown("---")

    df_infos= datas_manager.get_infos_indices(selected_comp)
    
    df_comp = datas_manager.get_composition_indice(selected_comp)
    
    if not df_comp.empty and not df_infos.empty:
        st.subheader("ℹ️ Informations sur l’indice")
        st.dataframe(df_infos, use_container_width=True)

        st.markdown("---")
        
        st.subheader("🧩 Composition de l’indice")
        st.dataframe(df_comp, use_container_width=True)
    else:
        st.info("Aucune donnée disponible.")


# ========================================
# 5. INFOS ACTIF
# ========================================
def infos_actifs(datas_manager, liste_actifs, actif_default, actif_type="actif"):
    # Sélection de l'actif
    selected_comp = st.selectbox(f"Choisissez un {actif_type}", liste_actifs, index=liste_actifs.index(actif_default) if actif_default in liste_actifs else 0)

    st.markdown("---")

    # Choix dynamique de la méthode à appeler selon le type d'actif
    if actif_type == "indice":
        if hasattr(datas_manager, "get_infos_indices"):
            df_infos = datas_manager.get_infos_indices(selected_comp)
        else:
            st.error("La méthode get_infos_indices n'existe pas pour ce datas_manager")
            return
    elif actif_type == "crypto":
        if hasattr(datas_manager, "get_infos_crypto"):
            df_infos = datas_manager.get_infos_crypto(selected_comp)
        else:
            st.error("La méthode get_infos_crypto n'existe pas pour ce datas_manager")
            return
    elif actif_type == "stock":
        if hasattr(datas_manager, "get_infos_stocks"):
            df_infos = datas_manager.get_infos_stocks(selected_comp)
        else:
            st.error("La méthode get_infos_stocks n'existe pas pour ce datas_manager")
            return
    elif actif_type == "etf":
        if hasattr(datas_manager, "get_infos_etfs"):
            df_infos = datas_manager.get_infos_etfs(selected_comp)
        else:
            st.error("La méthode get_infos_etfs n'existe pas pour ce datas_manager")
            return
    else:
        st.error("Type d'actif inconnu")
        return

    # Affichage
    if not df_infos.empty:
        st.subheader(f"ℹ️ Informations sur le {actif_type}")
        st.dataframe(df_infos, use_container_width=True)
    else:
        st.info("Aucune donnée disponible.")

import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go

# Titre principal
st.title("📊 Application de Finance")

# Menu de navigation dans la barre latérale
st.sidebar.title("Navigation")
menu_options = ["Datas indices", "Datas stocks", "Data ETF", "DCA VS LumpSum"]
selected_page = st.sidebar.radio("Choisissez une page", menu_options)

# Connexion à la base SQLite
db_path = "/Users/bastoch/ProjectFinance_alleger/ProjectFinance_Streamlit/sql/data_indices_stocks.db"
conn = sqlite3.connect(db_path)

# Page 1 : Datas indices
if selected_page == "Datas indices":
    st.subheader("📈 Données des indices")

    # Récupérer la liste des indices et leurs infos
    indices = pd.read_sql("SELECT DISTINCT Ticker_Yahoo_Finance FROM historique_indices", conn)["Ticker_Yahoo_Finance"].tolist()
    infos_indices_df = pd.read_sql("SELECT Ticker_Yahoo_Finance, Nom_Indice, Pays FROM infos_indices", conn)

    # Indice par défaut (S&P 500 si dispo, sinon premier indice)
    default_index = "^GSPC" if "^GSPC" in indices else indices[0]

    # Sélection pour le graphique
    selected_index = st.selectbox("Choisissez un indice pour le graphique", indices, index=indices.index(default_index))

    # Récupération des données pour le graphique
    df = pd.read_sql(f"SELECT Date, Close FROM historique_indices WHERE Ticker_Yahoo_Finance = '{selected_index}' ORDER BY Date", conn)
    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
        df = df.set_index("Date").resample("W").last().reset_index()

        fig = go.Figure(go.Scatter(x=df["Date"], y=df["Close"], mode='lines', name=selected_index))
        fig.update_layout(title=f"Évolution de {selected_index} - Clôture hebdomadaire", xaxis_title="Date", yaxis_title="Prix de clôture ($)")
        st.plotly_chart(fig)
    else:
        st.error("Aucune donnée trouvée pour cet indice.")

    # Initialisation du tableau des rendements dans la session
    if "rendement_data" not in st.session_state:
        st.session_state.rendement_data = pd.DataFrame()

    # Sélection multiple juste au-dessus du tableau
    st.subheader("📈 Tableau des rendements en pourcentage")
    selected_indices_for_table = st.multiselect("Ajoutez des indices au tableau", indices, default=[default_index])

    # Supprimer les indices qui ne sont plus sélectionnés
    st.session_state.rendement_data = st.session_state.rendement_data[st.session_state.rendement_data.index.isin(selected_indices_for_table)]

    # Ajout des nouveaux indices sans dupliquer les existants
    # Initialisation d'une liste vide pour stocker les indices à ajouter
    indices_to_add = []
    
    # Boucle pour vérifier chaque indice
    for idx in selected_indices_for_table:
        if idx not in st.session_state.rendement_data.index:
            indices_to_add.append(idx)
    
    # Mise à jour de la liste avec les indices à ajouter
    selected_indices_for_table = indices_to_add

    # Calcul et ajout des rendements
    periods = [6, 12, 24, 60, 120, 180]  # Périodes en mois

    for idx in selected_indices_for_table:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql(f"SELECT Date, Close FROM historique_indices WHERE Ticker_Yahoo_Finance = '{idx}' ORDER BY Date", conn)
        conn.close()

        if not df.empty:
            df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
            df = df.set_index("Date").resample("W").last().reset_index()

            # Calcul du rendement pour chaque période
            rendement = {}
            for period_months in periods:
                start_date = df["Date"].max() - pd.DateOffset(months=period_months)
                df_period = df[df["Date"] >= start_date]

                if len(df_period) > 1:  # Si on a plus d'une donnée dans la période
                    start_close = df_period.iloc[0]["Close"]
                    end_close = df_period.iloc[-1]["Close"]
                    rendement[f"{period_months} mois"] = "{:.2f}".format((end_close - start_close) / start_close * 100)  # Formatté à 2 décimales
                else:
                    rendement[f"{period_months} mois"] = None

            # Ajout des informations "Nom_Indice" et "Pays"
            info = infos_indices_df[infos_indices_df["Ticker_Yahoo_Finance"] == idx]
            rendement["Nom_Indice"] = info["Nom_Indice"].values[0] if not info.empty else "Inconnu"
            rendement["Pays"] = info["Pays"].values[0] if not info.empty else "Inconnu"

            # Mise à jour du DataFrame avec les rendements
            st.session_state.rendement_data = pd.concat([st.session_state.rendement_data, pd.DataFrame(rendement, index=[idx])])

    # Réorganiser les colonnes (sans la colonne "Ticker_Yahoo_Finance")
    st.session_state.rendement_data = st.session_state.rendement_data[["Nom_Indice", "Pays"] + [f"{p} mois" for p in periods]]

    # Fonction de coloration des rendements en fonction de leur signe (positif = vert, négatif = rouge)
    def color_rendement(val):
        color = 'green' if float(val) > 0 else ('red' if float(val) < 0 else 'black')
        return f'color: {color}'

    # Appliquer la mise en forme et le style sur les colonnes des rendements
    styled_df = st.session_state.rendement_data.style.applymap(color_rendement, subset=[f"{p} mois" for p in periods])

    # Afficher le tableau avec les rendements stylisés
    st.dataframe(styled_df)

# Page 2 : Datas stocks
elif selected_page == "Datas stocks":
    st.subheader("📈 Données des actions")
    # Ajouter ici ton code pour "Datas stocks"

# Page 3 : Data ETF
elif selected_page == "Data ETF":
    st.subheader("📈 Données des ETF")
    # Ajouter ici ton code pour "Data ETF"

# Page 4 : DCA VS LumpSum
elif selected_page == "DCA VS LumpSum":
    st.subheader("📊 DCA VS LumpSum")
    # Ajouter ici ton code pour "DCA VS LumpSum"

conn.close()

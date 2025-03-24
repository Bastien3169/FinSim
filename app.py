import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
from def_app import connect_to_db, get_list_actif, get_infos_actif,  get_hist_actif_for_graph, calculate_rendement, style_rendement



############################################### PRESENTATION GENERALE DE STREAMLIT ###############################################

# Titre principal
st.title("📊 Application de Finance!")

# Menu de navigation dans la barre latérale
st.sidebar.title("Navigation")
menu_options = ["Datas indices", "Datas stocks", "Data ETF", "DCA VS LumpSum"]
selected_page = st.sidebar.radio("Choisissez une page", menu_options)



########################################### CONNEXION .db ET RECUPERATION DATAS DE .db PROPRE AUX INDICES ###########################################
# Mise en place des paramètre pour les fonctions des requêtes SQL
table_hist_actif = "historique_indices"
table_infos_actif = "infos_indices"

# Connexion à la base SQLite
db_path = "/Users/bastoch/ProjectFinance_alleger/ProjectFinance_Streamlit/sql/data_indices_stocks.db"
conn = connect_to_db(db_path)

# Récupérer la liste des indices et leurs infos
liste_indices = get_list_actif(conn, table_hist_actif)
df_infos_indices = get_infos_actif(conn, table_infos_actif)



############################################### GRAPHIQUE ###############################################

# Sous-titre  pour la partie graph
st.subheader("📈 Données des indices")

# st.selectbox permet de choisir une seule option.
default_index = "^GSPC" # "index=indices.index(default_index)" attent un int pour index
selected_indice = st.selectbox("Choisissez un indice pour le graphique", liste_indices, index=liste_indices.index(default_index)) # arg1 : nom liste déroulante / arg2 : liste pour la liste déroulante / arg3 : opt par défaut de l'actif pour visualisation graph.

# Récupération des données "Dates" et "Close" de la base de donnée pour le graphique en dataframe
df = get_hist_actif_for_graph(conn, table_hist_actif, selected_indice)

# S'il y a des données dans les colonnes, graphique, sinon message d'erreur.
if not df.empty:
    fig = go.Figure(go.Scatter(x=df["Date"], y=df["Close"], mode='lines', name=selected_indice))
    fig.update_layout(title=f"Évolution de {selected_indice} - Clôture hebdomadaire", xaxis_title="Date", yaxis_title="Prix de clôture ($)")
    st.plotly_chart(fig)
else:
    st.error("Aucune donnée trouvée pour cet indice.")



############################################### TABLEAU RENDEMENT ###############################################

# Sous-titre  pour la partie tableau rdt
st.subheader("📈 Tableau des rendements en pourcentage")

# st.multiselect permet de choisir plusieurs options. 
default_indices = "^GSPC" 
selected_indices_for_table = st.multiselect("Ajoutez des indices au tableau", liste_indices, default= [default_indices]) # arg1 : nom liste déroulante / arg2 : liste pour la liste déroulante / arg3 : opt par défaut de l'actif sur le tableau. "default= [default_indices]" entre [] car attend une liste.

# st.session_state : dictionnaire persistant de Streamlit. Stock et conserve interactions de l'utilisateur pour ne pas avoir à recharger la page.
if "rendement_data" not in st.session_state: 
    st.session_state.rendement_data = pd.DataFrame() # ici, "rendement_data" est la clé du dico "st.session_state" et sa valeur est un dataframe vide.

# Suppression des indices qui ne sont plus sélectionnés
indices_to_remove = []
for i in st.session_state.rendement_data.index:
    if i not in selected_indices_for_table:
        indices_to_remove.append(i)
# Supprimer les indices non sélectionnés
if indices_to_remove:
    st.session_state.rendement_data = st.session_state.rendement_data.drop(indices_to_remove)

# Boucle à travers chaque indice dans selected_indices_for_table (ceux qui ont été selectionnés)
# 1. liste contenant les indices à ajouter, pas encore présent dans la valeur du dico de "st.session_state.rendement_data" qui est un df.
indices_to_add = []
for i in selected_indices_for_table:
    if i not in st.session_state.rendement_data.index: # Vérifie si l'indice n'est pas ds "st.rendement_data" avec ".index".
        indices_to_add.append(i)

# 2. Calculer et ajouter les rendements pour la liste des indices ds "indices_to_add" pas encore présent dans la valeur du dico de "st.session_state.rendement_data" qui est un df. pour chaque indice de la liste "indices_to_add"
periods = [6, 12, 24, 60, 120, 180]  # Périodes en mois
for i in indices_to_add:
    df = get_hist_actif_for_graph(conn, table_hist_actif, i) # On crée le df avec en colonne "Date" et "Close" pour chaque indice selectionnés ds "indices_to_add"
    if not df.empty:
        rendement = calculate_rendement(df, periods)

        # Ajout des informations et création des colonnes "Nom_Indice" et "Pays"
        info = df_infos_indices[df_infos_indices["Ticker_Yahoo_Finance"] == i]
        rendement["Nom_Indice"] = info["Nom_Indice"].values[0] if not info.empty else "Inconnu"
        rendement["Pays"] = info["Pays"].values[0] if not info.empty else "Inconnu"

        # 3. Ajout et écrase st.session_state.rendement_data avec rendement. C'est ici qu'on met en index "Ticker_Yahoo_Finance"
        st.session_state.rendement_data = pd.concat([st.session_state.rendement_data, pd.DataFrame(rendement, index=[i])])



############################################### ORGANISATION ET STYLISATION DU TABLEAU RENDEMENT ###############################################

# Réorganiser les colonnes (sans la colonne "Ticker_Yahoo_Finance")
st.session_state.rendement_data = st.session_state.rendement_data[["Nom_Indice", "Pays"] + [f"{p} mois" for p in periods]]

# Appliquer la mise en forme et le style sur les rendements
styled_df = style_rendement(st.session_state.rendement_data, periods)

# Afficher le tableau avec les rendements stylisés
st.dataframe(styled_df)


# Autres pages à gérer
# Ajouter ici ton code pour "Datas stocks"


conn.close()

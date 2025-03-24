import streamlit as st
import pandas as pd

st.title("Analyse des indices")

# Charger le fichier CSV
chemin_csv = "ProjectFinance_alleger/ProjectFinance_Streamlit/streamlit_app/historique_indices.csv"

df = pd.read_csv(chemin_csv, delimiter=";", parse_dates=["Date"])

# Garder seulement les clôtures hebdomadaires si nécessaire
#df = df.set_index("Date").resample("W").last().reset_index()

# Afficher dans Streamlit
st.title("Données de clôture hebdomadaires")
st.dataframe(df)

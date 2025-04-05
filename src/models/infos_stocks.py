import os
import glob
import pandas as pd


def infos_stocks()
    # Chemin des fichiers CSV
    fichiers_csv = glob.glob("ProjectFinance_alleger/ProjectFinance_Streamlit/src/modelels/csv/*.csv")
    
    # Liste pour stocker les DataFrames
    dfs = []
    
    # Chargement des fichiers CSV
    for i in fichiers_csv:
        df = pd.read_csv(i)
        dfs.append(df)
    
    # Concaténation de tous les DataFrames
    df_concat = pd.concat(dfs, ignore_index=True)
    
    # Suppression des doublons basés sur la colonne du ticker (remplace 'Ticker' par le vrai nom de la colonne)
    df_final = df_concat.drop_duplicates(subset=['Ticker'])
    
    # Enlever les colonnes qui ne ne veullent plus rien dire ici
    df = df.drop(columns=["Ponderation", "Nom_Indice", "Ticker_Indice_Yahoo", "Nombres_Entreprises"])
    
    # Sauvegarde du fichier fusionné sans doublons
    df_final.to_csv("ProjectFinance_alleger/ProjectFinance_Streamlit/src/modelels/csv/infos_stocks_concat.csv", index=False, encoding="utf-8")
    
    # Affichage du DataFrame final
    return df_final

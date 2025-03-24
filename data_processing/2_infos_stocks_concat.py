import os
import glob
import pandas as pd

# Chemin des fichiers CSV
fichiers_csv = glob.glob("/Users/bastoch/Desktop/datas_csv/data_stocks/*.csv")

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

# Sauvegarde du fichier fusionné sans doublons
df_final.to_csv("infos_stocks_concat.csv", index=False, encoding="utf-8")




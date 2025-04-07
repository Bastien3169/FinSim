import os
import glob
import pandas as pd


def infos_stocks(dossier_csv) :
    # Chemin des fichiers CSV
    fichiers_csv = glob.glob(os.path.join(dossier_csv, "composition_*.csv"))

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
    df_final = df_final.drop(columns=["Ponderation", "Nom_Indice", "Ticker_Indice_Yahoo", "Nombres_Entreprises"])
    
    # Sauvegarde du fichier fusionné sans doublons
    df_final.to_csv(os.path.join(dossier_csv, "infos_stocks.csv"), index=False, encoding="utf-8")

    print(f"[✅] Le fichier infos stocks a bien été enregistré sous le nom")

    # Affichage du DataFrame final
    return df_final

if __name__ == "__main__":
    infos_stocks = infos_stocks("csv") #Appel de la fonction
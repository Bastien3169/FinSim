import os
import glob
import sqlite3
import pandas as pd

def creation_db(db_path):
    """
    Crée la base de données et les tables nécessaires.
    """
    # Connexion à la base de données SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Création des tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS infos_indices (
        Nom_Indice TEXT,  
        Ticker TEXT,  
        Ticker_Yahoo_Finance TEXT PRIMARY KEY,  -- (clé primaire)
        Short_Name TEXT,
        Pays TEXT,
        Place_Boursiere TEXT,
        Nombres_Entreprises INTEGER,
        Devise TEXT  
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS infos_stocks (
        Nom_Entreprise TEXT,  
        Ticker TEXT,  
        Ticker_Yahoo_Finance TEXT PRIMARY KEY,  -- (clé primaire)
        Secteur_Activite TEXT,
        Pays TEXT,
        Place_Boursiere TEXT,
        Capitalisation_Boursiere REAL
    )
    ''')

    # Création des tables pour chaque indice (ex: SP500, NASDAQ, etc.)
    for i in glob.glob(os.path.join(dossier_csv, "composition_*.csv")):
        # Extraction du nom de la table à partir du nom du fichier
        nom_table = os.path.basename(i).replace('.csv', '')
        
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {nom_table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nom_Entreprise TEXT,
            Ticker TEXT,
            Ticker_Yahoo_Finance TEXT,
            Ponderation REAL,
            Secteur_Activite TEXT,
            Nom_Indice TEXT,
            Ticker_Indice_Yahoo TEXT,
            Pays TEXT,
            Place_Boursiere TEXT,
            Nombres_Entreprises INTEGER,
            Capitalisation_Boursiere REAL,
            FOREIGN KEY (Ticker_Yahoo_Finance) REFERENCES infos_stocks(Ticker_Yahoo_Finance)
        )
        ''')

    # Création des tables historiques
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS historique_indices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Date TEXT,
        Close REAL,
        Ticker TEXT,
        Ticker_Yahoo_Finance TEXT,
        Short_Name TEXT,
        FOREIGN KEY (Ticker_Yahoo_Finance) REFERENCES infos_indices(Ticker_Yahoo_Finance)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS historique_stocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Date TEXT,
        Close REAL,
        Ticker TEXT,
        Ticker_Yahoo_Finance TEXT,
        Nom_Entreprise TEXT,
        FOREIGN KEY (Ticker_Yahoo_Finance) REFERENCES infos_stocks(Ticker_Yahoo_Finance)
    )
    ''')

    # Valider les changements
    conn.commit()
    
    # Fermer la connexion
    conn.close()

    print("[✅] Tables créées avec succès.")

def import_csv_compo_indices(dossier_csv, db_path):
    """
    Importe tous les fichiers CSV du dossier vers la base de données SQLite.
    """
    # Connexion à la base de données SQLite
    conn = sqlite3.connect(db_path)
    
    # Parcours des fichiers CSV dans le dossier et sous-dossiers
    for i in glob.glob(os.path.join(dossier_csv, "*.csv"), recursive=True):
        try:
            # Lecture du fichier CSV
            df = pd.read_csv(i)
            
            # Création du nom de la table en fonction du nom du fichier
            table_name = os.path.basename(i).split('.')[0]
            
            # Enregistrement des données dans la base SQLite
            df.to_sql(table_name, conn, if_exists='append', index=False)
            print(f"Table {table_name} ajoutée avec succès.")
            
        except Exception as e:
            print(f"Erreur lors de l'importation du fichier {i}: {e}")

    # Fermer la connexion
    conn.close()
    
    print("[✅] Importation des CSV dans la base de données terminée.")

def main_creation_db(dossier_csv, db_path):
    # Étape 1: Créer la base de données et les tables
    creation_db(db_path)

    # Étape 2: Importer les fichiers CSV dans la base de données
    import_csv_compo_indices(dossier_csv, db_path)

if __name__ == "__main__":
    main_creation_db("csv", "csv/data.db")

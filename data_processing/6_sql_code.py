import os
import glob
import sqlite3
import pandas as pd

# Chemin vers la base de données SQLite (elle sera créée si elle n'existe pas)
db_path = '/Users/bastoch/ProjectFinance_alleger/sql/data_indices_stocks.db'

# Connexion à la base de données
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Création de la table des indices
cursor.execute('''
CREATE TABLE IF NOT EXISTS infos_indices (
    Indices TEXT,  
    Ticker TEXT,  
    Ticker_Yahoo_Finance TEXT PRIMARY KEY,  -- (clé primaire)
    Pays TEXT,
    Nom TEXT,
    Nombre_Entreprises INTEGER,
    Devise TEXT,
    Place_Boursiere TEXT
)
''')

# Création de la table des entreprises uniques
cursor.execute('''
CREATE TABLE IF NOT EXISTS infos_stocks (
    Nom TEXT,  
    Ticker TEXT,  
    Ticker_Yahoo_Finance TEXT PRIMARY KEY,  -- (clé primaire)
    Secteur_Activite TEXT,
    Nom_Indice TEXT,
    Ticker_Indice_Yahoo TEXT,
    Pays TEXT,
    Place_Boursiere TEXT,
    Nombre_Entreprises INTEGER,
    Capitalisation_Boursiere REAL
)
''')

# Création des tables des indices spécifiques (par exemple SP500, NASDAQ, etc.)
indices = [
    "composition_sp500", "composition_nasdaq", "composition_dowjones", "composition_france", "composition_allemagne", 
    "composition_angleterre", "composition_japon","composition_europe50", "composition_italie", 
    "composition_paysbas", "composition_finlande", "composition_danemark", "composition_suede", "composition_belgique", "composition_espagne"
]

for i in indices:
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {i} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Nom TEXT,
        Ticker TEXT,
        Ticker_Yahoo_Finance TEXT,
        Ponderation REAL,
        Secteur_Activite TEXT,
        Nom_Indice TEXT,
        Ticker_Indice_Yahoo TEXT,
        Pays TEXT,
        Place_Boursiere TEXT,
        Nombre_Entreprises INTEGER,
        Capitalisation_Boursiere REAL,
        FOREIGN KEY (Ticker_Yahoo_Finance) REFERENCES infos_stocks(Ticker_Yahoo_Finance)  -- Clé étrangère
    )
    ''')

# Création de la table historique des indices
cursor.execute('''
CREATE TABLE IF NOT EXISTS historique_indices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Date TEXT,
    Close REAL,
    Ticker TEXT,
    Ticker_Yahoo_Finance TEXT,
    Short_Name TEXT,
    FOREIGN KEY (Ticker_Yahoo_Finance) REFERENCES infos_indices(Ticker_Yahoo_Finance)  -- Clé étrangère
)
''')

# Création de la table historique des entreprises
cursor.execute('''
CREATE TABLE IF NOT EXISTS historique_stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Date TEXT,
    Close REAL,
    Ticker TEXT,
    Ticker_Yahoo_Finance TEXT,
    Short_Name TEXT,
    FOREIGN KEY (Ticker_Yahoo_Finance) REFERENCES infos_stocks(Ticker_Yahoo_Finance)  -- Clé étrangère
)
''')

# Valider les changements
conn.commit()

# Importer les fichiers CSV de tous les sous-dossiers
dossier_w = '/Users/bastoch/ProjectFinance_alleger/data_csv'

# Parcours des fichiers CSV dans le dossier et sous-dossiers
for i in glob.glob(os.path.join(dossier_w, "*.csv"), recursive=True):
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

# Fermer la connexion à la base de données
conn.close()

print("Base de données créée et remplie avec succès.")

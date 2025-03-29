import streamlit as st
import sqlite3
import hashlib
from def_app import *


####################################### STREAMLIT SQUELLETE #######################################

# Chargement du fichier CSS
with open("/Users/bastoch/ProjectFinance_alleger/ProjectFinance_Streamlit/css/streamlit.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# CSS titre principal
#st.title("📊 LES INDICES BOURSIERS")
st.markdown(f"""<div class="main-container"><h2>👤 Connexion</h2></div>""", unsafe_allow_html=True)


username = st.text_input("Nom d'utilisateur")
password = st.text_input("Mot de passe", type="password")
confirm_password = st.text_input("Confirmez le mot de passe", type="password")

if st.button("S'inscrire"):
    if password != confirm_password:
        st.error("Les mots de passe ne correspondent pas.")
    else:
        conn, cursor = connect_db()
        if user_exists(cursor, username):
            st.warning("Ce nom d'utilisateur existe déjà.")
        else:
            add_user(conn, cursor, username, password)
            st.success("Compte créé avec succès !") 



####################################### CONNEXION BD POUR ENREGISTREMENT USER #######################################

# Connexion à la base de données
def connect_db():
    conn = sqlite3.connect("/Users/bastoch/ProjectFinance_alleger/ProjectFinance_Streamlit/sql/users.db")  # Change en MySQL si nécessaire
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )"""
    )
    conn.commit()
    return conn, cursor


# Fonction pour hacher les mots de passe
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Fonction pour vérifier si un utilisateur existe
def user_exists(cursor, username):
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone() is not None


# Fonction pour ajouter un utilisateur
def add_user(conn, cursor, username, password):
    hashed_pwd = hash_password(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pwd))
    conn.commit()





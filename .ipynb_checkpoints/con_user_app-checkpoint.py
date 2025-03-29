import streamlit as st
import sqlite3
import hashlib
from def_app import *


# Interface Streamlit
st.title("Inscription")

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
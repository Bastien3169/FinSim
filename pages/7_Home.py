import streamlit as st

# ---------------------
# INITIALISATION
# ---------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to(page):
    st.session_state.page = page


# ---------------------
# NAVIGATION BAR
# ---------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Home"):
        go_to("home")

with col2:
    if st.button("Indices"):
        go_to("indices")

with col3:
    if st.button("Cryptos"):
        go_to("cryptos")

st.markdown("---")

# ---------------------
# ROUTER
# ---------------------
if st.session_state.page == "home":
    st.title("🏠 Accueil")
    st.write("Bienvenue sur la home page.")

elif st.session_state.page == "indices":
    st.title("📊 Indices")
    st.write("Page indices ici.")

elif st.session_state.page == "cryptos":
    st.title("💰 Cryptos")
    st.write("Page cryptos ici.")

else:
    st.error("Page inconnue.")

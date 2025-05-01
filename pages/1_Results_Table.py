import streamlit as st
import pandas as pd

# Import des fonctions de recherche (cache intégré)
from utils import (
    search_google_play_apps_cached,
    search_producthunt_cached,
    search_github_cached,
    update_search_history
)

# Configuration de la page
st.set_page_config(page_title="Recherche d'applications", layout="wide")
st.title(" Multi-source Application Search")

# Zone de recherche
if "selected_term" not in st.session_state:
    st.session_state.selected_term = ""
search_term = st.text_input("Enter search term:", value=st.session_state.selected_term)
st.session_state.selected_term = search_term




# 🎯 Recherche manuelle
if st.button("search"):
    if search_term.strip():
        update_search_history(search_term)
        st.session_state.selected_term = search_term  # Set the selected term to the current search term
        st.rerun()

# 💊 Historique en pills
if "search_history" in st.session_state and st.session_state.search_history:
    " *Historique de recherche*"
    with st.container():
        cols = st.columns(len(st.session_state.search_history))
        for i, term in enumerate(st.session_state.search_history):
            if cols[i].button(term, key=f"pill_{term}"):
                st.session_state.selected_term = term
                st.rerun()


# Recherche si un mot-clé est fourni
if search_term:
    with st.spinner("Waiting..."):

        # Recherche dans Google Play
        try:
            df_play = search_google_play_apps_cached(search_term)
        except Exception as e:
            st.error(f"❌ Erreur Google Play : {e}")
            df_play = pd.DataFrame()

        # Recherche dans Product Hunt
        try:
            df_ph = search_producthunt_cached(search_term)
        except Exception as e:
            st.error(f"❌ Erreur Product Hunt : {e}")
            df_ph = pd.DataFrame()

        # Recherche dans GitHub
        try:
            df_gh = search_github_cached(search_term)
        except Exception as e:
            st.error(f"❌ Erreur GitHub : {e}")
            df_gh = pd.DataFrame()

        # Vérification des résultats
        if df_play.empty and df_ph.empty and df_gh.empty:
            st.warning("⚠ Aucun résultat trouvé.")
        else:
            col1, col2, col3 = st.columns(3)

            if not df_play.empty:
                with col1:
                    st.subheader("📱 Google Play")
                    st.success(f"{len(df_play)} applications trouvées")
                    st.dataframe(df_play)

            if not df_ph.empty:
                with col2:
                    st.subheader("🚀 Product Hunt")
                    st.success(f"{len(df_ph)} produits trouvés")
                    st.dataframe(df_ph)

            if not df_gh.empty:
                with col3:
                    st.subheader("💻 GitHub")
                    st.success(f"{len(df_gh)} projets trouvés")
                    st.dataframe(df_gh)

        # Stockage des résultats
        st.session_state["google_play"] = df_play
        st.session_state["producthunt"] = df_ph
        st.session_state["github"] = df_gh
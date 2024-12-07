import streamlit as st


 # Upload-Button
uploaded_file = st.file_uploader("Datei hochladen", type=["xlsx"])

# Weiterleitungs-Button (nur sichtbar, wenn eine Datei hochgeladen wurde)
if uploaded_file:
    st.session_state["uploaded_file"] = uploaded_file  # Datei speichern
    if st.button("Weiter"):
       st.switch_page("pages/03_Diagramm.py")    # Navigation auf die Upload-Seite
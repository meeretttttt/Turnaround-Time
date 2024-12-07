import streamlit as st
from Data import process 



# Überprüfen, ob eine Datei vorhanden ist
if "uploaded_file" in st.session_state:
    uploaded_file = st.session_state["uploaded_file"]
    st.write("Hochgeladene Datei:")
    st.write(uploaded_file.name)
    df = process(uploaded_file)
    st.dataframe(df)
    
else:
    st.error("Keine Datei gefunden. Bitte kehren Sie zur Startseite zurück.")


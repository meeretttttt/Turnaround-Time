import streamlit as st
from Data import process 
from Data import box_whiskers_plot



# Überprüfen, ob eine Datei vorhanden ist
if "uploaded_file" in st.session_state:
    uploaded_file = st.session_state["uploaded_file"]
    st.write("Hochgeladene Datei:")
    st.write(uploaded_file.name)
    df,time_columns = process(uploaded_file, True)
    st.dataframe(df)

    box_whiskers_plot(df,time_columns)
    
else:
    st.error("Keine Datei gefunden. Bitte kehren Sie zur Startseite zurück.")


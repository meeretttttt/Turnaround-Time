import streamlit as st

st.set_page_config(page_title= "Willkommen", page_icon= None, layout="wide", initial_sidebar_state="auto", menu_items= None) 

st.title('Turnaround Time Calculator')

st.subheader("Mithilfe dieser App können die Turnaround Time von laboranalytischen Tests berechnet und visualisiert werden")
st.subheader("Anleitung")
st.write ("1. Laden Sie die Vorlage (Excel-Datei) herunter")
st.write ("2. Füllen Sie die Vorlage mit Ihren Daten, das Zeitformat sollte wie folgt sein: TT.MM.JJJJ hh:mm:ss")
st.write ("3. Mit dem Button Auswertung kann die gewünschte Datei hochgeladen werden")



# Download Button
with open("Vorlage_TAT.xlsx", "rb") as file:
    st.download_button(
        label="📥 Excel-Vorlage herunterladen",
        data=file,
        file_name="Vorlage_TAT.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
# Navigations-Button
if st.button("Zur Auswertung"):
   st.switch_page("pages/02_✏️_Auswertung.py")
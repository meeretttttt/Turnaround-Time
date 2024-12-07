import streamlit as st

st.set_page_config(page_title= "Willkommen", page_icon= None, layout="wide", initial_sidebar_state="auto", menu_items= None)

st.title('Turnaround Time Calculator')

st.subheader("Mithilfe dieser App können die Turnaround Time von laboranalytischen Tests berechnet und visualisiert werden")



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
   st.switch_page("pages/02_Auswertung.py")
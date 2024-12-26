import streamlit as st

st.set_page_config(page_title= "Willkommen", page_icon= None, layout="wide", initial_sidebar_state="auto", menu_items= None) 

st.title('Turnaround Time Calculator')

st.subheader("Mithilfe dieser App können die Turnaround Time von laboranalytischen Tests berechnet und visualisiert werden")
st.subheader("Anleitung")
st.write ("""1. Laden Sie die Vorlage (Excel-Datei) herunter. Es steht zudem eine Beispiel-Datei zur Verfügung.
2. Befüllen Sie die Vorlage mit Ihren Daten:

- **Daten einfügen**:  
   - Tragen Sie Ihre Daten in die bereitgestellte Vorlage ein.  
   - **Wichtig:** Verwenden Sie für Datums- und Zeitangaben folgendes Format:  
     **`TT.MM.JJJJ hh:mm:ss`**  (Sekunden sind optional)
          
     *(z. B. 25.12.2024 14:30:00)*  

- **Keine Änderungen an den ersten Spalten**:  
   - Die **ersten beiden Spalten** der Vorlage sind festgelegt und dürfen **nicht geändert** werden.  

- **Checkpoints und Phasen definieren**:  
   - Sie können **eigene Checkpoints** definieren und diese der passenden Phase zuordnen.  
   - Die Phasen können Sie nach Bedarf individuell benennen.  

- **Eindeutige Bezeichnungen**:  
   - Achten Sie darauf, dass alle **Checkpoints und Phasen eindeutig benannt** werden.
3. Mit dem Button \"Zur Auswertung\" kann die gewünschte Datei hochgeladen werden.""")




# Download Button Vorlage
with open("Vorlage_TAT.xlsx", "rb") as file:
    st.download_button(
        label="📥 Excel-Vorlage herunterladen",
        data=file,
        file_name="Vorlage_TAT.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

# Download Button Beispiel
with open ("Beispiel_TAT.xlsx", "rb") as file:
    st.download_button(
        label="📥 Excel-Beispiel herunterladen",
        data=file,
        file_name="Beispiel_TAT.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
# Navigations-Button
if st.button("Zur Auswertung"):
   st.switch_page("pages/02_✏️_Auswertung.py")
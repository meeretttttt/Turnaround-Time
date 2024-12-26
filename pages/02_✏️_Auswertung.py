import streamlit as st

st.title('Auswertung')


# Layout mit Spalten erstellen
col1, col2 = st.columns(2)

# Linke Spalte: Outlier-Auswahl
with col1:
    st.write("### Outlier-Einstellungen")
    outlier_option = st.radio(
    "Outlier-Einstellungen:",
    ["Mit Outliers", "Ohne Outliers"],index=1
    )

    # Speichern der Auswahl als Boolean im Session State
    if outlier_option == "Mit Outliers":
        st.session_state.remove_outlier = False
    else:
        st.session_state.remove_outlier= True

 # Upload-Button
uploaded_file = st.file_uploader("Datei hochladen", type=["xlsx"])

# Weiterleitungs-Button (nur sichtbar, wenn eine Datei hochgeladen wurde)
if uploaded_file:
    st.session_state["uploaded_file"] = uploaded_file  # Datei speichern
    if st.button("Weiter"):
       st.switch_page("pages/03_📊_Diagramme.py")    # Navigation auf die Upload-Seite


# Rechte Spalte: Diagrammauswahl
with col2:
    st.write("### Diagramm-Auswahl")
    st.session_state["boxplot_selected"] = st.checkbox("Box and Whiskers Plot", value=True)
    st.session_state["histogram_selected"] = st.checkbox("Histogramm", value=True)
    st.session_state["pie_chart_selected"] = st.checkbox("Pie-Chart")
    st.session_state["trend_selected"] = st.checkbox("Trend")
    st.session_state["weekday_comparison_selected"] = st.checkbox("Wochentagvergleich")


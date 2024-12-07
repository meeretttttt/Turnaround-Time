import streamlit as st



 # Upload-Button
uploaded_file = st.file_uploader("Datei hochladen", type=["xlsx"])

# Weiterleitungs-Button (nur sichtbar, wenn eine Datei hochgeladen wurde)
if uploaded_file:
    st.session_state["uploaded_file"] = uploaded_file  # Datei speichern
    if st.button("Weiter"):
       st.switch_page("pages/03_Diagramm.py")    # Navigation auf die Upload-Seite


# Layout mit Spalten erstellen
col1, col2 = st.columns(2)

# Linke Spalte: Outlier-Auswahl
with col1:
    st.write("### Outlier-Einstellungen")
    outlier_option = st.radio(
    "Outlier-Einstellungen:",
    ["Mit Outliers", "Ohne Outliers"],index=1
    )

# Rechte Spalte: Diagrammauswahl
with col2:
    st.write("### Diagramm-Auswahl")
    boxplot_selected = st.checkbox("Box and Whiskers Plot", value=True)
    histogram_selected = st.checkbox("Histogramm", value=True)
    pie_chart_selected = st.checkbox("Pie-Chart")
    trend_selected = st.checkbox("Trend")
    weekday_comparison_selected = st.checkbox("Wochentagvergleich")

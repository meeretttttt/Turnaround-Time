import streamlit as st
from Data import process 
from Data import box_whiskers_plot
from Data import pie_chart
from Data import histogramm
from Data import trend_total
from Data import trend_per_phase



# Überprüfen, ob eine Datei vorhanden ist
if "uploaded_file" in st.session_state:
    uploaded_file = st.session_state["uploaded_file"]
    st.write("Hochgeladene Datei:")
    st.write(uploaded_file.name)
    df,time_columns = process(uploaded_file, st.session_state.remove_outlier)
    st.dataframe(df)


    # Auswahl abrufen
    boxplot_selected = st.session_state["boxplot_selected"]
    histogram_selected = st.session_state["histogram_selected"]
    pie_chart_selected = st.session_state["pie_chart_selected"]
    trend_selected = st.session_state["trend_selected"]
    weekday_comparison_selected = st.session_state["weekday_comparison_selected"]

    # Diagramme anzeigen basierend auf der Auswahl
    if boxplot_selected:
        st.subheader("Box and Whiskers Plot")
        box_whiskers_plot(df,time_columns)

    if histogram_selected:
        st.subheader("Histogramm")
        histogramm (df, time_columns)

    if pie_chart_selected:
        st.subheader("Pie-Chart")
        pie_chart (df, time_columns)

    if trend_selected:
        st.subheader("Trend")
        trend_total (df)
        trend_per_phase(df, time_columns)

    if weekday_comparison_selected:
        st.subheader("Wochentagvergleich")
        # Füge hier den Code zur Anzeige des Wochentagvergleichs ein

    
else:
    st.error("Keine Datei gefunden. Bitte kehren Sie zur Startseite zurück.")


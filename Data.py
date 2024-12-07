
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import matplotlib.dates as mdates
from matplotlib.ticker import ScalarFormatter

def process (uploaded_file,remove_outliers_option): 
    df_TAT, phases = load_data(uploaded_file)
    df_TAT = calculate_TAT(df_TAT, phases)
    # Dynamisch die Zeitspalten basierend auf den Phasen-Schlüsseln auswählen
    time_columns = [f"{phase} in Minuten" for phase in phases.keys()]
    if remove_outliers_option:
        df_cleaned = remove_outliers(df_TAT, time_columns)
        return df_cleaned, time_columns
    else: 
        return df_TAT, time_columns

def load_data (uploaded_file):

    try:
        if uploaded_file.name.endswith(".xlsx"):
            df_TAT = pd.read_excel(uploaded_file,header=[0, 1])
    except Exception as e:
        st.error(f"Fehler beim Lesen der Datei: {e}")

    # Ab der dritten Spalte die Werte in datetime konvertieren
    for col in df_TAT.columns[2:]:  # Nur ab der dritten Spalte
        df_TAT[col] = pd.to_datetime(df_TAT[col], errors='coerce', dayfirst=True)  # Fehlerhafte Werte werden zu NaT

    # Dictionary zur Speicherung der Phasen und ihrer Schritte
    phases = {}

    # Iteration über die Spalten ab der dritten
    for col in df_TAT.columns[2:]:
        phase = col[0].strip()  # Übergeordnete Phase
        step = col[1].strip()   # Untergeordneter Schritt
        
        # Phase hinzufügen, falls noch nicht vorhanden
        if phase not in phases:
            phases[phase] = []
        
        # Schritt hinzufügen, falls noch nicht vorhanden
        if step not in phases[phase]:
            phases[phase].append(step)

    # Nur die zweite Hierarchieebene behalten
    df_TAT.columns = df_TAT.columns.droplevel(0)
    return df_TAT, phases

def calculate_TAT (df_TAT, phases):
    # Get the keys of the phases
    phase_keys = list(phases.keys())

    # Iterate through the phases
    for i in range(len(phase_keys)):
        current_phase = phase_keys[i]
        current_phase_checkpoints = phases[current_phase]

        last_phase = len(phase_keys) - 1 # With 3 phases, the last phase is 2

        if i < last_phase:
            # For all but the last phase, calculate the difference between the first column of the current phase and the next phase
            next_phase = phase_keys[i + 1]
            next_phase_checkpoints = phases[next_phase]

            coL_phase_start = current_phase_checkpoints[0]
            col_phase_end = next_phase_checkpoints[0]

            print(f"Calculating TAT for {current_phase}: {coL_phase_start} - {col_phase_end}")

            df_TAT[f"{current_phase}"] = df_TAT[col_phase_end] - df_TAT[coL_phase_start]

            df_TAT[f"{current_phase} in Minuten"] = df_TAT[current_phase].dt.total_seconds() / 60

        else:
            # For the last phase, calculate the difference between its first and last column

            coL_phase_start = current_phase_checkpoints[0]
            col_phase_end = current_phase_checkpoints[-1]
            
            print(f"Calculating TAT for {current_phase}: {coL_phase_start} - {col_phase_end}")

            df_TAT[f"{current_phase}"] = df_TAT[col_phase_end] - df_TAT[coL_phase_start]

            df_TAT[f"{current_phase} in Minuten"] = df_TAT[current_phase].dt.total_seconds() / 60


    # Calculate the difference between the first and last checkpoint over all phases
    first_checkpoint = phases[phase_keys[0]][0]
    last_checkpoint = phases[phase_keys[-1]][-1]

    df_TAT['Total_TAT'] = df_TAT[last_checkpoint] - df_TAT[first_checkpoint]
    df_TAT['Total_TAT in Minuten'] = df_TAT['Total_TAT'].dt.total_seconds() / 60

    return df_TAT


# # Diagramme

def plot_phase(df, phase_column, time_column='Eingang', time_format='%Y-%m-%d', title='Phase Plot'):
    """
    Dynamisches Plotten von Daten für jede Phase.
    
    Parameters:
        df (pd.DataFrame): DataFrame mit den Daten
        phase_column (str): Die Spalte, die die Phase repräsentiert (z. B. 'Präanalytische Phase in Minuten')
        time_column (str): Die Spalte, die das Datum/Zeit enthält (Standard: 'Eingang')
        time_format (str): Format für das Datum auf der x-Achse (Standard: '%Y-%m-%d')
        title (str): Titel des Diagramms
    """
    # Liniendiagramm erstellen
    fig = plt.figure(figsize=(10, 6))
    sns.lineplot(x=df[time_column], y=df[phase_column], marker='o')

    # Achsenanpassungen
    ax = plt.gca()

    # Datumsformat auf der x-Achse anpassen
    ax.xaxis.set_major_formatter(mdates.DateFormatter(time_format))

    # Wissenschaftliche Notation auf der y-Achse deaktivieren
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.get_offset_text().set_visible(False)  # Optional: Offset-Text entfernen

    # Datumswerte auf der x-Achse schön formatieren
    fig.autofmt_xdate()

    # Titel und Achsenbeschriftungen hinzufügen
    plt.title(title)
    plt.xlabel('Date and Time')
    plt.ylabel('Time (minutes)')

    # Diagramm anzeigen
    plt.show()

def box_whiskers_plot (df_TAT, time_columns):
    
    # Melt the DataFrame to long format for seaborn
    df_melted = df_TAT.melt(id_vars=[df_TAT.columns[2]], value_vars=time_columns, var_name='Phase', value_name='Time (minutes)')


    # Create separate box and whiskers plots for each phase
    phases_list = df_melted['Phase'].unique()
    # Plots erstellen und in Streamlit anzeigen
    for phase in phases_list:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(y='Time (minutes)', data=df_melted[df_melted['Phase'] == phase], ax=ax)
        ax.set_title(f'Time for {phase}')
        ax.set_ylabel('Time (minutes)')
        ax.set_xlabel(phase)
        st.pyplot(fig)  # Zeigt den aktuellen Plot in Streamlit an      

def pie_chart (df_TAT, time_columns):
    # Sum the total time for each phase
    phase_sums = df_TAT[time_columns].sum()

    # Create a pie chart
    plt.figure(figsize=(10, 6))
    plt.pie(phase_sums, labels=phase_sums.index, autopct='%1.1f%%', startangle=140)
    plt.title('Total Time Distribution for Each Phase')
    plt.show()


# Function to remove outliers using IQR
def remove_outliers_column(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

def remove_outliers(df_TAT, time_columns):
    # Remove outliers for each phase
    df_cleaned = df_TAT.copy()
    for phase in time_columns:
        df_cleaned = remove_outliers_column(df_cleaned, phase)

    return df_cleaned


def histogramm (df_TAT, time_columns):
    # Histogram for each phase
    for phase in time_columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(df_TAT[phase], bins=10, kde=True)
        plt.title(f'Histogram of {phase}')
        plt.xlabel('Time (minutes)')
        plt.ylabel('Frequency')
        plt.show()

def trend (df_TAT, time_columns):
    # Line plot to show the trend of TAT over time
    plt.figure(figsize=(10, 6))
    for phase in time_columns:
        sns.lineplot(x=df_TAT['Eingang'], y=df_TAT[phase], label=phase)
    plt.title('Trend of TAT Over Time')
    plt.xlabel('Date and Time')
    plt.ylabel('Time (minutes)')
    plt.legend()
    plt.show()





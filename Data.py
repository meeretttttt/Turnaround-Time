
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

# # Diagramme

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
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(phase_sums, labels=phase_sums.index, autopct='%1.1f%%', startangle=140)
    ax.set_title('Total Time Distribution for Each Phase')
    st.pyplot(fig) # Direkt in Streamlit anzeigen


def histogramm (df_TAT, time_columns):
    # Histogram for each phase
    for phase in time_columns:
        # Erstelle ein neues Diagramm für jede Phase
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(df_TAT[phase], bins=10, kde=True, ax=ax)
        ax.set_title(f'Histogram of {phase}')
        ax.set_xlabel('Time (minutes)')
        ax.set_ylabel('Frequency')
        st.pyplot(fig) # Direkt in Streamlit anzeigen

def trend_total (df_TAT):
    # Line plot to show the trend of TAT over time
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x=df_TAT['Eingang'], y=df_TAT["Total_TAT in Minuten"], label='Total TAT', ax=ax)
    ax.set_title('Trend of Total TAT Over Time')
    ax.set_xlabel('Date and Time')
    ax.set_ylabel('Time (minutes)')
    ax.legend()
    # x-Achsen-Beschriftung rotieren
    plt.xticks(rotation=45)
    st.pyplot(fig)     # Diagramm direkt in Streamlit anzeigen



def trend_per_phase(df_TAT, time_columns):
    """
    Erstellt ein separates Liniendiagramm für jede Phase und zeigt es direkt in Streamlit an.
    """
    for phase in time_columns:
        # Neues Diagramm für jede Phase erstellen
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(x=df_TAT['Eingang'], y=df_TAT[phase], ax=ax, label=phase)
        ax.set_title(f'Trend of {phase} Over Time')
        ax.set_xlabel('Date and Time')
        ax.set_ylabel('Time (minutes)')
        ax.legend()
        # x-Achsen-Beschriftung rotieren
        plt.xticks(rotation=45)

        # Diagramm direkt in Streamlit anzeigen
        st.subheader(f"Trend-Diagramm: {phase}")
        st.pyplot(fig)


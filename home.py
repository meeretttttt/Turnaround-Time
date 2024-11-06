import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


df_TAT = pd.read_csv ("Daten CSV.csv") # Path to the file
print(df_TAT.head()) 

phases = {
    "Präanalytische Phase": ["Erfassung der Anforderung", "Probenverteilung", "Proben auf Strasse","Zentrifugation"],
    "Analytische Phase": ["Analyten werden gemessen", "Resultate werden übermittel"],
    "Postanalytische Phase": ["Technische Validation","Medizinische Validation", "Erstellen & Versenden Bericht"]
}

# Example of accessing the data structure
for phase, checkpoints in phases.items():
    print(f"{phase}:")
    for checkpoint in checkpoints:
        print(f"  - {checkpoint}")



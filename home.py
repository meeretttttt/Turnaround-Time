import streamlit as st
from Data import process 

st.title('Turnaround Time Calculator')
st.balloons()

df = process()
st.dataframe(df)
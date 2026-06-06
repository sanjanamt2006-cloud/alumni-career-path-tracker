import streamlit as st
from utils.data_loader import load_data

df = load_data()

st.write(df.columns.tolist())

import streamlit as st
import pandas as pd

# This tells Streamlit to load the file only once and reuse it
@st.cache_data
def load_data():
    return pd.read_json("Data/ieom_full.json.gz", compression="gzip")

# Load the data
df = load_data()

# Show the number of papers loaded
st.title("📊 IEOM 2025 Explorer")
st.write(f"Loaded {len(df)} papers from the dataset.")

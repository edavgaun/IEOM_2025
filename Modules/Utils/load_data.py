import pandas as pd
import streamlit as st

@st.cache_data
def load_metadata():
    return pd.read_json("Data/ieom_full.json.gz", compression="gzip")

@st.cache_data
def load_bow():
    return pd.read_parquet("Data/ieom_bow.parquet")

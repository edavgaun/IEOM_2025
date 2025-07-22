import streamlit as st
import pandas as pd

@st.cache_data
def load_bow(region: str, year: int) -> pd.DataFrame:
    file_path = f"Data/parquet/bow_{region.lower()}_{year}.parquet"
    return pd.read_parquet(file_path)

# Modules/Utils/load_pickle.py
import streamlit as st
import pickle
import requests

@st.cache_data
def load_dictionary_norm_tf():
    url = 'https://github.com/edavgaun/IEOM_2025/raw/refs/heads/main/Data/tf_dfs.pkl'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return pickle.loads(response.content)
    except Exception as e:
        st.error(f"Error fetching tf_dfs.pkl: {e}")
        return None

@st.cache_data
def load_dictionary_tf_idf():
    url = 'https://github.com/edavgaun/IEOM_2025/raw/refs/heads/main/Data/tf_idfs.pkl'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return pickle.loads(response.content)
    except Exception as e:
        st.error(f"Error fetching tf_idfs.pkl: {e}")
        return None

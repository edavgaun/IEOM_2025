import streamlit as st
import pickle
import requests # You'll need to install this: pip install requests

# --- Correct way to load using pickle from a URL ---
@st.cache_data
def load_dictionary_norm_tf():
    url = 'https://github.com/edavgaun/IEOM_2025/raw/refs/heads/main/Data/tf_dfs.pkl'
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return pickle.loads(response.content)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching tf_dfs.pkl from GitHub: {e}")
        return None # Or raise the exception, depending on desired error handling
    except pickle.UnpicklingError as e:
        st.error(f"Error unpickling tf_dfs.pkl: {e}. File might be corrupted or not a valid pickle.")
        return None

# --- Correct way to load using pickle from a URL ---
@st.cache_data
def load_dictionary_tf_idf():
    url = 'https://github.com/edavgaun/IEOM_2025/raw/refs/heads/main/Data/tf_idfs.pkl'
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return pickle.loads(response.content)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching tf_idfs.pkl from GitHub: {e}")
        return None
    except pickle.UnpicklingError as e:
        st.error(f"Error unpickling tf_idfs.pkl: {e}. File might be corrupted or not a valid pickle.")
        return None

# --- Correct way to load using pickle ---
@st.cache_data
def load_dictionary_norm_tf():
    with open('https://github.com/edavgaun/IEOM_2025/raw/refs/heads/main/Data/tf_dfs.pkl', 'rb') as f:
        return pickle.load(f)

# --- Correct way to load using pickle ---
@st.cache_data
def load_dictionary_tf_idf():
    with open('https://github.com/edavgaun/IEOM_2025/raw/refs/heads/main/Data/tf_idfs.pkl', 'rb') as f:
        return pickle.load(f)

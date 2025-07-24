import streamlit as st
import sys
import os

# Add the Modules directory to the Python path
# This assumes your app3.py is in the root, and Modules/ is a direct subdirectory
# If app3.py is also in a subdirectory, you might need to adjust this path.
script_dir = os.path.dirname(__file__)
modules_path = os.path.join(script_dir, "Modules")
if modules_path not in sys.path:
    sys.path.append(modules_path)

# Now you can import from Modules.Utils
from Utils.load_pickle import load_dictionary_norm_tf, load_dictionary_tf_idf

st.title("My Streamlit App with GitHub Data")

# Load the data using the functions
tf_dfs = load_dictionary_norm_tf()
tf_idfs = load_dictionary_tf_idf()

if tf_dfs is not None and tf_idfs is not None:
    st.success("Data loaded successfully!")
    st.write("tf_dfs keys:", tf_dfs.keys())
    st.write("tf_idfs keys:", tf_idfs.keys())
    
    # You can now use tf_dfs and tf_idfs in your visualization or analysis
    # For example, display a part of the data:
    if 'annual' in tf_dfs and tf_dfs['annual'] and isinstance(tf_dfs['annual'][0], pd.DataFrame):
        st.subheader("Sample from tf_dfs['annual'][0]")
        st.dataframe(tf_dfs['annual'][0].head())
    
    if 'annual' in tf_idfs and isinstance(tf_idfs['annual'], pd.DataFrame):
        st.subheader("Sample from tf_idfs['annual']")
        st.dataframe(tf_idfs['annual'].head())

else:
    st.error("Failed to load data. Check the console for errors or the GitHub paths.")

# app3.py
import streamlit as st
import pandas as pd

# Import functions from your modules
from Modules.Utils.load_pickle import load_dictionary_norm_tf, load_dictionary_tf_idf
from Modules.Charts.drift_chart import semmantic_drift_plot_matplotlib
from Modules.UI.layout_config import set_layout
from Modules.UI.header import show_header
from Modules.UI.instructions import show_drift_instructions

# Layout
set_layout()

# Header
show_header("📊 Semantic Drift Analysis")

# Instructions
show_drift_instructions()

# Load TF and TF-IDF data from GitHub
with st.spinner("Loading data from GitHub..."):
    tf_dfs = load_dictionary_norm_tf()
    tf_idfs = load_dictionary_tf_idf()

if tf_dfs is None or tf_idfs is None:
    st.error("Could not load data. Please check your internet connection or the GitHub URLs.")
    st.stop()

# The data structure is a dictionary of lists of dataframes
# We need to get the keys and columns from the first element
available_regions = [r.title() if r!='annual' else 'International' for r in tf_dfs.keys()]
available_words= tf_dfs['annual'][0].index.values

# Conference sort
conferences = sorted(available_regions[1:])
conferences = [available_regions[0]] + conferences

conf = st.selectbox("Select Conference", ["International"] + sorted(conferences))
region_key = "annual" if conf == "International" else conf.lower()

available_years=tf_dfs[region_key][0].columns.values

year = st.selectbox("Select Year", available_years)

# Keyword Input
st.markdown("### 🔍 Keywords to Highlight")
keywords_input = st.multiselect(
    "Select KeyWords", options=available_words, 
    default=['generative ai', 'ai', 'machine learning', 'llm']
)

# --- Display the Plot ---
st.markdown("### 📈 TF-IDF vs. Normalized TF")

# Create and display the Scatter plot
semmantic_drift_plot_matplotlib(
    region=region_key,
    year=year,
    tf_dfs=tf_dfs,
    tf_idfs=tf_idfs,
    words=keywords_input,
    fz=12
)

# Add a markdown explanation for the plot
st.markdown("""
---
**Understanding the Plot:**
This chart visualizes the relationship between a term's frequency (TF) and its importance (TF-IDF) in the selected year.
-   **Normalized TF (X-axis):** How common the word is.
-   **TF-IDF (Y-axis):** How distinctive the word is.

**Key Quadrants:**
-   **Top Right (Green):** Frequent and distinctive words.
-   **Top Left (Orange):** Rare but highly distinctive (often new or emerging terms).
-   **Bottom Right (Blue):** Common and generic words.
-   **Bottom Left (Gray):** Rare and generic words (noise).
""")

# app3.py
import streamlit as st
import pandas as pd
import numpy as np # Needed for some previous functions

# Import functions from your modules
from Modules.Utils.load_pickle import load_dictionary_norm_tf, load_dictionary_tf_idf
from Modules.Charts.drift_chart import semmantic_drift_plot_matplotlib
from Modules.UI.layout_config import set_layout
from Modules.UI.header import show_header
from Modules.UI.instructions import show_drift_instructions
from Modules.UI.widgets import show_tfidf_widgets

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

# Get available regions and years from the loaded data
available_regions = [r.title() if r!='annual' else 'International' for r in tf_dfs.keys()]
available_words= tf_dfs['annual'][0].index.values

# Conference sort
conferences = sorted([r for r in available_regions if r != 'International'])
conferences = ['International'] + conferences


# --- CREATE THE TWO-COLUMN LAYOUT for the Widget section---
show_tfidf_widgets(conferences, tf_dfs)

# --- Display the Plot below the columns ---
st.markdown("---")
st.markdown("### 📈 TF-IDF vs. Normalized TF")

# Create and display the Scatter plot
semmantic_drift_plot_matplotlib(
    region=region_key,
    year=year,
    tf_dfs=tf_dfs,
    tf_idfs=tf_idfs,
    words=keywords_input, # <-- Using keywords_input as fixed in the last response
    fz=12
)

# Add a markdown explanation for the plot
st.markdown("""
---
**Understanding the Plot:**
This chart visualizes the relationship between a term's frequency (TF) and its importance (TF-IDF) in the selected year.
...
""")

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
available_years = sorted(tf_dfs['annual'][0].columns.values.tolist())


# --- CREATE THE TWO-COLUMN LAYOUT ---
col1, col2 = st.columns(2)

with col1:
    # Widgets for the left column
    conf = st.selectbox("Select Conference", conferences)
    region_key = "annual" if conf == "International" else conf.lower()
    
    # Get the specific years for the selected conference
    years_for_conf = sorted(tf_dfs[region_key][0].columns.values.tolist())
    
    # Create a slider for the year range
    start_year, end_year = st.slider(
        "Select Year Range",
        min_value=min(years_for_conf),
        max_value=max(years_for_conf),
        value=(min(years_for_conf), max(years_for_conf))
    )
    # The current logic of semmantic_drift_plot_matplotlib expects a single year,
    # so we'll need to adapt this. For now, let's just use the start year.
    # We'll use start_year for plotting and the slider for UI.
    year = start_year


with col2:
    # Widget for the right column
    st.markdown("### 🔍 Keywords to Highlight")
    keywords_input = st.multiselect(
        "Select KeyWords", options=available_words, 
        default=['generative ai', 'ai', 'machine learning', 'llm']
    )


# --- Display the Plot below the columns ---
st.markdown("---")
st.markdown("### 📈 TF-IDF vs. Normalized TF")

# Create and display the Matplotlib plot
fig = semmantic_drift_plot_matplotlib(
    region=region_key,
    year=year,
    tf_dfs=tf_dfs,
    tf_idfs=tf_idfs,
    words=keywords_input, # <-- Using keywords_input as fixed in the last response
    fz=12
)

st.pyplot(fig)

# Add a markdown explanation for the plot
st.markdown("""
---
**Understanding the Plot:**
This chart visualizes the relationship between a term's frequency (TF) and its importance (TF-IDF) in the selected year.
...
""")

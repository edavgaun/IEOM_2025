# app3.py
import streamlit as st
import pandas as pd
import numpy as np

# Import functions from your modules
from Modules.Utils.load_pickle import load_dictionary_norm_tf, load_dictionary_tf_idf
from Modules.Charts.drift_chart import semmantic_drift_plot_plotly
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

# Conference sort
conferences = sorted([r for r in available_regions if r != 'International'])
conferences = ['International'] + conferences


# --- CREATE THE TWO-COLUMN LAYOUT for the Widget section---
region_key, start_year, end_year, keywords_input = show_tfidf_widgets(conferences, tf_dfs)

# --- Display the Plot below the columns ---
st.markdown("---")
st.markdown("### 📈 TF-IDF vs. Normalized TF")

plot_col1, plot_col2 = st.columns(2)
with plot_col1:
    st.subheader("Chart for {}".format(start_year))
    fig1 = semmantic_drift_plot_plotly(
        region=region_key,
        year=start_year,
        tf_dfs=tf_dfs,
        tf_idfs=tf_idfs,
        words=keywords_input
    )
    st.plotly_chart(fig1, use_container_width=True)

with plot_col2:
    st.subheader("Chart for {}".format(end_year))
    fig2 = semmantic_drift_plot_plotly(
        region=region_key,
        year=end_year,
        tf_dfs=tf_dfs,
        tf_idfs=tf_idfs,
        words=keywords_input
    )
    st.plotly_chart(fig2, use_container_width=True)

# Add a markdown explanation for the plot
st.markdown("""
---
**Understanding the Plot:**
This chart visualizes the relationship between a term's frequency and its importance within a specific set of documents, allowing you to observe how topics and keywords change over time.
""")

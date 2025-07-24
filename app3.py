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

# Assume `tf_dfs` and `tf_idfs` have the same years and regions
# The data structure is a dictionary of lists of dataframes
# We need to get the keys and columns from the first element
available_regions = list(tf_dfs.keys())
available_years = sorted(tf_dfs[available_regions[0]][0].columns.tolist())

# Conference & Year Filters
conferences = available_regions
conferences.remove("annual")
conferences = [c.title() for c in conferences]

conf = st.selectbox("Select Conference", ["International"] + sorted(conferences))
region_key = "annual" if conf == "International" else conf.lower()
year = st.selectbox("Select Year", available_years)

# Keyword Input
st.markdown("### 🔍 Keywords to Highlight")
default_keywords = ['generative ai', 'ai', 'machine learning', 'llm']
keywords_input = st.text_area(
    "Enter keywords (comma-separated)",
    ", ".join(default_keywords),
    help="These words will be highlighted in the plot. Make sure they are lowercase."
)
custom_keywords = [word.strip().lower() for word in keywords_input.split(',') if word.strip()]


# --- Display the Plot ---
st.markdown("### 📈 TF-IDF vs. Normalized TF")

# Create and display the Matplotlib plot
fig = semmantic_drift_plot_matplotlib(
    region=region_key,
    year=year,
    tf_dfs=tf_dfs,
    tf_idfs=tf_idfs,
    words=custom_keywords,
    fz=12
)

# Display the Matplotlib plot in Streamlit
st.pyplot(fig)

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

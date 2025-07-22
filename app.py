import streamlit as st
import pandas as pd

from Modules.Charts.plot_umap import plot_umap_scatter
from Modules.Charts.add_centroids import add_centroids_to_umap

# Load dataset
@st.cache_data
def load_data():
    return pd.read_json("Data/ieom_full.json.gz", compression="gzip")

df = load_data()

# Layout
st.set_page_config(layout="wide")
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        .css-18e3th9 {
            padding-top: 0rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🧭 UMAP Embedding Explorer")

# Filters
selected_years = st.multiselect(
    "Select Years", sorted(df["Year"].unique()), default=sorted(df["Year"].unique())
)

selected_conferences = st.multiselect(
    "Select Conferences", sorted(df["Conference"].unique()), default=sorted(df["Conference"].unique())
)

selected_topics = st.multiselect(
    "Select Topics", options=df["FinalTopicName"].unique(), default=df["FinalTopicName"].unique()
)

# Plot UMAP
fig, filt_df = plot_umap_scatter(
    df,
    selected_years=selected_years,
    selected_conferences=selected_conferences,
    selected_topics=selected_topics
)

fig = add_centroids_to_umap(fig, filt_df)
st.plotly_chart(fig, use_container_width=True)

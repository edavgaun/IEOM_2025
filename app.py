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
            padding-top: 1.5rem;
            padding-bottom: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        .css-18e3th9 {
            padding-top: 0rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# Header with citation
st.title("🧭 UMAP Embedding Explorer")
st.caption("📘 Based on: Edgar Avalos-Gauna (2025), *15 Years of IEOM Proceedings*")
st.caption("Avalos-Gauna, E. (2025). *Tracing AI and Supply Chain Emphasis Across the Global IEOM Landscape, A Meta-Analysis Under Global Uncertainty*. 2nd IEOM World Congress on Industrial Engineering and Operations Management, Windsor, Ontario, Canada, October 14–16, 2025")

# Instructions
st.markdown("""
### 🧭 How to Use This App

This tool lets you explore over 11,000 IEOM conference papers in a 2D space generated using UMAP and LLM-based embeddings.

- **Filter** by year, conference, and topic to narrow down the dataset.
- Each dot represents a paper. Similar papers appear closer together.
- **Centroids** are added to help you visualize topic clusters.
- Hover over points (in Plotly) to see details and explore relationships between topics and years.

This interface supports meta-analysis, comparative research, and exploration of regional and thematic trends in AI and supply chain discussions.
""")

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

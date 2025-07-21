import streamlit as st
import pandas as pd
import numpy as np


# Import Utils Scripts
from Modules.Utils.get_text_to_embed import prepare_text
from Modules.Utils.get_embeddings import get_embeddings

# Import Chart Scripts
from Modules.Charts.plot_umap import plot_umap_scatter

# This tells Streamlit to load the file only once and reuse it
@st.cache_data
def load_data():
    return pd.read_json("Data/ieom_full.json.gz", compression="gzip")

df = load_data()

@st.cache_data
def load_embeddings():
    return np.load("Data/ieom_embeddings.npy")

embeddings = load_embeddings()


# Layout setup
st.set_page_config(layout="wide")
st.markdown("""
    <style>
        /* Remove default padding */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        /* Optional: tweak header spacing */
        .css-18e3th9 {
            padding-top: 0rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# Show the number of papers loaded
st.title("📊 IEOM 2025 Explorer")
st.caption("📘 Based on: Edgar Avalos-Gauna; (2025), *15 Years of IEOM Proceedings*")
st.caption("Avalos-Gauna, E. (2025). *Tracing AI and Supply Chain Emphasis Across the Global IEOM Landscape*. 2nd IEOM World Congress on Industrial Engineering and Operations Management, Windsor, Ontario, Canada, October 14–16, 2025")
st.write(f"Loaded {len(df)} papers from the dataset.")

# General Instructions
st.markdown("""
### 🧭 How to Use This Dashboard

- Use the **tabs** below to switch between different types of visual analyses.
- Each tab allows different types of filtering so make sure to familiarize yourself with them first.
- **Paper Overview** shows Conference Proceedings raw abstracts and metadata.
- **UMAP Projection** lets you explore papers in a 2D dimensional space.
- The **Network Graph** shows term co-occurrence.
- Use the **Radar Charts** to compare keyword relevance across two years.
- The **Bump Chart** tracks top keywords over time.
- The **LDA Chart** shows the Latent Dirichlet Allocation analysis made on the proceedings.

---
""")

# Tabs
tabs = st.tabs([
    "📄 Paper Overview",
    "🧭 UMAP Projection",
    "🌐 Co-occurrence Network",
    "📊 Radar Charts",
    "📈 Bump Chart",
    "🧠 Topic Modeling (LDA)"
])

st.markdown("<hr style='margin-top: -10px;'>", unsafe_allow_html=True)
st.write(f"{embeddings.shape[0]} Papers from 10 Regions (≤9 Editions)")

with tabs[1]:
    st.subheader("🧭 UMAP Embedding Explorer")

    # Filters
    selected_years = st.multiselect(
        "Select Years", sorted(df["Year"].unique()), default=sorted(df["Year"].unique())
    )

    selected_conferences = st.multiselect(
        "Select Conferences", sorted(df["Conference"].unique()), default=sorted(df["Conference"].unique())
    )

    # Plot
    fig = plot_umap_scatter(df, selected_years=selected_years, selected_conferences=selected_conferences)
    st.plotly_chart(fig, use_container_width=True)

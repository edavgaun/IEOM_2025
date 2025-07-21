import streamlit as st
import pandas as pd
import numpy as np
import nltk
nltk.download('stopwords')


# Import Utils Scripts
from Modules.Utils.get_text_to_embed import prepare_text

# Import Chart Scripts
from Modules.Charts.plot_umap import plot_umap_scatter
from Modules.Charts.add_centroids import add_centroids_to_umap

# This tells Streamlit to load the file only once and reuse it
@st.cache_data
def load_data():
    return pd.read_json("Data/ieom_full.json.gz", compression="gzip")

df = load_data()

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
- The **LDA Chart** shows the Latent Dirichlet Allocation analysis made on the proceedings.

---
""")

# Tabs
tabs = st.tabs([
    "📄 Paper Overview",
    "🧭 UMAP Projection",
    "🧠 Topic Modeling (LDA)"
])

st.markdown("<hr style='margin-top: -10px;'>", unsafe_allow_html=True)
st.write(f"{df.shape[0]:,} Papers from 10 Regions (≤9 Editions)")

# First Tab
with tabs[0]:
    st.subheader("📄 Paper Overview")

    # ROW 1
    with st.container():
        col1, coldf = st.columns([1, 3])

        with col1:
            st.markdown("### ⚙️ Settings")

            conferences=list(df["Conference"].unique())
            conferences.remove('annual')
            conferences=[c.title() for c in conferences]
            conf = st.selectbox("Select Conference", ['International'] + sorted(conferences), key="ieom_conference")
            if conf=='International':
                conf=='annual'
            df_conf = df[df["Conference"] == conf]
            
            year = st.selectbox("Select Year", sorted(df_conf["Year"].unique()), key="ieom_year")
            df_year = df_conf[df_conf["Year"] == year]

            max_rows = len(df_year)
            row_range = st.slider(
                "Select row range", 0, max_rows - 1,
                value=(0, min(10, max_rows - 1)),
                key="ieom_row_slider"
            )
            
            # Slice the dataframe based on user input
            df_slice = df_year.iloc[row_range[0]:row_range[1] + 1]
            
            # Set the index to reflect actual position in df_year (e.g., row 50–60)
            df_slice.index = list(range(row_range[0], row_range[1] + 1))

        with coldf:
            st.markdown("### 📑 Papers Found")
            st.dataframe(df_slice[["Title", "Abstract", "Keywords"]], use_container_width=True)

    # ROW 2
    with st.container():
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.markdown("""
            ### 📊 IEOM Paper Identification Summary
            
            The first chart shows the number of papers identified per region, with min–avg–max lines and dot size/color indicating conference maturity. ‘International’ leads in both volume and consistency.
            
            The second chart shows paper extraction success. Each icon = 5% of entries. Green means successful, red indicates failures (e.g., broken links). Most regions have strong coverage — except 'Central', which had major data issues.
            
            Together, these visuals highlight coverage depth and reliability across IEOM regions.
            """)



        # cols 2 & 3 show pictures related to the paper extraction process
        with col2:
            st.markdown("##### 📊 Identified Papers by Region")
            st.image("assets/Paper submissions.png", use_container_width=True)

        with col3:
            st.markdown("##### 📊 Paper Extraction Rate")
            st.image("assets/pct of papers.png", use_container_width=True)

    # ROW 3
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 2])

        with col1:
            st.markdown("### 🔢 Word Frequency Controls for the chosen Conference and Year")
            top_n = st.slider("Top N words", min_value=5, max_value=50, value=20, step=1)
            remove_stopwords = st.checkbox("Remove custom stopwords", value=True)

        with col2:
            st.markdown("### 🔤 Word Frequency Chart")

            


# Second Tab
with tabs[1]:
    st.subheader("🧭 UMAP Embedding Explorer")

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

    # Plot
    fig, filt_df = plot_umap_scatter(df, selected_years=selected_years, selected_conferences=selected_conferences, selected_topics=selected_topics)
    # Add centroids afterward
    fig = add_centroids_to_umap(fig, filt_df)
    st.plotly_chart(fig, use_container_width=True)

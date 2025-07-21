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

            conf = st.selectbox("Select Conference", sorted(df["Conference"].unique()), key="ieom_conference")
            df_conf = df[df["Conference"] == conf]
            
            year = st.selectbox("Select Year", sorted(df_conf["Year"].unique()), key="ieom_year")
            df_year = df[df["Year"] == year]

            max_rows = len(df_year)
            row_range = st.slider(
                "Select row range", 0, max_rows - 1,
                value=(0, min(10, max_rows - 1)),
                key="ieom_row_slider"
            )
            df_slice = df_year.iloc[row_range[0]:row_range[1] + 1]

        with coldf:
            st.markdown("### 📑 Papers Found")
            st.dataframe(df_slice[["Title", "Abstract", "Keywords"]], use_container_width=True)

    # ROW 2
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 2])

        with col1:
            st.markdown("##### 📊 Identified Papers by Region")
            st.image("assets/Paper submissions.png", use_container_width=True)

        # cols 2 & 3 continue dataframe or remain empty if not needed
        with col2:
            st.empty()

        with col3:
            st.empty()

    # ROW 3
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 2])

        with col1:
            st.markdown("##### 📊 Paper Extraction Rate")
            st.image("assets/pct of papers.png", use_container_width=True)

        with col2:
            st.markdown("### 🔢 Word Frequency Controls")
            top_n = st.slider("Top N words", min_value=5, max_value=50, value=20, step=1)
            remove_stopwords = st.checkbox("Remove custom stopwords", value=True)

        with col3:
            st.markdown("### 🔤 Word Frequency Chart")

            # Build frequency chart
            import re
            from collections import Counter
            from nltk.corpus import stopwords
            import altair as alt

            # If you have your own stopwords, load here
            try:
                with open("Data/own_stopwords.txt", "r") as f:
                    own_stopwords = set(word.strip() for word in f.readlines())
            except:
                own_stopwords = set()

            text = " ".join(df_slice["Paper"].dropna().astype(str).tolist()).lower()
            tokens = re.findall(r'\b[a-z]{3,}\b', text)

            stop_words = set(stopwords.words("english"))
            if remove_stopwords:
                stop_words = stop_words.union(own_stopwords)

            words = [w for w in tokens if w not in stop_words]
            word_freq = Counter(words).most_common(top_n)
            freq_df = pd.DataFrame(word_freq, columns=["Word", "Frequency"])

            chart = alt.Chart(freq_df).mark_bar().encode(
                x=alt.X("Word:N", sort="-y"),
                y=alt.Y("Frequency:Q"),
                tooltip=["Word", "Frequency"]
            ).properties(
                width=400,
                height=300,
                title=f"Top {top_n} Words in Selected Papers"
            )

            st.altair_chart(chart, use_container_width=True)


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

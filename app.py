import streamlit as st
import pandas as pd

# Import Utils Scripts
from Modules.Utils.get_text_to_embed import prepare_text

df = prepare_text(df, method="title")


# This tells Streamlit to load the file only once and reuse it
@st.cache_data
def load_data():
    return pd.read_json("Data/ieom_full.json.gz", compression="gzip")

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

# Load the data
df = load_data()

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
- **Word Cloud** and **Bubble Chart** let you explore keyword frequencies.
- The **Network Graph** shows term co-occurrence.
- Use the **Radar Charts** to compare keyword relevance across two years.
- The **Bump Chart** tracks top keywords over time.
- The **LDA Chart** shows the Latent Dirichlet Allocation analysis made on the proceedings.

---
""")

# Tabs
tabs = st.tabs([
    "📄 Paper Overview",
    "☁️ Word Cloud & Bubble Chart",
    "🌐 Co-occurrence Network",
    "📊 Radar Charts",
    "📈 Bump Chart",
    "🧠 Topic Modeling (LDA)"
])

st.markdown("<hr style='margin-top: -10px;'>", unsafe_allow_html=True)


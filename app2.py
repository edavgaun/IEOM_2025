import streamlit as st
import pandas as pd

from Modules.Utils.load_data import load_metadata, load_bow
from Modules.Charts.bow_freq_chart import get_top_terms, make_freq_chart
from Modules.UI.static_charts import show_static_charts
from Modules.UI.layout_config import set_layout

# Layout
set_layout()

# Load data
df_meta = load_metadata()
bow_df = load_bow()

# Header
st.title("🔤 BOW Frequency Explorer")
st.caption("📘 Based on: Edgar Avalos-Gauna (2025), *15 Years of IEOM Proceedings*")
st.caption("Avalos-Gauna, E. (2025). *Tracing AI and Supply Chain Emphasis Across the Global IEOM Landscape, A Meta-Analysis Under Global Uncertainty*. 2nd IEOM World Congress on Industrial Engineering and Operations Management, Windsor, Ontario, Canada, October 14–16, 2025")

# Instructions
st.markdown("""
### 🧭 How to Use This App

Explore vocabulary trends across IEOM regions using Bag-of-Words frequency.

- Filter by **conference**, **year**, and **row range** to view a subset of papers.
- See a table of the filtered papers (title, abstract, keywords).
- Use the **Top N words** slider to view the most common terms.
""")

# Filters
conferences = list(df_meta["Conference"].unique())
conferences.remove('annual')
conferences = [c.title() for c in conferences]
conf = st.selectbox("Select Conference", ['International'] + sorted(conferences))
if conf == 'International':
    conf = 'annual'

df_conf = df_meta[df_meta["Conference"] == conf]
year = st.selectbox("Select Year", sorted(df_conf["Year"].unique()))
df_year = df_conf[df_conf["Year"] == year]

max_rows = len(df_year)
row_range = st.slider("Select row range", 0, max_rows - 1, value=(0, min(10, max_rows - 1)))
selected_indices = df_year.index[row_range[0]:row_range[1] + 1]
df_slice = df_year.loc[selected_indices]
df_slice.index = list(range(row_range[0], row_range[1] + 1))
bow_slice = bow_df.loc[selected_indices]

# Static images
show_static_charts()

# Show filtered papers
st.markdown("### 📑 Filtered Papers")
st.dataframe(df_slice[["Title", "Abstract", "Keywords"]], use_container_width=True)

# Word frequency chart
st.markdown("### 🔤 Top Word Frequencies")
top_n = st.slider("Top N words", 5, 50, 20)
freq_df = get_top_terms(bow_slice, top_n=top_n)
chart = make_freq_chart(freq_df)
st.altair_chart(chart, use_container_width=True)

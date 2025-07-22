import streamlit as st
import pandas as pd

from Modules.Utils.load_data import load_metadata
from Modules.Utils.load_bow import load_bow
from Modules.Charts.bow_freq_chart import get_top_terms, make_freq_chart
from Modules.UI.static_charts import show_static_charts
from Modules.UI.layout_config import set_layout
from Modules.UI.header import show_header

# Layout
set_layout()

# Load metadata
df_meta = load_metadata()

# Header
show_header("🔤 BOW Frequency Explorer")

# Instructions
st.markdown("""
### 🧭 How to Use This App

Explore vocabulary trends across IEOM regions using Bag-of-Words frequency.

- Filter by **conference**, **year**, and **row range** to view a subset of papers.
- See a table of the filtered papers (title, abstract, keywords).
- Use the **Top N words** slider to view the most common terms.
""")

# Static images
show_static_charts()

# Conference & Year Filters
conferences = list(df_meta["Conference"].unique())
conferences.remove("annual")
conferences = [c.title() for c in conferences]
conf = st.selectbox("Select Conference", ["International"] + sorted(conferences))
region_key = "annual" if conf == "International" else conf.lower()

df_conf = df_meta[df_meta["Conference"] == region_key]
year = st.selectbox("Select Year", sorted(df_conf["Year"].unique()))
df_year = df_conf[df_conf["Year"] == year]

# Load corresponding BOW slice
try:
    bow_df = load_bow(region_key, year)
    bow_df.index = df_year.index
except FileNotFoundError:
    st.error(f"No BOW file found for: {region_key}_{year}. Please ensure the file exists.")
    st.stop()

# Row Range Slider
max_rows = len(df_year)
row_range = st.slider("Select row range", 0, max_rows - 1, value=(0, min(10, max_rows - 1)))
selected_indices = df_year.index[row_range[0]:row_range[1] + 1]
df_slice = df_year.loc[selected_indices]
df_slice.index = list(range(row_range[0], row_range[1] + 1))
bow_slice = bow_df.loc[selected_indices]

# Show filtered papers
st.markdown("### 📑 Filtered Papers")
st.dataframe(df_slice[["Title", "Abstract", "Keywords"]], use_container_width=True)

# Word frequency chart
st.markdown("### 🔤 Top Word Frequencies (from filtered selection)")
top_n = st.slider("Top N words", 5, 50, 20)
freq_df = get_top_terms(bow_slice, top_n=top_n)
chart = make_freq_chart(freq_df)
st.altair_chart(chart, use_container_width=True)

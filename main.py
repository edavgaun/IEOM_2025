import streamlit as st
from Modules.UI.layout_config import set_layout
from Modules.UI.header import show_header

# Layout and Header
set_layout()
show_header("🌍 IEOM 2025 Explorer Suite")

# Welcome Message
st.markdown("""
### 🧭 Choose a Visualization Tool

This dashboard suite helps you explore over 11,000 IEOM conference papers using two complementary apps.

- 🧭 **UMAP Embedding Explorer**  
  Explore papers in a 2D space based on semantic similarity.  
  👉 [Open UMAP Explorer](https://ieom-2025.streamlit.app/)

- 🔤 **BOW Frequency Explorer**  
  View the most frequent words in selected subsets of papers.  
  👉 [Open BOW Explorer](https://ieom-2025-bow.streamlit.app/)
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
📘 **Citation**  
Avalos-Gauna, E. (2025). *Tracing AI and Supply Chain Emphasis Across the Global IEOM Landscape, A Meta-Analysis Under Global Uncertainty*.  
2nd IEOM World Congress on Industrial Engineering and Operations Management, Windsor, Ontario, Canada, October 14–16, 2025.
""")

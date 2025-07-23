import streamlit as st
from Modules.UI.layout_config import set_layout
from Modules.UI.header import show_header
from Modules.UI.instructions import show_main_instructions


# Layout and Header
set_layout()
show_header("🌍 IEOM 2025 Explorer Suite")

# Welcome Message
show_main_instructions()

st.markdown("""
📘 **Citation**  
Avalos-Gauna, E. (2025). *Tracing AI and Supply Chain Emphasis Across the Global IEOM Landscape, A Meta-Analysis Under Global Uncertainty*.  
2nd IEOM World Congress on Industrial Engineering and Operations Management, Windsor, Ontario, Canada, October 14–16, 2025.
""")

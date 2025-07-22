import streamlit as st

def show_static_charts():
    st.markdown("### 📊 IEOM Paper Identification Summary")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown("""
        - **Left**: Paper volume per region with maturity markers.  
        - **Right**: Extraction success rate per region.  
        - Green = successful parsing; Red = broken/missing entries.
        """)
    with col2:
        st.markdown("##### 📊 Identified Papers by Region")
        st.image("assets/Paper submissions.png", use_container_width=True)
    with col3:
        st.markdown("##### 📊 Paper Extraction Rate")
        st.image("assets/pct of papers.png", use_container_width=True)

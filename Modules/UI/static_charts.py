import streamlit as st

def show_static_charts():
    st.markdown("### 📊 IEOM Paper Identification Summary")

    col1, col2, col3 = st.columns([2, 3, 3])
    with col1:
        st.markdown(f"""
- **Left Chart**: Number of papers published in each region. Dot size and lines show how established each region’s conference is.  
- **Right Chart**: Extraction success rate by region from IEOM website.  
  - 🟢 Green = successfully parsed papers  
  - 🔴 Red = missing or failed entries  

**Dataset Summary**  
- 📄 Total Papers Extracted: 11,297  
- 🔤 Total Unique Words After Filtering: 10,743
(Including Bigrams and Trigrams)
""")

    with col2:
        st.markdown("##### 📊 Identified Papers by Region")
        st.image("assets/Paper submissions.png", use_container_width=True)
    with col3:
        st.markdown("##### 📊 Paper Extraction Rate")
        st.image("assets/pct of papers.png", use_container_width=True)

# Modules/UI/instructions.py

import streamlit as st

def show_main_instructions():
    st.markdown("""
    ### 🧭 Choose a Visualization Tool

    This dashboard suite helps you explore over 11,000 IEOM conference papers using two complementary apps.

    - 🧭 **UMAP Embedding Explorer**  
      Explore papers in a 2D space based on semantic similarity.  
      👉 [Open UMAP Explorer](https://ieom-2025-umap.streamlit.app/)

    - 🔤 **BOW Frequency Explorer**  
      View the most frequent words in selected subsets of papers.  
      👉 [Open BOW Explorer](https://ieom-2025-bow.streamlit.app/)

    - 🔍 **BOW TF - IDF Analysis**  
      View the most frequent and Distinctive words given a particular Conference and Year.  
      👉 [Open BOW Explorer](https://ieom-2025-tf-idf.streamlit.app/)
      
    """, unsafe_allow_html=True)
    
    st.markdown("---")


def show_umap_instructions():
    st.markdown("""
    ### 🧭 How to Use This App

    This tool lets you explore over 11,000 IEOM conference papers in a 2D space generated using UMAP and LLM-based embeddings.

    - **Filter** by year, conference, and topic to narrow down the dataset.
    - Each dot represents a paper. Similar papers appear closer together.
    - **Centroids** are shown to help you visualize semantic drift (vertical dashed lines).
    - Hover over points (in Plotly) to see details and explore relationships between topics and years.

    This interface supports meta-analysis, comparative research, and exploration of regional and thematic trends in AI and supply chain discussions.
    """)


def show_bow_instructions():
    st.markdown("""
    ### 🧭 How to Use This App

    Explore vocabulary trends across IEOM regions using Bag-of-Words frequency.

    - Filter by **conference**, **year**, and **row range** to view a subset of papers.
    - See a table of the filtered papers (title, abstract, keywords).
    - Use the **Top N words** slider to view the most common terms of the filtered df.
    """)


def show_drift_instructions():
    st.markdown(
        """
        ### 🧭 How to Use This App
        
        This app visualizes the relationship between Term Frequency (TF) and Term Distinctiveness (TF-IDF) for Tokens given a particular Region and Year.
        
        -   Use the filters to select a specific conference and year.
        -   Enter keywords you wish to highlight in the text box.
        """
    )

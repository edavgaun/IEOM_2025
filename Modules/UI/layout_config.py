import streamlit as st

def set_layout():
    st.set_page_config(layout="wide")
    st.markdown("""
        <style>
            .block-container {
                padding-top: 1.5rem;
                padding-bottom: 1rem;
                padding-left: 2rem;
                padding-right: 2rem;
            }
            .css-18e3th9 {
                padding-top: 0rem !important;
            }
        </style>
    """, unsafe_allow_html=True)

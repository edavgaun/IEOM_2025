# Modules/Charts/drift_chart.py
import numpy as np
import pandas as pd
import streamlit as st

def semmantic_drift_plot(region, year, tf_dfs, tf_idfs,
                         words=['generative ai', 'ai', 'machine learning', 'llm']):

    tf_series = tf_dfs[region][0][year]
    tfidf_series = tf_idfs[region][year]
    
    chart_data = pd.DataFrame({
        'tf_values': tf_series,
        'tfidf_values': tfidf_series
    }).dropna()

    # --- FIX 1: Make keyword comparison case-insensitive ---
    keywords_lower = [w.lower() for w in words]
    chart_data['is_keyword'] = chart_data.index.str.lower().isin(keywords_lower)

    # --- FIX 2: Create a color column with explicit color names ---
    chart_data['color_coding'] = chart_data['is_keyword'].apply(lambda x: 'red' if x else '#1f77b4') # Blue hex code
    
    # --- FIX 3: Correct the st.scatter_chart() call with explicit colors ---
    st.scatter_chart(
        chart_data,
        x="tf_values",
        y="tfidf_values",
        color="color_coding"
    )

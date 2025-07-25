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

    chart_data['is_keyword'] = chart_data.index.isin(words)

    # --- THE FIX STARTS HERE ---
    # Create a new column with the color names 'red' or 'blue'
    chart_data['color_coding'] = chart_data['is_keyword'].apply(lambda x: 'red' if x else 'blue')
    
    # Update the color argument to use the new column
    st.scatter_chart(
        chart_data,
        x="tf_values",
        y="tfidf_values",
        color="color_coding", # <-- Use the new color column
    )

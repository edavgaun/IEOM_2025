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

    keywords_lower = [w.lower() for w in words]
    chart_data['is_keyword'] = chart_data.index.str.lower().isin(keywords_lower)

    # --- THE FINAL, CORRECT FIX FOR COLORS ---
    # Use a dictionary to map the boolean values to hex codes
    color_map = {True: '#FF0000', False: '#1f77b4'} 
    chart_data['color_coding'] = chart_data['is_keyword'].map(color_map)
    
    st.scatter_chart(
        chart_data,
        x="tf_values",
        y="tfidf_values",
        color="color_coding"
    )

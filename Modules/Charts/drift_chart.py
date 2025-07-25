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

    color_map = {True: '#FF0000', False: '#ADD8E6'}
    chart_data['color_coding'] = chart_data['is_keyword'].map(color_map)

    # --- Apply the log2 transformation ---
    chart_data['tf_values_log2'] = np.log2(chart_data['tf_values'].replace(0, 1e-20))
    chart_data['tfidf_values_log2'] = np.log2(chart_data['tfidf_values'].replace(0, 1e-20))

    # --- THE CORRECT FIX: Filter the DataFrame to set the axis range ---
    # Define the log-transformed ranges
    x_min_log2, x_max_log2 = -16, -5
    y_min_log2, y_max_log2 = -8, 2
    
    # Filter the DataFrame to the desired ranges
    filtered_chart_data = chart_data[
        (chart_data['tf_values_log2'] >= x_min_log2) &
        (chart_data['tf_values_log2'] <= x_max_log2) &
        (chart_data['tfidf_values_log2'] >= y_min_log2) &
        (chart_data['tfidf_values_log2'] <= y_max_log2)
    ].copy()

    st.scatter_chart(
        filtered_chart_data,
        x="tf_values_log2",
        y="tfidf_values_log2",
        color="color_coding"
    )
